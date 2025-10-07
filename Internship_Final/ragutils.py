import google.generativeai as genai
import numpy as np
import re
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import chromadb
import uuid
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="secrets.env")
google_api_key = os.getenv("GOOGLE_API_KEY")


# Configure Gemini
genai.configure(api_key=google_api_key)

# Initialize Persistent ChromaDB

DB_PATH = "chroma_storage"
client = chromadb.PersistentClient(path=DB_PATH)

# Load embedding model once
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
load_dotenv("secrets.env")

# Embedding Function

def get_embedding(text: str):
    """Return embedding vector for given text"""
    return np.array(model.encode(text))


# Text Splitting

def split_into_sentences(text):
    """Split text into sentences using regex"""
    sentences = re.split(r'(?<=[.!?]) +', text)
    return [s.strip() for s in sentences if s.strip()]


# Semantic Chunking

def semantic_chunk(sentences, threshold=0.75, overlap_sentences=1):
    """
    Group sentences into semantic chunks with overlap
    """
    if not sentences:
        return []

    chunks = []
    embeddings = [get_embedding(s) for s in sentences]  # cache embeddings
    current_chunk = [sentences[0]]

    for i in range(1, len(sentences)):
        sim = cosine_similarity(
            embeddings[i-1].reshape(1, -1),
            embeddings[i].reshape(1, -1)
        )[0][0]

        if sim > threshold:
            current_chunk.append(sentences[i])
        else:
            chunks.append(" ".join(current_chunk))
            # Overlap for context
            overlap = current_chunk[-overlap_sentences:] if overlap_sentences > 0 else []
            current_chunk = overlap + [sentences[i]]

    chunks.append(" ".join(current_chunk))
    return chunks


# Create or Get Collection

def create_collection(collection_name="audiobook_chunks"):
    """Create or get existing ChromaDB collection"""
    return client.get_or_create_collection(name=collection_name)


# Store Chunks

def store_chunks(collection, chunks, source_file="unknown.txt"):
    """
    Store chunks with embeddings and metadata in ChromaDB
    """
    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk).tolist()
        unique_id = str(uuid.uuid4())  # unique for each chunk
        
        metadata = {
            "file_path": source_file,
            "chunk_index": i
        }
        
        collection.add(
            ids=[unique_id],
            documents=[chunk],
            embeddings=[embedding],
            metadatas=[metadata]  # <-- important
        )
    print(f"Stored {len(chunks)} chunks with metadata in ChromaDB")



# Query Chunks
def query_chunks(collection, query, top_k=3):
    """
    Query ChromaDB for top-k relevant chunks and include citations
    """
    query_emb = get_embedding(query).tolist()
    
    results = collection.query(
        query_embeddings=[query_emb],
        n_results=top_k
    )
    
    if not results or "documents" not in results or not results['documents'][0]:
        return []

    retrieved_data = []
    for i in range(len(results['documents'][0])):
        retrieved_data.append({
            "chunk_text": results['documents'][0][i],
            "file_path": results['metadatas'][0][i]['file_path'],
            "chunk_index": results['metadatas'][0][i]['chunk_index'],
            "distance": results['distances'][0][i]
        })

    return retrieved_data
#query context
def build_context(retrieved_chunks, max_length=1500):
    """
    Combine retrieved chunks into a single context string
    """
    context_text = ""
    for chunk in retrieved_chunks:
        if len(context_text) + len(chunk['chunk_text']) > max_length:
            break
        context_text += f"{chunk['chunk_text']}\n\n"
    return context_text.strip()
#prompt for querying
def build_prompt(user_query, context_text, retrieved_chunks):
    """
    Build a final prompt for Gemini or any LLM, with citations
    """
    citation_info = "\n".join(
        [f"[{i+1}] {c['file_path']} (chunk {c['chunk_index']}, score: {c['distance']:.4f})"
         for i, c in enumerate(retrieved_chunks)]
    )

    prompt = f"""
You are an assistant that answers questions strictly based on the given context.
Do NOT hallucinate information. If the answer cannot be found, say "I don't know."

Question: {user_query}

Context:
{context_text}

Citations:
{citation_info}

Instructions:
- Always include citation numbers like [1], [2] when referencing sources.
- Do NOT make up any information.
- If possibke Based on the context form 2 to 3 senetences 
    """
    return prompt

#gemini feed

def query_with_gemini(user_query, collection):
    # 1. Retrieve top chunks
    retrieved_chunks = query_chunks(collection, user_query, top_k=3)
    
    if not retrieved_chunks:
        return "No relevant chunks found."

    # 2. Build context
    context_text = build_context(retrieved_chunks)
    # 3. Build prompt with citations
    prompt = build_prompt(user_query, context_text, retrieved_chunks)

    # 4. Call Gemini
    response = genai.GenerativeModel("gemini-2.5-flash-lite").generate_content(prompt)
    
    return response.text, retrieved_chunks
