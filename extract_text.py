import io, os
import pdfplumber
import docx
from PIL import Image
import pytesseract

# Windows-specific Tesseract path
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

def extract_text(path):
    if path.lower().endswith(".pdf"):
        return extract_text_from_pdf(path)
    elif path.lower().endswith(".docx"):
        return extract_text_from_docx(path)
    else:
        raise ValueError("Only PDF and DOCX supported.")

def save_to_markdown(text, filename="output.md"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("# Extracted Document\n\n")
        f.write(text)
    return filename

# Main program
if __name__ == "__main__":
    file_path = input("Enter the path to your PDF or DOCX file: ")
    try:
        text = extract_text(file_path)
        md_file = save_to_markdown(text, "extracted_output.md")
        print(f"Extraction complete! Markdown saved as {md_file}")
    except Exception as e:
        print(f"Error: {e}")