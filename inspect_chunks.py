import chromadb

# Connect to persistent ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")

# Try to get the collection
try:
    collection = client.get_collection("audiobook_chunks")
except Exception as e:
    print("❌ Error: Could not load collection. Did you create and store chunks?")
    print("Details:", e)
    exit()

# Fetch all documents
docs = collection.get()

# Check if anything is stored
if not docs or "documents" not in docs or len(docs["documents"]) == 0:
    print("⚠️ No chunks found in collection 'audiobook_chunks'.")
else:
    print(f"✅ Found {len(docs['documents'])} chunks in collection 'audiobook_chunks'.\n")

    # Print each chunk with metadata
    for i, doc in enumerate(docs["documents"]):
        doc_preview = doc[:200].replace("\n", " ") + ("..." if len(doc) > 200 else "")
        meta = docs["metadatas"][i] if "metadatas" in docs and docs["metadatas"] else {}
        print(f"Chunk {i} | ID: {docs['ids'][i]} | Meta: {meta}\n{doc_preview}\n{'='*80}\n")

