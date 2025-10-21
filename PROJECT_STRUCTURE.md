# AudioBook Generator - Project Structure

## Core Files
- `main.py` - FastAPI backend server
- `audiobook_generator.py` - Main audiobook generation logic
- `enhanced_extraction.py` - Text extraction from PDF/DOCX/TXT
- `requirements.txt` - Python dependencies

## RAG System
- `rag.py` - RAG query processing
- `pipeline_rag.py` - Document indexing pipeline
- `text_chunking.py` - Text chunking for embeddings
- `vector_embedding.py` - Vector embeddings
- `chroma_storing.py` - ChromaDB storage
- `unicode_utils.py` - Text cleaning utilities

## Frontend
- `frontend/` - React frontend application
  - `src/` - React components
  - `package.json` - Node.js dependencies
  - `vite.config.js` - Vite configuration

## Startup Scripts
- `start_api.py` - Start backend API
- `start_backend.bat` - Windows batch file for backend
- `run_app.bat` - Start both backend and frontend
- `run_localhost.py` - Interactive localhost setup

## Configuration
- `.env` - Environment variables (API keys)
- `.gitignore` - Git ignore rules
- `web_interface.py` - Alternative web interface

## Documentation
- `README.md` - Main project documentation
- `API_SETUP.md` - API setup instructions
- `SETUP.md` - General setup guide
- `LICENSE` - Project license

## Generated Directories (Empty by default)
- `uploads/` - Uploaded files
- `complete_audiobooks/` - Generated audiobook files
- `chroma_db/` - Vector database storage

## Key Features
✅ PDF/DOCX/TXT text extraction  
✅ AI-powered text enhancement (Gemini API)  
✅ High-quality TTS (Edge TTS)  
✅ RAG-based document Q&A  
✅ React frontend interface  
✅ FastAPI backend  
✅ Vector database storage  