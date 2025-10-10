import os
import logging
from typing import List, Dict, Optional
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction  
#from chromadb.config import Settings

# --- Logging ---#
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- ChromaDB Config ---#
COLLECTION_NAME = "documents"
PERSIST_DIR="chroma_db_audiobook"

# -------------------
# Helper: generate unique chunk ID
# -------------------
def generate_chunk_id(file_path: str, chunk_index: int) -> str:
    import hashlib
    file_stem = file_path.split('/')[-1].split('\\')[-1]
    if '.' in file_stem:
        file_stem = file_stem.rsplit('.', 1)[0]
    path_hash = hashlib.md5(file_path.encode('utf-8')).hexdigest()[:10]
    return f"{file_stem}-{path_hash}-{chunk_index}"

# --- Get ChromaDB Client ---
def get_chroma_client():
    """
    Initialize a persistent ChromaDB client.
    """

    client=chromadb.PersistentClient(path=PERSIST_DIR)
    logger.info("ChromaDB client initialized.")
    return client
# --- Get or Create Collection ---
def get_or_create_collection(client, collection_name: str = COLLECTION_NAME):
    """
    Get or create a ChromaDB collection.
    """
    embedding_function=SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_function
    )
    logger.info(f"Collection '{collection_name}' is ready.")
    return collection

# --- Store Chunks ---
def store_chunks(collection, texts: List[str], metadatas: List[Dict], ids: List[str] ,embeddings: List[List[float]]) :
    """
    Store text chunks in the specified collection.
    """
    if not texts:
        logger.warning("No texts provided for storage.")
        return 0

    collection.upsert(
        documents=texts,
        metadatas=metadatas,
        ids=ids,
        embeddings=embeddings
    )

    logger.info(f"Stored {len(texts)} chunks.")
    return len(texts)

# --- Persist Database ---
def persist_client(client) -> None:
    """
    Persist data to disk if supported by the client.
    """
    if hasattr(client, 'persist'):
        client.persist()
        logger.info("Database persisted to disk.")