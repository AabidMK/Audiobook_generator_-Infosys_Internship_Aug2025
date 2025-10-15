import os
import json
import time
import uuid
import asyncio
import shutil
import logging
import traceback
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException, Request
from fastapi.responses import FileResponse, StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Import main audiobook + RAG components
from final_pipeline import run_pipeline, UPLOAD_DIR, OUTPUT_DIR
from Rag_implementation.main import query_docs, index_documents

# ---------------------- Setup ----------------------
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
DOCS_DIR = Path(__file__).resolve().parent / "docs"
DOCS_DIR.mkdir(exist_ok=True)

app = FastAPI(title="AI Audiobook + RAG Server")

# Allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all during dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

JOBS = {}
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}

# ---------------------- Utils ----------------------
def generate_id():
    return str(uuid.uuid4())[:8]


def log_error(msg: str, e: Exception):
    logging.error(f"{msg}: {e}")
    traceback.print_exc()


# ---------------------- Upload API ----------------------
@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"File type {ext} not supported")

    job_id = generate_id()
    filename = file.filename
    path = os.path.join(UPLOAD_DIR, f"{job_id}_{filename}")

    data = await file.read()
    with open(path, "wb") as f:
        f.write(data)

    # Also copy file into docs folder for RAG
    shutil.copy(path, DOCS_DIR / filename)

    JOBS[job_id] = {
        "id": job_id,
        "filename": filename,
        "status": "uploaded",
        "created_at": time.time(),
    }

    # Start processing in background
    background_tasks.add_task(_process_job, job_id, path, filename)

    return {"job_id": job_id, "status": "uploaded"}


def _process_job(job_id, path, filename):
    try:
        JOBS[job_id]["status"] = "processing"
        result = run_pipeline(path, filename, job_id)

        # Once audiobook is done, index it for RAG
        print(f"📘 Indexing enriched text for RAG from: {filename}")
        index_documents(str(DOCS_DIR))

        JOBS[job_id].update(result)
    except Exception as e:
        JOBS[job_id]["status"] = "error"
        JOBS[job_id]["error_message"] = str(e)
        log_error("Pipeline failed", e)


# ---------------------- Job Management ----------------------
@app.get("/api/jobs")
async def get_jobs():
    return list(JOBS.values())


@app.delete("/api/jobs/{job_id}")
async def delete_job(job_id: str):
    if job_id in JOBS:
        for f in JOBS[job_id].get("audio_files", []):
            path = os.path.join(OUTPUT_DIR, f)
            if os.path.exists(path):
                os.remove(path)
        del JOBS[job_id]
        return {"status": "deleted"}
    raise HTTPException(404, "Job not found")


@app.get("/api/download/{job_id}/{file}")
async def download_audio(job_id: str, file: str):
    path = os.path.join(OUTPUT_DIR, file)
    if not os.path.exists(path):
        raise HTTPException(404, "File not found")
    return FileResponse(path, filename=file)


@app.get("/api/upload-progress/{job_id}")
async def upload_progress(job_id: str):
    async def gen():
        while True:
            job = JOBS.get(job_id)
            if not job:
                break
            yield f"data:{json.dumps({'status': job['status']})}\n\n"
            if job["status"] in ("completed", "error"):
                break
            await asyncio.sleep(1)
    return StreamingResponse(gen(), media_type="text/event-stream")


# ---------------------- RAG Q&A Endpoint ----------------------
@app.post("/api/ask")
async def ask_question(request: Request):
    """Frontend calls this endpoint for RAG-based question answering."""
    try:
        data = await request.json()
        question = data.get("question", "").strip()
        if not question:
            return {"answer": "Please provide a question.", "sources": []}

        print(f"🧠 RAG Query: {question}")

        result = query_docs(question, backend="chroma", llm_model="gemma3:1b")

        return {
            "answer": result.get("answer", "No answer found."),
            "sources": result.get("sources", [])
        }
    except Exception as e:
        log_error("Error answering question", e)
        return JSONResponse(
            status_code=500,
            content={"answer": f"Error: {str(e)}", "sources": []}
        )


# ---------------------- Health Check ----------------------
@app.get("/")
def root():
    return {"status": "ok", "message": "AI Audiobook + RAG backend is running"}
