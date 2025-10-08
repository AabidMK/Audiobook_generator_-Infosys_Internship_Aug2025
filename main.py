import sys
from extract_text import extract_text, save_to_markdown
from text_rewriter_gemini import rewrite_with_gemini
from tts_generator import main as tts_main

# RAG imports
from chunk_text import chunk_text
from create_embeddings import get_embeddings
from vector_db import store_embeddings

def run_pipeline(input_file):
    """
    This version is streamlined for frontend usage.
    Does NOT include interactive terminal RAG loop.
    """
    # Step 1: Extract text
    raw_text = extract_text(input_file)
    if not raw_text.strip():
        raise ValueError("No text found in the file.")

    # Step 2: Rewrite with Gemini
    rewritten_text = rewrite_with_gemini(raw_text)
    if not rewritten_text.strip():
        raise ValueError("Gemini did not return any output.")

    md_file = "narration_output.md"
    save_to_markdown(rewritten_text, md_file)

    # Step 3: Generate final audiobook
    tts_main(md_file)

    # Step 4: Create and store RAG embeddings
    chunks = chunk_text(raw_text, chunk_size=500, chunk_overlap=100)
    embeddings = get_embeddings(chunks)
    store_embeddings(chunks, embeddings)

    return md_file, "audiobook_voice.wav"  # Return paths for frontend