import os
import asyncio
import edge_tts
import soundfile as sf
import numpy as np
import re

# ----------- Helper function -----------
def split_text_by_limit(text, limit=250):
    """Split text into sub-chunks that are <= limit characters, without breaking words if possible."""
    words = text.split()
    chunks, current = [], ""

    for word in words:
        if len(word) > limit:
            while len(word) > limit:
                chunks.append(word[:limit])
                word = word[limit:]
        if len(current) + len(word) + (1 if current else 0) <= limit:
            current += (" " if current else "") + word
        else:
            chunks.append(current)
            current = word
    if current:
        chunks.append(current)
    return chunks

def clean_text(text):
    """Remove special characters and emojis from the text."""
    text = re.sub(r"[^\x00-\x7F]+", " ", text)  # Remove non-ASCII characters
    text = re.sub(r"[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251]", " ", text)  # Remove emojis
    return text

# ----------- Async Edge-TTS call with retry logic -----------
async def synthesize_chunk(text, voice="en-US-LolaMultilingualNeural", rate="+0%", pitch="+0Hz", retries=3):
    """Generate audio for a chunk using Edge TTS and return PCM samples as numpy array."""
    for attempt in range(retries):
        try:
            tts = edge_tts.Communicate(text=text, voice=voice, rate=rate, pitch=pitch)
            wav_file = "temp_chunk.wav"
            await tts.save(wav_file)
            audio, sr = sf.read(wav_file, dtype="float32")
            os.remove(wav_file)
            return audio, sr
        except edge_tts.exceptions.NoAudioReceived:
            print(f"⚠ No audio received, retry {attempt + 1}/{retries}...")
            await asyncio.sleep(1)
    raise RuntimeError("Failed to synthesize chunk after retries.")

# ----------- Main Audio Generation from File -----------
def generate_audio(text, output_file="audiobook_output.wav"):
    """
    Generate audiobook from a text file using Edge TTS with chunking.
    """

    text = "\n".join([line.strip() for line in text.splitlines() if line.strip()])
    paragraphs = [p for p in text.split("\n\n") if p]

    os.makedirs("edge_tts_output", exist_ok=True)

    all_audio = []
    sample_rate = None
    voice = "en-US-LolaMultilingualNeural"  # Updated voice for Edge TTS 7.2.3

    print(f"📘 Total paragraphs: {len(paragraphs)}")

    for i, para in enumerate(paragraphs):
        sub_chunks = split_text_by_limit(para, limit=250)
        print(f"📝 Paragraph {i + 1}/{len(paragraphs)} → {len(sub_chunks)} sub-chunks")

        for j, sub_chunk in enumerate(sub_chunks):
            sub_chunk = clean_text(sub_chunk)
            if not sub_chunk.strip():
                continue

            print(f"  🎙 Synthesizing sub-chunk {j + 1}/{len(sub_chunks)}...")
            audio, sr = asyncio.run(synthesize_chunk(sub_chunk, voice=voice))
            if sample_rate is None:
                sample_rate = sr
            all_audio.append(audio)
            asyncio.run(asyncio.sleep(0.2))

    # Merge all audio into one file
    if all_audio:
        merged_audio = np.concatenate(all_audio)
        sf.write(output_file, merged_audio, sample_rate)
        print(f"✅ Final audiobook saved as {output_file}")
    else:
        print("⚠ No audio generated.")