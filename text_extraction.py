import sys
from pathlib import Path
from tkinter import Tk, filedialog

from utils import save_text_output
from extract_txt import extract_text_file
from extract_docx import extract_docx
from extract_pdf import extract_pdf
from extract_image import extract_image


def main():
    # Hide the root Tk window
    Tk().withdraw()

    # Open file dialog
    input_file = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[
            ("All supported", "*.txt *.docx *.pdf *.jpg *.jpeg *.png"),
            ("Text files", "*.txt"),
            ("Word documents", "*.docx"),
            ("PDF files", "*.pdf"),
            ("Images", "*.jpg *.jpeg *.png"),
        ],
    )

    if not input_file:
        print("[!] No file selected. Exiting.")
        sys.exit(1)

    ext = Path(input_file).suffix.lower()
    extracted_text = ""

    try:
        if ext == ".txt":
            extracted_text = extract_text_file(input_file)
        elif ext == ".docx":
            extracted_text = extract_docx(input_file)
        elif ext == ".pdf":
            extracted_text = extract_pdf(input_file)
        elif ext in [".jpg", ".jpeg", ".png"]:
            extracted_text = extract_image(input_file)
        else:
            print(f"[!] Unsupported file format: {ext}")
            sys.exit(1)

        save_text_output(extracted_text, input_file)
        print(f"[+] Extraction complete. Saved output for {input_file}")

    except Exception as e:
        print(f"[ERROR] Failed to extract: {e}")
from pathlib import Path

def save_text_output(text, input_file):
    """
    Save extracted text into a Markdown (.md) file
    """
    input_path = Path(input_file)
    output_file = input_path.stem + "_output.md"   # Save as .md
    output_path = input_path.parent / output_file

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Extracted Content\n\n")   # Markdown header
        f.write(text)

    print(f"[+] Extracted text saved as: {output_path}")


if __name__ == "__main__":
    main()
