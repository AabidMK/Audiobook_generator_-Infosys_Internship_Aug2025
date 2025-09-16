import streamlit as st
import os
from text_extractor import extract_text
from llm_enrichment import enrich_text_with_llm
from tts_conversion import convert_text_to_audio

# --- Page Setup ---
st.title("AI AudioBook Generator")
st.write("Upload a document (PDF, DOCX, TXT) to automatically convert it into an engaging audiobook.")

# --- Define Country and Language Options ---
country_languages = {
    "United States": {"en-US": "English (US)"},
    "United Kingdom": {"en-GB": "English (UK)"},
    "India": {"hi": "Hindi", "en-IN": "English (India)"}, # Changed hi-IN to hi
    "France": {"fr-FR": "French (France)"},
    "Germany": {"de-DE": "German (Germany)"},
    "Spain": {"es-ES": "Spanish (Spain)"},
    "Japan": {"ja-JP": "Japanese (Japan)"},
    "China": {"zh-CN": "Chinese (Mandarin)"}
}

# --- UI Widgets ---
uploaded_file = st.file_uploader("Choose a document", type=['pdf', 'docx', 'txt'])

selected_country = st.selectbox("Select a Country", list(country_languages.keys()))

languages = country_languages[selected_country]
selected_lang_code = st.selectbox("Select a Language", list(languages.keys()), format_func=lambda x: languages[x])

# --- Main Logic ---
if uploaded_file is not None:
    file_extension = uploaded_file.name.split('.')[-1].lower()
    temp_dir = "temp_files"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
        
    file_path = os.path.join(temp_dir, uploaded_file.name)
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.info("Processing your document... Please wait.")

    try:
        with st.spinner('Extracting text...'):
            raw_text = extract_text(uploaded_file, file_extension)

        if not raw_text or raw_text.strip() == "":
            st.error("Could not extract text from the document. Please try a different file.")
        else:
            st.success("Text extracted successfully!")

            with st.spinner('Enhancing text for narration...'):
                enriched_text = enrich_text_with_llm(raw_text)

            st.success("Text enhanced successfully!")
            st.expander("View Enriched Text").write(enriched_text)

            with st.spinner('Generating audiobook...'):
                audio_file_path = convert_text_to_audio(enriched_text, lang_code=selected_lang_code)
            
            # --- Check if audio_file_path is not None before proceeding ---
            if audio_file_path:
                st.success("Audiobook generated successfully!")
                st.audio(audio_file_path, format='audio/mp3')
                
                with open(audio_file_path, "rb") as file:
                    st.download_button(
                        label="Download Audiobook",
                        data=file,
                        file_name="audiobook.mp3",
                        mime="audio/mp3"
                    )
            else:
                st.error("Audio generation failed. Please check the logs.")

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
    finally:
        # --- Ensure files are deleted before removing the directory ---
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        if 'audio_file_path' in locals() and audio_file_path and os.path.exists(audio_file_path):
            os.remove(audio_file_path)
        if os.path.exists(temp_dir) and not os.listdir(temp_dir):
            os.rmdir(temp_dir)