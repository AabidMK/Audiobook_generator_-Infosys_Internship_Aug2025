# storage.py (updated)

import chromadb

def chunk_text(text, chunk_size=300, overlap=50):
    """
    Split text into overlapping chunks.
    - chunk_size: number of words per chunk
    - overlap: number of overlapping words between consecutive chunks
    """
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start = end - overlap  # overlap for context

        # prevent negative start for next chunk
        if start < 0:
            start = 0

        # stop if we've reached the end
        if start >= len(words):
            break

    return chunks


def save_chunks_to_chromadb(text, embeddings, file_path="example.txt", collection_name="audiobook_chunks"):
    """
    Split text into chunks and store them with embeddings in ChromaDB.
    """
    # Split text into chunks
    chunks = chunk_text(text)

    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(name=collection_name)

    # Save chunks with IDs and metadata
    collection.add(
        ids=[f"{file_path}_chunk_{i}" for i in range(len(chunks))],
        documents=chunks,
        embeddings=embeddings,
        metadatas=[{"chunk_index": i, "file_path": file_path} for i in range(len(chunks))]
    )

    print(f"✅ Stored {len(chunks)} unique chunks in ChromaDB collection '{collection_name}'")
    return collection




