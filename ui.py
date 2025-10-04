import streamlit as st
from PyPDF2 import PdfReader
import docx
from retrieval import chunk_text, retrieve_answer, model
import pyttsx3

st.set_page_config(page_title="Audiobook Generator", layout="wide")
st.title("📖 AudioBook Generator")

# -------------------------
# Text extraction
# -------------------------
def extract_text(file):
    file_type = file.name.split('.')[-1].lower()
    text = ""
    if file_type == "pdf":
        reader = PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    elif file_type in ["docx", "doc"]:
        doc_file = docx.Document(file)
        for para in doc_file.paragraphs:
            text += para.text + "\n"
    elif file_type == "txt":
        text = file.read().decode("utf-8", errors="ignore")
    else:
        st.error("❌ Unsupported file type!")
        return None
    return text.strip()

# -------------------------
# Audio conversion
# -------------------------
def text_to_audio_pyttsx3(text, filename="output.wav"):
    engine = pyttsx3.init()
    engine.save_to_file(text, filename)
    engine.runAndWait()
    return filename

# -------------------------
# Main UI
# -------------------------
uploaded_file = st.file_uploader("📂 Upload your file (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

if uploaded_file is not None:
    raw_text = extract_text(uploaded_file)
    if not raw_text:
        st.stop()

    st.success("✅ File loaded successfully!")

    # -------------------------
    # Audiobook generation
    # -------------------------
    st.subheader("🎧 Convert File into Audiobook")
    audio_file_path = text_to_audio_pyttsx3(raw_text, "output.wav")

    with open(audio_file_path, "rb") as f:
        audio_bytes = f.read()

    st.audio(audio_bytes, format="audio/wav")
    st.download_button("⬇️ Download Audio", audio_bytes, file_name="audiobook.wav", mime="audio/wav")

    # -------------------------
    # Query answering
    # -------------------------
    st.subheader("💡 Ask Queries about the File")
    user_query = st.text_input("Enter your question here:")

    if user_query:
        with st.spinner("🔍 Retrieving answer..."):
            chunks = chunk_text(raw_text, chunk_size=80, overlap=20)
            results = retrieve_answer(user_query, chunks, model)

        if results:
            st.subheader("📖 Answer (from file)")
            # Most relevant chunk as answer
            answer_text = results[0][1]
            st.write(answer_text)

            # Display citations
            st.markdown("### 📌 Citations (Top Matches)")
            for idx, chunk_text in results:
                st.markdown(f"**Chunk {idx+1}:** {chunk_text[:150]}...")
        else:
            st.error("❌ No relevant answer found in the file.")


