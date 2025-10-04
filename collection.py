import chromadb
from sentence_transformers import SentenceTransformer

# --- Setup client ---
client = chromadb.Client()  # no extra arguments

# --- Create collection if not exists ---
try:
    collection = client.get_collection("audiobook_chunks")
except chromadb.errors.NotFoundError:
    collection = client.create_collection("audiobook_chunks")

# --- Example chunks ---
chunks = ["This is chunk 1", "This is chunk 2", "Another chunk 3"]
ids = [f"chunk_{i}" for i in range(len(chunks))]  # unique ids
metadatas = [{"file_path": "rewritten_output.md", "chunk_index": i} for i in range(len(chunks))]

# --- Generate embeddings ---
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
embeddings = [embedder.encode(c).tolist() for c in chunks]

# --- Add documents ---
collection.add(
    ids=ids,
    documents=chunks,
    metadatas=metadatas,
    embeddings=embeddings
)

print("✅ Collection created and chunks added")


