import os
import logging
from dotenv import load_dotenv
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from sentence_transformers import SentenceTransformer
import tiktoken
import google.generativeai as genai

# ---- Imports from your existing modules ----
from pipeline_extraction import extract_text
from pipeline_enrichment import enrich_text
from pipeline_audio_edgetts import generate_audio
from pipeline_chunking import chunk_multiple_documents
from pipeline_embedding import initialize_embedding_model, embed_chunks_for_pipeline
from pipeline_chroma import get_chroma_client, get_or_create_collection, store_chunks, persist_client
from pipeline_rag import run_qna_session 

# ----------------------------
# CONFIG

# ----------------------------
PERSIST_DIR = "chroma_db"
COLLECTION_NAME = "documents"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
GENAI_MODEL = "gemini-2.0-flash"
TOKEN_LIMIT = 3000
OUTPUT_AUDIO_FILE = "audiobook_output.wav"

# ----------------------------
# Logging
# ----------------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("main_pipeline")

# ----------------------------
# Init Gemini & Embedding Models
# ----------------------------
print("🔑 Configuring Gemini API...")
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ Gemini API key not found.")
genai.configure(api_key=api_key)
llm = genai.GenerativeModel(GENAI_MODEL)

print(" Loading embedding model...")
embedder = SentenceTransformer(EMBED_MODEL)  # for questions
embedding_model = initialize_embedding_model(EMBED_MODEL)  # for documents

# ----------------------------
# Token counter
# ----------------------------
tokenizer = tiktoken.get_encoding("cl100k_base")

def trim_to_budget(text, limit=TOKEN_LIMIT):
    tokens = tokenizer.encode(text)
    return text if len(tokens) <= limit else tokenizer.decode(tokens[:limit])

# ----------------------------
# Main Pipeline
# ----------------------------
def main():
    print("\n🚀 Welcome to the Unified Sequential Pipeline!\n")

    # Step 1: Multiple File Input
    file_paths = input("📂 Enter file paths separated by commas (.pdf, .docx, .png, .jpg): ").strip().split(",")
    file_paths = [fp.strip() for fp in file_paths if fp.strip()]

    if not file_paths:
        print("❌ No valid files provided.")
        return

    documents = []
    full_text_for_audio = ""

    for path in file_paths:
        extracted_text, error = extract_text(path)
        if error:
            print(f"❌ Error extracting {path}: {error}")
            continue
        full_text_for_audio += extracted_text + "\n"
        documents.append((extracted_text, "file", path))

    if not documents:
        print("❌ No text extracted from any provided files.")
        return
    print("✅ Step 1: Text extraction completed.")

    # Step 2: Text Enrichment
    enriched_text = enrich_text(full_text_for_audio)
    print("✅ Step 2: Text enrichment with Gemini completed.")
    enriched_output= "enriched.txt"

    # Step 3: Chunking
    chunks = chunk_multiple_documents(documents, chunk_size=500, chunk_overlap=100)
    print("✅ Step 3: Text chunking completed.")

    # Step 4: Embedding
    texts, embeddings, metadatas, ids = embed_chunks_for_pipeline(chunks, embedding_model)
    print("✅ Step 4: Embeddings generated.")

    # Step 5: Store in Vector Database
    client = get_chroma_client()
    collection = get_or_create_collection(client)
    stored_count = store_chunks(collection, texts, metadatas, ids,embeddings)
    persist_client(client)
    print(f"✅ Step 5: ChromaDB storage completed. Total chunks stored: {stored_count}")

    # Step 6: Audio Generation
    print("🎙 Generating audio from enriched text...")
    generate_audio(enriched_text)
    print(f"✅ Step 6: Audio generation completed. Audio saved as '{OUTPUT_AUDIO_FILE}'")

    # Step 7: Q&A Loop
    print("\n Step 7: Starting Q&A session.....")
    run_qna_session
    print("Step 7 complete ")

    print(f"\n🎧 Final audio file is ready for download: {OUTPUT_AUDIO_FILE}")
    print("✅ Pipeline completed successfully!")

if __name__ == "__main__":
    main()