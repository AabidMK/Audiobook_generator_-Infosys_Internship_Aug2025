# main2.py
from rag_pipeline import rag_pipeline

if __name__ == "__main__":
    print("=== Audiobook RAG Query System ===")
    
    while True:
        query = input("\n❓ Ask a question (or type 'exit'): ")
        if query.lower() == "exit":
            print("👋 Exiting Audiobook RAG System.")
            break

        # Call RAG pipeline
        answer, citations, docs = rag_pipeline(query)

        # Display answer
        print("\n=== 📖 ANSWER ===")
        print(answer)

        # Show where the answer came from
        print("\n=== 📌 SOURCES (chunks used) ===")
        for i, cite in enumerate(citations):
            print(f"Source {i+1}: file={cite['file_path']} | chunk={cite['chunk_index']} | distance={cite['distance']:.4f}")

        # Optional: print chunk text (debugging)
        print("\n=== 📂 Retrieved Chunks ===")
        for i, doc in enumerate(docs):
            print(f"Chunk {i+1}: {doc[:200]}...")  # only show first 200 chars


       
