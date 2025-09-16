import sys
import asyncio
from pathlib import Path
from tkinter import Tk, filedialog

# Import our modular scripts
from extract_txt import extract_text_file
from extract_docx import extract_docx
from extract_pdf import extract_pdf
from extract_image import extract_image
from llm_txt_generation import rewrite_text_with_gemini
from tts_enhancer import text_to_speech
from utils import save_text_output, save_as_md


def select_file():
    """Open a GUI dialog to select a supported file"""
    Tk().withdraw()  # hide the root window
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[
            ("All supported", "*.txt *.docx *.pdf *.jpg *.jpeg *.png"),
            ("Text files", "*.txt"),
            ("Word documents", "*.docx"),
            ("PDF files", "*.pdf"),
            ("Images", "*.jpg *.jpeg *.png"),
        ],
    )
    return file_path


async def main():
    #  Select file via GUI
    input_file = select_file()
    if not input_file:
        print("[!] No file selected. Exiting.")
        sys.exit(1)

    ext = Path(input_file).suffix.lower()

    # 2️⃣ Extract text
    print("[INFO] Extracting text...")
    if ext == ".txt":
        extracted_text = extract_text_file(input_file)
    elif ext == ".docx":
        extracted_text = extract_docx(input_file)
    elif ext == ".pdf":
        extracted_text = extract_pdf(input_file)
    elif ext in [".jpg", ".jpeg", ".png"]:
        extracted_text = extract_image(input_file)
    else:
        print(f"[!] Unsupported file type: {ext}")
        sys.exit(1)

    if not extracted_text.strip():
        print("[!] No text extracted. Exiting.")
        sys.exit(1)

    #  Save extracted text
    save_text_output(extracted_text, input_file)

    # Rewrite using Gemini
    print("[INFO] Rewriting text with Gemini...")
    rewritten_text = rewrite_text_with_gemini(extracted_text)

    #  Save rewritten text
    save_as_md(rewritten_text, input_file)

    # Generate audiobook
    print("[INFO] Generating audiobook...")
    output_file = Path(input_file).stem + "_audiobook.mp3"
    await text_to_speech(rewritten_text, output_file)

    print(f"[DONE] Full pipeline complete! Audiobook saved as: {output_file}")


if __name__ == "__main__":
    asyncio.run(main())
