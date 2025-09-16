from gtts import gTTS
import os

def convert_text_to_audio(text, output_filename="audiobook.mp3", lang_code='en'):
    """
    Converts the given text to an MP3 audio file using gTTS with a specified language.
    
    Args:
        text (str): The text to be converted to speech.
        output_filename (str): The name of the output audio file.
        lang_code (str): The language code (e.g., 'en', 'fr').
        
    Returns:
        str: The path to the generated audio file, or None if an error occurs.
    """
    try:
        tts = gTTS(text=text, lang=lang_code)
        tts.save(output_filename)
        print(f"Audio file saved as {output_filename}")
        return output_filename

    except Exception as e:
        print(f"An error occurred during TTS conversion: {e}")
        return None