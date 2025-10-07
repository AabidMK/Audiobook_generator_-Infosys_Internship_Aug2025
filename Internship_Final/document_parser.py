import os
from pdfparse import extract_pdf_text
from pptparse import extract_ppt_text
from imageparse import extract_image_text
from docxparse import extract_docx_text
def write_to_markdown(content, md_path):
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(content)
def extract_to_markdown(file_path, md_path="output.md"):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        content = extract_pdf_text(file_path)
    elif ext == ".docx":
        content = extract_docx_text(file_path)
    elif ext in [".png", ".jpg", ".jpeg", ".bmp", ".tiff"]:
        content = extract_image_text(file_path)
    elif ext == ".pptx":
        content = extract_ppt_text(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a PDF, DOCX, PPTX, or image.")
    write_to_markdown(content, md_path)