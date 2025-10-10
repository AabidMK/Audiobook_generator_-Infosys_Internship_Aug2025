import os
from dotenv import load_dotenv
import chromadb
import tiktoken
import google.generativeai as genai
from sentence_transformers import SentenceTransformer

# ----------------------------
# Config
# ----------------------------
PERSIST_DIR = "chroma_db"   # where your ChromaDB is stored
COLLECTION_NAME = "documents"
EMBED_MODEL = "all-MiniLM-L6-v2"  # use the same one you used when indexing
GENAI_MODEL = "gemini-2.0-flash"
TOKEN_LIMIT = 3000  # adjust based on Gemini model limit

# ----------------------------
# Init Embedding + ChromaDB
# ----------------------------
print("Loading embedding model....")
embedder = SentenceTransformer(EMBED_MODEL)
print("Connecting to chromadb....")
client = chromadb.PersistentClient(path=PERSIST_DIR)
collection = client.get_collection(COLLECTION_NAME)

# ----------------------------
# Init Gemini LLM
# ----------------------------
print("Configuring gemini api....")
load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Gemini api key not found")
genai.configure(api_key=api_key)
llm = genai.GenerativeModel(GENAI_MODEL)

# ----------------------------
# Token counter (for trimming context)
# ----------------------------
tokenizer = tiktoken.get_encoding("cl100k_base")

def trim_to_budget(text, limit=TOKEN_LIMIT):
    tokens = tokenizer.encode(text)
    if len(tokens) <= limit:
        return text
    trimmed = tokenizer.decode(tokens[:limit])
    return trimmed

# ----------------------------
# RAG Pipeline
# ----------------------------
def rag_pipeline(user_question: str, top_k: int = 5):
    # Step 2: Embed the query
    print("Step1:Embedding user question..")
    query_embedding = embedder.encode(user_question).tolist()
    print("Step1 complete.")

    # Step 3: Query ChromaDB
    print("Step2:Querying chromadb...")
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    print("Step2 complete.")

    # Step 4: Assemble context
    print("Step3:Assembling context....")
    chunks = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    context = "\n\n".join(chunks)
    context = trim_to_budget(context, TOKEN_LIMIT)
    print("Step3 complete.")

    # Step 5: Build prompt
    print("Step4: Building prompt")
    prompt = f"""
You are a factual  RAG assistant.
You will receive:
1.A user question .
2.The top 5 most relevant chunks from the reference file.
Instructions:
1.Carefully read all the provided chunks before answering.
2.Identify the one chunk that best answers the question:
-Use only that chunk's content as the core of your answer.
-You may rephrase or enrich the answer **so it is clear,coherent,and medium in length**(not too short ,not too long).
-Provide a answer that **explains the main points** and is **not too long but should main points**.
-Do not give a very short or vague answer.
-Make sure the answer is **directly related to the question**.
-If none of the chunks directly answer the question,reply excatly:
"The answer is not present in the provided file." 

Context:
{context}

Question:
{user_question}
"""
    print("Step4 complete.")
    # Step 6: Call Gemini
    print("Step5:Calling gemini llm....")
    response = llm.generate_content(prompt)
    print("Step5 complete")

    # Step 7: Attach citations
    print("Step6:Attaching citations...")
    citations = []
    for i, meta in enumerate(metadatas):
        citations.append({
            "file_path": meta.get("file_path"),
            "chunk_index": meta.get("chunk_id"),
            "distance": distances[i]
        })
        print("Step6 complete.")

    return response.text, citations

# ----------------------------
# Run Example
# ----------------------------
"""if __name__ == "__main__":
    print("\n Welcome to RAG Phase2 with Gemini")
    question = input("Enter the question :")
    answer, cites = rag_pipeline(question)

    print("\n--- Answer ---")
    print(answer)

    print("\n--- Citations ---")
    for c in cites:
        print(c)"""

# ----------------------------
# Run Example
# ----------------------------
if __name__ == "__main__":
    print("\nWelcome to RAG Phase2 with Gemini!")

    # 1. Ask first if they want to start
    continue_asking = input("Do you want to ask a question? (yes/no): ").lower().strip()

    # 2. Loop until user says no
    while continue_asking in ("yes", "y"):
        print("\n---------------------------------------------------")

        # Get the question
        question = input("Enter your question (or type 'exit' to quit): ").strip()

        # If user types 'exit', break out of the loop
        if question.lower() in ("exit", "quit"):
            break

        # Run pipeline
        answer, cites = rag_pipeline(question)

        # Show answer
        print("\n--- Answer ---")
        print(answer)

        print("\n--- Citations ---")
        for c in cites:
            print(c)

        # Ask again
        continue_asking = input("\nDo you want to ask another question? (yes/no): ").lower().strip()

    print("\nExiting RAG assistant. Goodbye! ")