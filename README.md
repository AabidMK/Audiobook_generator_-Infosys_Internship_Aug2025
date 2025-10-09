# 🎧 AI Audiobook Generator + 📚 RAG Question Answering System  
### Infosys Internship Project — August 2025  
Developed by **Mukul Sangwan**

---

## 🚀 Overview

This repository contains two integrated Streamlit applications that together form an **AI-powered Audiobook and RAG (Retrieval-Augmented Generation) Question-Answering system**.

1. **`app.py`** – A simple and efficient **AI Audiobook Generator**.
2. **`rag/audiobook_app.py`** – An advanced **Audiobook + RAG QA** platform combining text-to-speech, local LLM enrichment, and intelligent document querying.

---

## 🧠 Key Functionalities

### 🎧 **Audiobook Generation**
- Upload `.pdf`, `.docx`, or `.txt` files.
- Extract readable content automatically.
- Enhance the narration using a local **LLM (Meta-Llama 3 / LMStudio)**.
- Generate high-quality audio narration using **Coqui TTS**.
- Preview or download the final `.mp3` or `.wav` file.

### 💬 **Document Q&A (RAG System)**
- Automatically chunks and vectorizes text content from uploaded documents.
- Performs **semantic search** using local embeddings.
- Generates **context-aware answers** using a locally hosted LLM.
- Powered by `LMStudio` or any OpenAI-compatible endpoint.

---

## 🗂️ Project Structure

```plaintext
Audio_Book_Generator/
│
├── output/                         # Generated audio output files
│
├── rag/                            # RAG + Audiobook hybrid app
│   ├── audiobooks/                 # Stored audio outputs
│   ├── chromadb_store/             # Vector embeddings storage
│   ├── documents/                  # Uploaded document storage
│   ├── src/
│   │   ├── document_parser.py      # Handles PDF/DOCX/TXT parsing
│   │   ├── embedding_manager.py    # Manages embedding creation
│   │   ├── ollama_llm.py           # LMStudio/Ollama client wrapper
│   │   ├── text_chunker.py         # Splits text into retrievable chunks
│   │   ├── utils.py                # Utility and config functions
│   │   ├── vector_store.py         # Vector database for document search
│   │   └── __pycache__/            # Cached bytecode
│   │
│   ├── audiobook_app.py            # Main Streamlit app for Audiobook + QA
│   ├── qa_app.py                   # (Optional) QA-only version
│   ├── config.yaml                 # Configuration for models and settings
│   └── requirements.txt            # Python dependencies for RAG app
│
├── app.py                          # Simple Audiobook generator app
├── text_extractor.py               # Handles file text extraction
├── llm_enrichment.py               # Enriches text narration using LLM
├── tts_generator.py                # Converts enriched text to audio
├── utils.py                        # General utilities and config loader
├── config.json                     # Config file for basic audiobook app
├── requirements.txt                # Dependencies for main app
└── README.md                       # Project documentation
```

---

## ⚙️ Installation Guide

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/AabidMK/Audiobook_generator_-Infosys_Internship_Aug2025.git
cd Audiobook_generator_-Infosys_Internship_Aug2025
git checkout Mukul-Sangwan
```

### 2️⃣ Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Required Dependencies
For the base app:
```bash
pip install -r requirements.txt
```

For the RAG system:
```bash
cd rag
pip install -r requirements.txt
```

If you don’t have requirements files, install manually:
```bash
pip install streamlit pdfplumber python-docx TTS openai pyyaml numpy chromadb
```

---

## ⚙️ Configuration Files

### 🔹 `config.yaml` (for `rag/audiobook_app.py`)
```yaml
tts:
  model_name: "tts_models/en/ljspeech/tacotron2-DDC"
  use_gpu: false

llm:
  base_url: "http://localhost:1234/v1"
  model_name: "meta-llama/Meta-Llama-3-8B-Instruct"
```

### 🔹 `config.json` (for root `app.py`)
```json
{
  "output_dir": "output",
  "tts_model": "tts_models/en/ljspeech/tacotron2-DDC"
}
```

---

## 🖥️ How to Run

### ▶️ **Run the Simple Audiobook Generator**
```bash
streamlit run app.py
```

### ▶️ **Run the Full Audiobook + RAG QA App**
```bash
cd rag
streamlit run audiobook_app.py
```

Then open the local Streamlit URL in your browser (usually `http://localhost:8501`).

---

## 🧭 Usage Flow

### 🎧 **Audiobook Generation**
1. Upload `.pdf`, `.docx`, or `.txt` files.  
2. The app extracts and optionally enhances text via LLM.  
3. Audio narration is generated and can be downloaded.

### 💬 **Document QA (RAG Mode)**
1. Upload documents in the **Audiobook tab**.  
2. Switch to the **Q&A tab**.  
3. Ask any question related to uploaded files — responses are generated based on contextual search.

---

## 🧩 Technology Stack

| Component | Technology |
|------------|-------------|
| **UI Framework** | Streamlit |
| **LLM Integration** | LMStudio / Ollama (Meta-Llama 3) |
| **Speech Synthesis** | Coqui TTS |
| **Document Parsing** | pdfplumber, python-docx |
| **Vector Search** | Custom VectorStore + ChromaDB |
| **Language** | Python 3.10+ |

---

## 📈 Example Workflow

| Step | Process | Output |
|------|----------|--------|
| 1 | Upload `example.pdf` | Extracted text |
| 2 | LLM rewrites narration | Enriched storytelling |
| 3 | TTS converts text | `example.mp3` |
| 4 | Ask Q: “What is the story about?” | AI-generated summary |

---

## 🧩 Future Scope
- Multilingual audiobook generation (Hindi, French, etc.)
- Speaker voice cloning and tone control
- Integration with cloud-hosted vector databases
- Streamlit Cloud / Hugging Face deployment

---

## 👩‍💻 Contributors

| Name | Role |
|------|------|
| **Mukul Sangwan** | Developer, Research & Integration |
| **Aabid M K** | Project Maintainer, Mentor |

---

## 📜 License
This project is licensed under the **MIT License**.

---

## 💡 Acknowledgements
- [LM Studio](https://lmstudio.ai) — Local LLM hosting  
- [Coqui TTS](https://github.com/coqui-ai/TTS) — Speech synthesis  
- [Streamlit](https://streamlit.io) — Interactive UI framework  
- Infosys Internship Program (2025) — Research mentorship

---

⭐ **Star this repository** if you found it useful or inspiring!
