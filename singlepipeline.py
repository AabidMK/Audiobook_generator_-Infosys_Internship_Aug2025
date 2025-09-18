from TTS.api import TTS
import soundfile as sf
import numpy as np
import os

# -------- Helper: split text --------
def split_text_by_limit(text, limit=250):
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

# -------- 1. Load Coqui TTS model --------
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)

# Try fetching available speakers
try:
    available_speakers = list(tts.synthesizer.tts_model.speaker_manager.speakers.keys())
    print("✅ Available speakers:", available_speakers)
    DEFAULT_SPEAKER = available_speakers[0]  # first speaker
except Exception as e:
    print("⚠ Could not fetch speakers:", e)
    DEFAULT_SPEAKER = None

# -------- 2. Load rewritten text --------
with open("rewritten_output.md", "r", encoding="utf-8") as f:
    text = f.read()

paragraphs = text.split("\n\n")
os.makedirs("coqui_chunks", exist_ok=True)

all_audio = []
samplerate = 22050

# -------- 3. Generate audio chunks --------
for i, para in enumerate(paragraphs):
    if para.strip():
        sub_chunks = split_text_by_limit(para, limit=250)
        for j, chunk in enumerate(sub_chunks):
            out_path = f"coqui_chunks/chunk_{i}_{j}.wav"
            print(f"🎙 Generating chunk {i+1}.{j+1}...")

            if DEFAULT_SPEAKER:
                audio = tts.tts(text=chunk, speaker=DEFAULT_SPEAKER, language="en")
            else:
                audio = tts.tts(text=chunk, language="en")

            sf.write(out_path, audio, samplerate)
            all_audio.append(audio)

# -------- 4. Merge all audio --------
if all_audio:
    merged_audio = np.concatenate(all_audio)
    sf.write("coqui_audio.wav", merged_audio, samplerate)
    print(" Final audiobook saved as coqui_audio.wav")
else:
    print(" No audio generated.")