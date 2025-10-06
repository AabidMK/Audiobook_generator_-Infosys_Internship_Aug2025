import os
import shutil
import logging

# 🧠 Force Chroma to skip ONNX and use SentenceTransformer backend
os.environ["CHROMA_DEFAULT_EMBEDDING_FUNCTION"] = "sentence-transformers/all-MiniLM-L6-v2"

import chromadb
from chromadb.utils import embedding_functions as ef


class VectorStoreManager:
    """
    Handles creation, storage, and querying of vector embeddings using ChromaDB.
    This version completely disables ONNX and uses SentenceTransformer backend.
    """

    def __init__(self, backend="chroma", dim=384, collection="docs", persist_dir="chroma_db"):
        self.backend = backend
        self.dim = dim
        self.collection_name = collection
        self.persist_dir = persist_dir

        if backend == "chroma":
            # Initialize Chroma persistent client
            self.client = chromadb.PersistentClient(path=persist_dir)

            # ✅ Always use SentenceTransformer embeddings (no ONNX)
            embedding_fn = ef.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

            # Diagnostic confirmation
            print("✅ Using SentenceTransformer backend for embeddings (no ONNX).")

            try:
                self.collection = self.client.get_or_create_collection(
                    name=collection,
                    embedding_function=embedding_fn,
                )

            except Exception as e:
                logging.error(f"Chroma collection load failed: {e}")
                logging.warning("Resetting corrupted ChromaDB folder...")

                # 🧹 Remove corrupted Chroma directory and recreate
                if os.path.exists(persist_dir):
                    shutil.rmtree(persist_dir)

                self.client = chromadb.PersistentClient(path=persist_dir)
                self.collection = self.client.get_or_create_collection(
                    name=collection,
                    embedding_function=embedding_fn,
                )

        else:
            raise NotImplementedError(f"Backend '{backend}' not supported yet.")

    # ------------------------------------------------------
    # Add new embeddings
    # ------------------------------------------------------
    def add_embeddings(self, ids, embeddings, metadatas, documents):
        """Add embeddings and corresponding metadata to Chroma collection."""
        if self.backend == "chroma":
            try:
                self.collection.add(
                    ids=ids,
                    embeddings=embeddings,
                    metadatas=metadatas,
                    documents=documents,
                )
                logging.info(f"✅ Added {len(ids)} embeddings to Chroma collection '{self.collection_name}'.")
            except Exception as e:
                logging.error(f"Failed to add embeddings: {e}")

    # ------------------------------------------------------
    # Query existing embeddings
    # ------------------------------------------------------
    def query(self, query_embedding, n_results=3):
        """Query similar vectors using cosine similarity."""
        if self.backend == "chroma":
            try:
                return self.collection.query(
                    query_embeddings=[query_embedding],
                    n_results=n_results,
                )
            except Exception as e:
                logging.error(f"Error while querying vector store: {e}")
                return {"documents": [[]], "metadatas": [[]], "distances": [[]]}
