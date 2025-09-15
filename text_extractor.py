import os
import pdfplumber
import docx

try:
    from PIL import Image
    import pytesseract
except ImportError:
    pytesseract = None

class TextExtractor:
    @staticmethod
    def extract_text(file_path):
        ext = os.path.splitext(file_path)[-1].lower()
        if ext == ".pdf":
            return TextExtractor._from_pdf(file_path)
        elif ext == ".docx":
            return TextExtractor._from_docx(file_path)
        elif ext == ".txt":
            return TextExtractor._from_txt(file_path)
        else:
            raise ValueError("Unsupported file type")

    @staticmethod
    def _from_pdf(file_path):
        text = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
                elif pytesseract:
                    im = page.to_image(resolution=300).original
                    ocr_text = pytesseract.image_to_string(im)
                    text.append(ocr_text)
        return "\n".join(text)

    @staticmethod
    def _from_docx(file_path):
        doc = docx.Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

    @staticmethod
    def _from_txt(file_path):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
