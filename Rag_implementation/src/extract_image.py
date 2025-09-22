import pytesseract
from PIL import Image
import logging
from pathlib import Path
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Check if Tesseract is installed
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def check_tesseract():
    if not os.path.exists(TESSERACT_PATH):
        raise RuntimeError(
            "Tesseract is not installed or not found at expected location. "
            "Please install Tesseract or update the path."
        )

def extract_text_from_image(image_path: str) -> str:
    """
    Extract text from an image file using Tesseract OCR.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        str: Extracted text or empty string if extraction fails
    """
    try:
        # Check if Tesseract is installed
        check_tesseract()
        
        # Configure Tesseract path
        pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
        
        # Check if file exists
        if not Path(image_path).exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")
            
        # Open and process image
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang="eng") or ""
        
        logger.info(f"Successfully extracted text from {image_path}")
        return text.strip()
        
    except Exception as e:
        logger.error(f"Image extraction error for {image_path}: {e}", exc_info=True)
        return ""