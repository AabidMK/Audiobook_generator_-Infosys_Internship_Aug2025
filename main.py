import os
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import chromadb
from sentence_transformers import SentenceTransformer
from rag.rag_ingest import parse_file, chunk_text
from rag.rag_query import answer_question
from tts import text_to_speech

# ---------------- SETUP ----------------
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Directories
INPUT_DIR = Path("input_files")
DB_DIR = Path("chroma_db")
INPUT_DIR.mkdir(exist_ok=True)
DB_DIR.mkdir(exist_ok=True)

# Chroma client
chroma_client = chromadb.PersistentClient(path=str(DB_DIR))
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
collection = chroma_client.get_or_create_collection("documents")

# ---------------- STREAMLIT PAGE CONFIG ----------------
st.set_page_config(
    page_title="Audiobook + RAG Q&A",
    page_icon="🦚",
    layout="wide"
)

# ---------------- CUSTOM PEACOCK THEME CSS ----------------
st.markdown("""
    <style>
    /* Background gradient */
    .stApp {
        background: linear-gradient(135deg, #041C32, #064663, #0A3D62);
        color: #E8F9FD;
    }

    /* Header */
    h1 {
        text-align: center;
        background: -webkit-linear-gradient(#00FFFF, #00BFA6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.6em !important;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
    }

    /* Tabs */
    .stTabs [role="tab"] {
        background-color: #04293A !important;
        color: #E8F9FD !important;
        border-radius: 10px;
        padding: 10px 20px;
    }
    .stTabs [role="tab"][aria-selected="true"] {
        background-color: #007B7F !important;
        color: white !important;
        font-weight: bold;
    }

    /* Buttons */
    .stButton>button {
        background-color: #007B7F;
        color: white;
        border-radius: 10px;
        border: none;
        font-size: 16px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #00BFA6;
        color: #041C32;
        transform: scale(1.05);
    }

    /* Chat message boxes */
    .stChatMessage {
        background-color: #04293A !important;
        border-radius: 12px !important;
        padding: 12px !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- MAIN TITLE ----------------
st.markdown("<h1>🎧Audiobook Generator + 🤖Intelligent Q/A Assistant</h1>", unsafe_allow_html=True)

# ---------------- TABS ----------------
tab1, tab2 = st.tabs(["🎧 Audio Generation", "🤖 Q/A Chatbot"])

# ---------------- TAB 1: AUDIO ----------------
with tab1:
    st.header("Upload Document & Generate Audio")
    uploaded_file = st.file_uploader(
        "Upload your document", type=["pdf", "txt", "docx", "png", "jpg", "jpeg"]
    )

    if uploaded_file:
        file_path = INPUT_DIR / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        st.success(f"✅ File saved: {file_path.name}")

        # Extract text
        extracted_text = parse_file(file_path)
        if extracted_text:
            st.subheader("📖 Extracted Text Preview")
            st.text_area("Text", extracted_text[:1000], height=200)

            # Generate Audio
            if st.button("🎵 Generate Audio"):
                audio_file = text_to_speech(extracted_text, output_path="output_audio.mp3")
                if audio_file:
                    st.audio(audio_file, format="audio/mp3")
                    with open(audio_file, "rb") as f:
                        st.download_button("⬇️ Download Audio", f, file_name="audiobook.mp3")
                else:
                    st.error("❌ Failed to generate audio.")
        else:
            st.warning("⚠️ Could not extract text from this file.")

# ---------------- TAB 2: Q/A (CHATBOT) ----------------
with tab2:
    st.header("Chat with Your Documents 🤖")

    if st.button("📥 Ingest All Files"):
        for file_path in INPUT_DIR.iterdir():
            text = parse_file(file_path)
            if not text:
                continue
            chunks = chunk_text(text)
            embeddings = embedding_model.encode(chunks).tolist()

            collection.add(
                ids=[f"{file_path.stem}_{i}" for i in range(len(chunks))],
                documents=chunks,
                embeddings=embeddings,
                metadatas=[{"source": file_path.name, "chunk": i} for i in range(len(chunks))]
            )
            st.write(f"✅ {file_path.name} ingested with {len(chunks)} chunks")

        st.success("🎉 All files ingested into ChromaDB!")

    # Chat history in Streamlit session
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for role, msg in st.session_state.chat_history:
        if role == "user":
            st.chat_message("user").markdown(msg)
        else:
            st.chat_message("assistant").markdown(msg)

    # Input box for new question
    query = st.chat_input("Ask something about your documents...")
    if query:
        # Add user query
        st.session_state.chat_history.append(("user", query))
        st.chat_message("user").markdown(query)

        # Get answer
        answer, citations = answer_question(query)

        # Format citations
        citation_text = "\n\n**Sources:**\n" + "\n".join(
            [f"- {meta['source']} (chunk {meta['chunk']}, dist {dist:.2f})" for meta, dist in citations]
        )

        # Final message
        final_answer = answer + citation_text

        # Show + Save assistant response
        st.chat_message("assistant").markdown(final_answer)
        st.session_state.chat_history.append(("assistant", final_answer))
