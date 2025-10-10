import os
from dotenv import load_dotenv
import chromadb
import tiktoken
import google.generativeai as genai
from sentence_transformers import SentenceTransformer

# ----------------------------
# Config
# ----------------------------
PERSIST_DIR = "chroma_db_audiobook"
COLLECTION_NAME = "documents"
EMBED_MODEL = "all-MiniLM-L6-v2"
GENAI_MODEL = "gemini-2.0-flash"
TOKEN_LIMIT = 3000

# ----------------------------
# Initialize Embedding + ChromaDB + Gemini
# ----------------------------
def initialize_qna_pipeline():
    print("Loading embedding model...")
    embedder = SentenceTransformer(EMBED_MODEL)

    print("Connecting to ChromaDB...")
    client = chromadb.PersistentClient(path=PERSIST_DIR)
    collection = client.get_collection(COLLECTION_NAME)

    print("Configuring Gemini API...")
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("❌ Gemini API key not found in environment variables.")
    genai.configure(api_key=api_key)
    llm = genai.GenerativeModel(GENAI_MODEL)

    tokenizer = tiktoken.get_encoding("cl100k_base")

    return embedder, collection, llm, tokenizer


def trim_to_budget(text, tokenizer, limit=TOKEN_LIMIT):
    tokens = tokenizer.encode(text)
    if len(tokens) <= limit:
        return text
    return tokenizer.decode(tokens[:limit])


# ----------------------------
# Main Q&A Function
# ----------------------------
def run_qna_session(question,collection=None , embedding_model=None):
    """
    Run rag q&a seesion.If collection or embedding_model is None ,fallback to default initialization.
    """
    if collection is None or embedding_model is None:
        embedding_model, collection,llm,tokenizer = initialize_qna_pipeline()
    else:
        _, _, llm, tokenizer = initialize_qna_pipeline()

        # Step 1: Embed question
        print("Embedding your question...")
        q_vec = embedding_model.encode([question], convert_to_tensor=False)[0].tolist()

        # Step 2: Query ChromaDB
        print("Querying ChromaDB for relevant chunks...")
        if collection is None:
            return "No indexed documents found"
        results = collection.query(query_embeddings=[q_vec], n_results=5)

        chunks = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        # Step 3: Assemble context
        context = "\n\n".join(chunks)
        context = trim_to_budget(context, tokenizer, TOKEN_LIMIT)

        # Step 4: Build prompt
        prompt = f"""
You are a factual RAG assistant.
You will receive:
1. A user question.
2. The top 5 most relevant chunks from the reference files.

Instructions:
- Carefully read all provided chunks before answering.
- Identify the one chunk that best answers the question.
- Use only that chunk's content as the core of your answer.
- Rephrase or enrich so it's clear, coherent, medium in length.
- Explain the main points, directly related to the question.
- Do not give a very short answer. The answer should explain in detail about the question asked.
- If none of the chunks answer, reply exactly:
"The answer is not present in the provided file."

Context:
{context}

Question:
{question}
"""

        # Step 5: Generate answer
        print("🤖 Generating answer using Gemini LLM...")
        response = llm.generate_content(prompt)

        citations = []
        for i, meta in enumerate(metadatas):
            citations.append({
                "file_path": meta.get("file_path"),
                "chunk_index": meta.get("chunk_index"),
                "distance": distances[i]
            })
            return response.text,citations
