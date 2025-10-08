import chromadb_config

from create_embeddings import get_embeddings
import chromadb
import google.generativeai as genai
from dotenv import load_dotenv
import os
# -----------------------------
# ChromaDB setup
# -----------------------------
client = chromadb.PersistentClient(path="chroma_db")
collection_name = "audiobook_chunks"
collection = client.get_or_create_collection(
    name=collection_name,
    metadata={"hnsw:space": "cosine"},
    embedding_function=None
)

TOP_K = 5          
MAX_CONTEXT_TOKENS = 2000  

# -----------------------------
# Gemini LLM setup (pass api_key from env)
# -----------------------------
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("Set your GEMINI_API_KEY environment variable!")
genai.configure(api_key=API_KEY)
MODEL_NAME = "gemini-2.5-flash"
model = genai.GenerativeModel(MODEL_NAME)

# -----------------------------
# RAG query functions
# -----------------------------
def retrieve_relevant_chunks(question: str):
    """
    1. Embed the question
    2. Query ChromaDB for top-K nearest chunks
    """
    question_embedding = get_embeddings([question])[0]

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=TOP_K,
        include=["documents", "metadatas", "distances"]
    )
    return results

def assemble_context(results):
    """
    Assemble chunks into context string (within token limit)
    """
    context = ""
    for doc, distance in zip(results["documents"][0], results["distances"][0]):
        if len(context.split()) + len(doc.split()) > MAX_CONTEXT_TOKENS:
            break
        context += doc + "\n\n"
    return context

def build_prompt(question: str, context: str):
    """
    Optimized prompt for accurate RAG answers using context.
    Instructions:
    - Use only the provided context.
    - Do not invent information.
    - Be concise and factual.
    - Provide citations if possible.
    - If the answer is not in the context, say "I don't know based on the given context."
    """
    prompt = f"""
You are an expert AI assistant. Use the following context to answer the question below.

CONTEXT:
{context}

QUESTION:
{question}

Guidelines:
1. Use only the information in the context above. Do not hallucinate or add facts not present.
2. Answer concisely, clearly, and factually.
3. If relevant, include which part of the context supports your answer.
4. If the answer is not in the context, reply exactly: "I don't know based on the given context."

Answer:
"""
    return prompt

def answer_question(question: str):
    """
    Full RAG pipeline for a user question:
    - Retrieve chunks
    - Assemble context
    - Call Gemini LLM
    - Return answer + citations
    """
    results = retrieve_relevant_chunks(question)
    context = assemble_context(results)
    prompt = build_prompt(question, context)

    # Call Gemini
    response = model.generate_content(prompt)
    answer = response.text.strip()

    # Prepare citations
    citations = []
    for i, (doc, distance) in enumerate(zip(results["documents"][0], results["distances"][0])):
        citations.append({
            "chunk_index": i,
            "distance": distance,
            "content_preview": doc[:100]  # first 100 chars
        })

    return answer, citations