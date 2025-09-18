import os
from extract_text_pdf import extract_text_from_pdf
from extract_text_docx import extract_text_from_docx
from extract_text_image import extract_text_from_image
from extract_text_plain import extract_text_from_plaintext

def extract_text(path):
    if path.lower().endswith(".pdf"):
        return extract_text_from_pdf(path)
    elif path.lower().endswith(".docx"):
        return extract_text_from_docx(path)
    elif path.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff")):
        return extract_text_from_image(path)
    elif path.lower().endswith(".txt"):
        return extract_text_from_plaintext(path)
    else:
        raise ValueError("Unsupported file format. Use PDF, DOCX, TXT, or image.")

def save_to_markdown(text, filename="output.md"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("# Extracted Document\n\n")
        f.write(text)
    return filename

if __name__ == "__main__":
    file_path = input("Enter the path to your PDF, DOCX, TXT, or image: ")
    try:
        text = extract_text(file_path)
        md_file = save_to_markdown(text, "extracted_output.md")
        print(f"Extraction complete! Markdown saved as {md_file}")
    except Exception as e:
        print(f"Error: {e}")