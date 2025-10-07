# 📖 Audiobook Generator with Intelligent Q&A

This project is a **Streamlit-based web application** that converts text documents (PDF, DOCX, TXT) into **audiobooks** and allows users to **ask questions** about the uploaded content using **semantic search powered by Sentence Transformers**.

It can also display **citations** showing where the answer was found in the document.

---

## 🚀 Features

✅ **Audiobook Conversion** – Converts uploaded files into clear speech using `pyttsx3`.
✅ **Multi-format Support** – Works with `.pdf`, `.docx`, and `.txt` files.
✅ **Smart Q&A System** – Uses semantic similarity (Sentence-BERT) to retrieve answers from file content.
✅ **Citations** – Displays relevant text chunks as sources for the answer.
✅ **User-Friendly Interface** – Clean Streamlit layout with progress spinners and download options.

---

## 🧠 How It Works

1. **File Upload:**
   You upload a PDF, DOCX, or TXT file. The app extracts the full text.

2. **Text-to-Speech:**
   The extracted text is processed using `pyttsx3` to generate a downloadable `.wav` audiobook file.

3. **Chunking and Embedding:**
   The document text is split into overlapping chunks for better semantic understanding, and embeddings are generated using `SentenceTransformer (all-MiniLM-L6-v2)`.

4. **Question Answering:**
   When you enter a query, the app computes cosine similarity between your question and all chunks to find the most relevant ones.

5. **Citations:**
   It displays the top 5 matching text chunks (citations) showing where the answer came from.

---

## 🧩 Project Structure

```
Audiobook-Generator/
│
├── ui.py              # Streamlit frontend (UI + logic)
├── retrieval.py       # Embedding, chunking, and retrieval logic
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```

---

## ⚙️ Installation

### 1️⃣ Clone this repository

```bash
git clone https://github.com/yourusername/Audiobook-Generator.git
cd Audiobook-Generator
```

### 2️⃣ Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # on Windows
# or
source venv/bin/activate  # on macOS/Linux
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt example:**

```
streamlit
PyPDF2
python-docx
pyttsx3
sentence-transformers
torch
```

---

## ▶️ Run the App

Once everything is installed, launch the Streamlit app:

```bash
streamlit run ui.py
```

Then open the provided local URL (usually `http://localhost:8501`) in your browser.

---

## 🧩 How to Use

1. Click **“📂 Upload your file”** and choose a `.pdf`, `.docx`, or `.txt` file.
2. Wait for the text extraction confirmation ✅.
3. The app automatically generates an audiobook you can **play** or **download**.
4. In the **Q&A section**, type a question like:

   * “When was the company founded?”
   * “Explain the main idea of this report.”
   * “What are the key challenges mentioned?”
5. The app shows:

   * The **most relevant answer**
   * A list of **citations (source snippets)** where the answer came from

---

## 🧰 Technologies Used

| Component                 | Description                                |
| ------------------------- | ------------------------------------------ |
| **Streamlit**             | For creating the interactive web interface |
| **PyPDF2 / python-docx**  | For text extraction from PDF and DOCX      |
| **pyttsx3**               | Text-to-speech conversion                  |
| **Sentence Transformers** | Semantic text embeddings                   |
| **PyTorch**               | Backend for embedding model                |

---

## 📌 Example Output

**Question:**

> When was Cristiano Ronaldo born?

**Answer:**

> Cristiano Ronaldo dos Santos Aveiro was born on February 5, 1985, on the small island of Madeira, Portugal.

**Citations:**

* Chunk 2: "...Cristiano Ronaldo dos Santos Aveiro was born on February 5, 1985, on the small island of Madeira, Portugal..."
* Chunk 1: "Ronaldo grew up in a humble family..."

---

## 🧑‍💻 Developer Guide

### Modify Q&A Logic

You can adjust retrieval sensitivity in `retrieval.py`:

```python
retrieve_answer(query, chunks, model, top_k=5, similarity_threshold=0.4)
```

* `top_k`: Number of chunks returned as citations
* `similarity_threshold`: Minimum cosine similarity for filtering results

### Change TTS Engine Voice

In `ui.py`, modify `pyttsx3` voice parameters:

```python
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Choose a different voice
```

---

## 🧾 License

This project is released under the **MIT License**.
You are free to use, modify, and distribute it with attribution.

---

## 🌟 Acknowledgments

* [Streamlit](https://streamlit.io/) for making web apps simple in Python
* [Sentence Transformers](https://www.sbert.net/) for powerful semantic embeddings
* [Pyttsx3](https://pyttsx3.readthedocs.io/en/latest/) for offline text-to-speech support

---

### 💡 Future Enhancements

* Add support for **summarization** of long documents
* Add **highlighting of the exact sentence** for citations
* Option to select **voice type** and **speech rate**
* Cloud deployment on **Streamlit Community Cloud** or **Hugging Face Spaces**

---



