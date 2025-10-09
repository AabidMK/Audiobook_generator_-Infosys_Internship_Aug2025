import streamlit as st
import os
import tempfile
import pdfplumber
import docx
from TTS.api import TTS
from openai import OpenAI
import sys

# -----------------------------------
# ✅ Ensure local src folder is importable
# -----------------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(CURRENT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

from utils import load_config
from document_parser import DocumentParser
from text_chunker import TextChunker
from vector_store import VectorStore
from ollama_llm import LMStudioClient


# ---------- TEXT EXTRACTION ----------
def extract_text_from_file(uploaded_file):
    ext = uploaded_file.name.split(".")[-1].lower()
    text = ""

    if ext == "txt":
        text = uploaded_file.read().decode("utf-8")

    elif ext == "pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""

    elif ext == "docx":
        doc = docx.Document(uploaded_file)
        for para in doc.paragraphs:
            text += para.text + "\n"

    else:
        st.error("Unsupported file type. Please upload PDF, DOCX, or TXT.")
    return text.strip()


# ---------- LLM ENRICHMENT ----------
def enrich_text_with_llm(text, model="meta-llama/Meta-Llama-3-8B-Instruct"):
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
    system_prompt = (
        "You are an expert narrator. Rewrite the given text to make it engaging "
        "and suitable for audiobook narration while preserving meaning."
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content


# ---------- TTS GENERATION ----------
def generate_audio(enriched_text, config):
    tts_model = config["tts"]["model_name"]
    use_gpu = config["tts"]["use_gpu"]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_audio:
        tts = TTS(model_name=tts_model, progress_bar=False, gpu=use_gpu)
        tts.tts_to_file(text=enriched_text, file_path=tmp_audio.name)
        return tmp_audio.name


# ---------- MAIN STREAMLIT APP ----------
def main():
    st.set_page_config(page_title="Audiobook & RAG System", layout="wide")
    st.title("🎧 Audiobook Generator + 📚 RAG QA System")

    # ✅ Load config.yaml
    config_path = os.path.join(CURRENT_DIR, "config.yaml")
    if not os.path.exists(config_path):
        st.error(f"⚠️ config.yaml not found at {config_path}")
        st.stop()

    config = load_config(config_path)
    llm_client = LMStudioClient()
    vector_store = VectorStore()
    chunker = TextChunker()
    parser = DocumentParser()

    # Streamlit Tabs
    tabs = st.tabs(["🎧 Audiobook Generator", "💬 Document Q&A"])

    # ---- TAB 1: AUDIOBOOK GENERATOR ----
    with tabs[0]:
        st.header("Upload Documents to Generate Audiobook")

        uploaded_files = st.file_uploader(
            "📂 Upload one or more documents (PDF, DOCX, TXT)",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True
        )

        if uploaded_files:
            # Store uploaded files for reuse in Q&A tab
            if "uploaded_docs" not in st.session_state:
                st.session_state["uploaded_docs"] = {}

            for file in uploaded_files:
                st.write(f"📄 Processing: {file.name}")
                text = extract_text_from_file(file)
                if not text:
                    st.warning(f"No readable text in {file.name}")
                    continue

                # Save to session state for later RAG use
                st.session_state["uploaded_docs"][file.name] = text

                st.subheader("Step 1: LLM Narration Enrichment")
                with st.spinner("Rewriting text for narration..."):
                    enriched = enrich_text_with_llm(text)

                st.text_area("Enriched Text", enriched[:1500] + "...", height=200)

                st.subheader("Step 2: Text-to-Speech Conversion")
                with st.spinner("Generating audio..."):
                    audio_path = generate_audio(enriched, config)

                st.audio(audio_path)
                st.download_button(
                    label="⬇️ Download Audio",
                    data=open(audio_path, "rb").read(),
                    file_name=f"{os.path.splitext(file.name)[0]}.mp3",
                    mime="audio/mpeg"
                )
                st.success(f"Audiobook for {file.name} generated successfully!")

    # ---- TAB 2: RAG QA SYSTEM ----
    with tabs[1]:
        st.header("Ask Questions About Uploaded Documents")

        # ✅ Automatically use uploaded files from tab 1
        uploaded_docs = st.session_state.get("uploaded_docs", {})

        if not uploaded_docs:
            st.warning("⚠️ No documents uploaded yet. Please upload in the 'Audiobook Generator' tab first.")
            st.stop()
        else:
            st.success(f"✅ {len(uploaded_docs)} uploaded document(s) ready for Q&A.")

        # Build vector store only once
        if "vector_ready" not in st.session_state:
            with st.spinner("Building vector store from uploaded documents..."):
                docs = [{"text": text, "metadata": {"source_file": name}}
                        for name, text in uploaded_docs.items()]
                chunks = chunker.process_documents(docs)
                vector_store.add_chunks(chunks)
                st.session_state["vector_ready"] = True
                st.success("📚 Vector store ready! You can now ask questions.")

        question = st.text_input("💬 Enter your question:")
        if st.button("Get Answer") and question.strip():
            with st.spinner("🔎 Searching documents..."):
                results = vector_store.query(question)
                docs = results.get("documents", [[]])[0]
                context = "\n\n".join(docs)
                answer = llm_client.generate(context, question)
                st.markdown(f"**Answer:** {answer}")


if __name__ == "__main__":
    main()
