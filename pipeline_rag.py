import logging
from enhanced_extraction import EnhancedTextExtraction  
from text_chunking import chunk_multiple_documents 
from vector_embedding import initialize_embedding_model, embed_chunks_for_pipeline
from chroma_storing import get_chroma_client, get_or_create_collection, store_chunks, persist_client
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from unicode_utils import clean_unicode_text, safe_print

# --- Logging setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("pipeline") 

def run_pipeline(file_paths):
    """
    Full pipeline: extract → chunk → embed → store in ChromaDB
    """
    # 1. Extract text
    all_documents = []
    for path in file_paths:
        try:
            text = EnhancedTextExtraction.extract_text_from_any(path)
            if not text or text.startswith("Error"):
                logger.warning(f"No text extracted from {path}")
                continue
            # Clean Unicode characters from extracted text
            clean_text = clean_unicode_text(text)
            all_documents.append((clean_text, "file", path))
            logger.info(f"Extraction successful for {path}")
        except Exception as e:
            logger.error(f"Failed to extract text from {path}: {e}")
            continue

    if not all_documents:
        logger.warning("No valid text extracted from the provided files")
        return
    safe_print("Text extraction complete")
    # 2. Chunk documents
    chunks = chunk_multiple_documents(all_documents, chunk_size=500, chunk_overlap=100)
    safe_print("Text chunking successful")

    # 3. Generate embeddings
    embedding_model = initialize_embedding_model()
    texts, embeddings, metadatas, ids = embed_chunks_for_pipeline(chunks, embedding_model)
    safe_print("Text embedding successful")

    # 4. Store in ChromaDB
    client = get_chroma_client()
    collection = get_or_create_collection(client)
    stored_count = store_chunks(collection, texts, embeddings, metadatas, ids)
    safe_print("Storing in chromadb is successful")

    # 5. Persist database
    persist_client(client)

    logger.info(f"Pipeline completed. Total chunks stored: {stored_count}")
    safe_print("Chromadb persisted to disk successfully")


if __name__ == "__main__":
    # Example: process multiple files
    file_list = [
        "uploads/abstractfinal (7).pdf",
        "uploads/frontfinal (21).pdf"
    ]
    run_pipeline(file_list)