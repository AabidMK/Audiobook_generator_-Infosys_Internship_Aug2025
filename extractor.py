import os
import pytesseract
from PIL import Image
import PyPDF2
import docx

def extract_text(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    text = ""

    if ext == ".pdf":
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + "\n"

    elif ext == ".docx":
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"

    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

    elif ext in [".jpg", ".jpeg", ".png"]:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)

    else:
        raise ValueError(f"Unsupported file format: {ext}")

    return text
