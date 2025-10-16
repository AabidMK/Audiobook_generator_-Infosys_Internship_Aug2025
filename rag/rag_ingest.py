import os
from pathlib import Path
from dotenv import load_dotenv
import fitz  # PyMuPDF for PDF
import docx
from PIL import Image
import pytesseract
import chromadb
from sentence_transformers import SentenceTransformer

# Load environment
load_dotenv()

# Directories
INPUT_DIR = Path("input_files")
DB_DIR = Path("chroma_db")
DB_DIR.mkdir(exist_ok=True)

# Initialize ChromaDB and embedding model
chroma_client = chromadb.PersistentClient(path=str(DB_DIR))
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
collection = chroma_client.get_or_create_collection("documents")

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# ------------ FILE PARSERS ----------------
def parse_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text("text")
    return text.strip()

def parse_txt(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read().strip()

def parse_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

def parse_image(file_path):
    img = Image.open(file_path)
    text = pytesseract.image_to_string(img)
    return text.strip()

def parse_file(file_path):
    if file_path.suffix.lower() == ".pdf":
        return parse_pdf(file_path)
    elif file_path.suffix.lower() in [".txt"]:
        return parse_txt(file_path)
    elif file_path.suffix.lower() in [".docx"]:
        return parse_docx(file_path)
    elif file_path.suffix.lower() in [".png", ".jpg", ".jpeg"]:
        return parse_image(file_path)
    else:
        print(f"⚠️ Skipping unsupported file: {file_path.name}")
        return None

# ------------ CHUNKING ----------------
def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

# ------------ INGESTION ----------------
def ingest_files():
    for file_path in INPUT_DIR.iterdir():
        text = parse_file(file_path)
        if not text:
            continue

        chunks = chunk_text(text)
        embeddings = embedding_model.encode(chunks).tolist()

        collection.add(
            ids=[f"{file_path.stem}_{i}" for i in range(len(chunks))],
            documents=chunks,
            embeddings=embeddings,
            metadatas=[{"source": file_path.name, "chunk": i} for i in range(len(chunks))]
        )

        print(f"✅ {file_path.name} → {len(chunks)} chunks stored")

    print("🎉 Ingestion complete! All files stored in ChromaDB.")

# ------------ MAIN ----------------
if __name__ == "__main__":
    ingest_files()
