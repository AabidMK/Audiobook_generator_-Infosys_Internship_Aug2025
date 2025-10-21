#!/usr/bin/env python3
"""
Quick start script for the Audiobook Generator API
"""
import uvicorn
import os
import sys
from dotenv import load_dotenv

# Fix Windows encoding
if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Ensure required directories exist
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("complete_audiobooks", exist_ok=True)
    os.makedirs("chroma_db", exist_ok=True)
    
    from unicode_utils import safe_print
    safe_print("Starting Audiobook Generator API...")
    safe_print("Upload endpoint: POST /upload")
    safe_print("Generate audiobook: POST /generate-audiobook") 
    safe_print("Query RAG: POST /query")
    safe_print("API docs: http://localhost:8000/docs")
    safe_print("Frontend: Check your frontend directory")
    
    try:
        uvicorn.run(
            "main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info"
        )
    except Exception as e:
        safe_print(f"[ERROR] Failed to start server: {e}")