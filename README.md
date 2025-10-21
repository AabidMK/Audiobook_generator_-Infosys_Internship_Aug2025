# 🎧 AudioBook Generator

**Transform any document into professional audiobooks with AI-powered enhancement and high-quality text-to-speech.**

## ✨ Features

- 📄 **Multi-format Support**: PDF, DOCX, TXT file processing
- 🤖 **AI Enhancement**: Gemini API transforms text into engaging audiobook narration
- 🎙️ **Premium TTS**: Edge TTS with multiple voice styles (storytelling, authoritative, conversational)
- 🔍 **Smart Q&A**: RAG-powered document search and question answering
- 🌐 **Modern UI**: React frontend with real-time progress tracking
- ⚡ **Fast Processing**: Optimized pipeline with caching and batch processing

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AabidMK/Audiobook_generator_-Infosys_Internship_Aug2025.git
   cd Audiobook_generator_-Infosys_Internship_Aug2025
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup environment**
   ```bash
   # Create .env file
   echo "GEMINI_API_KEY=your_api_key_here" > .env
   ```

4. **Install frontend dependencies**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

### Running the Application

**Option 1: Full Stack (Recommended)**
```bash
run_app.bat  # Windows
# or
python run_localhost.py  # Cross-platform
```

**Option 2: Backend Only**
```bash
python start_api.py
```

**Option 3: Manual Setup**
```bash
# Terminal 1 - Backend
python start_api.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

## 🎯 Usage

1. **Upload Document**: Drag & drop or select PDF/DOCX/TXT files
2. **Generate Audiobook**: Choose voice style and click generate
3. **Download**: Get enhanced text and high-quality audio files
4. **Ask Questions**: Use RAG system to query document content

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React UI      │────│   FastAPI        │────│   Gemini API    │
│   (Frontend)    │    │   (Backend)      │    │   (Enhancement) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                    ┌─────────┼─────────┐
                    │         │         │
            ┌───────▼───┐ ┌───▼────┐ ┌──▼──────┐
            │ Edge TTS  │ │ ChromaDB│ │Text     │
            │ (Audio)   │ │ (RAG)   │ │Extraction│
            └───────────┘ └────────┘ └─────────┘
```

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python 3.8+
- **Frontend**: React, Vite, Axios
- **AI/ML**: Google Gemini API, ChromaDB, Sentence Transformers
- **TTS**: Microsoft Edge TTS
- **Text Processing**: PyMuPDF, python-docx, BeautifulSoup

## 📁 Project Structure

```
├── main.py                 # FastAPI backend server
├── audiobook_generator.py  # Core audiobook logic
├── enhanced_extraction.py  # Text extraction
├── rag.py                 # RAG system
├── frontend/              # React application
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables
```bash
GEMINI_API_KEY=your_gemini_api_key
LM_STUDIO_BASE_URL=http://localhost:1234  # Optional
```

### Voice Styles
- **storytelling**: Warm, expressive (default)
- **authoritative**: Deep, confident
- **conversational**: Natural, friendly
- **narrative**: Smooth, professional
- **dramatic**: Dynamic, emotional

## 🚨 Troubleshooting

### Port Conflicts
```bash
# Check ports
netstat -ano | findstr :8000

# Kill processes
taskkill /F /PID <PID>
```

### Common Issues
- **Indexing failed**: Check file permissions and format
- **Audio generation failed**: Verify Edge TTS installation
- **API errors**: Validate Gemini API key

## 📊 Performance

- **Text Processing**: ~2-5 seconds per page
- **AI Enhancement**: ~10-30 seconds per chunk
- **Audio Generation**: ~1-2x real-time speed
- **Supported File Size**: Up to 50MB documents

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Infosys Internship Program** - Project opportunity
- **Google Gemini API** - AI text enhancement
- **Microsoft Edge TTS** - High-quality speech synthesis
- **ChromaDB** - Vector database for RAG

---

**Made with ❤️ during Infosys Internship 2025**