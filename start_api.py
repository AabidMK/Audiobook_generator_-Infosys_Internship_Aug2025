#!/usr/bin/env python3
"""
Quick start script for the Audiobook Generator API
"""
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Ensure required directories exist
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("complete_audiobooks", exist_ok=True)
    os.makedirs("chroma_db", exist_ok=True)
    
    print(" Starting Audiobook Generator API...")
    print(" Upload endpoint: POST /upload")
    print(" Generate audiobook: POST /generate-audiobook") 
    print(" Query RAG: POST /query")
    print(" API docs: http://localhost:8000/docs")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )