#!/usr/bin/env python3
"""
Start only the backend API (frontend already running)
"""

import uvicorn
import os
from dotenv import load_dotenv
from unicode_utils import safe_print

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Check API key
    api_key = os.getenv('GEMINI_API_KEY', '')
    if not api_key:
        safe_print("[ERROR] GEMINI_API_KEY not found in .env file")
        exit(1)
    
    safe_print("[OK] Gemini API key loaded")
    safe_print("[INFO] Frontend detected at http://localhost:5173/")
    safe_print("[STARTING] Backend API at http://localhost:8000")
    safe_print("[INFO] API docs at http://localhost:8000/docs")
    
    # Ensure directories exist
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("complete_audiobooks", exist_ok=True)
    os.makedirs("chroma_db", exist_ok=True)
    
    try:
        uvicorn.run(
            "main:app",
            host="127.0.0.1",
            port=8000,
            reload=False,  # Disable reload for stability
            log_level="info"
        )
    except KeyboardInterrupt:
        safe_print("\n[STOPPED] Backend API stopped")
    except Exception as e:
        safe_print(f"[ERROR] Failed to start backend: {e}")