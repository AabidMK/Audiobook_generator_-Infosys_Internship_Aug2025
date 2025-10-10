# app.py
import os, sys, uuid, json, asyncio
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

import chromadb
from sentence_transformers import SentenceTransformer

# optional token counting
try:
    import tiktoken
    _enc = tiktoken.get_encoding("cl100k_base")
    def token_len(s: str) -> int: return len(_enc.encode(s))
except Exception:
    def token_len(s: str) -> int: return max(1, len(s)//4)

# local extract helpers (no GUI)
import pdfplumber
import docx

# your Gemini rewriter (writes *_rewritten.md next to the raw)
from text_extraction_gemini import rewrite_file as gemini_rewrite_file

# in-process Edge TTS
try:
    import edge_tts
except Exception:
    edge_tts = None

# Optional: PyMuPDF for scanned-PDF OCR fallback
try:
    import fitz  # PyMuPDF
    from PIL import Image
    HAS_PYMUPDF = True
except Exception:
    HAS_PYMUPDF = False

# EasyOCR (required for image OCR)
try:
    import easyocr
    _EASYOCR_READER = easyocr.Reader(["en"], gpu=False)
except Exception as e:
    _EASYOCR_READER = None


# ------------------------- Config -------------------------
PERSIST_PATH    = os.getenv("CHROMA_PATH", "vector_db")
COLLECTION_NAME = os.getenv("CHROMA_COLLECTION", "audiobook_chunks")
EMBED_MODEL     = os.getenv("EMBED_MODEL", "intfloat/e5-base-v2")

BASE_DIR   = os.getcwd()
DATA_DIR   = os.path.abspath(os.path.join(BASE_DIR, "data"))
UPLOAD_DIR = os.path.abspath(os.path.join(BASE_DIR, "uploads"))
for d in (DATA_DIR, UPLOAD_DIR): os.makedirs(d, exist_ok=True)

TOP_K = 5
MAX_CONTEXT_TOKENS = 6000

VOICE = os.getenv("EDGE_TTS_VOICE", "en-GB-SoniaNeural")
RATE  = os.getenv("EDGE_TTS_RATE", "-10%")

PREFERRED_GEMINI = [
    "gemini-2.5-flash",
    "gemini-flash-latest",
    "gemini-2.0-flash",
    "gemini-pro-latest",
]


# ------------------------- App -------------------------
app = FastAPI(title="Audiobook Pipeline API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Vector store + embedder ----------------
_embedder = SentenceTransformer(EMBED_MODEL)
_chroma   = chromadb.PersistentClient(path=PERSIST_PATH)
try:
    _col = _chroma.get_collection(COLLECTION_NAME)
except Exception:
    _col = _chroma.create_collection(COLLECTION_NAME)

# ---------------- Catalog ----------------
CATALOG_PATH = os.path.join(DATA_DIR, "audiobooks.json")
def _load_catalog():
    return json.load(open(CATALOG_PATH, "r", encoding="utf-8")) if os.path.exists(CATALOG_PATH) else {}
def _save_catalog(d):
    with open(CATALOG_PATH, "w", encoding="utf-8") as f: json.dump(d, f, indent=2)
_catalog = _load_catalog()


# ---------------- OCR helpers (EasyOCR only) ----------------
def _require_easyocr():
    if _EASYOCR_READER is None:
        raise HTTPException(
            status_code=500,
            detail="easyocr is not installed. Run: pip install easyocr pillow"
        )

def _ocr_image_pil(pil_img: "Image.Image") -> str:
    _require_easyocr()
    import numpy as np
    arr = np.array(pil_img.convert("RGB"))
    lines = _EASYOCR_READER.readtext(arr, detail=0)
    return "\n".join(lines).strip()


# ---------------- Extractors ----------------
def _extract_pdf(path: str, ocr_fallback: bool = True, ocr_min_chars: int = 20) -> str:
    """
    Extract text from a PDF using pdfplumber.
    If a page has too little text (likely scanned), and PyMuPDF is available,
    render page to image and OCR it with EasyOCR.
    """
    parts = []
    with pdfplumber.open(path) as pdf:
        total = len(pdf.pages)
        for i, page in enumerate(pdf.pages, start=1):
            page_text = (page.extract_text() or "").strip()
            if ocr_fallback and len(page_text) < ocr_min_chars and HAS_PYMUPDF:
                # OCR this page
                ocr_txt = _ocr_pdf_page(path, i)
                if ocr_txt.strip():
                    page_text = ocr_txt.strip()
            parts.append(f"\n\n## Page {i}\n\n{page_text}" if page_text else f"\n\n## Page {i}\n\n")
    return ("\n".join(parts)).strip()

def _ocr_pdf_page(pdf_path: str, page_number_1based: int, zoom: float = 2.0) -> str:
    if not HAS_PYMUPDF:
        return ""
    doc = fitz.open(pdf_path)
    try:
        page = doc[page_number_1based - 1]
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        return _ocr_image_pil(img)
    finally:
        doc.close()

def _extract_docx(path: str) -> str:
    d = docx.Document(path)
    return "\n".join(p.text for p in d.paragraphs).strip()

def _extract_txt(path: str) -> str:
    return open(path, "r", encoding="utf-8", errors="ignore").read().strip()

def _extract_image(path: str) -> str:
    """
    EasyOCR only for images (PNG/JPG/JPEG/TIFF/BMP).
    """
    _require_easyocr()
    from PIL import Image as _PILImage
    img = _PILImage.open(path)
    return _ocr_image_pil(img)

def extract_text_to_named_raw_md(src_path: str) -> str:
    """
    Save extracted text as <originalbase>_raw.md in the SAME folder as the upload.
    Supports: PDF, DOCX, TXT, MD, PNG, JPG, JPEG, TIFF, BMP
    """
    ext  = os.path.splitext(src_path)[1].lower()
    base = os.path.splitext(os.path.basename(src_path))[0]
    out_dir = os.path.dirname(src_path)
    raw_md_path = os.path.join(out_dir, f"{base}_raw.md")

    if ext == ".pdf":
        text = _extract_pdf(src_path, ocr_fallback=True, ocr_min_chars=20)
    elif ext == ".docx":
        text = _extract_docx(src_path)
    elif ext in [".txt", ".md"]:
        text = _extract_txt(src_path)
    elif ext in [".png", ".jpg", ".jpeg", ".tiff", ".bmp"]:
        text = _extract_image(src_path)
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")

    if not text.strip():
        raise HTTPException(status_code=400, detail="No text extracted from the file.")

    with open(raw_md_path, "w", encoding="utf-8") as f:
        f.write(f"# Extracted Text ({os.path.basename(src_path)})\n\n")
        f.write(text)
        if not text.endswith("\n"):
            f.write("\n")

    return raw_md_path


# ---------------- Helpers: RAG + TTS ----------------
def chunk_text(text: str, chunk_words: int = 500) -> List[str]:
    w = text.split()
    return [" ".join(w[i:i+chunk_words]) for i in range(0, len(w), chunk_words)]

def add_to_chroma(item_id: str, file_path: str, chunks: List[str]):
    embs = _embedder.encode(chunks, normalize_embeddings=True).tolist()
    ids   = [f"{item_id}_{i}" for i in range(len(chunks))]
    metas = [{"audiobook_id": item_id, "file_path": file_path, "chunk_id": i} for i in range(len(chunks))]
    _col.add(ids=ids, embeddings=embs, documents=chunks, metadatas=metas)

def trim_to_tokens(parts: List[str], limit: int) -> List[str]:
    out, used = [], 0
    for p in parts:
        t = token_len(p)
        if used + t > limit: break
        out.append(p); used += t
    return out

def search_chunks(question: str, audiobook_id: Optional[str] = None, top_k: int = TOP_K):
    q = _embedder.encode([question], normalize_embeddings=True).tolist()
    kwargs = dict(query_embeddings=q, n_results=top_k, include=["documents","metadatas","distances"])
    if audiobook_id: kwargs["where"] = {"audiobook_id": audiobook_id}
    res = _col.query(**kwargs)
    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    dists = [float(x) for x in res.get("distances", [[]])[0]]
    return docs, metas, dists

async def edge_tts_from_markdown(md_path: str) -> str:
    """Generate <originalbase>.mp3 next to the rewritten md, in-process."""
    if edge_tts is None:
        raise RuntimeError("edge-tts is not installed. Run: pip install edge-tts")

    base = os.path.splitext(os.path.basename(md_path))[0]
    if base.endswith("_rewritten"):
        base = base[:-10]
    out_dir = os.path.dirname(md_path)
    mp3_path = os.path.join(out_dir, f"{base}.mp3")

    text = open(md_path, "r", encoding="utf-8").read()
    communicate = edge_tts.Communicate(text=text, voice=VOICE, rate=RATE)
    await communicate.save(mp3_path)
    if not os.path.exists(mp3_path):
        raise RuntimeError("Edge TTS did not create an MP3 file.")
    return mp3_path


# ---------------- Gemini helpers ----------------
def _pick_gemini_model(preferred=PREFERRED_GEMINI) -> str:
    api_key = os.getenv("GOOGLE_API_KEY", "").strip()
    if not api_key:
        raise HTTPException(status_code=500, detail="GOOGLE_API_KEY is not set.")
    import google.generativeai as genai
    genai.configure(api_key=api_key)

    try:
        available = [
            m.name.split("/")[-1]
            for m in genai.list_models()
            if "generateContent" in getattr(m, "supported_generation_methods", [])
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini list_models failed: {e}")

    for cand in preferred:
        if cand in available:
            return cand
    # last resort
    if available:
        return available[0]
    raise HTTPException(status_code=500, detail="No suitable Gemini model available for generateContent.")


# ---------------- Schemas ----------------
class UploadResponse(BaseModel):
    id: str
    title: str
    play_url: str
    download_url: str

class AskRequest(BaseModel):
    question: str
    audiobook_id: Optional[str] = None

class AskResponse(BaseModel):
    answer: str
    citations: List[dict]


# ---------------- Routes ----------------
@app.post("/pipeline/ingest", response_model=UploadResponse)
def pipeline_ingest(file: UploadFile = File(...), title: str = Form(None)):
    """
    Mandatory pipeline and naming:
      <original>.ext, <original>_raw.md, <original>_rewritten.md, <original>.mp3
      Everything is stored under uploads/<session-id>/.
    Supports images: PNG, JPG, JPEG, TIFF, BMP.
    """
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in [".pdf", ".docx", ".txt", ".md", ".png", ".jpg", ".jpeg", ".tiff", ".bmp"]:
        raise HTTPException(status_code=400, detail="Supported: PDF, DOCX, TXT, MD, PNG, JPG, JPEG, TIFF, BMP")

    original_name = os.path.basename(file.filename)
    session_dir = os.path.join(UPLOAD_DIR, uuid.uuid4().hex[:8])
    os.makedirs(session_dir, exist_ok=True)
    upload_path = os.path.abspath(os.path.join(session_dir, original_name))
    with open(upload_path, "wb") as f:
        f.write(file.file.read())

    # 1) Extract -> <base>_raw.md
    raw_md_path = extract_text_to_named_raw_md(upload_path)

    # 2) Gemini rewrite (mandatory) -> <base>_rewritten.md
    rewritten_md_path = gemini_rewrite_file(raw_md_path)
    if not os.path.isabs(rewritten_md_path):
        rewritten_md_path = os.path.abspath(rewritten_md_path)

    # 3) Edge TTS in-process -> <base>.mp3
    try:
        mp3_path = asyncio.run(edge_tts_from_markdown(rewritten_md_path))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS failed: {e}")

    # 4) Index rewritten text into Chroma
    text = open(rewritten_md_path, "r", encoding="utf-8").read()
    chunks = chunk_text(text, 500)
    if chunks:
        add_to_chroma(os.path.basename(session_dir), rewritten_md_path, chunks)

    # 5) Catalog
    base = os.path.splitext(original_name)[0]
    item = {
        "id": os.path.basename(session_dir),
        "title": title or base,
        "filename": original_name,
        "raw_path": raw_md_path,
        "rewritten_path": rewritten_md_path,
        "audio_path": mp3_path,
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    _catalog[item["id"]] = item
    _save_catalog(_catalog)

    base_url = os.getenv("PUBLIC_BASE_URL", "").rstrip("/")
    play_url = f"{base_url}/audiobooks/{item['id']}/stream"
    download_url = f"{base_url}/audiobooks/{item['id']}/download"
    return UploadResponse(id=item["id"], title=item["title"], play_url=play_url, download_url=download_url)

@app.get("/audiobooks")
def list_audiobooks():
    items = list(_catalog.values())
    items.sort(key=lambda x: x["created_at"], reverse=True)
    return items

@app.get("/audiobooks/{uid}/stream")
def stream_audio(uid: str):
    item = _catalog.get(uid)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    path = item["audio_path"]
    if not os.path.exists(path): raise HTTPException(status_code=404, detail="Audio missing")
    return FileResponse(path, media_type="audio/mpeg")

@app.get("/audiobooks/{uid}/download")
def download_audio(uid: str):
    item = _catalog.get(uid)
    if not item: raise HTTPException(status_code=404, detail="Not found")
    path = item["audio_path"]
    if not os.path.exists(path): raise HTTPException(status_code=404, detail="Audio missing")
    return FileResponse(path, media_type="audio/mpeg", filename=os.path.basename(path))

@app.post("/rag/ask", response_model=AskResponse)
def rag_ask(req: AskRequest):
    q = req.question.strip()
    if not q: raise HTTPException(status_code=400, detail="Question required")

    docs, metas, dists = search_chunks(q, req.audiobook_id, TOP_K)
    if not docs:
        return AskResponse(answer="I don't know.", citations=[])

    parts = trim_to_tokens(docs, MAX_CONTEXT_TOKENS)
    context = "\n\n---\n\n".join(parts)

    prompt = (
        "Use ONLY the provided context. If the answer is not in the context, say 'I don't know.' "
        "Be concise.\n\n"
        f"# Context\n{context}\n\n# Question\n{q}\n\n# Answer\n"
    )

    answer = ""
    api_key = os.getenv("GOOGLE_API_KEY", "").strip()
    if api_key:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        try:
            model_name = _pick_gemini_model()
            model = genai.GenerativeModel(model_name)
            resp = model.generate_content(prompt, generation_config={"temperature": 0.2})
            answer = (getattr(resp, "text", "") or "").strip()
        except Exception:
            answer = ""
    if not answer:
        answer = "I don't know." if q.lower() not in context.lower() else context[:500] + "..."

    citations = []
    for m, dist in zip(metas, dists):
        citations.append({
            "file_path": m.get("file_path", "unknown"),
            "chunk_id": m.get("chunk_id", "n/a"),
            "audiobook_id": m.get("audiobook_id", ""),
            "distance": round(float(dist), 4),
            "similarity": round(1.0 - float(dist), 4),
        })
    return AskResponse(answer=answer, citations=citations)


# Simple health check
@app.get("/healthz")
def healthz():
    return {"ok": True}
