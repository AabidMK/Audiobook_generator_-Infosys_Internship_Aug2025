from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_text(text, chunk_size=1000, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_text(text)

# Example usage
with open("enriched_text.md", "r", encoding="utf-8") as f:
    raw_text = f.read()

chunks = chunk_text(raw_text)
print(f"✅ Split into {len(chunks)} chunks")

from sentence_transformers import SentenceTransformer

# Load embedding model
embedding_model = SentenceTransformer("BAAI/bge-large-en")

# Convert chunks to embeddings
embeddings = embedding_model.encode(chunks, convert_to_numpy=True, show_progress_bar=True)

print(f"✅ Generated {len(embeddings)} embeddings of dimension {embeddings.shape[1]}")

import chromadb
from chromadb.utils import embedding_functions

# Create Chroma client (local storage)
client = chromadb.PersistentClient(path="./chroma_store")

# Define collection
collection = client.get_or_create_collection(
    name="audiobook_chunks"
)

# Add chunks with embeddings
for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
    collection.add(
        ids=[f"chunk_{i}"],
        embeddings=[emb.tolist()],
        documents=[chunk],
        metadatas=[{"chunk_id": i}]
    )

print("✅ Stored chunks in ChromaDB")


query = "Explain the main idea of the introduction chapter."

query_emb = embedding_model.encode([query], convert_to_numpy=True)[0]

results = collection.query(
    query_embeddings=[query_emb.tolist()],
    n_results=3
)

print("🔎 Retrieved Chunks:")
for doc in results["documents"][0]:
    print("-", doc[:200], "...")
