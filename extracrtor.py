import pytesseract
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
from docx import Document
from PIL import Image
import os


def extract_from_pdf(pdf_path):
    text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        print("[WARN] PDF direct extraction failed:", e)

    if not text.strip():
        print("[INFO] OCR fallback for PDF...")
        images = convert_from_path(pdf_path)
        for img in images:
            text += pytesseract.image_to_string(img)
    return text


def extract_from_docx(docx_path):
    doc = Document(docx_path)
    text = "\n".join([p.text for p in doc.paragraphs])
    return text


def extract_from_image(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text


def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_from_pdf(file_path)
    elif ext == ".docx":
        return extract_from_docx(file_path)
    elif ext in [".png", ".jpg", ".jpeg"]:
        return extract_from_image(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
