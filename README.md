#  Audiobook Generator (FastAPI + Gemini + Edge-TTS + EasyOCR + RAG)

This project is a complete **AI-powered Audiobook Generator & Q&A System** that:
- Extracts text from **PDFs, DOCX, TXT, and images**
- Rewrites it with **Google Gemini** for audiobook-friendly narration
- Converts it to natural **MP3 speech using Microsoft Edge-TTS**
- Stores and indexes the rewritten content in **ChromaDB**
- Enables **Retrieval-Augmented Q&A (RAG)** on the processed text.

---

##  Architecture Overview

**Flow:**
Upload → Text Extraction → Gemini Rewrite → Edge TTS (MP3) → Index (Chroma) → RAG Q&A



**Tech Stack:**
| Component | Technology |
|------------|-------------|
| Backend | FastAPI |
| Frontend | React + Vite |
| OCR | EasyOCR |
| LLM | Google Gemini 2.5 Flash |
| Speech | Edge-TTS |
| Vector Store | ChromaDB |
| Embeddings | SentenceTransformer (intfloat/e5-base-v2) |

---

##  Installation Steps

### 1️ Clone the Repository

git clone 
cd audiobook-pipeline

### 2️ Setup Python Environment
conda create -n audiobook python=3.12 -y
conda activate audiobook

### 3️ Install Backend Dependencies
If you already have requirements-rag.txt, use:

pip install -r requirements-rag.txt
Otherwise, manually install:


pip install fastapi uvicorn google-generativeai python-dotenv easyocr edge-tts pdfplumber python-docx chromadb sentence-transformers
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

### 4️ Create .env File in Root Folder

GOOGLE_API_KEY=your_gemini_api_key_here
EDGE_TTS_VOICE=en-GB-SoniaNeural
EDGE_TTS_RATE=-10%
CHROMA_PATH=vector_db
CORS_ORIGINS=http://localhost:5173
PUBLIC_BASE_URL=http://127.0.0.1:8000
You can get a Gemini API key here:
 https://aistudio.google.com/apikey

### 5️ Run the FastAPI Backend
bash

uvicorn app:app --reload
 The server will start on http://127.0.0.1:8000

You’ll see:

Using model: gemini-2.5-flash
Saved rewritten: uploads/<session-id>/<filename>_rewritten.md

### 6️ Run the Frontend (Vite React)

cd audiobook-web
npm install
npm run dev
Visit the web interface at:
 http://localhost:5173

### How to Use
Click “Choose File” → upload a document or image.

The app will:

Extract text (via EasyOCR or pdfplumber)

Rewrite with Gemini for smooth audiobook narration

Generate an MP3 using Edge-TTS

Index the text in ChromaDB for retrieval.

The Preview Panel will let you play or download your MP3.

Use the RAG Q&A box to ask context-based questions about the uploaded document.


###  Project Folder Structure

Audiobook/
│
├── app.py                     # FastAPI app (main API)
├── text_extraction_gemini.py  # Gemini rewrite logic
├── rag_ingest.py              # Manual ingestion utility
├── rag_query.py               # RAG Q&A test script
├── uploads/                   # Temporary output files
├── vector_db/                 # Chroma vector database
├── data/audiobooks.json       # Audiobook catalog
├── audiobook-web/             # React + Vite frontend
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
├── requirements-rag.txt       # Backend dependencies
├── README.md                  # You are here
└── .env                       # Environment variables
 Common Issues & Fixes
Problem	Solution
TTS failed	Try another voice like en-US-JennyNeural
No text detected	Check OCR quality / use clear images
Processing stuck	Check FastAPI logs for Gemini or TTS errors
ChromaDB error	Delete vector_db/ and restart backend
Image not selectable	Refresh browser; accept="image/*" now supported


### Run:

uvicorn app:app --reload
and

npm run dev
then open http://localhost:5173 to use your Audiobook Pipeline.
