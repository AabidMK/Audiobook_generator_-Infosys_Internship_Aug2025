import os
import shutil
import logging
import chromadb
from chromadb.config import Settings


class VectorStoreManager:
    def __init__(self, backend="chroma", dim=384, collection="docs", persist_dir="chroma_db"):
        self.backend = backend
        self.dim = dim
        self.collection_name = collection
        self.persist_dir = persist_dir

        if backend == "chroma":
            self.client = chromadb.PersistentClient(path=persist_dir)
            try:
                self.collection = self.client.get_or_create_collection(collection)
            except Exception as e:
                logging.error(f"Chroma collection load failed: {e}")
                logging.warning(" Resetting corrupted ChromaDB folder...")

                # Remove corrupted folder
                if os.path.exists(persist_dir):
                    shutil.rmtree(persist_dir)

                # Recreate a clean DB
                self.client = chromadb.PersistentClient(path=persist_dir)
                self.collection = self.client.get_or_create_collection(collection)
        else:
            raise NotImplementedError(f"Backend {backend} not supported yet.")

    def add_embeddings(self, ids, embeddings, metadatas, documents):
        if self.backend == "chroma":
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                metadatas=metadatas,
                documents=documents,
            )

    def query(self, query_embedding, n_results=3):
        if self.backend == "chroma":
            return self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
            )
