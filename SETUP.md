# AudioBook Generator Setup Guide

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Installation

1. **Backend Setup**
   ```bash
   # Install Python dependencies
   pip install -r requirements.txt
   
   # Install additional dependencies for your specific modules
   pip install chromadb sentence-transformers torch transformers
   ```

2. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

### Running the Application

#### Option 1: Use the startup script (Windows)
```bash
run_app.bat
```

#### Option 2: Manual startup

**Terminal 1 - Backend:**
```bash
python start_api.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Access Points
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## API Endpoints

### File Upload & Processing
- `POST /upload` - Upload and index document for RAG
- `POST /generate-audiobook` - Generate audiobook from uploaded file
- `POST /query` - Query documents using RAG
- `GET /download/{file_type}/{filename}` - Download generated files

### Usage Flow
1. Upload a document (.pdf, .docx, .txt)
2. File gets indexed for RAG automatically
3. Audiobook generation starts
4. Use chat interface for Q&A about the document

## Features
- Document upload and text extraction
- RAG-based question answering
- Text-to-speech audiobook generation
- Interactive chat interface
- File download capabilities

## Troubleshooting
- Ensure all dependencies are installed
- Check that ports 8000 and 5173 are available
- Verify file paths in uploaded documents
- Check browser console for frontend errors