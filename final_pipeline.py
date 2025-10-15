# final_pipeline.py
import os, time, uuid, traceback, re, logging
from typing import List, Dict, Any
from tqdm import tqdm
import chromadb

# ✅ Disable Chroma telemetry and suppress warnings
# ✅ Universal fix: Disable ChromaDB telemetry across all versions
try:
    import chromadb
    if hasattr(chromadb.telemetry, "_Telemetry"):
        chromadb.telemetry._Telemetry.capture = lambda *a, **kw: None
    elif hasattr(chromadb.telemetry, "Telemetry"):
        chromadb.telemetry.Telemetry.capture = lambda *a, **kw: None
    else:
        # For very new versions (>=0.5.11) where telemetry uses posthog
        chromadb.telemetry.posthog = None
except Exception:
    pass

import logging
logging.getLogger("chromadb").setLevel(logging.WARNING)

logging.getLogger("chromadb").setLevel(logging.WARNING)

from sentence_transformers import SentenceTransformer
from text_enrichment import enrich_text
from audio_generation import synthesize_audio, clean_for_audio

# ---------------- PDF Parsing ----------------
try:
    import pypdfium2 as pdfium
    HAVE_PDFIUM = True
except ImportError:
    HAVE_PDFIUM = False

# ---------------- HuggingFace Model ----------------
hf_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# ---------------- Directories ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
DB_DIR = os.path.join(BASE_DIR, "chroma_db")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(DB_DIR, exist_ok=True)

# ---------------- ChromaDB Setup ----------------
client = chromadb.PersistentClient(path=DB_DIR)
COLLECTION_NAME = "audiobook_chunks"

try:
    client.delete_collection(COLLECTION_NAME)
except Exception:
    pass

collection = client.create_collection(COLLECTION_NAME, embedding_function=None)


# ---------------- Utility ----------------
def generate_id() -> str:
    return str(uuid.uuid4())


# ---------------- Text Extraction ----------------
def extract_text_from_file(path: str) -> str:
    """Extract text from PDF or TXT."""
    ext = os.path.splitext(path)[1].lower()
    try:
        if ext == ".txt":
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        elif ext == ".pdf" and HAVE_PDFIUM:
            pdf = pdfium.PdfDocument(path)
            texts = []
            for p in tqdm(range(len(pdf)), desc="📄 Reading PDF pages", unit="page"):
                page = pdf.get_page(p)
                texts.append(page.get_textpage().get_text_range())
                page.close()
            pdf.close()
            return "\n".join(texts)
        else:
            return f"[WARN] Unsupported file type: {ext}"
    except Exception as e:
        return f"[ERROR extracting text: {e}]"


# ---------------- Text Chunking ----------------
def chunk_text(text: str, chunk_size: int = 400, overlap: int = 50) -> List[str]:
    """Split long text into overlapping chunks."""
    words = text.split()
    chunks, i = [], 0
    while i < len(words):
        chunks.append(" ".join(words[i:i + chunk_size]))
        i += chunk_size - overlap
    return chunks if chunks else [text]


# ---------------- Embedding ----------------
def embed_texts(texts: List[str]) -> List[List[float]]:
    """Generate embeddings with progress bar."""
    print("🔢 Generating text embeddings...")
    all_embeddings = []
    for chunk in tqdm(texts, desc="🧠 Embedding chunks", unit="chunk"):
        emb = hf_model.encode([chunk], convert_to_numpy=True).tolist()[0]
        all_embeddings.append(emb)
    print("✅ Embeddings generated successfully.")
    return all_embeddings


# ---------------- Core Pipeline ----------------
def run_pipeline(file_path: str, filename: str, job_id: str) -> Dict[str, Any]:
    """Main audiobook + RAG embedding pipeline."""
    result = {"id": job_id, "filename": filename, "status": "processing", "created_at": time.time()}

    try:
        # Step 1️⃣ Extract
        print(f"\n📄 Step 1: Extracting text from {filename}...")
        text = extract_text_from_file(file_path)
        print(f"📝 Extracted sample:\n{text[:300]}...\n")

        # Step 2️⃣ Enrich
        print("✨ Step 2: Enriching text for better audiobook flow...")
        cleaned_text = clean_text(text)
        enriched_text = enrich_text(cleaned_text)
        print(f"📘 Enriched text preview:\n{enriched_text[:300]}...\n")

        # Step 3️⃣ Chunk
        print("✂️ Step 3: Chunking text for embeddings...")
        chunks = chunk_text(enriched_text)
        print(f"✅ Total chunks created: {len(chunks)}\n")

        # Step 4️⃣ Embeddings
        print("🔢 Step 4: Generating embeddings...")
        embeddings = embed_texts(chunks)

        # Step 5️⃣ Store in ChromaDB
        print("💾 Step 5: Storing chunks and embeddings in ChromaDB...")
        ids = [f"{job_id}_chunk_{i}" for i in range(len(chunks))]
        metas = [{"source_file": filename, "chunk_index": i, "text_preview": chunks[i][:200]} for i in range(len(chunks))]
        collection.upsert(ids=ids, documents=chunks, metadatas=metas, embeddings=embeddings)
        print(f"📚 Stored {len(chunks)} chunks in ChromaDB.\n")

        # Step 6️⃣ Audio Generation
        print("🎧 Step 6: Generating clean audiobook (this may take a few minutes)...")
        audio_path = os.path.join(OUTPUT_DIR, f"{job_id}.mp3")
        cleaned_for_audio = clean_for_audio(enriched_text)
        synthesize_audio(cleaned_for_audio, audio_path)
        print(f"✅ Audiobook saved as: {audio_path}\n")

        result.update({
            "status": "completed",
            "audio_files": [os.path.basename(audio_path)],
            "completed_at": time.time()
        })
        print(f"🏁 Pipeline completed successfully for {filename} ✅\n")

    except Exception as e:
        print("❌ Pipeline crashed:")
        traceback.print_exc()
        result.update({"status": "error", "error_message": str(e)})

    return result


# ---------------- RAG QA System ----------------
def answer_question(question: str) -> dict:
    """Answer questions based on uploaded document context."""
    vector_store = collection
    try:
        print(f"🧠 RAG Query: {question}")
        query_embedding = hf_model.encode([question], convert_to_numpy=True).tolist()
        results = vector_store.query(
            query_embeddings=query_embedding,
            n_results=5,
            include=["documents", "metadatas", "distances"]
        )

        if not results or not results.get("documents"):
            return {"answer": "No relevant data found in uploaded documents.", "citations": []}

        docs = results["documents"][0]
        metas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]
        context = "\n\n".join(docs)
        print(f"📚 Retrieved {len(docs)} relevant chunks.")

        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel("gemini-flash-latest")

        prompt = f"""Based on the following context, answer the user's question in a clear and concise way.
Question: {question}

Context:
{context}

Answer:"""

        response = model.generate_content(prompt)
        answer = response.text.strip() if hasattr(response, "text") else "No valid response generated."

        citations = [{
            "source_file": m.get("source_file", "unknown"),
            "chunk_index": m.get("chunk_index", 0),
            "text_preview": d[:150],
            "relevance_score": f"{1 - dist:.3f}"
        } for d, m, dist in zip(docs, metas, distances)]

        print("✅ Answer generated successfully.")
        return {"answer": answer, "citations": citations}

    except Exception as e:
        print(f"❌ Error in answer_question: {e}")
        traceback.print_exc()
        return {"answer": "Error generating response.", "citations": []}


# ---------------- Text Cleaning ----------------
def clean_text(text: str) -> str:
    """Basic cleaner before enrichment."""
    text = re.sub(r"[^a-zA-Z0-9\s.,;:!?'\-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text
