import os
import logging
from typing import List, Dict, Optional
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from unicode_utils import clean_unicode_text, clean_list_strings, clean_dict_values  

# --- Logging ---#
logging.basicConfig(level=logging.INFO)
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
    try:
        # Try to get existing collection first
        collection = client.get_collection(name=collection_name)
        logger.info(f"Using existing collection '{collection_name}'.")
        return collection
    except:
        # If collection doesn't exist, create it with embedding function
        try:
            # Delete existing collection if it has conflicts
            client.delete_collection(name=collection_name)
            logger.info(f"Deleted existing collection '{collection_name}' due to conflicts.")
        except:
            pass
        
        embedding_function = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        collection = client.create_collection(
            name=collection_name,
            embedding_function=embedding_function
        )
        logger.info(f"Created new collection '{collection_name}'.")
        return collection

# --- Store Chunks ---
def store_chunks(collection, texts: List[str], embeddings: List[List[float]], metadatas: List[Dict], ids: List[str]) -> int:
    """
    Store text chunks in the specified collection.
    """
    if not texts:
        logger.warning("No texts provided for storage.")
        return 0

    # Clean Unicode characters from all text data
    clean_texts = clean_list_strings(texts)
    clean_metadatas = [clean_dict_values(meta) for meta in metadatas]
    clean_ids = clean_list_strings(ids)

    collection.upsert(
        documents=clean_texts,
        embeddings=embeddings,
        metadatas=clean_metadatas,
        ids=clean_ids
    )

    logger.info(f"Stored {len(clean_texts)} chunks.")
    return len(clean_texts)

# --- Persist Database ---
def persist_client(client) -> None:
    """
    Persist data to disk if supported by the client.
    """
    if hasattr(client, 'persist'):
        client.persist()
        logger.info("Database persisted to disk.")