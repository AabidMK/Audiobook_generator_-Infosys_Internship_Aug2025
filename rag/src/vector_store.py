# rag/src/vector_store.py
import logging
import chromadb
from chromadb.config import Settings
from src.embedding_manager import GemmaEmbedder

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, persist_dir="./chromadb_store", collection_name="documents"):
        self.client = chromadb.Client(Settings(persist_directory=persist_dir))
        self.collection = self.client.get_or_create_collection(name=collection_name)
        self.embedder = GemmaEmbedder()

    def add_chunks(self, chunks):
        if not chunks:
            logger.warning("No chunks to add to vector database.")
            return
            
        texts = [chunk.text for chunk in chunks]
        embeddings = self.embedder.encode(texts)
        ids = [f"{chunk.source_file}_chunk_{chunk.chunk_index}" for chunk in chunks]
        metadatas = [{"chunk_index": chunk.chunk_index, "source_file": chunk.source_file} for chunk in chunks]

        self.collection.add(
            documents=texts,
            embeddings=embeddings.tolist(),
            ids=ids,
            metadatas=metadatas
        )
        logger.info(f"Added {len(chunks)} chunks to vector database")

    def query(self, query_text, n_results=3):
        query_embedding = self.embedder.encode([query_text]).tolist()
        return self.collection.query(
            query_embeddings=query_embedding, 
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )