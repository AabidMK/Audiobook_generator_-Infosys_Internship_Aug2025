import os
import re
import argparse
from TTS.api import TTS
from pydub import AudioSegment

MODEL_NAME = "tts_models/en/vctk/vits"

# Pick 3 voices from VCTK dataset (p225=female, p227=female, p229=male)
VOICES = ["p225", "p227", "p229"]

def read_markdown_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def split_into_chunks(text, max_chars=500):
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks, current = [], ""
    for s in sentences:
        if len(current) + len(s) < max_chars:
            current += " " + s
        else:
            chunks.append(current.strip())
            current = s
    if current:
        chunks.append(current.strip())
    return chunks

def clean_tags(text):
    """Remove [voice=...] and [/voice] tags so they are not spoken aloud."""
    return re.sub(r'\[/?voice[^\]]*\]', '', text).strip()

def synthesize_chunks(chunks, output_path):
    tts = TTS(MODEL_NAME)

    # Print available speakers (if supported by this model)
    if hasattr(tts, "speakers") and tts.speakers:
        print("🔊 Available speakers:", tts.speakers)
    else:
        print("⚠️ This model doesn’t expose speaker list. Check docs for supported IDs.")

    audio_segments = []
    for i, chunk in enumerate(chunks):
        chunk = chunk.strip()
        if not chunk:
            continue  # skip empty chunks

        voice = VOICES[i % len(VOICES)]  # rotate voices
        print(f"🎙️ Generating chunk {i+1}/{len(chunks)} with voice {voice}...")

        # Clean text before TTS
        clean_text = clean_tags(chunk)

        temp_file = f"temp_{i}.wav"
        tts.tts_to_file(text=clean_text, speaker=voice, file_path=temp_file)
        audio_segments.append(AudioSegment.from_wav(temp_file))
        os.remove(temp_file)

    if audio_segments:
        final_audio = sum(audio_segments[1:], audio_segments[0])
        final_audio.export(output_path, format="wav")
        print(f"✅ Audiobook saved to {output_path}")
    else:
        print("⚠️ No audio generated (all chunks empty).")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input markdown file")
    parser.add_argument("-o", "--output", default="audiobook.wav", help="Output wav file")
    args = parser.parse_args()

    text = read_markdown_file(args.input)
    chunks = split_into_chunks(text)
    synthesize_chunks(chunks, args.output)