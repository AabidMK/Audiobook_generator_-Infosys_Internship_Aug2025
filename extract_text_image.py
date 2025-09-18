from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(path):
    try:
        pil_img = Image.open(path).convert("RGB")
        text = pytesseract.image_to_string(pil_img).strip()
        return text
    except Exception as e:
        return f"Error extracting text from image: {e}"