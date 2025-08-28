import os
import pdfplumber
import docx
from PIL import Image
from tkinter import Tk, filedialog


# ---------- Extractors ----------
def extract_pdf(path: str) -> str:
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.strip()


def extract_docx(path: str) -> str:
    d = docx.Document(path)
    return "\n".join(p.text for p in d.paragraphs).strip()


def extract_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read().strip()


def extract_image(path: str, use_easyocr: bool = True) -> str:
    text = ""
    if use_easyocr:
        # Lazy import to avoid environment issues when OCR is not needed
        try:
            import easyocr
        except ImportError:
            raise RuntimeError("easyocr not installed. Install with: pip install easyocr")
        reader = easyocr.Reader(["en"])
        result = reader.readtext(path, detail=0)
        text = "\n".join(result)
    else:
        try:
            import pytesseract
        except ImportError:
            raise RuntimeError("pytesseract not installed. Install with: pip install pytesseract")
        text = pytesseract.image_to_string(Image.open(path))
    return text.strip()


# ---------- Save Markdown ----------
def save_as_markdown(text: str, input_path: str) -> str:
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_path = f"{base_name}.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# Extracted Text from {os.path.basename(input_path)}\n\n")
        f.write(text)
    print(f"Text saved to {output_path}")
    return output_path


# ---------- Dispatcher ----------
def extract_text(file_path: str, use_easyocr: bool = True) -> str:
    ext = os.path.splitext(file_path)[-1].lower()

    if ext == ".pdf":
        text = extract_pdf(file_path)
    elif ext == ".docx":
        text = extract_docx(file_path)
    elif ext == ".txt":
        text = extract_txt(file_path)
    elif ext in [".png", ".jpg", ".jpeg", ".tiff", ".bmp"]:
        text = extract_image(file_path, use_easyocr=use_easyocr)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    save_as_markdown(text, file_path)
    return text


# ---------- GUI File Picker ----------
if __name__ == "__main__":
    print("Text Extraction Script Started")
    root = Tk()
    root.withdraw()   # Hide the main Tk window
    root.update()     # Ensure Tk initializes properly before opening dialog

    file_path = filedialog.askopenfilename(
        title="Select a PDF, DOCX, TXT, or Image file",
        filetypes=(
            ("Supported files", "*.pdf *.docx *.txt *.png *.jpg *.jpeg *.tiff *.bmp"),
            ("All files", "*.*"),
        ),
    )

    if file_path:
        print(f"Selected File: {file_path}")
        # Set use_easyocr=True to use EasyOCR; set to False to use pytesseract
        text = extract_text(file_path, use_easyocr=True)
        print("\n--- Extracted Text ---\n")
        print(text)  # print entire text with no limit
    else:
        print("No file selected.")
