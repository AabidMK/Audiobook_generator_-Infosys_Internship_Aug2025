import fitz  # PyMuPDF
import google.generativeai as genai

API_KEY = "AIzaSyAXfVlsUZKXYneqUkJA20vOwI5hIyGxNG0"
PDF_FILE = "invoice.pdf"
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
    # Use the working model name here
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"Rewrite the following text to improve narration and listener experience:\n\n{text}"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Gemini API Error: {e}"

if __name__ == "__main__":
    print("📄 Extracting text from PDF...")
    extracted_text = extract_text_from_pdf(PDF_FILE)

    if not extracted_text:
        print("❌ No text found in the PDF.")
    else:
        print("🚀 Sending text to Gemini for rewriting...")
        rewritten_text = rewrite_text_with_gemini(extracted_text)

        print("\n🔁 Rewritten Text:\n")
        print(rewritten_text)

        with open(MARKDOWN_FILE, "w", encoding="utf-8") as f:
            f.write("# Rewritten PDF Content\n\n")
            f.write(rewritten_text)

        print(f"\n✅ Output saved to: {MARKDOWN_FILE}")
