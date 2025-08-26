import PyPDF2
from pdf2image import convert_from_path
import pytesseract

def extract_pdf(file_path: str) -> str:
    """Extract text from PDF (text + OCR for scanned PDFs)"""
    text = ""

    # Step 1: Extract normal text
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""

    # Step 2: If no text found → OCR scanned PDF
    if not text.strip():
        print("[!] No text found, running OCR on PDF images...")
        images = convert_from_path(file_path)
        for img in images:
            text += pytesseract.image_to_string(img)

    return text
