import logging
import pdfplumber
import docx
import pytesseract
from PIL import Image
from pdf2image import convert_from_path  # requires: pip install pdf2image

# ⚠️ Adjust this path to your Tesseract install
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def ocr_image(image: Image.Image) -> str:
    """Run OCR on a PIL image."""
    try:
        return pytesseract.image_to_string(image, lang="eng")
    except Exception as e:
        logging.error(f"OCR Error: {e}", exc_info=True)
        return ""


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from PDF:
    - pdfplumber for embedded text
    - OCR on page images
    - Merge both results
    """
    all_text = []
    try:
        # 1. Extract with pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                text = page.extract_text() or ""
                if text.strip():
                    logging.info(f"Pdfplumber extracted {len(text)} chars from page {page_num}")
                else:
                    logging.info(f"No embedded text on page {page_num}, OCR will handle it")
                all_text.append(text)

        # 2. OCR every page
        pages = convert_from_path(pdf_path, dpi=300)
        for i, page in enumerate(pages, start=1):
            ocr_text = ocr_image(page)
            if ocr_text.strip():
                logging.info(f"OCR extracted {len(ocr_text)} chars from page {i}")
                all_text.append(ocr_text)
            else:
                logging.warning(f"OCR produced no text on page {i} of {pdf_path}")

    except Exception as e:
        logging.error(f"PDF Extraction Error for {pdf_path}: {e}", exc_info=True)

    # 3. Merge all results
    final_text = "\n\n".join(t for t in all_text if t.strip())
    if not final_text:
        logging.warning(f"No text extracted at all from {pdf_path}")
    return final_text


def extract_text_from_docx(docx_path: str) -> str:
    """Extract text from DOCX."""
    try:
        doc = docx.Document(docx_path)
        text = "\n\n".join(p.text.strip() for p in doc.paragraphs if p.text.strip())
        if not text:
            logging.warning(f"No text extracted from {docx_path}")
        return text
    except Exception as e:
        logging.error(f"DOCX Extraction Error for {docx_path}: {e}", exc_info=True)
        return ""


def extract(file_path: str) -> str:
    """Unified extractor for RAG (PDF text + OCR + DOCX)."""
    if file_path.lower().endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.lower().endswith(".docx"):
        return extract_text_from_docx(file_path)
    else:
        logging.error(f"Unsupported file type: {file_path}. Only PDF and DOCX supported.")
        return ""
