from sentence_transformers import SentenceTransformer
import chromadb
import os

# --- 1. Load embedding model ---
embedder = SentenceTransformer("intfloat/e5-base-v2")

# --- 2. Init ChromaDB persistent client ---
client = chromadb.PersistentClient(path="vector_db")

# Create collection if it doesn’t exist
try:
    collection = client.get_collection("audiobook_chunks")
except:
    collection = client.create_collection("audiobook_chunks")

# --- 3. Load rewritten text (latest *_rewritten.md) ---
rewritten_files = [f for f in os.listdir() if f.endswith("_rewritten.md")]
if not rewritten_files:
    raise RuntimeError("No *_rewritten.md files found. Run text extraction + rewriting first.")

latest_file = max(rewritten_files, key=os.path.getmtime)
print(f"Ingesting: {latest_file}")

with open(latest_file, "r", encoding="utf-8") as f:
    text = f.read()

# --- 4. Chunk text ---
def chunk_text(text, chunk_size=500):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i:i+chunk_size])

chunks = list(chunk_text(text))

# --- 5. Embed and add to Chroma ---
for i, chunk in enumerate(chunks):
    emb = embedder.encode([chunk], normalize_embeddings=True).tolist()[0]
    collection.add(
        ids=[f"{latest_file}_{i}"],
        embeddings=[emb],
        documents=[chunk],
        metadatas=[{"file_path": latest_file, "chunk_id": i}]
    )

print(f" Ingested {len(chunks)} chunks into 'audiobook_chunks'")
