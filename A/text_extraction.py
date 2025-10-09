import os
import fitz  # PyMuPDF for PDFs
import docx  # python-docx for DOCX
from PIL import Image
import pytesseract
import easyocr

# 👉 If using pytesseract, set the path to installed Tesseract:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_pdf(pdf_path: str) -> str:
    """Extract text from PDF using PyMuPDF."""
    doc = fitz.open(pdf_path)
    text = "\n\n".join(page.get_text() for page in doc)
    return f"# Extracted from PDF\n\n{text.strip()}"


def extract_docx(docx_path: str) -> str:
    """Extract text from DOCX using python-docx."""
    doc = docx.Document(docx_path)
    text = "\n\n".join(p.text for p in doc.paragraphs if p.text.strip())
    return f"# Extracted from DOCX\n\n{text.strip()}"


def extract_txt(txt_path: str) -> str:
    """Extract text from plain TXT file."""
    with open(txt_path, "r", encoding="utf-8") as f:
        text = f.read()
    return f"# Extracted from TXT\n\n{text.strip()}"


def extract_image(img_path: str, method="pytesseract") -> str:
    """Extract text from image using OCR (pytesseract or easyocr)."""
    if method == "pytesseract":
        img = Image.open(img_path)
        text = pytesseract.image_to_string(img)
    else:
        reader = easyocr.Reader(["en"])  # English
        result = reader.readtext(img_path, detail=0)
        text = "\n".join(result)

    return f"# Extracted from Image ({method.upper()})\n\n{text.strip()}"


def extract_text(file_path: str) -> str:
    """Detect file type and extract text accordingly."""
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return extract_pdf(file_path)
    elif ext == ".docx":
        return extract_docx(file_path)
    elif ext == ".txt":
        return extract_txt(file_path)
    elif ext in [".png", ".jpg", ".jpeg", ".tif", ".bmp"]:
        return extract_image(file_path, method="pytesseract")  # or "easyocr"
    else:
        raise ValueError(f"Unsupported file format: {ext}")


if __name__ == "__main__":
    file_path = input("Enter file path (PDF/DOCX/TXT/Image): ").strip()
    try:
        text = extract_text(file_path)

        # Save extracted text as Markdown
        out_path = os.path.splitext(file_path)[0] + "_extracted.md"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"\n✅ Extracted text saved as Markdown: {out_path}\n")
        print("Preview (first 500 chars):\n")
        print(text[:500])

    except Exception as e:
        print(f"Error: {e}")
