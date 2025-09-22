import os
import logging
from pathlib import Path
from pydub import AudioSegment
from tqdm import tqdm
from TTS.api import TTS
import shutil

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("audio_generation.log", encoding="utf-8"),
              logging.StreamHandler()]
)

def generate_audiobook(text: str, output_basename: str, chunk_size: int = 700):
    """
    Generate audiobook from text using Coqui TTS.
    Saves audio in Output folder with .wav and .mp3 formats.
    """
    output_path = Path(output_basename)
    chunk_dir = output_path.parent / "chunks"
    chunk_dir.mkdir(parents=True, exist_ok=True)

    # Initialize Coqui TTS
    device = "cuda" if "cuda" in TTS.list_models()[0] else "cpu"  # fallback device detection
    tts = TTS("tts_models/en/ljspeech/tacotron2-DDC", progress_bar=True, gpu=(device=="cuda"))
    logging.info(f"Using Coqui TTS on device: {device}")

    # Split text into chunks
    paragraphs = text.split("\n\n")
    chunks, current = [], ""
    for p in paragraphs:
        if len(current) + len(p) < chunk_size:
            current += p + "\n\n"
        else:
            if current.strip():
                chunks.append(current.strip())
            current = p + "\n\n"
    if current.strip():
        chunks.append(current.strip())

    logging.info(f"Total audio chunks: {len(chunks)}")

    # Generate audio
    final_audio = AudioSegment.silent(duration=500)
    for idx, chunk in enumerate(tqdm(chunks, desc="Synthesizing", unit="chunk")):
        chunk_path = chunk_dir / f"chunk_{idx:04d}.wav"
        if chunk_path.exists():
            final_audio += AudioSegment.from_wav(chunk_path) + AudioSegment.silent(duration=300)
            continue
        try:
            tts.tts_to_file(text=chunk, file_path=str(chunk_path))
            final_audio += AudioSegment.from_wav(chunk_path) + AudioSegment.silent(duration=300)
        except Exception as e:
            logging.error(f"TTS Error in chunk {idx}: {e}", exc_info=True)

    # Export final audio
    final_audio.export(str(output_path) + ".wav", format="wav")
    final_audio.export(str(output_path) + ".mp3", format="mp3", bitrate="192k")
    logging.info(f"Audiobook generated: {output_path}.mp3")

    # Cleanup chunks
    try:
        shutil.rmtree(chunk_dir)
        logging.info("Cleaned up temporary audio chunk files.")
    except Exception as e:
        logging.warning(f"Cleanup failed: {e}")
