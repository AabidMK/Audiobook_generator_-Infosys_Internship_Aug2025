import fitz
from sentence_transformers import SentenceTransformer
import chromadb
import textwrap
import os
import sys

try:
    from google import genai
except ImportError:
    print("FATAL ERROR: The 'google-genai' library is required for the API call.")
    print("Please run: pip install google-genai")
    sys.exit(1)


# --- Configuration ---
PERSIST_DIR = "audiobook_chroma"
COLLECTION_NAME = "audiobook"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 3 # Number of nearest chunks to retrieve
PDF_FILE = "AI AudioBook Generator.pdf"
LLM_MODEL = "gemini-2.5-flash" 

# CRITICAL FIX: Add your API key here to resolve the error
# Get your key from Google AI Studio and replace the placeholder below.
GEMINI_API_KEY = "AIzaSyDHXlI0m9PPWeArbQqc0QZabfi2aT3HNTk" 

# PHASE 1: INDEXING (Data Setup)

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file using fitz (PyMuPDF)"""
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
    """Manages the creation and indexing of the ChromaDB vector store."""
    def __init__(self, persist_dir, collection_name):
        self.persist_dir = persist_dir
        self.collection_name = collection_name
        
        # Initialize using PersistentClient
        self.client = chromadb.PersistentClient(path=self.persist_dir)
        
        self.collection = self.client.get_or_create_collection(name=self.collection_name)
        print(f"ChromaDB client initialized and collection '{self.collection_name}' ready.")

    def chunk_text(self, text, chunk_size=1000, overlap=200):
        """Split text into overlapping chunks"""
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start += chunk_size - overlap
        return chunks

    def index_text(self, text, embedding_model):
        """Index text chunks into ChromaDB"""
        chunks = self.chunk_text(text)
        embeddings = embedding_model.encode(chunks).tolist()
        ids = [f"chunk_{i}" for i in range(len(chunks))]
        
        metadatas = [{"source_file": PDF_FILE, "chunk_index": i} for i in range(len(chunks))]

        self.collection.upsert(
            documents=chunks, 
            embeddings=embeddings, 
            ids=ids,
            metadatas=metadatas
        )
        print(f"Indexed {len(chunks)} chunks into ChromaDB at {self.persist_dir}/")


# PHASE 2: RAG QUERY (Query Execution)

def rag_query_execution(user_question: str):
    """
    Implements the 7 steps of the Phase 2 RAG process, using Gemini API for generation.
    """
    if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE" or not GEMINI_API_KEY:
        return "ERROR: Please set your Gemini API key in the GEMINI_API_KEY variable in the code.", []
        
    print("\n" + "="*80)
    print("Phase 2: Retrieval-Augmented Generation (RAG) Query ")
    print(f"User Question: {user_question}")
    print("="*80)
    print(f"2. Loading embedding model: {EMBEDDING_MODEL_NAME}...")
    try:
        embed_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    except Exception as e:
        print(f"ERROR loading SentenceTransformer: {e}")
        return "Error: Could not load embedding model.", []
        
    question_embedding = embed_model.encode(user_question).tolist()
    print(" Question embedded.")

    # 3. Query ChromaDB for top-K nearest items
    print(f"3. Querying persistent ChromaDB at '{PERSIST_DIR}' for Top-K={TOP_K}...")
    try:
        client_db = chromadb.PersistentClient(path=PERSIST_DIR)
        collection = client_db.get_collection(name=COLLECTION_NAME)
    except Exception as e:
        print(f"ERROR connecting to ChromaDB: {e}. Please ensure Phase 1 indexing completed.")
        return "Error: Could not connect to the Vector Store.", []


    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=TOP_K,
        include=['documents', 'metadatas', 'distances']
    )
    
    if not results or not results.get('documents') or not results['documents'][0]:
        print(" No relevant chunks found.")
        return "I am unable to answer as no relevant documents were retrieved from the knowledge base.", []

    retrieved_chunks = results['documents'][0]
    retrieved_metadatas = results['metadatas'][0]
    retrieved_distances = results['distances'][0]
    print(f"Retrieved {len(retrieved_chunks)} relevant chunks.")

    # 4. Assemble the returned chunks into a context string
    context_parts = []
    citations = []
    
    print("4. Assembling context and preparing citations...")
    for i, chunk in enumerate(retrieved_chunks):
        metadata = retrieved_metadatas[i]
        distance = retrieved_distances[i]
        
        source_id = f"[Source {i+1}]"
        context_parts.append(f"{source_id} {chunk}")
        
        # 7. Attach citations (Metadata preparation)
        citations.append({
            "source_id": source_id,
            "file_path": metadata.get('source_file', 'N/A'),
            "chunk_index": metadata.get('chunk_index', 'N/A'),
            "distance": f"{distance:.4f}"
        })
        
    context_string = "\n--- CHUNK BREAK ---\n".join(context_parts)

    # 5. Build a prompt that instructs the LLM to use the context
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
    print(" LLM prompt built with context and guardrails.")
    print("\n6. Calling LLM (Gemini API) for final answer generation...")
    
    try:
        # FIX: Pass the API key explicitly
        client_llm = genai.Client(api_key=GEMINI_API_KEY)
        
        response = client_llm.models.generate_content(
            model=LLM_MODEL,
            contents=prompt,
            # Use low temperature for factual RAG tasks
            config=genai.types.GenerateContentConfig(temperature=0.0)
        )
        
        final_answer = response.text.strip()
        print("LLM response received.")
        
    except Exception as e:
        final_answer = f" ERROR: Failed to call Gemini API. Check your API key validity or network connection. Details: {e}"
        print(final_answer)

    return final_answer, citations

# MAIN EXECUTION
if __name__ == "__main__":
    
    print("="*80)
    print("Starting Full RAG Process (Phase 1: Indexing)")
    print("="*80)

    # --- PHASE 1 EXECUTION ---
    
    if not os.path.exists(PDF_FILE):
        print(f"FATAL ERROR: Required file '{PDF_FILE}' not found. Cannot proceed.")
    else:
        raw_text = extract_text_from_pdf(PDF_FILE)
        embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

        db = VectorStoreManager(persist_dir=PERSIST_DIR, collection_name=COLLECTION_NAME)
        db.index_text(raw_text, embedding_model)

        # --- PHASE 2 EXECUTION (Single Query) ---
        
        # CHANGE THIS STRING to test a different query!
        user_query = "What are all the technology stack used for this project?"
        
        print("\n" + "="*80)
        print("RUNNING SINGLE QUERY")
        
        answer, sources = rag_query_execution(user_query)
        
        print("\n" + "="*80)
        print(f" FINAL RAG OUTPUT for: {user_query}")
        print("="*80)
        
        print("\n**1. Generated Answer:**")
        print(answer)
        
        print("\n**2. Citations Used:**")
        if sources:
            for citation in sources:
                print(f"  {citation['source_id']} | Source File: {citation['file_path']} | Chunk Index: {citation['chunk_index']} | Relevance Score (Distance): {citation['distance']}")
        else:
            print("  No citations retrieved.")
        
        print("\n" + "="*80)