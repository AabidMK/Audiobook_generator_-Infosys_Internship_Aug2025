# tts.py
import pyttsx3
import os
import time

def text_to_audio_pyttsx3(text, output_file="output.wav"):
    """Convert text to audio using pyttsx3 (offline)"""
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Words per minute
    engine.setProperty('volume', 1.0)

    engine.save_to_file(text, output_file)
    engine.runAndWait()

    # Wait until file is fully written
    while not os.path.exists(output_file) or os.path.getsize(output_file) == 0:
        time.sleep(0.1)

    return output_file




