from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embeddings(chunks):
    """
    Convert a list of text chunks into embeddings.
    """
    if not chunks:
        return []

    print(f"Generating embeddings for {len(chunks)} chunks...")
    embeddings = model.encode(chunks, show_progress_bar=False)
    print("Embeddings generated successfully.")

    return embeddings.tolist() 