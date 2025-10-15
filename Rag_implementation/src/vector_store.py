#vector_store.py
import os
import shutil
import logging
import warnings
import chromadb
from chromadb.utils import embedding_functions as ef
from chromadb.config import Settings

# 🔇 Suppress telemetry and warnings completely
warnings.filterwarnings("ignore", category=UserWarning)
logging.getLogger("chromadb.telemetry").setLevel(logging.ERROR)

# 🧠 Disable telemetry & force SentenceTransformer backend
os.environ["ANONYMIZED_TELEMETRY"] = "false"
os.environ["CHROMA_DEFAULT_EMBEDDING_FUNCTION"] = "sentence-transformers/all-MiniLM-L6-v2"


class VectorStoreManager:
    """
    Handles creation, storage, and querying of vector embeddings using ChromaDB.
    Supports cosine similarity and SentenceTransformer embeddings.
    """

    def __init__(self, backend="chroma", dim=384, collection="docs", persist_dir="chroma_db", metric="cosine"):
        self.backend = backend
        self.dim = dim
        self.collection_name = collection
        self.persist_dir = persist_dir
        self.metric = metric  # cosine, l2, ip

        if backend == "chroma":
            try:
                # ✅ Create persistent Chroma client
                self.client = chromadb.PersistentClient(
                    path=persist_dir,
                    settings=Settings(anonymized_telemetry=False)
                )

                # ✅ Use SentenceTransformer embeddings (no ONNX)
                embedding_fn = ef.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

                print(f"✅ Using SentenceTransformer backend (metric: {metric})")

                # ✅ Create or load collection with metric type
                self.collection = self.client.get_or_create_collection(
                    name=collection,
                    embedding_function=embedding_fn,
                    metadata={"hnsw:space": metric}
                )

            except Exception as e:
                logging.error(f"⚠️ Failed to load Chroma collection: {e}")
                logging.warning("🧹 Resetting corrupted ChromaDB folder...")

                # Reset Chroma if corrupted
                if os.path.exists(persist_dir):
                    shutil.rmtree(persist_dir)

                self.client = chromadb.PersistentClient(
                    path=persist_dir,
                    settings=Settings(anonymized_telemetry=False)
                )
                embedding_fn = ef.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

                self.collection = self.client.get_or_create_collection(
                    name=collection,
                    embedding_function=embedding_fn,
                    metadata={"hnsw:space": metric}
                )
        else:
            raise NotImplementedError(f"Backend '{backend}' not supported yet.")

    # ------------------------------------------------------
    # Add embeddings
    # ------------------------------------------------------
    def add_embeddings(self, ids, embeddings, metadatas, documents):
        """Add embeddings and metadata to Chroma collection."""
        if self.backend == "chroma":
            try:
                self.collection.add(
                    ids=ids,
                    embeddings=embeddings,
                    metadatas=metadatas,
                    documents=documents,
                )
                logging.info(f" Added {len(ids)} embeddings to collection '{self.collection_name}'.")
            except Exception as e:
                logging.error(f" Failed to add embeddings: {e}")

    # ------------------------------------------------------
    # Query embeddings
    # ------------------------------------------------------
    def query(self, query_embedding, n_results=5):
        """Query similar vectors using cosine similarity."""
        if self.backend == "chroma":
            try:
                return self.collection.query(
                    query_embeddings=[query_embedding],
                    n_results=n_results,
                )
            except Exception as e:
                logging.error(f" Error while querying vector store: {e}")
                return {"documents": [[]], "metadatas": [[]], "distances": [[]]}
