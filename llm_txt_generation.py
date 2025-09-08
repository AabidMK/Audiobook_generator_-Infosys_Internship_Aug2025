import os
from pathlib import Path
import google.generativeai as genai
from tkinter import Tk, filedialog

from PyPDF2 import PdfReader
import docx
import pytesseract
from PIL import Image

# 🔹 Configure Gemini with API Key (store API key in environment variable)
genai.configure(api_key=os.getenv("API KEY"))

# 🔹 Extract text from TXT
def extract_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# 🔹 Extract text from DOCX
def extract_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])

# 🔹 Extract text from PDF
def extract_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()

# 🔹 Extract text from Images using OCR
def extract_image(file_path):
    image = Image.open(file_path)
    return pytesseract.image_to_string(image)

# 🔹 Rewrite using Gemini with detailed instructions
# 🔹 Rewrite using Gemini with audiobook enrichment (handles large files by chunking)
def rewrite_text_with_gemini(text: str, chunk_size: int = 3000) -> str:
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Split text into smaller chunks
        words = text.split()
        chunks = [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

        rewritten_chunks = []
        for i, chunk in enumerate(chunks, start=1):
            print(f"[INFO] Processing chunk {i}/{len(chunks)}...")

            prompt = f"""
You are an expert audiobook editor and narrator. Your task is to rewrite the following extracted text
to make it **enriched, engaging, and clear for audiobook narration**.

Instructions:
1. Enrich the text by improving clarity, readability, and narrative flow — without altering the core meaning.  
2. Use smooth, natural, and conversational language so it feels like it’s being spoken to a listener.  
3. Add subtle emphasis and variation in phrasing to keep the narration lively and engaging.  
4. Break long paragraphs into shorter, audiobook-friendly segments.  
5. Ensure logical transitions between sections so the listener feels guided through the content.  
6. Correct grammar, remove noise/duplication (common in OCR/PDF), and make sentences fluid.  
7. If lists or bullet points exist, format them clearly so they can be easily spoken aloud.  
8. Preserve all important facts, numbers, and details — do not remove meaning.  
9. Do NOT invent or hallucinate information; only rewrite and enrich what’s provided.  
10. Final text should sound like a polished audiobook script, ready for narration.  

Now, rewrite and enrich the following text:

{chunk}
"""

            response = model.generate_content(prompt)
            rewritten_chunks.append(response.text)

        return "\n\n".join(rewritten_chunks)

    except Exception as e:
        return f"[ERROR] LLM rewriting failed: {e}"

# 🔹 Save to Markdown
def save_as_md(content, input_file):
    output_file = Path(input_file).stem + "_rewritten.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[+] Rewritten content saved as: {output_file}")

# 🔹 Main
def main():
    # File selection dialog
    Tk().withdraw()  # Hide Tkinter root window
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("All Supported", "*.pdf *.docx *.txt *.jpg *.jpeg *.png")]
    )

    if not file_path:
        print("No file selected.")
        return

    ext = Path(file_path).suffix.lower()

    if ext == ".txt":
        extracted_text = extract_text_file(file_path)
    elif ext == ".docx":
        extracted_text = extract_docx(file_path)
    elif ext == ".pdf":
        extracted_text = extract_pdf(file_path)
    elif ext in [".jpg", ".jpeg", ".png"]:
        extracted_text = extract_image(file_path)
    else:
        print(f"[!] Unsupported format: {ext}")
        return

    print("\n[INFO] Extracted text preview:")
    print(extracted_text[:500], "...")  # preview first 500 chars

    rewritten_text = rewrite_text_with_gemini(extracted_text)
    save_as_md(rewritten_text, file_path)


if __name__ == "__main__":
    main()

