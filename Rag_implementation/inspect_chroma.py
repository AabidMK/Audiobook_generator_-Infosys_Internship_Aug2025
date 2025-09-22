
import chromadb
from chromadb.config import Settings
client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="chroma_db"))
print("Collections:", client.list_collections())

try:
    col = client.get_collection("documents")
    print("Collection metadata count approx:", len(col.get(include=['metadatas'])['metadatas']))
except Exception as e:
    print("Could not open collection 'documents':", e)
