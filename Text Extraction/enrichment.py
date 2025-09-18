import fitz  # PyMuPDF
import google.generativeai as genai

API_KEY =  "YOUR_API_KEY"  
PDF_FILE = "ronaldo.pdf"
MARKDOWN_FILE = "rewritten_output.md"

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text.strip()

def rewrite_text_with_gemini(text):
    genai.configure(api_key=API_KEY)

    #  Use system prompt so it REWRITES instead of summarising
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=(
            "You are an audiobook narrator. Rewrite the input text so it is natural, "
            "engaging, and listener-friendly. Do NOT summarise or shorten. "
            "Preserve all details and structure, but improve clarity, flow, and narration style."
        )
    )

    response = model.generate_content(text)
    return response.text

if __name__ == "__main__":
    print("Extracting text from PDF...")
    extracted_text = extract_text_from_pdf(PDF_FILE)

    if not extracted_text:
        print("No text found in the PDF.")
    else:
        print("Sending text to Gemini for rewriting...")
        rewritten_text = rewrite_text_with_gemini(extracted_text)

        print("\n Rewritten Text:\n")
        print(rewritten_text)

        with open(MARKDOWN_FILE, "w", encoding="utf-8") as f:
            f.write("# Rewritten PDF Content\n\n")
            f.write(rewritten_text)

        print(f"\n Output saved to: {MARKDOWN_FILE}")