import logging
from  embedding_extraction import extract_text
from chunking import chunk_multiple_documents
from embedding import initialize_embedding_model, embed_chunks_for_pipeline
from chroma_store import get_chroma_client, get_or_create_collection, store_chunks, persist_client
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# --- Logging setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("pipeline")

def run_pipeline(file_paths):
    """
    Full pipeline: extract → chunk → embed → store in ChromaDB
    """
    # 1. Extract text
    documents = []
    for path in file_paths:
        text, error = extract_text(path)
        if error:
            logger.error(f"Failed to process {path}: {error}")
            continue
        documents.append((text, "file", path))  # source = "file"

    if not documents:
        logger.warning("No valid documents to process.")
        return
    print("Text extraction successful")

    # 2. Chunk documents
    chunks = chunk_multiple_documents(documents, chunk_size=500, chunk_overlap=100)
    print("Text chunking successful")

    # 3. Generate embeddings
    embedding_model = initialize_embedding_model()
    texts, embeddings, metadatas, ids = embed_chunks_for_pipeline(chunks, embedding_model)
    print("Text embedding successful")

    # 4. Store in ChromaDB
    client = get_chroma_client()
    collection = get_or_create_collection(client)
    embedding_function=SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    collection._embedding_function=embedding_function
    stored_count = store_chunks(collection, texts, metadatas, ids)
    print("Storing in chromadb is successful")

    # 5. Persist database
    persist_client(client)

    logger.info(f"Pipeline completed. Total chunks stored: {stored_count}")
    print("Chromadb persisted to disk successfully")


if __name__ == "__main__":
    # Example: process multiple files
    file_list = [
        "embedding_input.pdf"
    ]
    run_pipeline(file_list)