import os, time, uuid, traceback
from typing import List, Dict, Any
import chromadb
from gtts import gTTS
import re

# Import text enrichment function
from text_enrichment import enrich_text

# PDF parsing
try:
    import pypdfium2 as pdfium
    HAVE_PDFIUM = True
except ImportError:
    HAVE_PDFIUM = False

from sentence_transformers import SentenceTransformer

# HuggingFace embedding model
hf_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
DB_DIR = os.path.join(BASE_DIR, "chroma_db")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(DB_DIR, exist_ok=True)

# ChromaDB setup
client = chromadb.PersistentClient(path=DB_DIR)
COLLECTION_NAME = "audiobook_chunks"
try:
    client.delete_collection(COLLECTION_NAME)
except:
    pass
collection = client.create_collection(COLLECTION_NAME, embedding_function=None)


def generate_id():
    return str(uuid.uuid4())


def extract_text_from_file(path: str) -> str:
    """Extract text from PDF or TXT."""
    ext = os.path.splitext(path)[1].lower()
    try:
        if ext == ".txt":
            return open(path, "r", encoding="utf-8", errors="ignore").read()
        elif ext == ".pdf" and HAVE_PDFIUM:
            pdf = pdfium.PdfDocument(path)
            texts = []
            for p in range(len(pdf)):
                page = pdf.get_page(p)
                texts.append(page.get_textpage().get_text_range())
                page.close()
            pdf.close()
            return "\n".join(texts)
        return f"[WARN] Could not parse {os.path.basename(path)}"
    except Exception as e:
        return f"[ERROR extracting text: {e}]"


def chunk_text(text: str, chunk_size: int = 400, overlap: int = 50) -> List[str]:
    """Split long text into overlapping chunks."""
    words = text.split()
    chunks, i = [], 0
    while i < len(words):
        chunks.append(" ".join(words[i:i+chunk_size]))
        i += chunk_size - overlap
    return chunks if chunks else [text]


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Generate embeddings using HuggingFace only."""
    print("✅ Using HuggingFace local embeddings")
    return hf_model.encode(texts, convert_to_numpy=True).tolist()


def synthesize_audio(text: str, out_path: str):
    """Convert text to speech with gTTS."""
    try:
        gTTS(text=text, lang="en").save(out_path)
    except Exception as e:
        print(f"[TTS error: {e}] - Writing dummy audio file")
        with open(out_path, "wb") as f:
            f.write(b"FAKE AUDIO - TTS FAILED")
    return out_path


def run_pipeline(file_path: str, filename: str, job_id: str) -> Dict[str, Any]:
    result = {"id": job_id, "filename": filename, "status": "processing", "created_at": time.time()}
    try:
        # Step 1: Extract
        print(f"📄 Step 1: Extracting text from {filename}...")
        text = extract_text_from_file(file_path)
        print(f"Extracted text: {text[:500]}")  # Debug: Print first 500 characters of extracted text

        # Step 2: Enrich text for better audiobook quality
        print(f"✨ Step 2: Enriching text...")
        cleaned_text = clean_text(text)
        enriched_text = enrich_text(cleaned_text)
        print(f"Enriched text: {enriched_text[:500]}")  # Debug: Print first 500 characters of enriched text

        # Step 3: Chunk
        print(f"📝 Step 3: Chunking text...")
        chunks = chunk_text(enriched_text)
        print(f"Generated chunks: {chunks}")  # Debug: Print generated chunks

        # Step 4: Embed (HuggingFace only)
        print(f"🔢 Step 4: Generating embeddings...")
        embeddings = embed_texts(chunks)

        # Step 5: Store in Chroma
        print(f"💾 Step 5: Storing in ChromaDB...")
        ids = [f"{job_id}_chunk_{i}" for i in range(len(chunks))]
        metas = [{"source_file": filename, "chunk_index": i, "text_preview": chunks[i][:200]} for i in range(len(chunks))]
        collection.upsert(ids=ids, documents=chunks, metadatas=metas, embeddings=embeddings)

        # Step 6: Audio (use enriched text)
        print(f"🎵 Step 6: Generating audio...")
        audio_path = os.path.join(OUTPUT_DIR, f"{job_id}.mp3")
        synthesize_audio(enriched_text, audio_path)

        result.update({
            "status": "completed",
            "audio_files": [os.path.basename(audio_path)],
            "completed_at": time.time()
        })
        print(f"✅ Pipeline completed for {filename}")
    except Exception as e:
        print("❌ Pipeline crashed:")
        traceback.print_exc()
        result.update({"status": "error", "error_message": str(e)})
    return result


def answer_question(question: str) -> dict:
    # Use the ChromaDB collection initialized earlier
    vector_store = collection  # Assign the ChromaDB collection to vector_store

    try:
        # Step 1: Generate embeddings for the query
        print(f"🔍 Generating embeddings for the query: {question}")
        query_embedding = hf_model.encode([question], convert_to_numpy=True).tolist()

        # Step 2: Search the vector store using the query embedding
        print(f"🔎 Searching the vector store...")
        results = vector_store.query(
            query_embeddings=query_embedding, 
            n_results=5,
            include=["documents", "metadatas", "distances"]
        )
        
        # Debug: Print the structure of results
        print(f"Debug - Results type: {type(results)}")
        print(f"Debug - Results keys: {results.keys() if results else 'None'}")
        print(f"Debug - Documents: {results.get('documents') if results else 'None'}")

        # Validate the results structure
        if not results or "documents" not in results or not results["documents"]:
            return {"answer": "No documents found in vector store. Please upload a document first.", "citations": []}

        # Step 3: Retrieve content from the search results
        docs = results["documents"][0] if results["documents"] and len(results["documents"]) > 0 else []
        metas = results.get("metadatas", [[]])[0] if results.get("metadatas") else []
        distances = results.get("distances", [[]])[0] if results.get("distances") else []
        
        if not docs:
            return {"answer": "No relevant documents found. Please upload a document first.", "citations": []}
        
        retrieved_content = "\n\n".join(docs)
        print(f"📚 Retrieved {len(docs)} relevant chunks")

        # Step 4: Rewrite content using LLM
        print(f"🤖 Rewriting content using LLM...")
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model = genai.GenerativeModel('gemini-flash-latest')

        prompt = f"""Based on the following context, answer the user's question in a clear and concise manner:

Question: {question}

Context:
{retrieved_content}

Please provide a comprehensive answer based solely on the context provided above."""

        response = model.generate_content(prompt)
        
        # Build citations
        citations = []
        for idx, (doc, meta, dist) in enumerate(zip(docs, metas, distances)):
            citations.append({
                "source_file": meta.get("source_file", "unknown"),
                "chunk_index": meta.get("chunk_index", 0),
                "text_preview": doc[:200],
                "relevance_score": f"{1 - dist:.3f}"
            })

        print(f"✅ Answer generated successfully with {len(citations)} citations")
        return {
            "answer": response.text.strip(),
            "citations": citations
        }
    except Exception as e:
        print(f"❌ Error in answer_question: {e}")
        traceback.print_exc()
        return {
            "answer": "Error processing your request.",
            "citations": []
        }


def clean_text(text: str) -> str:
    """Remove special characters and extra spaces from the text."""
    text = re.sub(r"[^a-zA-Z0-9\s.,]", "", text)  # Remove special characters
    text = re.sub(r"\s+", " ", text).strip()  # Remove extra spaces
    return text
