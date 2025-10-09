import asyncio
import tkinter as tk
from tkinter import filedialog
from qa_embedding import EmbeddingModule
from qa_vectordb import VectorDB
from llm_txt_generation import rewrite_text_with_gemini  # Gemini polishing

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
    results = db.query(query_emb, n_results=5)

    if not results or not results.get("documents"):
        print("[INFO] No results found.")
        return

    print("\n[QA] Query:", query)

    output_file = "rag_output.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"# RAG Output\n\n**Query:** {query}\n\n")

        # Collect retrieved chunks + citations
        docs = results["documents"][0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        f.write("## Retrieved Chunks\n\n")
        for i, (doc, meta, dist) in enumerate(zip(docs, metadatas, distances), 1):
            file_meta = meta.get("file_path", "unknown") if meta else "unknown"
            chunk_id = meta.get("chunk_id", i) if meta else i
            citation = f"- File: {file_meta} | Chunk: {chunk_id} | Distance: {dist:.4f}"
            print(citation)
            f.write(f"{citation}\n\n")
            f.write(doc + "\n\n")

        # === LLM rewrite step ===
        context_text = "\n".join(docs)
        prompt = f"Question: {query}\n\nContext:\n{context_text}\n\nAnswer:"
        polished_answer = rewrite_text_with_gemini(prompt)

        f.write("\n## Polished Answer\n\n")
        f.write(polished_answer)

    print(f"\n[+] Full output saved to: {output_file}")

if __name__ == "__main__":
    asyncio.run(main())
