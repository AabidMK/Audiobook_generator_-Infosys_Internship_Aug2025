# 📘 AssistifyAI — RAG Document AI with Audio Generation

> An intelligent assistant that allows users to **upload documents**, ask **contextual questions** using **RAG (Retrieval-Augmented Generation)**, and even **convert them into audiobooks** using **Text-to-Speech (TTS)**.

---

## 🧠 Tech Stack

- **Frontend:** React + TailwindCSS  
- **Backend:** FastAPI  
- **AI:** LangChain + Ollama (Llama3)  
- **Embeddings:** nomic-embed-text  
- **Audio Generation:** Google Text-to-Speech (gTTS)

---

## 🗂️ Project Structure

rag-document-ai/
│
├── backend/
│ ├── app.py # Main FastAPI backend
│ ├── rag_utils.py # RAG logic (vector store, retriever, chain)
│ ├── tts_conversion.py # Text-to-Speech conversion
│ ├── llm_enrichment.py # Optional LLM enrichment utilities
│ ├── text_extractor.py # Document parsing utilities
│ ├── requirements.txt # Backend dependencies
│ ├── .env # Environment variables (optional)
│ └── temp_files/ # Uploaded docs + generated audio
│
└── frontend/
├── src/
│ ├── App.js # Main React app
│ ├── reflection.css # Ripple & glow effect styling
│ └── ...
├── package.json
└── public/

yaml
Copy code

---

## ⚙️ Backend Setup
```bash
1️⃣ Create and Activate Virtual Environment

cd backend
python -m venv venv
venv\Scripts\activate      # (Windows)
# OR source venv/bin/activate  (Mac/Linux)
2️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt
3️⃣ Pull Required Ollama Models
Ensure Ollama is installed and running.

bash
Copy code
ollama pull llama3
ollama pull nomic-embed-text
Verify installation:

bash
Copy code
ollama list
Expected:

vbnet
Copy code
NAME                 ID           SIZE
llama3:latest        365c0bd3c000 4.7 GB
nomic-embed-text     0a109f422b47 274 MB
4️⃣ Run Backend
bash
Copy code
uvicorn app:app --reload --port 8000
Server runs at: http://127.0.0.1:8000

## 💻 Frontend Setup
1️⃣ Install Dependencies
``bash
Copy code
cd frontend
npm install
2️⃣ Run Frontend
bash
Copy code
npm start
App will be live at: http://localhost:3000

🔐 Login Credentials
Username	Password
admin	password123

🧠 How It Works
Login to access the app.

Upload a .pdf, .txt, or .docx file.

Backend:

Loads and splits document.

Embeds content using nomic-embed-text.

Creates a Chroma vector database.

Ask Questions — answers generated using Llama3 and retrieved context.

Generate Audiobook — converts entire document into .mp3 audio using Google TTS.

🎧 Supported Audio Languages
Supports all Google TTS Languages:

scss
Copy code
en (English), es (Spanish), fr (French), de (German),
hi (Hindi), ja (Japanese), zh (Chinese), ar (Arabic), etc.
🗃️ API Endpoints
Method	Endpoint	Description
POST	/api/login	Authenticate user
POST	/api/upload	Upload and process a document
POST	/api/answer	Ask a question using RAG
POST	/api/audiobook	Generate audio file
GET	/api/langs	Get supported TTS languages
GET	/api/qa-history	Fetch previous Q&A pairs

⚠️ Common Issues
Issue	Solution
401 Unauthorized	Log in again; token may have expired
500 Internal Server Error	Ensure Ollama is running (ollama serve)
Chroma object has no attribute 'persist'	Fixed — remove old .persist() usage
LangChainDeprecationWarning	Replace imports with langchain_community and langchain_chroma

🌟 Future Enhancements
Persistent history (SQLite or PostgreSQL)

Voice selection (male/female tone)

PDF summarization

Cloud-based vector DB integration (e.g., Pinecone)

Enhanced UI/UX animations

🧾 License
MIT License © 2025 — Developed by Sai Pavan








<!-- # Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify) -->
