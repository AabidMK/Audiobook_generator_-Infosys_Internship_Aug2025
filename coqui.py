# -------- Imports --------
from TTS.api import TTS

# -------- Step 1: Load Markdown File --------
def load_markdown(file_path):
    """
    Reads a markdown file and returns plain text
    """
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    
    # Optional: remove simple markdown formatting (#, *, etc.)
    import re
    text = re.sub(r'#', '', text)          # remove headers
    text = re.sub(r'\*', '', text)         # remove asterisks
    text = re.sub(r'\n{2,}', '\n', text)  # remove extra blank lines
    return text

# -------- Step 2: Generate Audio using Coqui TTS --------
def generate_audio(text, output_file="narration.wav"):
    """
    Generates audio from text using Coqui TTS
    """
    # Load a pre-trained TTS model (English VITS)
    tts = TTS(model_name="tts_models/en/ljspeech/vits")  

    # Generate audio file
    tts.tts_to_file(text=text, file_path=output_file)
    print(f"✅ Audio saved as {output_file}")

# -------- Main Program --------
if __name__ == "__main__":
    markdown_file = "rewritten_output.md"  # Replace with your Markdown file
    text = load_markdown(markdown_file)
    
    print("📄 Loaded Markdown content:")
    print(text[:500], "...")  # Print first 500 chars for preview

    generate_audio(text, "narration.wav")


