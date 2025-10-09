import asyncio
import tkinter as tk
from tkinter import filedialog
from qa_embedding import EmbeddingModule
from qa_vectordb import VectorDB

async def main():
    # === File input (GUI) ===
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select a Document",
        filetypes=[("Documents", "*.pdf *.docx *.png *.jpg *.jpeg")]
    )

    if not file_path:
        print("[ERROR] No file selected.")
        return

    print(f"[INFO] Selected file: {file_path}")

    # --- Chunk size + Overlap control ---
    CHUNK_SIZE = 500
    OVERLAP = 100

    # === Embedding pipeline ===
    embedder = EmbeddingModule()
    chunks, embeddings, metadatas = embedder.process_and_embed(
    file_path, chunk_size=CHUNK_SIZE, overlap=OVERLAP
)


    # === Store in DB ===
    db = VectorDB()
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    db.add_documents(chunks, embeddings, ids, metadatas)

    print("[INFO] Stored in ChromaDB")

    # === User enters query ===
    query = input("\nEnter your question: ").strip()
    if not query:
        print("[ERROR] No query entered. Exiting.")
        return

    # === Query embedding ===
    query_emb = embedder.embed_query(query)

    # === Search DB ===
    results = db.query(query_emb, n_results=3)

    print("\n[QA] Query:", query)
    if not results or not results.get("documents"):
        print("[INFO] No results found.")
        return

    for i, doc in enumerate(results["documents"][0], 1):
        print(f"\n--- Result {i} ---")
        print(doc[:500], "..." if len(doc) > 500 else "")

if __name__ == "__main__":
    asyncio.run(main())
