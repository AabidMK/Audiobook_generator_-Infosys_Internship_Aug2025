import fitz
import os
import sys
import shutil
import hashlib
import base64
from typing import List, Dict

# --- RAG Core Imports ---
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# TTS Specific Imports: Switched from google.cloud.texttospeech to gTTS
# This is the easiest alternative and does NOT require separate Google Cloud authentication/billing.
try:
    from gtts import gTTS
    import io
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("WARNING: 'gTTS' not installed. Audio generation will be disabled.")

# RAG Core Imports
from sentence_transformers import SentenceTransformer
import chromadb
from google import genai
import textwrap

# --- Configuration ---
# NOTE: GEMINI_API_KEY is for RAG/LLM. 
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "**********************") 
LLM_MODEL = "gemini-2.5-flash"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
BASE_PERSIST_DIR = "uploaded_document_stores"
COLLECTION_NAME = "uploaded_doc_rag"
TOP_K = 3

# --- Initialize FastAPI App ---
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- RAG Core Logic Functions (Retained) ---

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
        return text
    except FileNotFoundError:
        print(f"Error: PDF file '{pdf_path}' not found.")
        return ""

class VectorStoreManager:
    def __init__(self, persist_dir, collection_name):
        self.persist_dir = persist_dir
        self.collection_name = collection_name
        os.makedirs(self.persist_dir, exist_ok=True)
        self.client = chromadb.PersistentClient(path=self.persist_dir)
        try:
             self.collection = self.client.get_collection(name=self.collection_name)
        except:
             self.collection = self.client.create_collection(name=self.collection_name)

    def chunk_text(self, text, chunk_size=1000, overlap=200):
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start += chunk_size - overlap
        return chunks

    def index_text(self, text, embedding_model, file_name):
        if self.collection.count() > 0:
            print("Collection already indexed. Skipping re-indexing.")
            return

        chunks = self.chunk_text(text)
        embeddings = embedding_model.encode(chunks).tolist()
        ids = [f"chunk_{i}" for i in range(len(chunks))]
        metadatas = [{"source_file": file_name, "chunk_index": i} for i in range(len(chunks))]

        self.collection.upsert(
            documents=chunks, 
            embeddings=embeddings, 
            ids=ids,
            metadatas=metadatas
        )

def rag_query_execution(user_question: str, persist_dir: str):
    """
    Executes the RAG query and returns the text answer and citations.
    """
    if not GEMINI_API_KEY:
        raise ValueError("Gemini API key is not set.")
        
    embed_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    question_embedding = embed_model.encode(user_question).tolist()

    try:
        client_db = chromadb.PersistentClient(path=persist_dir)
        collection = client_db.get_collection(name=COLLECTION_NAME)
    except Exception as e:
        return "Error: Could not connect to the Vector Store for this document.", []

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=TOP_K,
        include=['documents', 'metadatas', 'distances']
    )
    
    if not results or not results.get('documents') or not results['documents'][0]:
        return "I am unable to answer as no relevant documents were retrieved from the knowledge base.", []

    retrieved_chunks = results['documents'][0]
    retrieved_metadatas = results['metadatas'][0]
    retrieved_distances = results['distances'][0]

    context_parts = []
    citations = []
    
    for i, chunk in enumerate(retrieved_chunks):
        metadata = retrieved_metadatas[i]
        distance = retrieved_distances[i]
        source_id = f"[Source {i+1}]"
        context_parts.append(f"{source_id} {chunk}")
        citations.append({
            "source_id": source_id,
            "file_path": metadata.get('source_file', 'N/A'),
            "chunk_index": metadata.get('chunk_index', 'N/A'),
            "distance": f"{distance:.4f}"
        })
        
    context_string = "\n--- CHUNK BREAK ---\n".join(context_parts)

    prompt = textwrap.dedent(f"""
        You are an expert Q&A system. Use ONLY the provided context to answer the user's question.
        For each piece of information in your answer, you MUST append the corresponding [Source X] marker(s) from the context.
        If the answer cannot be found in the context, state: "I am unable to answer based on the provided sources."

        --- CONTEXT (Token limit check assumed to be handled) ---
        {context_string}
        
        --- USER QUESTION ---
        {user_question}
        
        --- ANSWER ---
    """)
    
    try:
        client_llm = genai.Client(api_key=GEMINI_API_KEY)
        response = client_llm.models.generate_content(
            model=LLM_MODEL,
            contents=prompt,
            config=genai.types.GenerateContentConfig(temperature=0.0)
        )
        final_answer = response.text.strip()
        
    except Exception as e:
        final_answer = f"ERROR: Failed to call Gemini API. Details: {e}"
        print(final_answer)

    return final_answer, citations

# --- FastAPI Endpoints (Retained) ---

@app.post("/upload_and_index/")
async def upload_and_index_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    file_content = await file.read()
    file_id = hashlib.sha256(file.filename.encode() + str(len(file_content)).encode()).hexdigest()[:10]
    
    persist_dir = os.path.join(BASE_PERSIST_DIR, file_id)
    temp_file_path = os.path.join(persist_dir, file.filename)
    
    os.makedirs(persist_dir, exist_ok=True)
    
    with open(temp_file_path, "wb") as buffer:
        buffer.write(file_content)

    try:
        raw_text = extract_text_from_pdf(temp_file_path)
        if not raw_text:
            raise Exception("Could not extract text from PDF.")

        embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        db = VectorStoreManager(persist_dir=persist_dir, collection_name=COLLECTION_NAME)
        db.index_text(raw_text, embedding_model, file.filename)

        return JSONResponse(content={
            "message": f"File '{file.filename}' indexed successfully.",
            "file_id": file_id
        })

    except Exception as e:
        print(f"Indexing Error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process and index PDF: {e}")


@app.post("/rag_query/")
async def run_rag_query(query: str = Form(...), file_id: str = Form(...)):
    persist_dir = os.path.join(BASE_PERSIST_DIR, file_id)

    if not os.path.exists(persist_dir):
        raise HTTPException(status_code=404, detail="File ID not found. Please upload and index a file first.")

    try:
        answer, citations = rag_query_execution(query, persist_dir)

        return JSONResponse(content={
            "query": query,
            "answer": answer,
            "citations": citations
        })

    except Exception as e:
        print(f"RAG Query Error: {e}")
        raise HTTPException(status_code=500, detail=f"RAG query execution failed: {e}")


@app.post("/generate_audio/")
async def generate_audio_answer(text_answer: str = Form(...)):
    """
    UPDATED ENDPOINT: Generates an audio file from the provided text answer using gTTS (Google Text-to-Speech via Google Translate API).
    This alternative does NOT require separate Google Cloud authentication.
    Returns the audio content as a base64 string.
    """
    if not TTS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Text-to-Speech service is unavailable ('gTTS' module not installed).")

    if not text_answer:
        raise HTTPException(status_code=400, detail="No text provided for audio generation.")

    try:
        # Strip source markers like [Source X] before feeding to TTS
        clean_text = text_answer
        for i in range(1, 10): # Clean up common source markers
            clean_text = clean_text.replace(f"[Source {i}]", "")
            
        # 1. Create gTTS object
        tts = gTTS(text=clean_text, lang='en', slow=False)
        
        # 2. Save the audio to an in-memory binary file (BytesIO)
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        
        # 3. Read the content and encode it to base64
        audio_content_base64 = base64.b64encode(mp3_fp.read()).decode('utf-8')
        
        return JSONResponse(content={
            "audio_base64": audio_content_base64,
            "message": "Audio generated successfully using gTTS."
        })

    except Exception as e:
        print(f"gTTS Error: {e}")
        raise HTTPException(status_code=500, detail=f"Audio generation failed (gTTS). Details: {e}")

# To run the backend:
# uvicorn main:app --reload --port 8000
