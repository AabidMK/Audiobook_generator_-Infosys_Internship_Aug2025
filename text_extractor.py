import os
import pdfplumber
import docx
import argparse
from PIL import Image
import pytesseract
import easyocr

# Initialize EasyOCR reader (English for now, can add more langs)
reader = easyocr.Reader(['en'], gpu=False)


def extract_text(file_path: str) -> str:
    """
    Extract text from PDF, DOCX, or TXT file.
    Falls back to OCR if text is missing (images only).
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return extract_pdf_text(file_path)
    elif ext == ".docx":
        return extract_docx_text(file_path)
    elif ext == ".txt":
        return extract_txt(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")


def extract_pdf_text(file_path: str) -> str:
    """Extract text from a PDF using PDFplumber with OCR fallback."""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
            else:
                # OCR fallback for image-only pages
                print(f"⚠️ No text found on page {i+1}, running OCR...")
                pil_image = page.to_image(resolution=300).original
                # OCR with pytesseract
                ocr_text = pytesseract.image_to_string(pil_image)
                if not ocr_text.strip():
                    # If pytesseract fails, try EasyOCR
                    ocr_result = reader.readtext(pil_image)
                    ocr_text = " ".join([res[1] for res in ocr_result])
                text += ocr_text + "\n"
    return text.strip()


def extract_docx_text(file_path: str) -> str:
    """Extract text from a DOCX using python-docx."""
    doc = docx.Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.strip()


def extract_txt(file_path: str) -> str:
    """Read text from a plain TXT file."""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read().strip()


def save_as_markdown(text: str, output_path: str):
    """Save extracted text into Markdown format with basic formatting."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Extracted Text\n\n")
        for line in text.splitlines():
            # If line is ALL CAPS → treat it as a heading
            if line.strip().isupper() and len(line.split()) < 10:
                f.write(f"## {line.strip()}\n\n")
            else:
                f.write(line.strip() + "\n")
    print(f"✅ Extracted text saved to {output_path}")


# Command-line support
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract text from PDF, DOCX, TXT (with OCR) and save to Markdown.")
    parser.add_argument("file", help="Path to the input file")
    parser.add_argument("-o", "--output", help="Path to save extracted text (optional, defaults to .md)")

    args = parser.parse_args()
    extracted_text = extract_text(args.file)

    # Default output filename if not provided
    if args.output:
        output_path = args.output
    else:
        base, _ = os.path.splitext(args.file)
        output_path = base + "_extracted.md"

    save_as_markdown(extracted_text, output_path)


