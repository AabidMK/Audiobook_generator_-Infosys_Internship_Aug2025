from TTS.api import TTS
import os
import soundfile as sf
import numpy as np

# ----------- Helper function -----------
def split_text_by_limit(text, limit=250):
    """Split text into sub-chunks that are <= limit characters, without breaking words if possible."""
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
#Function for audio extraction
def generate_audio(text,output_file="final_audiobook.wav"):
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
    # Specification of speaker
    speaker_choice="Sofia Hellen"

    # ----------- 5. Split into paragraphs -----------
    paragraphs = text.split("\n\n")   # main chunks
    os.makedirs("xtts_output", exist_ok=True)
    all_audio = []
    samplerate = 22050  # default sample rate

    # ----------- 6. Generate audio -----------
    for i, para in enumerate(paragraphs):
        if para.strip():
        # Further split into <=250 char sub-chunks
            sub_chunks = split_text_by_limit(para, limit=250)
            for j, sub_chunk in enumerate(sub_chunks):
                output_path = f"xtts_output/chunk_{i}_{j}.wav"
                print("Generating chunk {i+1}.{j+1}/{len(paragraphs)}")
                audio=tts.tts(text=sub_chunk, speaker=speaker_choice,language="en")
                sf.write(output_path,audio,samplerate)
                all_audio.append(audio)
               


# ----------- 7. Merge all into one file -----------
    if all_audio:
        merged_audio = np.concatenate(all_audio)
        sf.write(output_file, merged_audio, samplerate)
        print(f"✅ Final audiobook saved as {output_file}")
    else:
        print("⚠ No audio generated")
