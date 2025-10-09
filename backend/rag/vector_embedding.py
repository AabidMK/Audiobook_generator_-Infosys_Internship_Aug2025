import logging
import hashlib
from typing import List, Dict, Tuple
from sentence_transformers import SentenceTransformer

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

def initialize_embedding_model(model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> SentenceTransformer:
    """
    Initializes and returns the SentenceTransformer embedding model.
    """
    try:
        model = SentenceTransformer(model_name)
        logging.info(f"Initialized embedding model: {model_name}")
        return model
    except Exception as e:
        logging.error(f"Failed to initialize embedding model ({model_name}): {e}")
        raise RuntimeError("Sentence-transformers must be installed to use this function") from e

def generate_embeddings(texts: List[str], embedding_model: SentenceTransformer) -> List[List[float]]:
    """
    Generates embeddings for a list of texts using the provided SentenceTransformer model.
    """
    if not texts:
        logging.warning("No texts provided for embedding generation")
        return []

    logging.info(f"Generating embeddings for {len(texts)} texts")
    try:
        embeddings = embedding_model.encode(texts, convert_to_tensor=False)  # np.ndarray
        embeddings = embeddings.tolist()  # convert to list of lists
        if len(embeddings) != len(texts):
            raise ValueError("Number of generated embeddings does not match number of texts.")
        logging.debug(f"Generated embeddings shape: {len(embeddings)} x {len(embeddings[0])}")
        return embeddings
    except Exception as e:
        logging.error(f"Failed to generate embeddings: {e}")
        raise

def generate_chunk_id(file_path: str, chunk_index: int) -> str:
    """
    Generates a unique ID for a text chunk based on its file path and index.
    """
    file_stem = file_path.split('/')[-1].split('\\')[-1]
    if '.' in file_stem:
        file_stem = file_stem.rsplit('.', 1)[0]
    
    path_hash = hashlib.md5(file_path.encode('utf-8')).hexdigest()[:10]
    return f"{file_stem}-{path_hash}-{chunk_index}"

def embed_chunks_for_pipeline(
    chunks: List[Dict],
    embedding_model: SentenceTransformer
) -> Tuple[List[str], List[List[float]], List[Dict], List[str]]:
    """
    Takes a list of chunk dictionaries, generates embeddings, and prepares data
    for the next pipeline step.
    
    Args:
        chunks (List[Dict]): Each dict must have 'text', 'file_path', 'chunk_index'.
        embedding_model (SentenceTransformer): Pre-initialized model.

    Returns:
        Tuple[List[str], List[List[float]], List[Dict], List[str]]:
            - A list of the chunk texts.
            - A list of the generated embeddings.
            - A list of metadata dictionaries.
            - A list of unique IDs for each chunk.
    """
    if not chunks:
        logging.warning("No chunks provided for embedding")
        return [], [], [], []

    texts = [chunk["text"] for chunk in chunks]
    embeddings = generate_embeddings(texts, embedding_model)

    metadatas, ids = [], []
    for chunk in chunks:
        chunk_id = generate_chunk_id(chunk["file_path"], chunk["chunk_index"])
        ids.append(chunk_id)

        metadata = {
            "source": chunk.get("source", ""),   # keep original source if available
            "file_path": chunk["file_path"],
            "chunk_index": chunk["chunk_index"],
            "chunk_text_length": len(chunk["text"])
        }
        metadatas.append(metadata)

    logging.info(f"Prepared {len(chunks)} chunks for vector database storage")
    return texts, embeddings, metadatas, ids