# import os
# import re
# from gtts import gTTS
# from pydub import AudioSegment
# from pydub.utils import which

# AudioSegment.converter = r"C:\Users\Hardik Rokde\Downloads\ffmpeg-8.0-essentials_build\ffmpeg-8.0-essentials_build\bin\ffmpeg.exe"

# def preprocess_markdown(md_text: str) -> str:
#     # Remove code blocks (``` ... ```)
#     md_text = re.sub(r"```.*?```", "", md_text, flags=re.DOTALL)

#     # Headings → add pauses (replace # Heading with "Heading. ...")
#     md_text = re.sub(r"#+\s*(.*)", r"\1. ", md_text)

#     # Lists → make them sound natural
#     md_text = re.sub(r"^\s*[-*]\s+", "- ", md_text, flags=re.MULTILINE)
#     md_text = md_text.replace("- ", "• ")

#     # Remove extra markdown symbols
#     md_text = re.sub(r"[>*_`#]", "", md_text)

#     # Collapse multiple spaces
#     md_text = re.sub(r"\s+", " ", md_text)

#     return md_text.strip()

# def split_text(text: str, max_chars: int = 4500):
#     """Split text into chunks under the character limit."""
#     parts = []
#     while len(text) > max_chars:
#         # Find last sentence end before max_chars
#         split_at = text.rfind('.', 0, max_chars)
#         if split_at == -1:
#             split_at = max_chars
#         parts.append(text[:split_at+1].strip())
#         text = text[split_at+1:].strip()
#     if text:
#         parts.append(text)
#     return parts

# # --- MAIN SCRIPT ---
# with open("enriched_text.md", "r", encoding="utf-8") as f:
#     raw_text = f.read()

# clean_text = preprocess_markdown(raw_text)

# # Split into chunks for gTTS
# chunks = split_text(clean_text)

# audio_files = []
# for i, chunk in enumerate(chunks):
#     tts = gTTS(text=chunk, lang="en", slow=False)
#     filename = f"chunk_{i}.mp3"
#     tts.save(filename)
#     audio_files.append(filename)
#     print(f"✅ Saved {filename} ({len(chunk)} chars)")

# # Merge chunks into one MP3
# final_audio = AudioSegment.empty()
# for f in audio_files:
#     final_audio += AudioSegment.from_mp3(f)

# final_audio.export("output_expressive.mp3", format="mp3")

# print("🎶 Final expressive audio saved as output_expressive.mp3")



# from sarvamai import SarvamAI

# client = SarvamAI(
#     api_subscription_key="sk_vf4ahup5_2al499Fw3mxnX1iTN02C45Y9",
# )

# response = client.text_to_speech.convert(
#     text="",
#     target_language_code="en-IN",
#     speaker="manisha",
#     pitch=0.1,
#     pace=1,
#     loudness=1.5,
#     speech_sample_rate=22050,
#     enable_preprocessing=True,
#     model="bulbul:v2"
# )

# print(response)


import os
import re
import base64
from sarvamai import SarvamAI
from pydub import AudioSegment

AudioSegment.converter = r"C:\\Users\\Hardik Rokde\\Downloads\\ffmpeg-8.0-essentials_build\\ffmpeg-8.0-essentials_build\\bin\\ffmpeg.exe"  # update path

def preprocess_markdown(md_text: str) -> str:
    md_text = re.sub(r"```.*?```", "", md_text, flags=re.DOTALL)
    md_text = re.sub(r"#+\s*(.*)", r"\1. ", md_text)
    md_text = re.sub(r"^\s*[-*]\s+", "- ", md_text, flags=re.MULTILINE)
    md_text = md_text.replace("- ", "• ")
    md_text = re.sub(r"[>*_`#]", "", md_text)
    md_text = re.sub(r"\s+", " ", md_text)
    return md_text.strip()

def split_text(text: str, max_chars: int = 2400):
    parts = []
    while len(text) > max_chars:
        split_at = text.rfind('.', 0, max_chars)
        if split_at == -1:
            split_at = max_chars
        parts.append(text[:split_at+1].strip())
        text = text[split_at+1:].strip()
    if text:
        parts.append(text)
    return parts

# --- Main Script ---
with open("enriched_text.md", "r", encoding="utf-8") as f:
    raw_text = f.read()

clean_text = preprocess_markdown(raw_text)
chunks = split_text(clean_text)

client = SarvamAI(api_subscription_key="sk_vf4ahup5_2al499Fw3mxnX1iTN02C45Y9")

audio_files = []
for i, chunk in enumerate(chunks):
    response = client.text_to_speech.convert(
        text=chunk,
        target_language_code="en-IN",
        speaker="manisha",
        pitch=0,
        pace=1,
        loudness=1.5,
        speech_sample_rate=22050,
        enable_preprocessing=True,
        model="bulbul:v2"
    )

    # Access the base64 audio from the 'audios' list
    base64_audio = response.audios[0]  # assume one chunk → one audio
    audio_bytes = base64.b64decode(base64_audio)

    filename = f"chunk_{i}.wav"
    with open(filename, "wb") as f_out:
        f_out.write(audio_bytes)
    audio_files.append(filename)
    print(f"✅ Saved {filename} ({len(chunk)} chars)")

# Merge the chunks
final_audio = AudioSegment.empty()
for af in audio_files:
    final_audio += AudioSegment.from_file(af, format="wav")

final_audio.export("output_sarvam.mp3", format="mp3")
print("🎉 Final audiobook: output_sarvam.mp3")

