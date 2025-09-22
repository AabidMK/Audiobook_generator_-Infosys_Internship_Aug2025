import logging
import pdfplumber
from pdf2image import convert_from_path
import pytesseract
from PIL import Image

#  Set Tesseract path if needed (adjust if installed elsewhere)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Hardcode your Poppler path
POPLER_PATH = r"C:\Users\kjish\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin"

def ocr_image(image: Image.Image) -> str:
    """Run OCR on an image."""
    try:
        return pytesseract.image_to_string(image, lang="eng")
    except Exception as e:
        logging.error(f"OCR Error: {e}", exc_info=True)
        return ""

def extract_text_from_pdf(pdf_path: str, force_ocr: bool = False) -> str:
    """
    Extract text from PDF using pdfplumber and OCR fallback.
    If force_ocr=True, runs OCR on all pages.
    """
    all_text = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                text = page.extract_text() or ""
                if text.strip() and not force_ocr:
                    logging.info(f"pdfplumber extracted {len(text)} chars from page {page_num}")
                    all_text.append(text)
                else:
                    logging.info(f"Page {page_num}: no embedded text, will try OCR")

        # OCR pass (always runs to capture scanned content)
        try:
            pages = convert_from_path(pdf_path, dpi=300, poppler_path=POPLER_PATH)
            for i, page in enumerate(pages, start=1):
                ocr_text = ocr_image(page)
                if ocr_text.strip():
                    logging.info(f"OCR extracted {len(ocr_text)} chars from page {i}")
                    all_text.append(ocr_text)
        except Exception as e:
            logging.error(f"pdf2image/Poppler failed: {e}", exc_info=True)

    except Exception as e:
        logging.error(f"PDF Extraction Error for {pdf_path}: {e}", exc_info=True)

    final = "\n\n".join(t for t in all_text if t and t.strip())
    if not final:
        logging.warning(f"No text extracted at all from {pdf_path}")
    return final
