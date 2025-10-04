from sentence_transformers import SentenceTransformer

def generate_embeddings(chunks):
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    embeddings = model.encode(chunks, convert_to_tensor=False)
    return embeddings


