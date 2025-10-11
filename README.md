### AudioBook Generator 

AudioBook Generator is a web application that allows users to upload one or more text 
documents (PDF, DOCX, TXT) and automatically converts them into high-quality 
audiobooks. The application leverages Large Language Models (LLMs) to rewrite extracted 
text in an engaging, listener-friendly “audiobook style” before using open-source Text-to
Speech (TTS) technology to produce downloadable audio files. This project enhances 
accessibility, productivity, and the enjoyment of written content.

# AudioBook Generator — Run Instructions

This file explains the steps to run the AudioBook Generator project locally using `uv` for Python dependency management and `npm` for the React frontend.

## Features

- **Document Upload**: Upload PDF, DOCX, or TXT files
- **AI-Powered Text Enrichment**: Uses Google Gemini AI to enhance text for better audiobook narration
- **Text-to-Speech**: Converts enriched text to audio using gTTS
- **RAG Q&A Assistant**: Ask questions about your uploaded documents using Retrieval-Augmented Generation
- **Vector Search**: Uses ChromaDB with HuggingFace embeddings for semantic document search

## Prerequisites

- **Python 3.10 or newer**
- **Node.js 16+** (for frontend)
- **uv** installed (`pip install uv`) or alternative virtual environment workflow
- **Google AI API Key** (for Gemini text enrichment and Q&A features)
- (Optional) **Tesseract OCR** if you need OCR for scanned PDFs

## Installation

### 1. Install `uv` (Python Package Manager)

If you do not have `uv` installed, install it using one of these methods (PowerShell):

```powershell
# Install via pip
pip install uv

# Verify installation
uv --version

# (Optional on Windows) Install via winget if available
winget install --id Astral.Sh.Uv -e
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root directory with the following content:

```env
GOOGLE_API_KEY=your_actual_google_ai_api_key_here
```

**Important**: Replace `your_actual_google_ai_api_key_here` with your actual API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

**Security Note**: Never commit the `.env` file to version control. It should be in your `.gitignore`.

### 3. Install Python Dependencies

From the project root directory:

```powershell
# Install all dependencies from pyproject.toml
uv sync
```

This creates a virtual environment (`.venv`) and installs all required packages including:
- FastAPI & Uvicorn (backend server)
- Google Generative AI (Gemini)
- ChromaDB (vector database)
- SentenceTransformers (embeddings)
- gTTS (text-to-speech)
- pypdfium2 (PDF parsing)
- And other dependencies

## Running the Application

### 4. Start the Backend (FastAPI Server)

From the project root directory:

```powershell
uv run uvicorn server:app --reload --host 127.0.0.1 --port 8000
```

- The backend will run at: http://127.0.0.1:8000
- API documentation (Swagger UI) available at: http://127.0.0.1:8000/docs
- The server uses `--reload` for development (auto-restart on file changes)

### 5. Install and Start the Frontend (React App)

Open a **new PowerShell terminal** and navigate to the frontend directory:

```powershell
cd frontend
npm install
npm start
```

- The React dev server will run at: http://localhost:3000
- The frontend will automatically connect to the backend at `http://localhost:8000`

## Usage

1. **Open the Application**: Navigate to http://localhost:3000 in your web browser

2. **Upload a Document**: 
   - Click on the upload area or drag-and-drop a PDF, DOCX, or TXT file
   - Wait for the processing to complete (text extraction → AI enrichment → chunking → embedding → audio generation)

3. **Download Audio**: 
   - Once processing is complete, click "Download Audio" to get your audiobook MP3 file

4. **Ask Questions (Q&A Assistant)**:
   - Use the Q&A Assistant panel on the right side
   - Type a question about your uploaded document
   - Click "Ask" to get an AI-generated answer based on the document content
   - The system uses RAG (Retrieval-Augmented Generation) to provide accurate, context-aware answers

## Architecture Overview

### Backend (`server.py` & `final_pipeline.py`)
- **FastAPI** web server
- **Document Processing Pipeline**:
  1. Text extraction (PDF/DOCX/TXT)
  2. Text enrichment with Gemini AI
  3. Text chunking for embeddings
  4. Embedding generation with HuggingFace SentenceTransformer
  5. Vector storage in ChromaDB
  6. Audio synthesis with gTTS
- **RAG Q&A System**:
  - Query embedding generation
  - Semantic search in ChromaDB
  - Context retrieval and answer generation with Gemini

### Frontend (`frontend/src/`)
- **React** application with Tailwind CSS
- **Main Components**:
  - Upload form for document submission
  - Job status display
  - Audio download interface
  - Q&A Assistant for document queries

## Troubleshooting

### Backend Issues

**Problem**: `API key not valid` error
- **Solution**: Ensure your `GOOGLE_API_KEY` is correctly set in the `.env` file and is a valid key from Google AI Studio

**Problem**: `uv sync` fails with file access error
- **Solution**: Close all terminals and VS Code, delete the `.venv` folder, then run `uv sync` again

**Problem**: `'NoneType' object is not iterable` in Q&A
- **Solution**: Make sure you've uploaded a document before asking questions. The vector database needs to be populated first.

**Problem**: Module import errors
- **Solution**: Run `uv sync` to ensure all dependencies are installed correctly

### Frontend Issues

**Problem**: Frontend can't connect to backend
- **Solution**: Verify the backend is running on port 8000 and check that `BACKEND_URL` in frontend components points to `http://localhost:8000`

**Problem**: Q&A Assistant shows "Error processing your request"
- **Solution**: Check backend terminal logs for detailed error messages. Ensure your Google API key is valid and has not exceeded quota limits.

## Development Notes

### Adding New Dependencies

**Python**: Add to `pyproject.toml` and run `uv sync`
**Frontend**: Run `npm install <package>` in the `frontend/` directory

### Gemini API Rate Limits
- Free tier: 60 requests/minute, 1000 requests/day
- If you hit limits, consider upgrading to a paid plan or implement request queuing

### Modifying the AI Prompt
- Text enrichment prompt: Edit `text_enrichment.py`
- Q&A answer generation prompt: Edit `final_pipeline.py` in the `answer_question` function

## Alternative Setup (Without `uv`)

If you prefer not to use `uv`:

1. Create a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

3. Run the backend:
   ```powershell
   python -m uvicorn server:app --reload --host 127.0.0.1 --port 8000
   ```

## Project Structure

```
Audiobook_generator_-Infosys_Internship_Aug2025/
├── server.py                 # FastAPI backend server
├── final_pipeline.py         # Core processing pipeline & RAG Q&A
├── text_enrichment.py        # AI text enrichment with Gemini
├── text_extraction.py        # Document text extraction
├── audio_generation.py       # TTS audio generation
├── pyproject.toml            # Python dependencies (uv)
├── requirements.txt          # Python dependencies (pip)
├── .env                      # Environment variables (not in git)
├── uploads/                  # Uploaded files storage
├── outputs/                  # Generated audio files
├── chroma_db/                # ChromaDB vector database
└── frontend/                 # React frontend application
    ├── src/
    │   ├── App.js
    │   └── components/
    │       └── ui/
    │           ├── QABox.js           # Q&A Assistant component
    │           └── UploadBox.js       # Upload interface
    ├── package.json
    └── README.md
```

## Support

For issues or questions, please check:
- Backend logs in the terminal running `uvicorn`
- Frontend console logs in browser DevTools (F12)
- Google AI Studio for API key status and quotas

## License

See LICENSE file for details.
