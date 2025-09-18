import io
import pdfplumber
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text += page_text + "\n"
            for img in page.images:
                try:
                    x0, top, x1, bottom = img["x0"], img["top"], img["x1"], img["bottom"]
                    crop = page.within_bbox((x0, top, x1, bottom))
                    pil_img = crop.to_image(resolution=300).original
                    if isinstance(pil_img, (bytes, bytearray)):
                        pil_img = Image.open(io.BytesIO(pil_img)).convert("RGB")
                    ocr_txt = pytesseract.image_to_string(pil_img).strip()
                    if ocr_txt:
                        text += "\n" + ocr_txt + "\n"
                except:
                    continue
    return text.strip()