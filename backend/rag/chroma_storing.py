import os
import logging
from typing import List, Dict, Optional
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction  

# --- Logging ---#
logging.basicConfig(level=logging.INFO, encoding='utf-8')
logger = logging.getLogger(__name__)
 
# --- ChromaDB Config ---#
COLLECTION_NAME = "documents"
PERSIST_DIR="chroma_db"

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
def store_chunks(collection, texts: List[str], embeddings: List[List[float]] ,metadatas: List[Dict], ids: List[str]) -> int:
    """
    Store text chunks in the specified collection.
    """
    if not texts:
        logger.warning("No texts provided for storage.")
        return 0

    collection.upsert(
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
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