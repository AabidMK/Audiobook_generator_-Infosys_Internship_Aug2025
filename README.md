🎧 AI Audiobook Generator 

📘 Overview

AI Audiobook Generator is an intelligent document reader that automatically converts PDF or text files into speech while also enabling Retrieval-Augmented Generation (RAG) based question answering on the uploaded documents.

It combines:

🧠 Backend (Python) — Uses ChromaDB vector store, SentenceTransformers for embeddings, and Google Gemini for retrieval-based answering.

🗣 Text-to-Speech — Uses Coqui TTS to generate natural-sounding audiobook narration.

💻 Frontend — A Streamlit UI that allows uploading PDFs, generating audio, and asking document-based questions interactively.



---

📂 Project Structure

Audiobook_generator
│
├── coqui_env/                # Virtual environment
├── chromadb_store/           # Local ChromaDB vector database
├── rewritten_output.md       # Extracted & cleaned text from PDF
├── embed_store.py            # Chunking + Embedding + Vector store
├── rag_sys.py                # RAG Question Answering using Gemini
├── singlepipeline.py         # Combined audiobook generation
├── ui.py                     # Streamlit interface (Main UI)
├── requirements.txt          # Dependencies
├── .env                      # API keys (Google / Gemini)
└── README.md                 # Project documentation


---

⚙ Setup Instructions

1️⃣ Create Virtual Environment

python -m venv coqui_env
coqui_env\Scripts\activate        # On Windows


2️⃣ Install Dependencies

pip install -r requirements.txt

If any error appears:

pip install streamlit chromadb sentence-transformers PyPDF2 google-generativeai TTS qdrant-client

3️⃣ Add API Key

Create a .env file in your project root:

GOOGLE_API_KEY=YOUR_KEY_HERE


---

🚀 Run the Application

▶ Step 1: Run the Streamlit UI

streamlit run ui.py

Then open the local link shown in terminal, for example:

http://localhost:8501

▶ Step 2: Upload a PDF

The system extracts text → chunks → generates embeddings → stores them in ChromaDB.

It also generates an audiobook voice output using Coqui TTS.


▶ Step 3: Ask Questions

Type any question related to the uploaded document, and the model (Gemini) will answer from the stored embeddings.


---

🧩 Features

✅ Upload and parse PDF / text files
✅ Generate embeddings using MiniLM / e5 model
✅ Store vectors locally in ChromaDB
✅ Retrieve top chunks based on user query (RAG)
✅ Ask natural questions — powered by Google Gemini
✅ Generate audiobook from document text using Coqui TTS
✅ Interactive UI built with Streamlit


---

🧠 How It Works (Pipeline)

1️⃣ User uploads a PDF
2️⃣ Text is extracted & cleaned
3️⃣ The text is chunked and embedded (MiniLM model)
4️⃣ Stored in ChromaDB vector store
5️⃣ On user query → top relevant chunks are retrieved
6️⃣ Gemini LLM generates a final answer using retrieved context
7️⃣ The full text is converted to speech (Audiobook)


