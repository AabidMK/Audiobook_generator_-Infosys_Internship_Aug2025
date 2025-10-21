# 🚀 Running Your Project on Localhost

## Quick Start

### Option 1: Windows (Recommended)
```bash
# Double-click or run:
start_localhost.bat
```

### Option 2: Python Script
```bash
python run_localhost.py
```

### Option 3: Manual Setup
```bash
# Terminal 1 - Backend
python start_api.py

# Terminal 2 - Frontend  
cd frontend
npm install
npm run dev
```

---

## 🔧 What Runs Where

### Backend API (Port 8000)
- **URL**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Endpoints**:
  - `POST /upload` - Upload documents
  - `POST /generate-audiobook` - Generate audiobooks
  - `POST /query` - RAG Q&A
  - `GET /download/{type}/{filename}` - Download files

### Frontend (Port 3000 or 5173)
- **React + Vite** application
- **URL**: Usually http://localhost:3000 or http://localhost:5173
- **Features**: File upload, audiobook generation, Q&A interface

---

## ✅ Features Available

### 🎵 **Audiobook Generator**
1. Upload PDF/DOCX/TXT files
2. Generate enhanced audiobook text (Gemini API)
3. Create high-quality audio (Edge TTS)
4. Download both text and audio files

### 🤖 **RAG Q&A System**
1. Upload documents for indexing
2. Ask questions about your documents
3. Get AI-powered answers with citations
4. Semantic search through document content

### 🔧 **Technical Features**
- ✅ Unicode-safe processing
- ✅ Gemini API integration
- ✅ ChromaDB vector storage
- ✅ Edge TTS audio generation
- ✅ CORS enabled for frontend
- ✅ File upload/download
- ✅ Error handling

---

## 🛠 Troubleshooting

### Backend Won't Start
```bash
# Check dependencies
pip install -r requirements.txt

# Check API key
echo %GEMINI_API_KEY%

# Test imports
python -c "from main import app; print('OK')"
```

### Frontend Won't Start
```bash
cd frontend
npm install
npm run dev
```

### CORS Issues
- Backend allows `localhost:3000` and `localhost:5173`
- Check your frontend URL matches allowed origins

### File Upload Issues
- Ensure `uploads/` directory exists
- Check file permissions
- Supported formats: PDF, DOCX, TXT

---

## 📊 API Usage Examples

### Upload File
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@document.pdf"
```

### Generate Audiobook
```bash
curl -X POST "http://localhost:8000/generate-audiobook" \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "uploads/document.pdf",
    "voice_style": "storytelling",
    "generate_audio": true
  }'
```

### Query Documents
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the main topic?",
    "top_k": 5
  }'
```

---

## 🎯 Ready to Use!

Your project is now running on localhost with:
- ✅ **Backend API**: Full functionality
- ✅ **Frontend Interface**: React application  
- ✅ **Unicode Support**: No encoding errors
- ✅ **Gemini Integration**: AI-powered processing
- ✅ **File Processing**: PDF/DOCX/TXT support
- ✅ **Audio Generation**: High-quality TTS

**Access your application at the frontend URL and start creating audiobooks!** 🎉