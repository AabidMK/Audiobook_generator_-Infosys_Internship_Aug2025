import streamlit as st
import asyncio
import tempfile
import nest_asyncio
from pathlib import Path

# Apply async patch for running asyncio in Streamlit
nest_asyncio.apply()

# === Import custom modules ===
from extract_txt import extract_text_file          # Handles .txt files
from extract_docx import extract_docx              # Handles .docx files
from extract_pdf import extract_pdf                # Handles .pdf files
from extract_image import extract_image            # Handles image files (.jpg, .png)
from llm_txt_generation import rewrite_text_with_gemini  # Gemini-based text rewriting
from tts_enhancer import text_to_speech            # Convert text to speech
from qa_embedding import EmbeddingModule           # For embeddings
from qa_vectordb import VectorDB                   # Vector database for RAG


# ===================== Helper Functions =====================

def extract_file(file):
    """Extract text from uploaded file."""
    ext = Path(file.name).suffix.lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp_file:
        tmp_file.write(file.read())
        tmp_path = tmp_file.name

    if ext == ".txt":
        return extract_text_file(tmp_path)
    elif ext == ".docx":
        return extract_docx(tmp_path)
    elif ext == ".pdf":
        return extract_pdf(tmp_path)
    elif ext in [".jpg", ".jpeg", ".png"]:
        return extract_image(tmp_path)
    else:
        return ""


async def process_pipeline(file):
    """Process file: extract, rewrite, and convert to audio."""
    raw_text = extract_file(file)
    if not raw_text.strip():
        return None, "❌ No text extracted from the file."

    # Rewrite text using Gemini model
    rewritten_text = rewrite_text_with_gemini(raw_text)

    # Convert rewritten text to audio
    audio_file = Path(file.name).stem + "_audiobook.mp3"
    await text_to_speech(rewritten_text, audio_file)

    return rewritten_text, audio_file


def setup_rag(file):
    """Prepare RAG embeddings and vector database."""
    file.seek(0)
    ext = Path(file.name).suffix.lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp_file:
        tmp_file.write(file.read())
        tmp_path = tmp_file.name

    embedder = EmbeddingModule()
    chunks, embeddings, metadatas = embedder.process_and_embed(
        tmp_path,
        chunk_size=500,
        overlap=100
    )

    db = VectorDB()
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    db.add_documents(chunks, embeddings, ids, metadatas)

    return embedder, db


def perform_rag_qna(embedder, db, query):
    """Perform retrieval + Gemini-polished Q&A."""
    query_emb = embedder.embed_query(query)
    results = db.query(query_emb, n_results=5)

    if not results or not results.get("documents"):
        return "No relevant information found in the document."

    docs = results["documents"][0]
    context_text = "\n".join(docs)

    prompt = f"""
You are a knowledgeable AI assistant. Use only the provided context to answer accurately.

Context:
{context_text}

Question:
{query}

If the context does not contain the answer, say "The document does not contain specific information about that."

Answer:
"""
    polished_answer = rewrite_text_with_gemini(prompt)
    return polished_answer


# ===================== Streamlit UI =====================

st.set_page_config(
    page_title="AI Audiobook & RAG Studio",
    page_icon="🎧",
    layout="wide",
)

# --- Custom Dark UI ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #fafafa; font-family: 'Poppins', sans-serif; }
    .stButton>button { background: linear-gradient(90deg, #3b82f6, #9333ea); color: white; border: none; border-radius: 10px; padding: 0.6rem 1.2rem; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.05); background: linear-gradient(90deg, #9333ea, #3b82f6); }
    .stFileUploader label { background-color: #1e1e1e; color: #fafafa; border: 2px dashed #3b82f6; border-radius: 10px; padding: 1rem; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.sidebar.title("⚙️ System Status")
st.sidebar.success("✅ Ready for Processing")
st.sidebar.info("Upload a document to generate audiobook and ask questions")

st.markdown("<h1 style='text-align:center; color:#60a5fa;'>🎧 AI Audiobook & RAG Studio</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray;'>Convert documents into audiobooks and interact with them using AI</p>", unsafe_allow_html=True)
st.divider()


# ===================== File Upload & Processing =====================

uploaded_file = st.file_uploader(
    "📂 Upload a PDF, DOCX, TXT, or Image file",
    type=["pdf", "docx", "txt", "jpg", "jpeg", "png"]
)

if uploaded_file:
    file_ext = Path(uploaded_file.name).suffix.lower()  # get the file extension

    with st.spinner("⏳ Processing your document..."):
        rewritten_text, audio_file = asyncio.get_event_loop().run_until_complete(
            process_pipeline(uploaded_file)
        )

    if rewritten_text is None:
        st.error(audio_file)
    else:
        st.success("✅ Audiobook Generated Successfully!")
        st.markdown("### 📘 Rewritten Text (Preview)")
        st.text_area("", rewritten_text[:1500], height=300)

        st.markdown("### 🔊 Listen to the Audiobook")
        st.audio(audio_file, format="audio/mp3")

        st.divider()
        st.markdown("## 💬 Ask Questions about the Document")

        embedder, db = setup_rag(uploaded_file)
        question = st.text_input("💭 Enter your question below:")

        if question:
            with st.spinner("🧠 Retrieving and generating answer..."):
                answer = perform_rag_qna(embedder, db, question)

            st.markdown("### 🧾 Gemini-Polished Answer")
            st.write(answer)

        # === Dynamic Citation (Includes Uploaded File Name) ===
        st.divider()
        st.markdown("## 📚 Citation / Reference")

        citation_dict = {
            ".txt": "extract_txt – Custom TXT extraction module",
            ".docx": "extract_docx – Custom DOCX extraction module",
            ".pdf": "extract_pdf – Custom PDF extraction module",
            ".jpg": "extract_image – Custom image extraction module",
            ".jpeg": "extract_image – Custom image extraction module",
            ".png": "extract_image – Custom image extraction module"
        }

        citation_text = citation_dict.get(file_ext, "Unknown file type module")
        file_name = uploaded_file.name

        st.info(f"📄 **File Name:** {file_name}\n\n🔖 **Citation:** {citation_text}")

else:
    st.info("📄 Please upload a document to begin.")
