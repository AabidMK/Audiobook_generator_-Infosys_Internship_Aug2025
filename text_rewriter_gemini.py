import os
import sys
import google.generativeai as genai

from extract_text import extract_text, save_to_markdown

API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-1.5-flash"
model = genai.GenerativeModel(MODEL_NAME)

def split_into_chunks(text, max_chars=8000):
    if len(text) <= max_chars:
        return [text]
    parts, current = [], []
    size = 0
    for para in text.split("\n\n"):
        block = (para + "\n\n")
        if size + len(block) > max_chars and current:
            parts.append("".join(current))
            current, size = [], 0
        current.append(block)
        size += len(block)
    if current:
        parts.append("".join(current))
    return parts

NARRATION_PROMPT_PREFIX = (
    "Rewrite the following text into a smooth, listener-friendly audiobook narration. "
    "Keep all facts accurate and do not add extra information. "
    "Focus on clarity, natural flow, and conversational tone. "
    "Use shorter sentences and well-paced paragraphs to make it engaging for listening. "
    "Return only the rewritten narration as plain text.\n\n"
)

def rewrite_with_gemini(text: str) -> str:
    chunks = split_into_chunks(text, max_chars=8000)
    outputs = []
    for i, chunk in enumerate(chunks, start=1):
        prompt = NARRATION_PROMPT_PREFIX + chunk
        resp = model.generate_content(prompt)
        outputs.append(resp.text or "")
        print(f"Chunk {i}/{len(chunks)} rewritten.")
    return "\n\n".join(outputs).strip()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        inpath = input("Enter path to your PDF or DOCX file: ").strip()
    else:
        inpath = sys.argv[1]

    print(f"Extracting text from: {inpath}")
    raw_text = extract_text(inpath)

    if not raw_text or not raw_text.strip():
        print("No text extracted.")
        sys.exit(1)

    print("Sending text to Gemini...")
    rewritten = rewrite_with_gemini(raw_text)

    if not rewritten:
        print("LLM returned empty output.")
        sys.exit(1)

    out_file = "narration_output.md"
    save_to_markdown(rewritten, out_file)
    print(f"Done. Rewritten narration saved to: {out_file}")