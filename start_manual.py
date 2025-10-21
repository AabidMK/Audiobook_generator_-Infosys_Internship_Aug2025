#!/usr/bin/env python3
"""
Manual start script - run this directly
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create required directories
os.makedirs("uploads", exist_ok=True)
os.makedirs("complete_audiobooks", exist_ok=True)
os.makedirs("chroma_db", exist_ok=True)

print("🚀 Starting Audiobook Generator Backend...")
print("📁 Directories created")
print("🔑 Environment loaded")
print("🌐 Server will start at: http://localhost:8000")
print("📚 API docs at: http://localhost:8000/docs")
print()

# Import and run
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)