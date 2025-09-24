import fitz
import docx
import pytesseract
import easyocr
from PIL import Image
import os

reader = easyocr.Reader(['en'])

def extract_text_from_pdf(pdf_path, output_txt="output.txt"):
    doc = fitz.open(pdf_path)
    with open(output_txt, "w", encoding="utf-8") as f:
        for page_num in range(len(doc)):
            page = doc[page_num]

            text = page.get_text()
            f.write(f"\n--- Page {page_num+1} ---\n")
            f.write(text + "\n")

            for img_index, img in enumerate(page.get_images(full=True)):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]

                image_path = f"temp_img_{page_num+1}_{img_index}.png"
                with open(image_path, "wb") as img_file:
                    img_file.write(image_bytes)

                ocr_text_tess = pytesseract.image_to_string(Image.open(image_path))

                ocr_text_easy = reader.readtext(image_path, detail=0)

                f.write(f"\n[Image {img_index+1} OCR - Tesseract]:\n{ocr_text_tess}\n")
                f.write(f"\n[Image {img_index+1} OCR - EasyOCR]:\n{' '.join(ocr_text_easy)}\n")

                os.remove(image_path) 

def extract_text_from_docx(docx_path, output_txt="output.txt"):
    doc = docx.Document(docx_path)
    with open(output_txt, "w", encoding="utf-8") as f:
        for para in doc.paragraphs:
            f.write(para.text + "\n")

def extract_text_from_txt(txt_path, output_txt="output.txt"):
    with open(txt_path, "r", encoding="utf-8") as infile, open(output_txt, "w", encoding="utf-8") as outfile:
        outfile.write(infile.read())

def extract_text(file_path, output_txt="output.txt"):
    ext = file_path.split(".")[-1].lower()
    if ext == "pdf":
        extract_text_from_pdf(file_path, output_txt)
    elif ext == "docx":
        extract_text_from_docx(file_path, output_txt)
    elif ext == "txt":
        extract_text_from_txt(file_path, output_txt)
    else:
        raise ValueError("Unsupported file format. Use PDF, DOCX, or TXT.")
    print(f"✅ Extracted text saved to {output_txt}")

extract_text("./LLM based project titles_250918_142744.pdf", "extracted_text1.txt")