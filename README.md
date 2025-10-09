# 📚 AI Audiobook Generator with RAG

A professional-grade audiobook generation system with Retrieval-Augmented Generation (RAG) for intelligent question-answering about your documents.

## ✨ Features

- **📖 Multi-format Support**: Process PDF, DOCX, and TXT files
- **🎙️ High-Quality Audio**: Generate natural-sounding audiobooks using Edge TTS
- **🤖 AI Enhancement**: LLM-powered text enhancement for better narration
- **💬 RAG Q&A System**: Ask questions about your documents and get intelligent answers
- **🎨 Modern Web Interface**: Beautiful React-based frontend
- **🔍 Vector Search**: ChromaDB-powered semantic search
- **⚡ Fast Processing**: Optimized pipeline for quick generation

## 🏗️ Project Structure

```
audiobook-generator/
├── backend/                    # Python backend
│   ├── core/                   # Core audiobook generation
│   ├── rag/                    # RAG and vector search
│   └── pipeline/               # Orchestration and indexing
├── frontend/                   # React web interface
├── tests/                      # Test suite
├── docs/                       # Documentation
├── outputs/                    # Generated audiobooks
├── data/                       # Databases and cache
├── scripts/                    # Utility scripts
├── server.py                   # Main entry point
└── requirements.txt            # Python dependencies
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Gemini API key (for RAG features)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd audiobook-generator
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up Frontend**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

4. **Configure Environment**
   ```bash
   copy .env.template .env
   # Edit .env and add your GEMINI_API_KEY
   ```

### Running the Application

**Option 1: Use the startup script (Recommended)**
```powershell
.\scripts\start_servers.ps1
```

**Option 2: Manual start**
```bash
# Terminal 1 - Backend
python server.py serve

# Terminal 2 - Frontend
cd frontend
npm run dev
```

Then open your browser to: **http://localhost:5173**

## 📖 Usage

### Generate an Audiobook

1. Open the web interface
2. Upload a document (PDF, DOCX, or TXT)
3. Enter an initial question about the document
4. Click "Generate Audiobook & Answer"
5. Wait for processing (1-3 minutes)
6. Listen to the audiobook and read the answer

### Ask Questions (RAG)

1. After uploading a document, use the chat box
2. Type your question
3. Get intelligent answers based on document content
4. Ask follow-up questions

### Command Line Usage

**Index documents for RAG:**
```bash
python server.py index --files document.pdf another.docx
```

**Query documents:**
```bash
python server.py query --question "What is the main topic?"
```

**Generate audiobook:**
```bash
python server.py audiobook --file document.pdf --voice storytelling
```

## 🧪 Testing

Run the test suite:
```bash
# Run all tests
python -m pytest tests/

# Run specific test
python tests/test_rag_pipeline.py
```

## 📚 Documentation

- **[Setup Guide](docs/SETUP_GUIDE.md)** - Detailed installation instructions
- **[Testing Guide](docs/TESTING_GUIDE.md)** - How to test the system
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions
- **[Project Structure](docs/PROJECT_STRUCTURE.md)** - Architecture overview
- **[RAG Fix History](docs/RAG_FIX_HISTORY.md)** - Development history

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Required for RAG features
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: Local LLM support
LM_STUDIO_URL=http://localhost:1234
```

### Frontend Configuration

Edit `frontend/.env`:

```env
VITE_API_URL=http://localhost:8080
```

## 🏛️ Architecture

### Backend Components

- **Core**: Text extraction and audiobook generation
- **RAG**: Vector embeddings, ChromaDB storage, and question-answering
- **Pipeline**: Orchestration and document indexing

### Technology Stack

**Backend:**
- Python 3.8+
- Flask (API server)
- ChromaDB (vector database)
- Sentence Transformers (embeddings)
- Google Gemini (LLM)
- Edge TTS (text-to-speech)

**Frontend:**
- React 18
- Vite
- Axios
- Modern CSS

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📄 License

See [LICENSE](LICENSE) file for details.

## 🐛 Troubleshooting

### Common Issues

**"Connection refused" error**
- Ensure backend is running: `python server.py serve`

**"Collection not found" error**
- Index documents first: `python server.py index --files your_file.pdf`

**"Gemini API key not found" error**
- Check `.env` file exists with valid `GEMINI_API_KEY`

**Import errors**
- Ensure you're in the project root directory
- Check that `backend/` folder exists with all modules

For more help, see [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

## 📊 Performance

- **Text Extraction**: ~1-2 seconds per page
- **Audio Generation**: ~30-60 seconds per minute of audio
- **RAG Query**: ~5-10 seconds per question
- **Document Indexing**: ~10-30 seconds per document

## 🎯 Roadmap

- [ ] Support for more audio voices
- [ ] Batch processing
- [ ] API authentication
- [ ] Docker deployment
- [ ] Cloud storage integration
- [ ] Multi-language support

## 💡 Tips

- Use specific questions for better RAG answers
- Larger documents take longer to process
- Keep documents under 50 pages for best performance
- Use the storytelling voice for narrative content

## 📞 Support

For issues and questions:
1. Check [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
2. Review [docs/TESTING_GUIDE.md](docs/TESTING_GUIDE.md)
3. Open an issue on GitHub

## 🙏 Acknowledgments

- Google Gemini for LLM capabilities
- ChromaDB for vector storage
- Edge TTS for high-quality audio
- Sentence Transformers for embeddings

---

**Made with ❤️ for Infosys Internship Aug 2025**
