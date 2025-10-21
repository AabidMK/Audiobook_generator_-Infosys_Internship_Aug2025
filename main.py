from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import shutil
from typing import Optional, List
import asyncio
from dotenv import load_dotenv
from unicode_utils import clean_unicode_text

# Load environment variables
load_dotenv()

from audiobook_generator import StateOfTheArtAudiobookGenerator
from rag import rag_pipeline
from pipeline_rag import run_pipeline as run_rag_indexing

app = FastAPI(title="Audiobook Generator API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class QueryRequest(BaseModel):
    question: str
    top_k: int = 5

class QueryResponse(BaseModel):
    answer: str
    citations: List[dict]

class AudiobookRequest(BaseModel):
    file_path: str
    voice_style: str = "storytelling"
    generate_audio: bool = True
    audio_length_limit: int = 25000

class AudiobookResponse(BaseModel):
    success: bool
    audiobook_file: Optional[str] = None
    audio_file: Optional[str] = None
    audio_url: Optional[str] = None
    status: str
    total_time: float
    error: Optional[str] = None

# Global generator instance
generator = None

@app.on_event("startup")
async def startup_event():
    # Quick startup - lazy load generator
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("complete_audiobooks", exist_ok=True)
    os.makedirs("chroma_db", exist_ok=True)
    print("[OK] API ready - generator will load on first request")

@app.on_event("shutdown")
async def shutdown_event():
    if generator:
        await generator.close()

@app.get("/")
async def root():
    return {"message": "Audiobook Generator API", "endpoints": ["/upload", "/generate-audiobook", "/query"]}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload and index a file for RAG"""
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    
    if not file.filename.lower().endswith(('.pdf', '.docx', '.txt')):
        raise HTTPException(status_code=400, detail="Only PDF, DOCX, and TXT files are supported")
    
    # Check file size (limit to 50MB)
    file_content = await file.read()
    if len(file_content) > 50 * 1024 * 1024:  # 50MB limit
        raise HTTPException(status_code=400, detail="File too large (max 50MB)")
    
    if len(file_content) == 0:
        raise HTTPException(status_code=400, detail="Empty file uploaded")
    
    # Sanitize filename
    import re
    safe_filename = re.sub(r'[^\w\-_\.]', '_', file.filename)
    safe_filename = os.path.basename(safe_filename)
    
    # Add timestamp to avoid conflicts
    import time
    timestamp = str(int(time.time()))
    name, ext = os.path.splitext(safe_filename)
    safe_filename = f"{name}_{timestamp}{ext}"
    
    file_path = os.path.join("uploads", safe_filename)
    
    # Ensure uploads directory exists
    os.makedirs("uploads", exist_ok=True)
    
    try:
        # Write file content
        with open(file_path, "wb") as buffer:
            buffer.write(file_content)
        
        print(f"[UPLOAD] File saved: {file_path} ({len(file_content):,} bytes)")
        
        # Verify file was written correctly
        if not os.path.exists(file_path) or os.path.getsize(file_path) != len(file_content):
            raise Exception("File write verification failed")
        
        # Try indexing with error handling
        indexed = False
        try:
            print(f"[INDEX] Starting indexing for {file_path}")
            run_rag_indexing([file_path])
            indexed = True
            print(f"[INDEX] Successfully indexed {file_path}")
        except Exception as idx_error:
            print(f"[INDEX] Indexing failed: {idx_error}")
            # Don't fail upload if indexing fails
        
        message = f"File '{file.filename}' uploaded successfully"
        if indexed:
            message += " and indexed for search"
        else:
            message += " (indexing failed - search may not work)"
            
        return {
            "success": True,
            "message": message, 
            "file_path": file_path,
            "filename": safe_filename,
            "original_filename": file.filename,
            "file_size": len(file_content),
            "indexed": indexed
        }
        
    except Exception as e:
        # Clean up file if upload fails
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass
        print(f"[UPLOAD ERROR] {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.post("/generate-audiobook")
async def generate_audiobook(request: AudiobookRequest):
    """Generate audiobook text and audio from uploaded file"""
    global generator
    if generator is None:
        print("[LOADING] Loading generator...")
        generator = StateOfTheArtAudiobookGenerator(local_only=False)
    
    if not os.path.exists(request.file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        result = await generator.generate_complete_audiobook_with_fast_audio(
            file_path=request.file_path,
            generate_audio=request.generate_audio,
            voice_style=request.voice_style,
            audio_length_limit=request.audio_length_limit
        )
        
        # Return audio URL for frontend
        audio_url = f"/download/audio/{os.path.basename(result.get('audio_file', ''))}" if result.get('audio_file') else None
        
        return {
            "success": result['success'],
            "audiobook_file": result.get('audiobook_file'),
            "audio_file": result.get('audio_file'),
            "audio_url": audio_url,
            "status": result['status'],
            "total_time": result['total_time'],
            "error": result.get('error')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audiobook generation failed: {str(e)}")

@app.post("/query")
async def query_documents(request: QueryRequest):
    """Query indexed documents using RAG"""
    try:
        clean_question = clean_unicode_text(request.question)
        answer, citations = rag_pipeline(clean_question, top_k=request.top_k)
        return {"answer": clean_unicode_text(answer), "citations": citations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

@app.get("/download/{file_type}/{filename}")
async def download_file(file_type: str, filename: str):
    """Download generated audiobook or audio files"""
    # Sanitize filename to prevent path traversal
    safe_filename = os.path.basename(filename)
    
    if file_type == "audiobook":
        file_path = os.path.join("complete_audiobooks", safe_filename)
    elif file_type == "audio":
        file_path = safe_filename  # Audio files are in root directory
    else:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(file_path, filename=safe_filename)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)