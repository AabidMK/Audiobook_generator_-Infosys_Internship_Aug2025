# 🎧 AI Audiobook Generator

**Author:** Aditya Kadam  
---

## 📘 Description

The **AI Audiobook Generator** is a full-stack application that transforms any document (PDF, DOCX, or TXT) into a **natural-sounding audiobook** while also allowing users to **interact with the content** through an intelligent **chat assistant** powered by **Retrieval-Augmented Generation (RAG)**.

This project integrates a multi-stage pipeline involving:
1. **Text extraction and cleaning** from uploaded files  
2. **Text enrichment** using a locally hosted language model (LM Studio)  
3. **Natural speech narration** via Coqui TTS  
4. **Knowledge retrieval** using Qdrant vector database and e5-large embeddings  
5. **Interactive querying** through a React-based user interface  

The goal of this project is to create a seamless experience where users can both **listen to documents** and **ask questions** about their content — effectively merging reading, listening, and understanding into one intelligent system.

---

## 🧠 Core Objectives

- Automate the process of generating audiobooks from documents.  
- Make AI narration sound natural and engaging.  
- Enable context-aware Q&A through RAG integration.  
- Provide an intuitive, single-page web interface for accessibility.

---

## 🧰 Technologies Used

### **Backend**
- **FastAPI** – Primary backend framework  
- **LM Studio (Local LLM)** – Used for intelligent text rewriting  
- **Coqui TTS** – Converts enriched text into lifelike audio narration  
- **Qdrant** – Vector database for document retrieval  
- **Hugging Face `intfloat/e5-large-v2`** – Embedding model for RAG search  
- **Pydub** – Audio concatenation and export handling  
- **FFmpeg** – Required for audio file processing  

### **Frontend**
- **React + Vite** – Fast, modern frontend framework  
- **Tailwind CSS** – For responsive and clean styling  
- **Axios** – Handles API requests to backend  
- **React Audio Player** – Plays generated audiobook files  

---

## ⚙️ Features

### 🎙️ Audiobook Generation
- Upload PDF/DOCX/TXT files.  
- Automatically extracts and rewrites text for clarity using LM Studio.  
- Synthesizes audio using **multi-voice Coqui TTS**.  
- Provides a **downloadable .wav file** and an **in-browser audio player**.

### 💬 Intelligent RAG Chat
- Users can chat with the document after it’s processed.  
- The system retrieves relevant chunks from **Qdrant**.  
- Generates answers using **context-aware LLM inference**.  
- Each answer includes **citations** for transparency.

### 🧩 Modular Backend Pipeline
The backend is modular, ensuring each stage of the pipeline can be run independently:
1. Text extraction  
2. Text enrichment  
3. Audiobook narration  
4. Vector indexing  
5. RAG-based Q&A  

### 🌐 Web UI
A single-page web interface that includes:
- File upload and progress indicators  
- Audiobook playback controls  
- Download option  
- Chat interface for RAG Q&A  

---

## 🏗️ System Design

      +-------------------+
      |   React Frontend  |
      |-------------------|
      | Upload | Player | Chat |
      +-------------------+
                |
                ▼
      +-------------------+
      |  FastAPI Backend  |
      +-------------------+
      | Extract | Rewrite |
      | Narrate | Index  |
      | Retrieve | Answer |
      +-------------------+
                |
                ▼
      +-------------------+
      |  Qdrant Vector DB  |
      +-------------------+

---

## 📂 File Descriptions

### **Backend Files**
- `pipeline.py` – Main orchestrator combining all steps of the audiobook + RAG pipeline.  
- `Text_extractor.py` – Extracts raw text from PDF, DOCX, or TXT files.  
- `text_llm.py` – Connects to LM Studio to rewrite and improve text quality.  
- `multivoiceTTS.py` – Handles text-to-speech generation with multiple Coqui voices.  
- `index_builder.py` – Embeds document chunks and stores them in Qdrant.  
- `rag_pipeline.py` – Performs RAG retrieval and generates context-based answers.  
- `query_retriever.py` – Handles vector-based document searching.  
- `static/audios/` – Stores generated audiobook `.wav` files.

### **Frontend Files**
- `App.jsx` – Core layout combining upload, playback, and chat.  
- `UploadForm.jsx` – Handles file selection and upload.  
- `AudioPlayer.jsx` – Renders and controls the generated audiobook.  
- `ChatBox.jsx` – User interface for asking RAG-based questions.  
- `api.js` – Defines API endpoints for backend communication.  
- `index.css` & `App.css` – Style sheets for responsive UI.  

---

## 🧩 Design Decisions

### 1. **Local AI Models**
To ensure privacy and offline capability, LM Studio (for LLM inference) and Coqui TTS (for speech synthesis) were used locally instead of cloud APIs like OpenAI or ElevenLabs.

### 2. **Embedding Consistency**
The same embedding model (`intfloat/e5-large-v2`) was used during both indexing and querying to ensure maximum retrieval accuracy.

### 3. **Multi-Voice Narration**
To make the audiobook engaging, alternating voices (`p225`, `p227`, `p229`) from the VCTK dataset were used to simulate dynamic narration.

### 4. **Simplified File Management**
Each generated file (text, markdown, and audio) is named uniquely with timestamps to prevent overwriting and allow batch processing.

---

## 🧱 How to Run

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt
uvicorn main:app --reload

Frontend Setup

cd UI
npm install
npm run dev

Access the web app at:
👉 http://localhost:5173
Backend API runs at:
👉 http://localhost:8000

⸻

🔍 How It Works
	1.	Upload Document – User selects a file from the frontend.
	2.	Extraction – Backend extracts and cleans the text.
	3.	Rewriting – LM Studio improves clarity and flow.
	4.	Narration – Coqui TTS generates lifelike audio.
	5.	Indexing – Text chunks are embedded and stored in Qdrant.
	6.	Interaction – Users can query the document through chat.

⸻

🧠 What I Learned
	•	Implementing a multi-stage AI pipeline combining LLMs, embeddings, and TTS.
	•	Managing FastAPI and React integration using REST APIs.
	•	Handling vector databases and semantic search with Qdrant.
	•	Working with audio synthesis, cleanup, and merging via Pydub.
	•	Debugging token and speaker mismatches in Coqui TTS.
	•	Understanding the importance of modular, testable architecture.

⸻

🚀 Future Improvements
	•	Add voice selection and speech speed controls in UI.
	•	Integrate GPU acceleration for faster TTS generation.
	•	Save and display query history for better usability.
	•	Allow multi-language support using multilingual TTS models.
	•	Enable fine-tuning on specific narration styles (e.g., academic, storytelling).
	•	Add PDF summarization and chapter-wise playback features.


