import os
import sys
import io
import pdfplumber
import docx
import pytesseract
import google.generativeai as genai
import logging

# -----------------------------------------------------------------------------
# Logging Setup
# -----------------------------------------------------------------------------

# Configure logging to write to a file and the console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("text_extraction.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

# -----------------------------------------------------------------------------
# OCR Engine Setup
# -----------------------------------------------------------------------------

OCR_ENGINE = None
reader = None
try:
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    OCR_ENGINE = "pytesseract"
    logging.info("Using pytesseract for OCR (less memory intensive).")
except ImportError:
    try:
        import easyocr
        OCR_ENGINE = "easyocr"
        reader = easyocr.Reader(['en'], gpu=False)
        logging.info("Using easyocr for OCR.")
    except ImportError:
        logging.warning("No OCR engine (pytesseract or easyocr) found. OCR will be disabled.")

# -----------------------------------------------------------------------------
# Output Configuration
# -----------------------------------------------------------------------------

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# -----------------------------------------------------------------------------
# OCR Function
# -----------------------------------------------------------------------------

def ocr_image(image):
    """
    Extract text from an image using OCR.
    """
    if OCR_ENGINE is None:
        return "[OCR library not installed]"

    try:
        pil_img = image
        if OCR_ENGINE == "easyocr":
            import numpy as np
            np_img = np.array(pil_img)
            result = reader.readtext(np_img, detail=0, paragraph=True)
            return "\n".join(result)
        elif OCR_ENGINE == "pytesseract":
            return pytesseract.image_to_string(pil_img)
        else:
            return "[OCR library not configured]"
    except Exception as e:
        logging.error(f"OCR Error: {e}", exc_info=True)
        return f"[OCR Error: {e}]"

# -----------------------------------------------------------------------------
# PDF Extraction Function
# -----------------------------------------------------------------------------

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file, using OCR on pages and images as needed.
    """
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                text += f"\n\n## Page {page_num}\n"
                page_text = page.extract_text() or ""
                if page_text.strip():
                    text += page_text
                else:
                    pil_img = page.to_image(resolution=300).original
                    ocr_text = ocr_image(pil_img)
                    text += f"\n[OCR Extracted Text]\n{ocr_text}"

                for img_idx, img in enumerate(page.images, start=1):
                    try:
                        img_obj = page.images[img_idx - 1]
                        img_bbox = (img_obj['x0'], img_obj['top'], img_obj['x1'], img_obj['bottom'])
                        pil_img = page.crop(img_bbox).to_image(resolution=300).original
                        ocr_text = ocr_image(pil_img)
                        text += f"\n[Image {img_idx} OCR Text]\n{ocr_text}"
                    except Exception as e:
                        logging.error(f"Error extracting text from image {img_idx}: {e}", exc_info=True)
                        text += f"\n[Error extracting text from image {img_idx}: {e}]"

                text += "\n"
    except Exception as e:
        logging.error(f"PDF Extraction Error: {e}", exc_info=True)
        return f"[PDF Extraction Error: {e}]"
    return text

# -----------------------------------------------------------------------------
# DOCX Extraction Function
# -----------------------------------------------------------------------------

def extract_text_from_docx(docx_path):
    """
    Extract text from a DOCX file.
    """
    try:
        doc = docx.Document(docx_path)
        text = "\n\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        logging.error(f"DOCX Extraction Error: {e}", exc_info=True)
        return f"[DOCX Extraction Error: {e}]"

# -----------------------------------------------------------------------------
# Markdown Saving Function
# -----------------------------------------------------------------------------

def save_as_markdown(content, output_path):
    """
    Save the extracted content to a Markdown file.
    """
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        logging.info(f"Successfully saved to {output_path}")
    except Exception as e:
        logging.error(f"Error saving Markdown: {e}", exc_info=True)

# -----------------------------------------------------------------------------
# Gemini API Function
# -----------------------------------------------------------------------------

def rewrite_with_gemini(text, api_key):
    """
    Rewrites the given text using the Google Gemini API.
    """
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"Rewrite the following text for better narration and listener experience:\n\n{text}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logging.error(f"Gemini API Error: {e}", exc_info=True)
        return f"[Gemini API Error: {e}]"

# -----------------------------------------------------------------------------
# Main Function
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    file_path = r"C:\Users\kjish\pdf_extraction_test\sample12.pdf"
    repo_path = r"C:\Users\kjish\pdf_extraction_test"  # Replace with your repository path
    file_ext = os.path.splitext(file_path)[1].lower()

    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        sys.exit(1)

    if file_ext == ".pdf":
        extracted_text = extract_text_from_pdf(file_path)
    elif file_ext == ".docx":
        extracted_text = extract_text_from_docx(file_path)
    else:
        logging.error("Unsupported file format! Use .pdf or .docx")
        sys.exit(1)

    raw_md = os.path.join(os.path.dirname(file_path), "raw_extracted.md")
    save_as_markdown(extracted_text, raw_md)
    logging.info(f"Raw extracted text saved as: {raw_md}")

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        logging.error("Gemini API key not found! Set GEMINI_API_KEY as an environment variable.")
        sys.exit(1)

    improved_text = rewrite_with_gemini(extracted_text, GEMINI_API_KEY)

    improved_md = os.path.join(os.path.dirname(file_path), "improved_narration.md")
    save_as_markdown(improved_text, improved_md)

    logging.info(f"Improved narration saved as: {improved_md}")
    logging.info("Pipeline complete!")