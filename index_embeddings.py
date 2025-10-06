# index_embeddings.py
from sentence_transformers import SentenceTransformer
import chromadb
import os
from typing import List

PERSIST_PATH = "vector_db"
COLLECTION_NAME = "audiobook_chunks"
EMBED_MODEL = "intfloat/e5-base-v2"
CHUNK_WORDS = 500  # ~safe default for RAG

def chunk_text(text: str, chunk_size: int = CHUNK_WORDS) -> List[str]:
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

def main():
    # 1) Embedder
    embedder = SentenceTransformer(EMBED_MODEL)

    # 2) Chroma (persistent)
    client = chromadb.PersistentClient(path=PERSIST_PATH)
    try:
        collection = client.get_collection(COLLECTION_NAME)
    except Exception:
        collection = client.create_collection(COLLECTION_NAME)

    # 3) Index ALL *_rewritten.md files (idempotent by file_path)
    rewritten_files = [f for f in os.listdir() if f.endswith("_rewritten.md")]
    if not rewritten_files:
        raise RuntimeError("No *_rewritten.md files found. Run text extraction and rewriting first.")

    total_chunks = 0
    for file in sorted(rewritten_files):
        # Remove any previous chunks for this file to avoid duplicate-id errors
        try:
            collection.delete(where={"file_path": file})
        except Exception:
            pass

        with open(file, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = chunk_text(text, CHUNK_WORDS)
        if not chunks:
            continue

        # Embed all chunks in one go for speed
        embeddings = embedder.encode(chunks, normalize_embeddings=True).tolist()

        ids = [f"{file}_{i}" for i in range(len(chunks))]
        metas = [{"file_path": file, "chunk_id": i} for i in range(len(chunks))]

        collection.add(ids=ids, embeddings=embeddings, documents=chunks, metadatas=metas)
        total_chunks += len(chunks)
        print(f"Indexed {len(chunks):4d} chunks from {file}")

    print(f"\nFinished indexing. Total chunks: {total_chunks}")

if __name__ == "__main__":
    main()
