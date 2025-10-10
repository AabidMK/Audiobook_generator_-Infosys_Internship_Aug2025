import os
import fitz  # PyMuPDF
import docx  # python-docx
import cv2
import pytesseract
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ---------------- TEXT EXTRACTION FUNCTIONS ----------------

# Extract text from PDF
def extract_from_pdf(file_path):
    text = ""
    pdf_document = fitz.open(file_path)
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num) 
        text += page.get_text()
    pdf_document.close()
    return text.strip()

# Extract text from DOCX
def extract_from_docx(file_path):
    doc = docx.Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.strip()

# Extract text from Image (using OCR)
def extract_from_image(file_path):
    img = cv2.imread(file_path)
    if img is None:
        return ""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    text = pytesseract.image_to_string(thresh)
    return text.strip()

# Unified function
def extract_text(file_path):
    if not os.path.exists(file_path):
        return None, "File not found."

    ext = file_path.lower()

    if ext.endswith(".pdf"):
        return extract_from_pdf(file_path), None
    elif ext.endswith(".docx"):
        return extract_from_docx(file_path), None
    elif ext.endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff")):
        return extract_from_image(file_path), None
    else:
        return None, "Unsupported file format. Use PDF, DOCX, or Image."

# ---------------- MAIN PROGRAM ----------------
if __name__ == "__main__":
    file_path = input("Enter the file path (.pdf, .docx, .png, .jpg): ")

    extracted_text, error = extract_text(file_path)

    if error:   # if something went wrong
        print(f"Error: {error}")
    else:
        # Save output as .md file
        output_file = os.path.splitext(file_path)[0] + "_output.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(extracted_text)

        print(f"\n✅ Text successfully extracted and saved to: {output_file}")