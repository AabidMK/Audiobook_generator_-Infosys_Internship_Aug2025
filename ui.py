import os
import tempfile
import streamlit as st
import chromadb
from chromadb.utils import embedding_functions
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from TTS.api import TTS

# ---------------- CONFIG ----------------
GEMINI_API_KEY = ".............."  # Paste your key here
genai.configure(api_key=GEMINI_API_KEY)

CHROMA_PATH = "chromadb_store"
COLLECTION_NAME = "audiobook_chunks"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# ---------------- UI SETUP ----------------
st.set_page_config(page_title="RAG + Audiobook Generator", page_icon="🎧", layout="wide")

st.title("📚 RAG + Audiobook Generator 🎧")
st.markdown(
    """
    <style>
    .big-font {font-size:20px !important;}
    .citation {font-size:14px; color:#888;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- FUNCTIONS ----------------
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def store_embeddings(chunks):
    st.info(" Storing chunks in ChromaDB...")
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=MODEL_NAME)
    collection = client.get_or_create_collection(name=COLLECTION_NAME, embedding_function=embedding_func)

    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            ids=[str(i)],
            metadatas=[{"source": "uploaded_pdf", "chunk_id": i}],
        )
    st.success(f" Stored {len(chunks)} chunks successfully!")
    return collection

def retrieve_relevant_chunks(collection, query, top_k=3):
    results = collection.query(query_texts=[query], n_results=top_k)
    return results["documents"][0], results["metadatas"][0], results["distances"][0]

def ask_gemini(query, context):
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = f"""
    You are a helpful assistant. Use the following context to answer the user's question accurately.

    Context:
    {context}

    Question: {query}

    Answer only from the provided context.
    """
    response = model.generate_content(prompt)
    return response.text

def generate_audio(answer_text):
    st.info("🎙 Generating audiobook...")
    tts = TTS("tts_models/en/ljspeech/tacotron2-DDC")
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    tts.tts_to_file(text=answer_text, file_path=temp_audio.name)
    st.success(" Audio generated successfully!")
    return temp_audio.name

# ---------------- MAIN APP ----------------
uploaded_file = st.file_uploader(" Upload a PDF file", type=["pdf"])
query = st.text_input("Ask a question about the PDF:")

if uploaded_file is not None:
    st.write(f" Uploaded: *{uploaded_file.name}*")

    if st.button(" Process PDF & Generate Answer"):
        with st.spinner("Processing... Please wait ⏳"):
            text = extract_text_from_pdf(uploaded_file)
            chunks = chunk_text(text)
            collection = store_embeddings(chunks)

            if query:
                st.info("🔍 Retrieving relevant information...")
                docs, metas, distances = retrieve_relevant_chunks(collection, query)
                context = "\n".join(docs)

                st.success("Retrieved top relevant chunks!")
                st.markdown("<h4> Gemini Answer:</h4>", unsafe_allow_html=True)
                answer = ask_gemini(query, context)
                st.markdown(f"<div class='big-font'>{answer}</div>", unsafe_allow_html=True)

                # Citations Section
                st.markdown("<h4>Citations:</h4>", unsafe_allow_html=True)
                for meta, dist in zip(metas, distances):
                    st.markdown(
                        f"<div class='citation'>• Source: {meta['source']} | Chunk ID: {meta['chunk_id']} | Similarity: {1 - dist:.2f}</div>",
                        unsafe_allow_html=True,
                    )

                # Generate and Play Audio
                audio_path = generate_audio(answer)
                st.audio(audio_path, format="audio/wav")
            else:
                st.warning("⚠ Please enter a question before generating an answer.")