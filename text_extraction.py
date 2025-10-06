# text_extraction.py
import os
import pdfplumber
import docx
from PIL import Image
from tkinter import Tk, filedialog

def extract_pdf(path: str) -> str:
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.strip()

def extract_docx(path: str) -> str:
    d = docx.Document(path)
    return "\n".join(p.text for p in d.paragraphs).strip()

def extract_txt(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read().strip()

def extract_image(path: str, use_easyocr: bool = True) -> str:
    if use_easyocr:
        try:
            import easyocr
        except ImportError:
            raise RuntimeError("easyocr not installed. pip install easyocr")
        reader = easyocr.Reader(["en"])
        result = reader.readtext(path, detail=0)
        return "\n".join(result).strip()
    else:
        try:
            import pytesseract
        except ImportError:
            raise RuntimeError("pytesseract not installed. pip install pytesseract")
        return pytesseract.image_to_string(Image.open(path)).strip()

def save_as_markdown_raw(text: str, input_path: str) -> str:
    base = os.path.splitext(os.path.basename(input_path))[0]
    out = f"{base}_raw.md"
    with open(out, "w", encoding="utf-8") as f:
        f.write(f"# Extracted Text from {os.path.basename(input_path)}\n\n")
        f.write(text)
    print(f"Saved raw: {out}")
    return out

def extract_text(file_path: str, use_easyocr: bool = True) -> str:
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".pdf":
        text = extract_pdf(file_path)
    elif ext == ".docx":
        text = extract_docx(file_path)
    elif ext == ".txt":
        text = extract_txt(file_path)
    elif ext in [".png", ".jpg", ".jpeg", ".tiff", ".bmp"]:
        text = extract_image(file_path, use_easyocr=use_easyocr)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
    return save_as_markdown_raw(text, file_path)

if __name__ == "__main__":
    print("Text Extraction: file picker")
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select a PDF, DOCX, TXT, or Image",
        filetypes=(
            ("Supported files", "*.pdf *.docx *.txt *.png *.jpg *.jpeg *.tiff *.bmp"),
            ("All files", "*.*"),
        ),
    )
    if file_path:
        extract_text(file_path, use_easyocr=True)
    else:
        print("No file selected.")
