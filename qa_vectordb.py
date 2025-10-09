import chromadb
from chromadb.utils import embedding_functions

class VectorDB:
    def __init__(self, collection_name="rag_collection"):
        # Create Chroma client
        self.client = chromadb.Client()
        self.collection_name = collection_name
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=None,  # embeddings are provided manually
            metadata={"hnsw:space": "cosine"}  # cosine similarity
        )

    def add_documents(self, chunks, embeddings, ids, metadatas=None):
        """
        Store documents + embeddings + metadata in ChromaDB
        """
        if metadatas is None:
            metadatas = [{} for _ in range(len(chunks))]

        if not (len(chunks) == len(embeddings) == len(ids) == len(metadatas)):
            raise ValueError("[ERROR] Length mismatch in add_documents input")

        self.collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas
        )
        print(f"[DB] Added {len(chunks)} documents with metadata")

    def query(self, query_embedding, n_results=3):
        """
        Query nearest neighbors in ChromaDB
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )
        return results

    def reset_collection(self):
        """
        Reset (delete + recreate) the collection
        """
        self.client.delete_collection(self.collection_name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=None
        )
        print(f"[DB] Collection '{self.collection_name}' has been reset")
