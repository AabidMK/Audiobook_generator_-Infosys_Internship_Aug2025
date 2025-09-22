
import logging
import chromadb
from chromadb.config import Settings
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest


class VectorStoreManager:
    def __init__(self, backend="chroma", persist_dir="chroma_db", collection="documents", dim: int = 384):
        self.backend = backend
        self.persist_dir = persist_dir

        if backend == "chroma":
            
            self.client = chromadb.PersistentClient(path=persist_dir)
            self.collection = self.client.get_or_create_collection(collection)
        elif backend == "qdrant":
            from qdrant_client import QdrantClient
            from qdrant_client.http import models as rest
            self.client = QdrantClient(path=persist_dir)
            self.collection = collection
            try:
                self.client.recreate_collection(
                    collection_name=collection,
                    vectors_config=rest.VectorsConfig(size=dim, distance=rest.Distance.COSINE)
                )
            except Exception:
                pass
        else:
            raise ValueError("Unsupported backend")


    def add_embeddings(self, ids, embeddings, metadatas, documents):
        if self.backend == "chroma":
            self.collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas, documents=documents)
            # persist for chroma
            try:
                self.client.persist()
            except Exception:
                pass
        else:
            points = [rest.PointStruct(id=i, vector=vec, payload={"doc": doc, **meta}) for i,(vec,doc,meta) in enumerate(zip(embeddings, documents, metadatas))]
            self.client.upsert(collection_name=self.collection, points=points)

    def query(self, query_emb, n_results=3):
        if self.backend == "chroma":
            return self.collection.query(query_embeddings=[query_emb], n_results=n_results)
        else:
            return self.client.search(collection_name=self.collection, query_vector=query_emb, limit=n_results)
