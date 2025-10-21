#!/usr/bin/env python3
"""
Simple web interface for the Audiobook Generator
"""

from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import shutil
import asyncio
from dotenv import load_dotenv
from unicode_utils import safe_print

load_dotenv()

app = FastAPI(title="Audiobook Generator Web Interface")

# Create templates directory if it doesn't exist
os.makedirs("templates", exist_ok=True)
os.makedirs("static", exist_ok=True)
os.makedirs("uploads", exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Global generator
generator = None

@app.on_event("startup")
async def startup():
    safe_print("Starting Audiobook Generator Web Interface...")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload file"""
    if not file.filename.endswith(('.pdf', '.docx', '.txt')):
        return {"success": False, "error": "Only PDF, DOCX, and TXT files supported"}
    
    safe_filename = os.path.basename(file.filename)
    file_path = os.path.join("uploads", safe_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"success": True, "filename": safe_filename, "file_path": file_path}

@app.post("/generate")
async def generate_audiobook(file_path: str = Form(...), voice_style: str = Form("storytelling")):
    """Generate audiobook"""
    global generator
    if generator is None:
        from audiobook_generator import StateOfTheArtAudiobookGenerator
        generator = StateOfTheArtAudiobookGenerator()
    
    try:
        result = await generator.generate_complete_audiobook_with_fast_audio(
            file_path=file_path,
            generate_audio=True,
            voice_style=voice_style,
            audio_length_limit=10000  # Smaller for demo
        )
        
        return {
            "success": result['success'],
            "audiobook_file": result.get('audiobook_file'),
            "audio_file": result.get('audio_file'),
            "status": result['status'],
            "total_time": result['total_time']
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/query")
async def query_rag(question: str = Form(...)):
    """Query RAG system"""
    try:
        from rag import rag_pipeline
        answer, citations = rag_pipeline(question, top_k=3)
        return {"success": True, "answer": answer, "citations": citations}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/download/{filename}")
async def download_file(filename: str):
    """Download generated files"""
    # Check multiple locations
    locations = [
        filename,  # Root directory
        os.path.join("complete_audiobooks", filename),
        os.path.join("uploads", filename)
    ]
    
    for file_path in locations:
        if os.path.exists(file_path):
            return FileResponse(file_path, filename=filename)
    
    return {"error": "File not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)