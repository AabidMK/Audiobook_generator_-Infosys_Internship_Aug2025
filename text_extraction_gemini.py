import os
import re
import time
import argparse
from typing import List

import fitz  # PyMuPDF
from docx import Document
from PIL import Image
import tkinter as tk
from tkinter import filedialog

# Correct Google SDK import
import google.generativeai as genai


# ---------------- Config (tuned for free tier) ----------------
GEMINI_MODEL = "gemini-1.5-flash"
DEFAULT_PAGES_PER_CHUNK = 24      # e.g., 600 pages -> ~25 requests
DEFAULT_TEMPERATURE = 0.4
MAX_REQUESTS_PER_RUN = 45         # safety below ~50/day free tier
PAUSE_BETWEEN_CALLS_SEC = 0.15

REWRITE_PROMPT = (
    "Rewrite the following text for clear, engaging narration suitable for an audiobook listener. "
    "Keep factual content, do not invent details, improve flow and coherence, use concise sentences, "
    "and keep or enhance Markdown headings and bullet lists where helpful. "
    "Normalize spacing and punctuation. Return only the rewritten text."
)


# ---------------- Helpers ----------------
def normalize_text(s: str) -> str:
    s = s.replace("\u00A0", " ")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\r?\n\s*", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def ensure_api_key():
    api_key = os.environ.get("GOOGLE_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY is not set. In PowerShell run:\n"
            '  setx GOOGLE_API_KEY "YOUR_API_KEY"\n'
            "Open a new terminal and run again."
        )
    genai.configure(api_key=api_key)


def save_header_once(path: str, header: str):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(header + "\n\n")


def append_md(path: str, content: str):
    with open(path, "a", encoding="utf-8") as f:
        f.write(content)
        if not content.endswith("\n"):
            f.write("\n")


# ---------------- Extractors ----------------
def extract_pdf_pages(pdf_path: str):
    """Yield (1-based page_number, text, total_pages) and print terminal progress."""
    doc = fitz.open(pdf_path)
    total = len(doc)
    for i in range(total):
        text = doc[i].get_text("text") or ""
        text = normalize_text(text)
        print(f"Extracting page {i+1}/{total} ...")
        yield (i + 1, text, total)
    doc.close()


def extract_docx(path: str) -> str:
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs).strip()


def extract_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read().strip()


def extract_image(path: str) -> str:
    """
    Prefer easyocr to avoid triggering pandas/numexpr stack pulled by pytesseract.
    Import lazily so NumPy/pandas issues don’t break startup.
    """
    try:
        import easyocr
        reader = easyocr.Reader(["en"])
        result = reader.readtext(path, detail=0)
        return "\n".join(result).strip()
    except Exception as e:
        # Fallback to pytesseract only if available; may need numpy<2 or updated deps
        try:
            import pytesseract
            img = Image.open(path)
            return pytesseract.image_to_string(img).strip()
        except Exception as e2:
            raise RuntimeError(
                f"OCR failed. easyocr error: {e}. pytesseract error: {e2}. "
                "Consider: pip install easyocr OR install Tesseract and ensure numpy/pandas stack is compatible."
            )


# ---------------- Gemini ----------------
def rewrite_with_gemini_retry(text: str, temperature: float, max_retries: int = 3) -> str:
    ensure_api_key()
    model = genai.GenerativeModel(GEMINI_MODEL)
    prompt = f"{REWRITE_PROMPT}\n\n---\n{text}"
    last_err = None
    for attempt in range(1, max_retries + 1):
        try:
            resp = model.generate_content(
                prompt,
                generation_config={"temperature": temperature},
            )
            return (resp.text or "").strip()
        except Exception as e:
            last_err = e
            wait_s = 5 * attempt
            try:
                msg = str(e)
                if "retry_delay" in msg and "seconds" in msg:
                    import re as _re
                    m = _re.search(r"retry_delay\s*{\s*seconds:\s*(\d+)", msg)
                    if m:
                        wait_s = max(wait_s, int(m.group(1)))
            except Exception:
                pass
            if attempt == max_retries:
                break
            print(f"[429/backoff] Waiting {wait_s}s then retrying (attempt {attempt}/{max_retries})...")
            time.sleep(wait_s)
    raise last_err if last_err else RuntimeError("Rewrite failed")


# ---------------- Core processing ----------------
def process_pdf(path: str, pages_per_chunk: int, do_rewrite: bool, temperature: float):
    base = os.path.splitext(os.path.basename(path))[0]
    out_dir = os.path.dirname(os.path.abspath(path))
    raw_md = os.path.join(out_dir, f"{base}_raw.md")
    rew_md = os.path.join(out_dir, f"{base}_rewritten.md")

    save_header_once(raw_md, f"# Extracted Text ({base})")
    if do_rewrite:
        save_header_once(rew_md, f"# Rewritten Text ({base})")

    used_requests = 0
    buf: List[str] = []
    chunk_start = None

    # Iterate pages; write raw per page; rewrite in big chunks
    total = None
    for pageno, text, total in extract_pdf_pages(path):
        if text:
            append_md(raw_md, f"\n\n## Page {pageno}\n\n{text}\n")
        print(f"Progress: Page {pageno}/{total}")

        if do_rewrite and text:
            if chunk_start is None:
                chunk_start = pageno
            buf.append(text)

            if len(buf) >= pages_per_chunk:
                if used_requests >= MAX_REQUESTS_PER_RUN:
                    print(f"Reached MAX_REQUESTS_PER_RUN={MAX_REQUESTS_PER_RUN}. Stopping rewrites.")
                    buf = []
                    chunk_start = None
                else:
                    _flush_chunk(buf, chunk_start, pageno, rew_md, temperature)
                    used_requests += 1
                    buf = []
                    chunk_start = None
                    time.sleep(PAUSE_BETWEEN_CALLS_SEC)

    # Flush remainder
    if do_rewrite and buf and chunk_start is not None and used_requests < MAX_REQUESTS_PER_RUN:
        end_p = chunk_start + len(buf) - 1
        _flush_chunk(buf, chunk_start, end_p, rew_md, temperature)
        used_requests += 1

    print("\nSaved:")
    print(f"  {raw_md}")
    if do_rewrite:
        print(f"  {rew_md}")


def _flush_chunk(buf: List[str], start_p: int, end_p: int, rew_md: str, temperature: float):
    piece = "\n\n".join(buf).strip()
    print(f"\nRewriting pages {start_p}–{end_p} ...")
    try:
        rewritten = rewrite_with_gemini_retry(piece, temperature)
        if not rewritten:
            rewritten = "(empty response)"
        append_md(rew_md, f"\n\n## Rewritten pages {start_p}–{end_p}\n\n{rewritten}\n")
        print(f"Appended rewritten pages {start_p}–{end_p}")
    except Exception as e:
        append_md(rew_md, f"\n\n## Rewritten pages {start_p}–{end_p}\n\n[Rewrite failed: {e}]\n")
        print(f"[rewrite failed] {e}")


def process_simple_text_like(path: str, do_rewrite: bool, temperature: float, loader):
    base = os.path.splitext(os.path.basename(path))[0]
    out_dir = os.path.dirname(os.path.abspath(path))
    raw_md = os.path.join(out_dir, f"{base}_raw.md")
    rew_md = os.path.join(out_dir, f"{base}_rewritten.md")

    save_header_once(raw_md, f"# Extracted Text ({base})")
    if do_rewrite:
        save_header_once(rew_md, f"# Rewritten Text ({base})")

    raw = normalize_text(loader(path))
    append_md(raw_md, raw + "\n")
    print(f"Saved raw to {raw_md}")

    if do_rewrite:
        try:
            rewritten = rewrite_with_gemini_retry(raw, temperature)
            append_md(rew_md, rewritten + "\n")
            print(f"Saved rewritten to {rew_md}")
        except Exception as e:
            append_md(rew_md, f"[Rewrite failed: {e}]\n")
            print(f"[rewrite failed] {e}")


# ---------------- File picker + CLI-like options ----------------
def pick_file():
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askopenfilename(
        title="Select a PDF, DOCX, TXT, or Image",
        filetypes=(
            ("Supported files", "*.pdf;*.docx;*.txt;*.png;*.jpg;*.jpeg;*.tiff;*.bmp"),
            ("All files", "*.*"),
        ),
    )
    root.destroy()
    return path


def main():
    # “Args” as env/variables so you can tweak defaults without typing:
    pages_per_chunk = int(os.environ.get("PAGES_PER_CHUNK", DEFAULT_PAGES_PER_CHUNK))
    no_rewrite = os.environ.get("NO_REWRITE", "").lower() in ("1", "true", "yes")
    temperature = float(os.environ.get("TEMPERATURE", DEFAULT_TEMPERATURE))

    fpath = pick_file()
    if not fpath:
        print("No file selected.")
        return
    fpath = os.path.abspath(fpath)

    ext = os.path.splitext(fpath)[1].lower()
    do_rewrite = not no_rewrite

    if ext == ".pdf":
        process_pdf(fpath, pages_per_chunk=pages_per_chunk, do_rewrite=do_rewrite, temperature=temperature)
    elif ext == ".docx":
        process_simple_text_like(fpath, do_rewrite, temperature, extract_docx)
    elif ext == ".txt":
        process_simple_text_like(fpath, do_rewrite, temperature, extract_txt)
    elif ext in (".png", ".jpg", ".jpeg", ".tiff", ".bmp"):
        process_simple_text_like(fpath, do_rewrite, temperature, extract_image)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


if __name__ == "__main__":
    main()
