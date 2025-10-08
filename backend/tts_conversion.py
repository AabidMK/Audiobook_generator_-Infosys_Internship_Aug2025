import os
from gtts import gTTS
import gtts.lang
from llm_enrichment import enrich_text_with_llm

def convert_text_to_audio(text, output_filename="audiobook.mp3", lang_code='en'):
    """
    Converts the given text to an MP3 audio file in the chosen language.
    """
    try:
        # Check if the provided language is supported by gTTS
        if lang_code not in gtts.lang.tts_langs():
            print(f"Language not supported: {lang_code}")
            return None
        
        # Rewrite the text in the selected language using the LLM
        enriched_text = enrich_text_with_llm(text, lang_code=lang_code)

        # Use gTTS with the rewritten text and the specified language
        tts = gTTS(text=enriched_text, lang=lang_code)
        tts.save(output_filename)
        return output_filename
    except Exception as e:
        print(f"An error occurred during TTS conversion: {e}")
        return None