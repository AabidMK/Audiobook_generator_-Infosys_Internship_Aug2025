import pytesseract
import fitz  # PyMuPDF
import pdfplumber
import docx
from PIL import Image

# Tell pytesseract where tesseract.exe is installed
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_pdf(filepath):
    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(filepath):
    doc = docx.Document(filepath)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_txt(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def extract_text_from_image(filepath):
    img = Image.open(filepath)
    text = pytesseract.image_to_string(img)
    return text

# -------- MAIN PROGRAM --------
file_path = input("Enter file path (PDF/DOCX/TXT/Image): ").strip()

if file_path.lower().endswith(".pdf"):
    print(extract_text_from_pdf(file_path))
elif file_path.lower().endswith(".docx"):
    print(extract_text_from_docx(file_path))
elif file_path.lower().endswith(".txt"):
    print(extract_text_from_txt(file_path))
elif file_path.lower().endswith((".png", ".jpg", ".jpeg")):
    print(extract_text_from_image(file_path))
else:
    print("Unsupported file format")
