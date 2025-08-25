import os
import sys
import io
import pdfplumber
import docx
import pytesseract

OCR_ENGINE = None
reader = None
try:
    
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' 
    OCR_ENGINE = "pytesseract"
    print("Using pytesseract for OCR (less memory intensive).")
except ImportError:
    try:
        import easyocr
        OCR_ENGINE = "easyocr"
        reader = easyocr.Reader(['en'], gpu=False)  
        print("Using easyocr for OCR.")
    except ImportError:
        print("No OCR engine (pytesseract or easyocr) found. OCR will be disabled.")

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

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
        else:
            return "[OCR library not configured]"
    except Exception as e:
        return f"[OCR Error: {e}]"

def extract_text_from_pdf(pdf_path):
    
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
                        text += f"\n[Error extracting text from image {img_idx}: {e}]"

                text += "\n"
    except Exception as e:
        return f"[PDF Extraction Error: {e}]"
    return text

def extract_text_from_docx(docx_path):
    try:
        doc = docx.Document(docx_path)
        text = "\n\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        return f"[DOCX Extraction Error: {e}]"

def save_as_markdown(content, output_path):
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        print(f"[Error saving Markdown: {e}]")

if __name__ == "__main__":
    file_path = r"C:\Users\kjish\pdf_extraction_test\sample12.pdf"
    file_ext = os.path.splitext(file_path)[1].lower()

    if not os.path.exists(file_path):
        print(f"[ERROR] File not found: {file_path}")
        sys.exit(1)

    if file_ext == ".pdf":
        extracted_text = extract_text_from_pdf(file_path)
    elif file_ext == ".docx":
        extracted_text = extract_text_from_docx(file_path)
    else:
        print("Unsupported file format! Use .pdf or .docx")
        sys.exit(1)

    output_md = os.path.join(os.path.dirname(file_path), "samplex.md")
    save_as_markdown(extracted_text, output_md)

    print(f"Extracted text saved as: {output_md}")
    print("Extraction complete!")
    
