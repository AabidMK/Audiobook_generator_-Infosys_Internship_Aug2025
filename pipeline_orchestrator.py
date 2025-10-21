"""
Pipeline Orchestrator: Integrates extraction, chunking, embedding, Chroma storage,
RAG query and audiobook generation (text -> LLM rewrite -> Edge TTS audio).

Drop this file next to the provided modules and run via CLI. It re-uses the
uploaded modules: enhanced_extraction.py, text_chunking.py, vector_embedding.py,
chroma_storing.py, pipeline_rag.py, audiobook_generator.py and rag.py

Dependencies (high-level):
 - chromadb, sentence-transformers, sentencepiece, tiktoken, google-generativeai
 - edge-tts (optional, for audio), pyttsx3/gTTS as fallback
 - aiohttp, pymupdf (fitz), pytesseract, pillow

Example usage:
  python pipeline_orchestrator.py index --files testing.pdf other.docx
  python pipeline_orchestrator.py audiobook --file testing.pdf --voice storytelling
  python pipeline_orchestrator.py query --question "What is X?"

"""

import argparse
import asyncio
import logging
import os
from typing import List, Optional

# Reuse user-provided modules
from pipeline_rag import run_pipeline as run_rag_indexing
from audiobook_generator import StateOfTheArtAudiobookGenerator
from rag import rag_pipeline

# chroma client helpers
from chroma_storing import get_chroma_client, get_or_create_collection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pipeline_orchestrator")


def index_files(file_paths: List[str]):
    """Run the existing pipeline_rag indexing flow for a list of files.
    It will extract, chunk, embed and store vectors in ChromaDB.
    """
    logger.info("Starting indexing for %d files", len(file_paths))
    run_rag_indexing(file_paths)
    logger.info("Indexing finished")


async def generate_audiobook(file_path: str, generate_audio: bool = True, voice_style: str = "storytelling", audio_length_limit: int = 25000, local_only: bool = False):
    """Generate enhanced audiobook text and (optionally) audio.

    Returns the result dict from StateOfTheArtAudiobookGenerator.
    """
    logger.info("Running audiobook generation for: %s", file_path)
    generator = StateOfTheArtAudiobookGenerator(local_only=local_only)
    try:
        result = await generator.generate_complete_audiobook_with_fast_audio(
            file_path, generate_audio=generate_audio, voice_style=voice_style, audio_length_limit=audio_length_limit
        )
        return result
    finally:
        await generator.close()


def query_rag(question: str, top_k: int = 5):
    """Run the RAG pipeline (uses rag.rag_pipeline from uploaded rag.py).

    Returns tuple (answer_text, citations)
    """
    logger.info("Running RAG query: %s", question)
    answer, cites = rag_pipeline(question, top_k=top_k)
    return answer, cites


def run_simple_http_service(host: str = "0.0.0.0", port: int = 8080):
    """Optional: small Flask app exposing /query for RAG queries and /health.

    This is intentionally minimal — production deployments should use proper
    servers and auth.
    """
    try:
        from flask import Flask, request, jsonify
    except ImportError:
        raise RuntimeError("Flask is required to run the simple HTTP service")

    app = Flask("pipeline_orchestrator")

    @app.route("/health")
    def health():
        return ("ok", 200)

    @app.route("/query", methods=["POST"])
    def query():
        payload = request.get_json(force=True)
        q = payload.get("question") or payload.get("q")
        top_k = int(payload.get("top_k", 5))
        if not q:
            return jsonify({"error": "missing question"}), 400
        answer, cites = query_rag(q, top_k=top_k)
        return jsonify({"answer": answer, "citations": cites})

    logger.info("Starting HTTP service on %s:%d", host, port)
    app.run(host=host, port=port)


def main():
    parser = argparse.ArgumentParser(description="Pipeline Orchestrator for Audio + RAG")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_index = sub.add_parser("index", help="Index files into ChromaDB (extract -> chunk -> embed -> store)")
    p_index.add_argument("--files", nargs='+', required=True, help="Files to index (pdf/docx/txt)")

    p_audio = sub.add_parser("audiobook", help="Generate audiobook text and optional audio")
    p_audio.add_argument("--file", required=True, help="Source file to convert to audiobook")
    p_audio.add_argument("--voice", default="storytelling", help="Edge TTS voice style")
    p_audio.add_argument("--no-audio", action="store_true", help="Generate text only (no audio)")
    p_audio.add_argument("--local-only", action="store_true", help="Run LLMs in local-only fallback mode")

    p_query = sub.add_parser("query", help="Ask a question against the indexed ChromaDB via RAG")
    p_query.add_argument("--question", required=True, help="Question to ask")
    p_query.add_argument("--top-k", type=int, default=5, help="How many chunks to retrieve")

    p_serve = sub.add_parser("serve", help="Run a small HTTP server exposing a /query endpoint")
    p_serve.add_argument("--host", default="0.0.0.0")
    p_serve.add_argument("--port", type=int, default=8080)

    args = parser.parse_args()

    if args.cmd == "index":
        index_files(args.files)

    elif args.cmd == "audiobook":
        generate_audio = not args.no_audio
        coro = generate_audiobook(args.file, generate_audio=generate_audio, voice_style=args.voice, local_only=args.local_only)
        result = asyncio.run(coro)
        print("\n=== Audiobook Result ===")
        for k, v in result.items():
            print(f"{k}: {v}")

    elif args.cmd == "query":
        ans, cites = query_rag(args.question, top_k=args.top_k)
        print("\n--- Answer ---\n")
        print(ans)
        print("\n--- Citations ---\n")
        for c in cites:
            print(c)

    elif args.cmd == "serve":
        run_simple_http_service(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
