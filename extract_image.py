import pytesseract
from PIL import Image

def extract_image(file_path: str) -> str:
    """Extract text from images using OCR"""
    img = Image.open(file_path)
    return pytesseract.image_to_string(img)
