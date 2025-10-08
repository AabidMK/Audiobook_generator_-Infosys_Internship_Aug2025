# 🧠 RAG Document AI — Full Stack Intelligent Document Assistant

## 📘 Overview
**RAG Document AI** is a full-stack intelligent document processing system that uses **Retrieval-Augmented Generation (RAG)** to analyze, understand, and interact with uploaded documents.

It combines:
- 🧩 **Backend** — FastAPI + LangChain + Ollama  
- ⚛️ **Frontend** — React + TailwindCSS  
- 🔄 **Concurrent Integration** for a seamless development experience

---

## 📂 Project Structure

rag-document-ai/
│

├── backend/ # FastAPI backend server

│ ├── app.py # Main backend entry point

│ ├── requirements.txt # Backend dependencies

│ ├── rag_utils.py # RAG setup and vector store logic

│ ├── tts_conversion.py # Text-to-speech conversion

│ ├── text_extractor.py # Document text extraction

│ └── temp_files/ # Uploaded files
│

├── frontend/ # React frontend

│ ├── src/

│ │ ├── App.jsx # Main React component

│ │ ├── reflection.css # Styling with reflection & ripple
│ │ └── ...

│ ├── package.json

│ └── vite.config.js

│
├── .gitignore # Ignored files

└── README.md # Project documentation


---

## ⚙️ Setup Instructions

### 🔧 Backend Setup

```bash
🔧 Backend Setup
cd backend
python -m venv venv
venv\Scripts\activate       # (Use `source venv/bin/activate` for Mac/Linux)
pip install -r requirements.txt

Run the backend:
uvicorn app:app --reload
```

### 💻 Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 🔁 Run Both Together (Using Concurrently)

From the project root (rag-document-ai):
```bash
npm install concurrently
npm run dev
```


✅ The frontend and backend will run together automatically:

Frontend → http://localhost:5173

Backend → http://127.0.0.1:8000

### 🧩 Features

✅ Upload and parse PDF / DOCX / TXT files

✅ Get instant context-aware Q&A using LangChain + Ollama

✅ Generate Audiobook from text using Google TTS

✅ Interactive UI with reflection effects

✅ Concurrent Frontend + Backend integration

✅ Clean, modular architecture

### 🚀 GitHub & Deployment Guide

If you are working on your branch (e.g., saipavan), follow these steps to safely update your code on GitHub.

1️⃣ Connect to the Correct Remote Repository
git remote remove origin
git remote add origin https://github.com/AabidMK/Audiobook_generator_-Infosys_Internship_Aug2025.git
git remote -v

2️⃣ Checkout / Create Your Branch
git checkout -b saipavan

3️⃣ Stage and Commit Changes
git add .
git commit -m "🧠 Full RAG Document AI Project Update"

4️⃣ Force Push to Your Branch

⚠️ This will overwrite the existing files in your GitHub branch with your local version.

git push origin saipavan --force

5️⃣ Set Upstream for Future Pushes
git push --set-upstream origin saipavan


Now, simply use:

git push


for future updates.

🧰 Troubleshooting

1️⃣ Invalid Credentials in UI

Use login credentials:
Username: admin
Password: password123

2️⃣ Missing Python Modules

pip install unstructured langchain_ollama langchain_chroma


3️⃣ Line Ending (CRLF/LF) Warnings
These are harmless; fix globally using:

git config --global core.autocrlf true


4️⃣ DOCX Upload Error
If you see:

unstructured package not found


Run:
```
pip install "unstructured[all-docs]"
```


## 🧑‍💻 Contributor

### Sai Pavan — RAG pipeline & backend integration

## 🏁 License
All rights reserved © 2025.





