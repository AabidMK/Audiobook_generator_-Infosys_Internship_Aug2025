import os
import sys
import pdfplumber
import docx
import pytesseract
import logging

try:
    import easyocr  # Optional: used if pytesseract is unavailable
except ImportError:
    easyocr = None

# --- Logging Setup: Detailed logs for troubleshooting ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("text_extraction.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

# --- OCR Handling: Selects best OCR engine available ---
OCR_ENGINE = None
reader = None
if pytesseract:
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    OCR_ENGINE = "pytesseract"
    logging.info("Using pytesseract for OCR.")
elif easyocr:
    OCR_ENGINE = "easyocr"
    reader = easyocr.Reader(['en'], gpu=False)
    logging.info("Using easyocr for OCR.")
else:
    logging.warning("No OCR engine available.")

# --- OCR function: Extracts text from images using the best available engine ---
def ocr_image(image):
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
    except Exception as e:
        logging.error(f"OCR Error: {e}", exc_info=True)
        return f"[OCR Error: {e}]"

def extract_text_from_pdf(pdf_path):
    """
    Reads each page of a PDF. Extracts text directly if selectable, 
    otherwise applies OCR to images to avoid missing any words.
    """
    all_text = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                page_text = page.extract_text() or ""
                if page_text.strip():
                    all_text.append(page_text)
                else:
                    pil_img = page.to_image(resolution=300).original
                    ocr_text = ocr_image(pil_img)
                    all_text.append(ocr_text)
    except Exception as e:
        logging.error(f"PDF Extraction Error: {e}", exc_info=True)
        return f"[PDF Extraction Error: {e}]"
    return "\n".join(all_text)

def extract_text_from_docx(docx_path):
    try:
        doc = docx.Document(docx_path)
        return "\n\n".join([para.text.strip() for para in doc.paragraphs if para.text.strip()])
    except Exception as e:
        logging.error(f"DOCX Extraction Error: {e}", exc_info=True)
        return f"[DOCX Extraction Error: {e}]"

def save_as_markdown(content, output_path):
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        logging.info(f"Saved to {output_path}")
    except Exception as e:
        logging.error(f"Error saving Markdown: {e}", exc_info=True)

def enrich_for_audiobook(text, api_key):
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = (
            "Rewrite the following extracted text into an engaging, audiobook-ready format:\n"
            "- For EVERY sentence, provide a plain language summary or explanation so no sentence goes unexplained.\n"
            "- Add a short summary at the start.\n"
            "- Highlight key points in bullet lists.\n"
            "- Extract important terms, giving each a simple definition.\n"
            "- Narrate with excitement, rhythm, and famous quotes where suitable.\n\n"
            "EXTRACTED TEXT STARTS BELOW:\n"
            f"{text}\n"
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logging.error(f"Gemini API Error: {e}", exc_info=True)
        return f"[Gemini API Error: {e}]"

# --- Pipeline entry: detects file type, coordinates full extraction and enrichment ---
if __name__ == "__main__":
    file_path = r"C:\Users\kjish\pdf_extraction_test\receptors.pdf"  # Change as needed
    file_ext = os.path.splitext(file_path)[1].lower()

    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        sys.exit(1)

    if file_ext == ".pdf":
        extracted_text = extract_text_from_pdf(file_path)
    elif file_ext == ".docx":
        extracted_text = extract_text_from_docx(file_path)
    else:
        logging.error("Unsupported file format!")
        sys.exit(1)

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        logging.error("Gemini API key not found!")
        sys.exit(1)

    # Enrich output so every sentence is explained and nothing is missed
    final_text = enrich_for_audiobook(extracted_text, GEMINI_API_KEY)

    output_md = os.path.join(os.path.dirname(file_path), "audiobook_ready.md")
    save_as_markdown(final_text, output_md)

    logging.info("Pipeline complete! Audiobook-ready text saved.")
