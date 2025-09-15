import streamlit as st
from text_extractor import TextExtractor
from llm_enrichment import enrich_text
from tts_generator import text_to_speech
from utils import load_config, create_output_dir, validate_file
import os

config = load_config()
create_output_dir(config['output_dir'])

st.title("📚 AI Audiobook Generator")

uploaded_files = st.file_uploader("Upload TXT, PDF, or DOCX files", type=['txt', 'pdf', 'docx'], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_path = os.path.join(config['output_dir'], uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        try:
            validate_file(file_path)
            st.success(f"Processing: {uploaded_file.name}")

            # Text extraction
            text = TextExtractor.extract_text(file_path)
            st.text_area("Extracted Text", text, height=200)

            # Text enrichment
            enriched_text = enrich_text(text)
            st.text_area("Enriched Text", enriched_text, height=200)

            # TTS conversion
            output_audio = os.path.join(config['output_dir'], uploaded_file.name + ".wav")
            text_to_speech(enriched_text, output_audio)
            st.audio(output_audio, format="audio/wav")

        except Exception as e:
            st.error(f"Error processing {uploaded_file.name}: {str(e)}")
