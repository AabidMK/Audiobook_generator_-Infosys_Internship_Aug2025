import os
import chromadb
from chromadb.utils import embedding_functions
import google.generativeai as genai

# -------------------
# Configurations
# -------------------
GOOGLE_API_KEY = "A.............Y"   
COLLECTION_NAME = "audiobook_chunks"

# -------------------
# Initialize ChromaDB
# -------------------
print("Script started...")
client = chromadb.PersistentClient(path="chromadb_store")
print("Chroma client initialized...")

embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
print(" Embedding function loaded...")

collection = client.get_collection(COLLECTION_NAME)
print(f"Connected to collection: {COLLECTION_NAME}")

# -------------------
# Initialize Gemini
# -------------------
genai.configure(api_key=GOOGLE_API_KEY)
llm_model = "gemini-2.5-flash"   # tested available model
print("Gemini client initialized...")

# -------------------
# Query loop
# -------------------
while True:
    user_question = input("Ask a question (or type 'exit'): ")
    if user_question.lower() == "exit":
        break

    print(" User query received...")

    # Retrieve top chunks
    results = collection.query(
        query_texts=[user_question],
        n_results=3
    )
    print(" Retrieved top chunks from ChromaDB")

    # Assemble context
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    context = ""
    citations = []
    for doc, meta in zip(docs, metas):
        context += f"{doc}\n\n"
        source = meta.get("source", "Unknown")
        chunk_id = meta.get("chunk_id", "NA")
        citations.append(f"{source} [chunk {chunk_id}]")

    print(" Context prepared...")

    # Build prompt
    prompt = f"""
You are an assistant answering based on the provided context.

Context:
{context}

Question: {user_question}

Answer clearly and cite sources like this (Source: filename [chunk id]).
"""

    try:
        response = genai.GenerativeModel(llm_model).generate_content(prompt)
        answer = response.text
        print("\n Answer:\n", answer)
        print("\n Citations:", ", ".join(citations))
    except Exception as e:
        print("Error while calling Gemini:", e)