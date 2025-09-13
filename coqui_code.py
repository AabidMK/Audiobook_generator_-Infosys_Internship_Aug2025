from TTS.api import TTS
import os
import soundfile as sf
import numpy as np

# ----------- Helper function -----------
def split_text_by_limit(text, limit=250):
    """Split text into sub-chunks that are <= limit characters, 
    without breaking words if possible."""
    words = text.split()
    chunks, current = [], ""

    for word in words:
        if len(current) + len(word) + 1 <= limit:
            current += (" " if current else "") + word
        else:
            chunks.append(current)
            current = word
    if current:
        chunks.append(current)
    return chunks

# ----------- 1. Load XTTS v2 -----------
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)

# ----------- 2. Show available speakers -----------
print("Available speakers:")
for spk in tts.speakers:
    print("-", spk)

# ----------- 3. Let user choose speaker -----------
speaker_choice = input("\n👉 Enter the speaker you want to use: ").strip()

# ----------- 4. Read input text -----------
with open("coqui_input.txt", "r", encoding="utf-8") as f:
    text = f.read()

# ----------- 5. Split into paragraphs -----------
paragraphs = text.split("\n\n")   # main chunks
os.makedirs("xtts_output", exist_ok=True)

# To hold audio arrays for merging
all_audio = []
samplerate = 22050  # default sample rate

# ----------- 6. Generate audio -----------
for i, para in enumerate(paragraphs):
    if para.strip():
        # Further split into <=250 char sub-chunks
        sub_chunks = split_text_by_limit(para, limit=250)
        for j, sub_chunk in enumerate(sub_chunks):
            out_path = f"xtts_output/chunk_{i}_{j}.wav"
            print(f"🎙 Generating chunk {i+1}.{j+1}/{len(paragraphs)} with speaker {speaker_choice}...")

            # Generate audio with chosen speaker + language
            audio = tts.tts(
                text=sub_chunk,
                speaker=speaker_choice,
                language="en"
            )

            # Save each file
            sf.write(out_path, audio, samplerate)

            # Keep audio for merging
            all_audio.append(audio)

# ----------- 7. Merge all into one file -----------
if all_audio:
    merged_audio = np.concatenate(all_audio)
    sf.write("coqui_output.wav", merged_audio, samplerate)
    print(f"✅ Final audiobook saved as coqui_output.wav (speaker: {speaker_choice})")
else:
    print("⚠ No text chunks were processed.")