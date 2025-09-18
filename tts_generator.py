import os
import sys
import tempfile
import wave
import re
from TTS.api import TTS

MODEL_NAME = "tts_models/en/vctk/vits"   
USE_GPU = False                          
CHUNK_MAX_CHARS = 1500                   
OUT_WAV = "audiobook_voice.wav"          
DEFAULT_SPEAKER = "p230"                 

def read_markdown(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def clean_text_for_tts(text: str) -> str:
    """Remove non-speech junk like PDF artifacts or long numbers."""
    text = re.sub(r"<<.*?>>", " ", text, flags=re.DOTALL)
    text = re.sub(r"stream.*?endstream", " ", text, flags=re.DOTALL)
    text = re.sub(r"\b[0-9a-fA-F]{6,}\b", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def split_for_tts(text, max_chars=CHUNK_MAX_CHARS):
    """Split into safe character-based chunks (ignores missing paragraphs)."""
    text = text.strip()
    if not text:
        return []
    parts = []
    for i in range(0, len(text), max_chars):
        parts.append(text[i:i+max_chars])
    return parts

def synthesize_chunks_to_wav(chunks, model_name=MODEL_NAME, use_gpu=USE_GPU, out_wav=OUT_WAV):
    tts = TTS(model_name=model_name, progress_bar=False, gpu=use_gpu)
    tmp_files = []

    for i, chunk in enumerate(chunks, start=1):
        print(f"Synthesizing chunk {i}/{len(chunks)} (length {len(chunk)} chars)...")
        tmp = tempfile.NamedTemporaryFile(suffix=f"_part{i}.wav", delete=False)
        tmp_name = tmp.name
        tmp.close()
        tts.tts_to_file(text=chunk, file_path=tmp_name, speaker=DEFAULT_SPEAKER)
        tmp_files.append(tmp_name)

    if not tmp_files:
        raise RuntimeError("No chunks synthesized.")

    print("Combining chunks into final WAV...")
    params = None
    frames_list = []
    for f in tmp_files:
        with wave.open(f, "rb") as r:
            if params is None:
                params = r.getparams()
            else:
                if r.getparams()[:3] != params[:3]:
                    raise RuntimeError(f"WAV parameters mismatch in {f}")
            frames_list.append(r.readframes(r.getnframes()))

    with wave.open(out_wav, "wb") as w:
        w.setparams(params)
        for frames in frames_list:
            w.writeframes(frames)

    for f in tmp_files:
        try:
            os.remove(f)
        except:
            pass

    print(f"Master WAV saved to: {out_wav}")
    return out_wav

def main(input_md):
    if not os.path.exists(input_md):
        print("Input file not found:", input_md)
        return
    text = read_markdown(input_md)
    if not text.strip():
        print("No text found in the input file.")
        return

    text = clean_text_for_tts(text)
    chunks = split_for_tts(text)
    print(f"Text split into {len(chunks)} chunk(s).")

    synthesize_chunks_to_wav(chunks, out_wav=OUT_WAV)
    print("Done.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tts_generator.py narration_output.md")
        sys.exit(1)
    main(sys.argv[1])