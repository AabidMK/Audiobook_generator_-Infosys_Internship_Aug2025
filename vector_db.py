import chromadb_config

import chromadb
import time  

def store_embeddings(chunks, embeddings, collection_name="audiobook_chunks", persist_dir="chroma_db"):
    """
    Store chunks and embeddings in ChromaDB.
    """
    try:
        print("DEBUG: Initializing ChromaDB PersistentClient...", flush=True)
        client = chromadb.PersistentClient(path=persist_dir)
        print("DEBUG: Client initialized.", flush=True)
        collection = client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
            embedding_function=None
        )
        print(f"DEBUG: Collection '{collection_name}' ready.", flush=True)

        print(f"DEBUG: Adding {len(chunks)} embeddings to collection...", flush=True)
        try:
            run_id = int(time.time())
            ids = [f"{run_id}_{i}" for i in range(len(chunks))]
            
            print(f"DEBUG: Generated {len(ids)} unique IDs", flush=True)
            print(f"DEBUG: Embeddings type: {type(embeddings)}, length: {len(embeddings)}", flush=True)
            if embeddings:
                print(f"DEBUG: First embedding type: {type(embeddings[0])}, length: {len(embeddings[0]) if hasattr(embeddings[0], '__len__') else 'N/A'}", flush=True)
            
            print("DEBUG: About to call collection.add()...", flush=True)
            collection.add(
                documents=chunks,
                embeddings=embeddings,
                ids=ids
            )
            print(f"DEBUG: collection.add() completed successfully!", flush=True)
            print(f"Stored {len(chunks)} embeddings in ChromaDB collection '{collection_name}' (appended to existing data if any)", flush=True)
        except Exception as e:
            print(f"Error adding embeddings to collection: {type(e).__name__}: {e}", flush=True)
            import traceback
            traceback.print_exc()
            raise e

    except Exception as e:
        print("Error initializing or storing embeddings in ChromaDB:", e, flush=True)
        raise e

    return True