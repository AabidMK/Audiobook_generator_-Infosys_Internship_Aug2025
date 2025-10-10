### AudioBook Generator 

Convert any text, PDF, or document  into a *natural-sounding audiobook* using AI-powered text-to-speech (TTS).  
Built with *Streamlit, **Edge-TTS, and **Transformers*, this app provides an easy-to-use interface and powerful backend pipeline for generating, previewing, and downloading audio files.

---
##  Features
-  High-quality AI voice generation  
-  Supports plain text, PDFs, and multi-document processing  
-  Paragraph and sub-chunk based audio generation  
-  Fast, asynchronous text-to-speech processing  
-  Adjustable voice parameters (speed, rate, etc.)  
-  Intelligent memory using RAG (Retrieval-Augmented Generation)  
-  Simple, interactive Streamlit UI

----
##  Installation
1. Clone the repository:
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo

2. (Optional) Create a virtual environment:
python -m venv env

3. Activate the virtual environment:
Windows : env\Scripts\activate
Mac/Linux : source env/bin/activate

4. Install the required packages : pip install -r requirements.txt

---
## RAG Workflow Overview 
The project uses *Retrieval-Augmented Generation (RAG)* to store and reuse document context intelligently:
1. *Document Extraction* – Text is extracted and cleaned from uploaded files.  
2. *Chunking* – The text is split into smaller chunks and sub-chunks for better handling.  
3. *Embedding* – Each chunk is converted into a numerical embedding using *SentenceTransformers*.  
4. *Storage* – The embeddings are stored in *ChromaDB*, a local vector database.  
5. *Retrieval* – When queried later, the app retrieves relevant chunks to provide context-aware responses or continue generating audio seamlessly.
This makes the system *context-aware*, allowing you to work with multiple documents without losing previous progress.

---
##  Project Structure
├── audiobook_ui.py            # Streamlit UI
├── pipeline_audio_edgttse.py      # Handles TTS audio generation 
├── pipeline_extraction.py   # Extracts text intelligently from PDFs or documents
|__ pipeline_enrichment.py   #Enriches extracted text using google gemini api
├── pipeline_chunking.py           # Splits text into manageable chunks 
├── pipeline_embedding.py        # Embeds text chunks for semantic retrieval
├── pipeline_chroma.py          # Handles ChromaDB storage and retrieval
|__ pipeline_rag.py             # Handles the rag part 
├── audiobook_requirements.txt           # Python dependencies
└── README.md

---
## Tech Stack
Python 3.10+
Streamlit – UI framework
Python-docx , pytesseract,pymupdf -  Text extraction
Google generative ai api key - Text enrichment
Edge-TTS – Text-to-Speech conversion
Transformers / SentenceTransformers – Text embedding
ChromaDB – Vector storage for document memory
