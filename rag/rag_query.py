import os
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv
import chromadb
from sentence_transformers import SentenceTransformer

# Load env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Chroma and embedding model
chroma_client = chromadb.PersistentClient(path=str(Path("chroma_db")))
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
collection = chroma_client.get_or_create_collection("documents")

# Use a working Gemini model
MODEL_NAME = "models/gemini-2.5-flash"

def embed_text(texts):
    """Convert text to embeddings using MiniLM"""
    return embedding_model.encode(texts).tolist()

def answer_question(query, k=3):
    """Answer a question using retrieved chunks from ChromaDB"""
    query_embedding = embed_text([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    if not results["documents"] or len(results["documents"][0]) == 0:
        return "⚠️ No relevant context found.", []

    retrieved_chunks = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    # Build context string
    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
You are a helpful assistant. Use the following context from documents to answer the user’s question.
If the answer is not present in the context, say you don't know.

Context:
{context}

Question: {query}
Answer:
    """

    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)

    return response.text.strip(), list(zip(metadatas, distances))

def chat_loop():
    print("🤖 RAG Q/A System (multi-turn). Type 'exit' to quit.\n")
    while True:
        query = input("❓ Question: ")
        if query.lower() in ["exit", "quit"]:
            break
        answer, citations = answer_question(query)
        print("\n💡 Answer:\n", answer)
        print("\n📚 Citations:")
        for meta, dist in citations:
            print(f"- {meta['source']} (chunk {meta['chunk']}, dist {dist:.2f})")
        print()

if __name__ == "__main__":
    print("🤖 RAG Q&A ready! Ask your questions (type 'exit' to quit).")
    while True:
        query = input("\n❓ Question: ")
        if query.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        answer, citations = answer_question(query)

        print("\n💡 Answer:\n", answer)
        print("\n📚 Citations:")
        for meta, dist in citations:
            print(f"- {meta['source']} (chunk {meta['chunk']}, dist {dist:.2f})")
        print()
