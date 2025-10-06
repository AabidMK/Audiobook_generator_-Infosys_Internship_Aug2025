### AudioBook Generator 

AudioBook Generator is a web application that allows users to upload one or more text 
documents (PDF, DOCX, TXT) and automatically converts them into high-quality 
audiobooks. The application leverages Large Language Models (LLMs) to rewrite extracted 
text in an engaging, listener-friendly “audiobook style” before using open-source Text-to
Speech (TTS) technology to produce downloadable audio files. This project enhances 
accessibility, productivity, and the enjoyment of written content.

# AudioBook Generator — Run Instructions

This file explains the minimal steps to run the project locally using `uv` for Python dependency management and `npm` for the frontend.

Prerequisites
- Python 3.10 or newer
- Node.js 16+ (for frontend)
- `uv` installed (pip install uv) or have an alternative virtual environment workflow ready
- (Optional) Tesseract OCR if you need OCR for scanned PDFs

## Install uv

If you do not have `uv` installed, install it using one of these methods (PowerShell):

```powershell
# Install via pip
pip install uv

# Verify installation
uv --version

# (Optional on Windows) Install via winget if available
winget install --id Astral.Sh.Uv -e
```

Quick steps (PowerShell)

1. Install / sync Python dependencies

```powershell
# From project root
uv sync
```

This creates a virtual environment and installs the Python packages declared in `pyproject.toml`.

2. Start the backend (FastAPI)

```powershell
# From project root
uv run uvicorn server:app --reload --host 127.0.0.1 --port 8000
```

- The API docs will be available at: http://127.0.0.1:8000/docs
- The backend listens on port 8000 by default.

3. Install and run the frontend

```powershell
cd frontend
npm install
npm start
```

- The React dev server usually runs at http://localhost:3000
- If the frontend is configured with a different backend URL, update the `BACKEND_URL` or fetch endpoints in the frontend source.

Notes
- If you prefer not to use `uv`, create and activate a virtual environment and run `pip install -r requirements.txt` instead.
- If you change Python dependencies, re-run `uv sync`.
- For file uploads, the backend expects multipart form data; if you see an error about `python-multipart`, install it and re-run `uv sync` or `pip install python-multipart`.
- If you want LLM-powered RAG answers, ensure the `Rag_implementation` dependencies and an LLM backend (Ollama or remote API keys) are available, and modify `server.py` to call the RAG query function.

If you want this README committed or edited further, tell me and I will update it.
