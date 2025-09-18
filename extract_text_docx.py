import io
import docx
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_docx(path):
    d = docx.Document(path)
    text = [p.text for p in d.paragraphs if p.text.strip()]
    for rel in d.part.rels.values():
        try:
            if "image" in (rel.reltype or "") or "image" in (rel.target_ref or ""):
                img_bytes = rel.target_part.blob
                pil_img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
                ocr_txt = pytesseract.image_to_string(pil_img).strip()
                if ocr_txt:
                    text.append(ocr_txt)
        except:
            continue
    return "\n".join(text).strip()