import os
import pdfplumber
from docx import Document
from markdownify import markdownify as md  # For converting TXT to Markdown
import pytesseract
from PIL import Image
import pytesseract
import pytesseract

# Point to the installed Tesseract OCR exe
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# ---------------- PDF ----------------
def extract_text_from_pdf(file_path):
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + '\n'
    except Exception as e:
        print(f"Error reading PDF file: {e}")
    return text.strip()

# ---------------- DOCX ----------------
def extract_text_from_docx(file_path):
    text = ""
    try:
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + '\n'
    except Exception as e:
        print(f"Error reading DOCX file: {e}")
    return text.strip()

# ---------------- TXT ----------------
def extract_text_from_txt(file_path):
    text = ""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        print(f"Error reading TXT file: {e}")
    return text.strip()

# ---------------- IMAGE (OCR) ----------------
def extract_text_from_image(file_path):
    text = ""
    try:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)
    except Exception as e:
        print(f"Error reading Image file: {e}")
    return text.strip()

# ---------------- Main Extract Function ----------------
def extract_text(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext == '.docx':
        return extract_text_from_docx(file_path)
    elif ext == '.txt':
        return extract_text_from_txt(file_path)
    elif ext in ['.png', '.jpg', '.jpeg']:
        return extract_text_from_image(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")

# ---------------- Run Script ----------------
if __name__ == "__main__":
    files_to_extract = ["csapdf.pdf", "UHV-3.docx", "regex.txt", "Superman.jpg"]

    for file_name in files_to_extract:
        print(f"\n--- Extracting from: {file_name} ---\n")
        try:
            text = extract_text(file_name)
            print(text if text else "[No text found]")

            # Convert TXT to Markdown
            if file_name.lower().endswith('.txt'):
                markdown_text = md(text)
                md_filename = file_name.replace('.txt', '.md')
                with open(md_filename, 'w', encoding='utf-8') as md_file:
                    md_file.write(markdown_text)
                print(f"[Markdown saved to {md_filename}]")

            # Save OCR text to Markdown
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                md_filename = file_name.rsplit('.', 1)[0] + ".md"
                with open(md_filename, 'w', encoding='utf-8') as md_file:
                    md_file.write(text)
                print(f"[Markdown saved to {md_filename}]")

        except Exception as e:
            print(f"Error: {e}")