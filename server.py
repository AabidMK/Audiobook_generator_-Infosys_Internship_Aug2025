from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import os, json, time, asyncio, uuid
from fastapi import FastAPI, Request
from final_pipeline import run_pipeline, answer_question, UPLOAD_DIR, OUTPUT_DIR

# Ensure folders exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

app = FastAPI()

# Allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Track jobs
JOBS = {}
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}


def generate_id():
    return str(uuid.uuid4())[:8]


@app.post("/api/upload")
async def api_upload(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"File type {ext} not supported")

    job_id = generate_id()
    filename = file.filename
    path = os.path.join(UPLOAD_DIR, f"{job_id}_{filename}")

    data = await file.read()
    with open(path, "wb") as f:
        f.write(data)

    JOBS[job_id] = {
        "id": job_id,
        "filename": filename,
        "status": "uploaded",
        "created_at": time.time(),
    }

    background_tasks.add_task(_process, job_id, path, filename)
    return {"job_id": job_id, "status": "uploaded"}


def _process(job_id, path, filename):
    try:
        JOBS[job_id]["status"] = "processing"
        result = run_pipeline(path, filename, job_id)
        JOBS[job_id].update(result)
    except Exception as e:
        JOBS[job_id]["status"] = "error"
        JOBS[job_id]["error_message"] = str(e)


@app.get("/api/jobs")
async def api_jobs():
    return list(JOBS.values())


@app.delete("/api/jobs/{job_id}")
async def api_delete(job_id: str):
    if job_id in JOBS:
        for f in JOBS[job_id].get("audio_files", []):
            path = os.path.join(OUTPUT_DIR, f)
            if os.path.exists(path):
                os.remove(path)
        del JOBS[job_id]
        return {"status": "deleted"}
    raise HTTPException(404, "Job not found")


@app.get("/api/download/{job_id}/{file}")
async def api_download(job_id: str, file: str):
    path = os.path.join(OUTPUT_DIR, file)
    if not os.path.exists(path):
        raise HTTPException(404, "File not found")
    return FileResponse(path, filename=file)


@app.post("/api/qa")
async def api_qa(payload: dict):
    q = payload.get("question")
    if not q:
        raise HTTPException(400, "Missing question")
    return answer_question(q)


@app.get("/api/upload-progress/{job_id}")
async def api_progress(job_id: str):
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


# Question and Answering endpoint
import logging

@app.post("/api/ask")
async def ask_question(request: Request):
    """
    Receives a question from the frontend and uses the answer_question function.
    """
    try:
        data = await request.json()
        question = data.get("question", "").strip()

        if not question:
            return {"answer": "Please provide a question.", "citations": []}

        print(f"📩 Received question: {question}")

        # Call the answer_question function from final_pipeline
        result = answer_question(question)

        return {
            "answer": result.get("answer", "No answer found."),
            "citations": result.get("citations", [])
        }

    except Exception as e:
        logging.error(f"Error in /api/ask: {str(e)}", exc_info=True)
        return {"answer": f"Server error: {str(e)}", "citations": []}
