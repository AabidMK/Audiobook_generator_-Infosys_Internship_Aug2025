from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import shutil
from typing import Optional, List
import asyncio

from audiobook_generator import StateOfTheArtAudiobookGenerator
from rag import rag_pipeline
from pipeline_rag import run_pipeline as run_rag_indexing

app = FastAPI(title="Audiobook Generator API", version="1.0.0")

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
    status: str
    total_time: float
    error: Optional[str] = None

# Global generator instance
generator = None

@app.on_event("startup")
async def startup_event():
    global generator
    generator = StateOfTheArtAudiobookGenerator(local_only=False)
    os.makedirs("uploads", exist_ok=True)

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
    if not file.filename.endswith(('.pdf', '.docx', '.txt')):
        raise HTTPException(status_code=400, detail="Only PDF, DOCX, and TXT files are supported")
    
    file_path = f"uploads/{file.filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Index the file for RAG
    try:
        run_rag_indexing([file_path])
        return {"message": f"File {file.filename} uploaded and indexed successfully", "file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Indexing failed: {str(e)}")

@app.post("/generate-audiobook", response_model=AudiobookResponse)
async def generate_audiobook(request: AudiobookRequest):
    """Generate audiobook text and audio from uploaded file"""
    if not os.path.exists(request.file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        result = await generator.generate_complete_audiobook_with_fast_audio(
            file_path=request.file_path,
            generate_audio=request.generate_audio,
            voice_style=request.voice_style,
            audio_length_limit=request.audio_length_limit
        )
        
        return AudiobookResponse(
            success=result['success'],
            audiobook_file=result.get('audiobook_file'),
            audio_file=result.get('audio_file'),
            status=result['status'],
            total_time=result['total_time'],
            error=result.get('error')
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audiobook generation failed: {str(e)}")

@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Query indexed documents using RAG"""
    try:
        answer, citations = rag_pipeline(request.question, top_k=request.top_k)
        return QueryResponse(answer=answer, citations=citations)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

@app.get("/download/{file_type}/{filename}")
async def download_file(file_type: str, filename: str):
    """Download generated audiobook or audio files"""
    if file_type == "audiobook":
        file_path = f"complete_audiobooks/{filename}"
    elif file_type == "audio":
        file_path = filename  # Audio files are in root directory
    else:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(file_path, filename=filename)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)