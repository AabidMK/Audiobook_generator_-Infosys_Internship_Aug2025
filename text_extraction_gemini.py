"""
Text Extraction + Google Gemini Rewrite (GUI file picker)

- Supports PDF, DOCX, TXT, and images (PNG/JPG/JPEG/TIFF/BMP).
- Extracts full text and saves <basename>.md.
- Sends extracted text to Google Gemini for listener-friendly rewrite.
- Saves rewritten text to <basename>_rewritten.md.
- Uses EasyOCR by default for images; can switch to pytesseract.

Setup:
  pip install pdfplumber python-docx pillow google-generativeai
  pip install easyocr  # for OCR on images (preferred)
  # or: pip install pytesseract  (requires external Tesseract engine)

Environment:
  Set your API key once in PowerShell, then restart terminal:
    setx GOOGLE_API_KEY "YOUR_KEY"

Run:
  python text_extraction_gemini.py
"""

import os
import re
import pdfplumber
import docx
from PIL import Image
from tkinter import Tk, filedialog
import google.generativeai as genai


# =========================
# Configuration
# =========================
GEMINI_MODEL = "gemini-1.5-flash"   # "gemini-1.5-pro" for maximum quality
TEMPERATURE = 0.5
USE_EASYOCR = True                  # True -> EasyOCR, False -> pytesseract
MAX_CHARS_PER_CHUNK = 12000         # conservative chunk size


# =========================
# Helpers
# =========================
def normalize_text(s: str) -> str:
    s = s.replace("\u00A0", " ")  # non-breaking space
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\r?\n\s*", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def split_into_chunks(text: str, limit: int = MAX_CHARS_PER_CHUNK):
    if len(text) <= limit:
        return [text]
    parts, cur = [], ""
    for para in text.split("\n\n"):
        if len(cur) + len(para) + 2 <= limit:
            cur += (("\n\n" if cur else "") + para)
        else:
            if cur:
                parts.append(cur)
            cur = para
    if cur:
        parts.append(cur)
    return parts


def save_markdown(text: str, input_path: str, suffix: str = "") -> str:
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    out_name = f"{base_name}{suffix}.md"
    with open(out_name, "w", encoding="utf-8") as f:
        title = f"# Extracted Text from {os.path.basename(input_path)}" if not suffix else f"# Rewritten Text ({os.path.basename(input_path)})"
        f.write(title + "\n\n")
        f.write(text)
    return out_name


# =========================
# Extractors
# =========================
def extract_pdf(path: str) -> str:
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return normalize_text(text)


def extract_docx(path: str) -> str:
    d = docx.Document(path)
    return normalize_text("\n".join(p.text for p in d.paragraphs))


def extract_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return normalize_text(f.read())


def extract_image(path: str, use_easyocr: bool = USE_EASYOCR) -> str:
    if use_easyocr:
        try:
            import easyocr
        except ImportError:
            raise RuntimeError("easyocr not installed. Install with: pip install easyocr")
        reader = easyocr.Reader(["en"])
        result = reader.readtext(path, detail=0)
        text = "\n".join(result)
    else:
        try:
            import pytesseract
        except ImportError:
            raise RuntimeError("pytesseract not installed. Install with: pip install pytesseract")
        text = pytesseract.image_to_string(Image.open(path))
    return normalize_text(text)


def extract_text(file_path: str) -> str:
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".pdf":
        return extract_pdf(file_path)
    if ext == ".docx":
        return extract_docx(file_path)
    if ext == ".txt":
        return extract_txt(file_path)
    if ext in [".png", ".jpg", ".jpeg", ".tiff", ".bmp"]:
        return extract_image(file_path, use_easyocr=USE_EASYOCR)
    raise ValueError(f"Unsupported file type: {ext}")


# =========================
# Gemini
# =========================
def configure_gemini():
    api_key = os.environ.get("GOOGLE_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("Missing GOOGLE_API_KEY environment variable.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(GEMINI_MODEL)


REWRITE_PROMPT = (
    "Rewrite the following text for clear, engaging narration suitable for an audiobook listener. "
    "Keep factual content, do not invent details, improve flow and coherence, use concise sentences, "
    "and keep or enhance Markdown headings and bullet lists where helpful. Normalize spacing and punctuation."
)


def rewrite_with_gemini(text: str, model) -> str:
    chunks = split_into_chunks(text, MAX_CHARS_PER_CHUNK)
    outputs = []
    for idx, chunk in enumerate(chunks, 1):
        prompt = (
            f"{REWRITE_PROMPT}\n\n"
            f"---\n"
            f"Chunk {idx} of {len(chunks)}:\n\n"
            f"{chunk}"
        )
        resp = model.generate_content(
            prompt,
            generation_config={"temperature": TEMPERATURE}
        )
        outputs.append(resp.text or "")
    return "\n\n".join(outputs).strip()


# =========================
# Main (GUI)
# =========================
if __name__ == "__main__":
    print("Text Extraction + Gemini Rewrite")
    root = Tk()
    root.withdraw()
    root.update()

    file_path = filedialog.askopenfilename(
        title="Select a PDF, DOCX, TXT, or Image",
        filetypes=(
            ("Supported files", "*.pdf *.docx *.txt *.png *.jpg *.jpeg *.tiff *.bmp"),
            ("All files", "*.*"),
        ),
    )

    if not file_path:
        print("No file selected.")
        raise SystemExit(0)

    print(f"Selected: {file_path}")

    # Extract
    raw_text = extract_text(file_path)
    raw_md = save_markdown(raw_text, file_path, suffix="")
    print(f"Saved raw extract: {raw_md}")

    # Rewrite with Gemini
    try:
        model = configure_gemini()
        rewritten = rewrite_with_gemini(raw_text, model)
        out_md = save_markdown(rewritten, file_path, suffix="_rewritten")
        print(f"Saved rewritten: {out_md}")
    except Exception as e:
        print(f"Gemini rewrite failed: {e}")
        print("You still have the raw extraction file.")

    # Print entire extracted text to console
    print("\n--- Extracted Text (full) ---\n")
    print(raw_text)
