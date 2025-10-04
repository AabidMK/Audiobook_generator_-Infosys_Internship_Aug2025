from sentence_transformers import SentenceTransformer, util
import re

# Load embedding model once
model = SentenceTransformer('all-MiniLM-L6-v2')

def chunk_text(text, chunk_size=100, overlap=20):
    """Split text into overlapping chunks."""
    words = text.split()
    chunks, start = [], 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(" ".join(words[start:end]))
        start += chunk_size - overlap
    return chunks

def retrieve_answer(query, chunks, model=model, top_k=5, similarity_threshold=0.4):
    """
    Retrieve top_k relevant chunks for the query.
    Returns list of tuples: (chunk_index, chunk_text)
    """
    if not chunks:
        return []

    query_embedding = model.encode(query, convert_to_tensor=True)
    chunk_embeddings = model.encode(chunks, convert_to_tensor=True)

    similarities = util.cos_sim(query_embedding, chunk_embeddings)[0]

    # keep track of index + text + similarity
    scored_chunks = list(zip(range(len(chunks)), chunks, similarities))

    # sort by similarity
    scored_chunks = sorted(scored_chunks, key=lambda x: x[2], reverse=True)

    # filter by threshold
    filtered = [(i, c) for i, c, s in scored_chunks if s.item() >= similarity_threshold]

    return filtered[:top_k]






