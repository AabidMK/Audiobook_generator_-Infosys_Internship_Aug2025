import os
import argparse
from openai import OpenAI
from Text_extractor import extract_text

client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="not-needed"  
)

MODEL_NAME = "mistralai/mistral-7b-instruct-v0.3"

def chunk_text(text, max_chunk_size=2000):
    """
    Split text into smaller chunks so they fit within the LLM context window.
    """
    words = text.split()
    chunks, current_chunk = [], []

    for word in words:
        if sum(len(w) for w in current_chunk) + len(current_chunk) + len(word) > max_chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
        current_chunk.append(word)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def rewrite_with_lmstudio(text: str) -> str:
    """
    Rewrite text using LM Studio's local LLM API with system prompt.
    Handles long inputs by chunking them.
    """
    chunks = chunk_text(text, max_chunk_size=2000)
    rewritten_chunks = []

    for i, chunk in enumerate(chunks, 1):
        print(f"🔍 Sending chunk {i}/{len(chunks)} to LM Studio...")

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": (
                        "You are a professional audiobook narrator and editor. Your job is to take raw extracted text from books, reports, or documents and rewrite it so that it flows naturally when spoken aloud. Guidelines:- Preserve the original meaning, facts, and key ideas.- Rewrite in a smooth, conversational, and engaging style, suitable for listening.- Break long, complex sentences into shorter, easier-to-follow sentences.- Add slight storytelling flair where appropriate, but do not invent new information.- Ensure the tone is clear, pleasant, and keeps the listener’s attention.- Format headings and sections in Markdown (#, ##, etc.) so the structure is preserved for later audiobook narration."
                        f"Text:\n{chunk}"
                    )
                }
            ],
            temperature=0.7,
            max_tokens=1000
        )

        rewritten_text = response.choices[0].message.content.strip()
        rewritten_chunks.append(rewritten_text)

    return "\n\n".join(rewritten_chunks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract and rewrite text with LM Studio (local LLM).")
    parser.add_argument("file", help="Path to input PDF/DOCX/TXT file")
    parser.add_argument("-o", "--output", help="Path to save rewritten Markdown")
    args = parser.parse_args()

    # Step 1: Extract text
    raw_text = extract_text(args.file)

    # Step 2: Rewrite with LM Studio
    rewritten = rewrite_with_lmstudio(raw_text)

    # Step 3: Save as Markdown
    output_path = args.output or os.path.splitext(args.file)[0] + "_rewritten.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Rewritten Text\n\n")
        f.write(rewritten)

    print(f"✅ Rewritten text saved to {output_path}")


