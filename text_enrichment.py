import re
import logging
from tqdm import tqdm

def clean_text_for_tts(text: str) -> str:
    """Clean text for TTS, remove unwanted symbols."""
    text = text.replace("\\", " ").replace("•", "-").replace("·", "-")
    text = re.sub(r"[^A-Za-z0-9\s\.,;:!\?'\-\(\)\"/]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def chunk_text(text: str, max_length: int = 2000) -> list[str]:
    """Split text into chunks for enrichment or TTS."""
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

def local_enrichment(text: str) -> str:
    """Basic enrichment for audiobook narration."""
    text = clean_text_for_tts(text)
    return f"[Audiobook narration]\n{text}"

def enrich_text(text: str) -> str:
    """Enrich text in chunks for audiobook."""
    chunks = chunk_text(text)
    enriched_chunks = []
    for c in tqdm(chunks, desc="Enriching text", unit="chunk"):
        enriched_chunks.append(local_enrichment(c))
    return "\n\n".join(enriched_chunks)

def save_markdown(content: str, path: str):
    """Save enriched text as Markdown."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        logging.info(f"Markdown saved at {path}")
    except Exception as e:
        logging.error(f"Error saving Markdown: {e}", exc_info=True)
