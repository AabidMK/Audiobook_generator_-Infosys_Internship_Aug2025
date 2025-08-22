import pdfplumber
import docx
import os
import sys
import io

OCR_ENGINE = None
reader = None
try:
    import easyocr
    OCR_ENGINE = "easyocr"
    reader = easyocr.Reader(['en'], gpu=True)
except ImportError:
    try:
        import pytesseract
        from PIL import Image
        OCR_ENGINE = "pytesseract"
    except ImportError:
        OCR_ENGINE = None

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def ocr_page(page):
    """
    Render the page as an image and extract text using OCR.
    """
    if OCR_ENGINE is None:
        return "[OCR library not installed]"
    pil_img = page.to_image(resolution=300).original
    if OCR_ENGINE == "easyocr":
        import numpy as np
        np_img = np.array(pil_img)
        result = reader.readtext(np_img, detail=0, paragraph=True)
        return "\n".join(result)
    elif OCR_ENGINE == "pytesseract":
        return pytesseract.image_to_string(pil_img)
    else:
        return "[OCR library not installed]"

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text() or ""
            text += f"\n\n## Page {page_num}\n"
            if page_text.strip():
                text += page_text
            else:
                ocr_text = ocr_page(page)
                text += f"\n[OCR Extracted Text]\n{ocr_text}"
            text += "\n"
    return text

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    text = "\n\n".join([para.text for para in doc.paragraphs])
    return text

def save_as_markdown(content, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    file_path = r"C:\Users\kjish\pdf_extraction_test\sample-tables.pdf"
    file_ext = os.path.splitext(file_path)[1].lower()

    if file_ext == ".pdf":
        extracted_text = extract_text_from_pdf(file_path)
    elif file_ext == ".docx":
        extracted_text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format! Use .pdf or .docx")

    output_md = os.path.splitext(file_path)[0] + ".md"
    save_as_markdown(extracted_text, output_md)

    print(f"Extracted text saved as: {output_md}")