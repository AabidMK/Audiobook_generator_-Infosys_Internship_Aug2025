import streamlit as st
import os
import tempfile
from main import run_pipeline
from tts_generator import OUT_WAV
from rag_query import answer_question

# ---------- Streamlit UI ----------
st.set_page_config(page_title="AI Audiobook Generator", layout="wide")
st.title("🎧 AI Audiobook Generator with Q&A")

# ---------------------------
# Session State Initialization
# ---------------------------
if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False
if "processing_done" not in st.session_state:
    st.session_state.processing_done = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------------------
# File Upload Section
# ---------------------------
uploaded_file = st.file_uploader(
    "Upload your document (PDF, DOCX, TXT, Image)",
    type=["pdf", "docx", "txt", "png", "jpg", "jpeg"]
)

if uploaded_file:
    temp_path = os.path.join(tempfile.gettempdir(), uploaded_file.name)
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.session_state.file_uploaded = True
    st.success(f"File {uploaded_file.name} uploaded successfully!")

# ---------------------------
# Generate Audiobook
# ---------------------------
if st.session_state.file_uploaded and st.button("Generate Audiobook"):
    if not st.session_state.processing_done:
        with st.spinner("Processing your file... This may take a few minutes."):
            try:
                md_file, audio_file = run_pipeline(temp_path)
                st.session_state.processing_done = True
                st.success("Audiobook generated successfully!")
            except Exception as e:
                st.error(f"Error during generation: {e}")

# ---------------------------
# Play & Download Audio
# ---------------------------
if st.session_state.processing_done and os.path.exists(OUT_WAV):
    st.subheader("Listen to Your Audiobook")
    st.audio(OUT_WAV, format="audio/wav")

    with open(OUT_WAV, "rb") as f:
        st.download_button(
            label="Download Audiobook",
            data=f,
            file_name="audiobook.wav",
            mime="audio/wav"
        )

# ---------------------------
# Interactive Q&A Section
# ---------------------------
st.subheader("Ask Questions About Your Document")

user_question = st.text_input("Enter your question:")

if st.button("Get Answer") and user_question:
    if st.session_state.processing_done:
        with st.spinner("Fetching answer..."):
            try:
                answer, citations = answer_question(user_question)
                st.session_state.chat_history.append({"question": user_question, "answer": answer, "citations": citations})
            except Exception as e:
                st.error(f"Error during Q&A: {e}")
    else:
        st.warning("Please generate the audiobook first before asking questions.")

# ---------------------------
# Display Chat History
# ---------------------------
if st.session_state.chat_history:
    st.subheader("Q&A Chat History")
    for entry in st.session_state.chat_history[::-1]:
        st.markdown(f"**Q:** {entry['question']}")
        st.markdown(f"**A:** {entry['answer']}")
        st.markdown("**Citations:**")
        for c in entry["citations"]:
            st.markdown(f"- {c['content_preview']} ... (distance: {c['distance']:.4f})")
        st.markdown("---")

# ---------------------------
# Optional: Clean up temporary files
# ---------------------------
if st.button("Clear Temporary Files"):
    try:
        if st.session_state.file_uploaded and os.path.exists(temp_path):
            os.remove(temp_path)
        if os.path.exists(OUT_WAV):
            os.remove(OUT_WAV)
        st.session_state.processing_done = False
        st.session_state.file_uploaded = False
        st.session_state.chat_history = []
        st.success("Temporary files cleared!")
    except Exception as e:
        st.error(f"Error clearing files: {e}")