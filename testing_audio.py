import os
import sys
import re
import logging
import pdfplumber
import docx
import pytesseract
from pydub import AudioSegment
from tqdm import tqdm
import torch
from TTS.api import TTS
import google.generativeai as genai   

os.environ["PHONEMIZER_ESPEAK_PATH"] = "C:/Program Files (x86)/eSpeak/command_line/espeak.exe"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("audiobook_pipeline.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)


ffmpeg_path = r"C:\Users\kjish\ffmpeg\bin"
os.environ["PATH"] += os.pathsep + ffmpeg_path

# --- Tesseract OCR setup ---
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def ocr_image(image):
    try:
        return pytesseract.image_to_string(image)
    except Exception as e:
        logging.error(f"OCR Error: {e}", exc_info=True)
        return ""


def extract_text_from_pdf(pdf_path):
    all_text = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                text = page.extract_text()
                if text and text.strip():
                    all_text.append(text)
                else:
                    logging.info(f"Page {page_num} empty, using OCR fallback")
                    pil_img = page.to_image(resolution=300).original
                    ocr_text = ocr_image(pil_img)
                    if ocr_text.strip():
                        all_text.append(ocr_text)
    except Exception as e:
        logging.error(f"PDF Extraction Error: {e}", exc_info=True)
    return "\n\n".join(all_text)


def extract_text_from_docx(docx_path):
    try:
        doc = docx.Document(docx_path)
        return "\n\n".join(p.text.strip() for p in doc.paragraphs if p.text.strip())
    except Exception as e:
        logging.error(f"DOCX Extraction Error: {e}", exc_info=True)
        return ""

def clean_text_for_tts(text):
    # Normalize unicode
    text = text.encode("ascii", "ignore").decode()   # remove accents & ligatures
    text = text.replace("•", "-").replace("·", "-")
    text = text.replace("…", "...").replace("–", "-").replace("—", "-")
    text = text.replace("“", '"').replace("”", '"').replace("’", "'")
    text = text.replace("/", " or ")
    text = text.replace("&", " and ").replace("+", " plus ")
    text = text.replace("%", " percent ").replace("#", " number ")
    # Only safe characters
    text = re.sub(r"[^A-Za-z0-9\s\.,;:!\?'\-\(\)\"]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def save_as_markdown(content, path):
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        logging.info(f"Markdown saved at {path}")
    except Exception as e:
        logging.error(f"Error saving Markdown: {e}", exc_info=True)


def chunk_text(text, max_length=2000):
    paragraphs = text.split("\n\n")
    chunks, current = [], ""
    for p in paragraphs:
        if len(current) + len(p) < max_length:
            current += p + "\n\n"
        else:
            if current.strip():
                chunks.append(current.strip())
            current = p + "\n\n"
    if current.strip():
        chunks.append(current.strip())
    logging.info(f"Total text chunks: {len(chunks)}")
    return chunks


def local_enrichment(text):
    text = clean_text_for_tts(text)
    return f"[Audiobook narration]\n{text}"


def gemini_enrichment(text, api_key):
    """Use Gemini API to rewrite text for audiobook narration."""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = (
            "Rewrite the following text in an engaging, natural audiobook narration style. "
            "Make it sound clear, listener-friendly, and smooth for text-to-speech.\n\n"
            f"{text}"
        )
        response = model.generate_content(prompt)
        return clean_text_for_tts(response.text)
    except Exception as e:
        logging.error(f"Gemini Enrichment Error: {e}", exc_info=True)
        return local_enrichment(text)


def enrich_for_audiobook(text, api_key=None):
    chunks = chunk_text(text)
    enriched_chunks = []
    for idx, c in enumerate(tqdm(chunks, desc="Enriching text", unit="chunk")):
        if api_key:
            enriched_chunks.append(gemini_enrichment(c, api_key))
        else:
            enriched_chunks.append(local_enrichment(c))
    return "\n\n".join(enriched_chunks)


def generate_audiobook(text, basename, chunk_size=300):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS("tts_models/en/ljspeech/tacotron2-DDC")
    logging.info(f"Using Coqui TTS on {device}")

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
    chunk_dir = os.path.join(os.path.dirname(basename), "chunks")
    os.makedirs(chunk_dir, exist_ok=True)

    final_audio = AudioSegment.silent(duration=500)
    for idx, chunk in enumerate(tqdm(chunks, desc="Synthesizing", unit="chunk")):
        chunk = clean_text_for_tts(chunk)
        if not chunk.strip():
            continue
        chunk_path = os.path.join(chunk_dir, f"chunk_{idx:04d}.wav")
        if os.path.exists(chunk_path):
            final_audio += AudioSegment.from_wav(chunk_path) + AudioSegment.silent(duration=300)
            continue
        try:
            tts.tts_to_file(text=chunk, file_path=chunk_path)
            final_audio += AudioSegment.from_wav(chunk_path) + AudioSegment.silent(duration=300)
        except Exception as e:
            logging.error(f"TTS Error in chunk {idx}: {e}", exc_info=True)

    wav_path = basename + ".wav"
    final_audio.export(wav_path, format="wav")
    mp3_path = basename + ".mp3"
    final_audio.export(mp3_path, format="mp3", bitrate="192k")
    logging.info(f"Audiobook generated: {mp3_path}")

    import shutil
    try:
        shutil.rmtree(chunk_dir)
        logging.info("Cleaned up temporary audio chunk files.")
    except Exception as e:
        logging.warning(f"Cleanup failed: {e}")


if __name__ == "__main__":
    path = "C:/Users/kjish/Downloads/AI AudioBook Generator.pdf"
    if not os.path.exists(path):
        logging.error("File not found!")
        sys.exit(1)

    
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", None)

    # Extract text
    text = extract_text_from_pdf(path) if path.lower().endswith(".pdf") else extract_text_from_docx(path)
    if not text.strip():
        logging.error("No text extracted from file. Aborting.")
        sys.exit(1)

    # Enrich text with Gemini (if key is provided), else local
    enriched_text = enrich_for_audiobook(text, api_key=GEMINI_API_KEY)

    # Save enriched text
    md_path = os.path.join(os.path.dirname(path), "audiobook_ready.md")
    save_as_markdown(enriched_text, md_path)

    # Generate audio
    basename = os.path.join(os.path.dirname(path), "audiobook")
    generate_audiobook(enriched_text, basename)
    logging.info("Audiobook pipeline completed successfully.")
