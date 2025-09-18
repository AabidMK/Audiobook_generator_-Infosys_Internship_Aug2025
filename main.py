import sys
from extract_text import extract_text, save_to_markdown
from text_rewriter_gemini import rewrite_with_gemini
from tts_generator import main as tts_main

def run_pipeline(input_file):
    print("Step 1: Extracting text...")
    raw_text = extract_text(input_file)
    if not raw_text.strip():
        print("No text found in the file.")
        return

    print("Step 2: Rewriting with Gemini...")
    rewritten_text = rewrite_with_gemini(raw_text)
    if not rewritten_text.strip():
        print("Gemini did not return any output.")
        return

    md_file = "narration_output.md"
    save_to_markdown(rewritten_text, md_file)
    print(f"Rewritten narration saved to {md_file}")

    print("Step 3: Generating final audiobook...")
    tts_main(md_file)

    print("Final audiobook is ready: audiobook_voice.wav")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_file>")
        sys.exit(1)

    input_path = sys.argv[1]
    run_pipeline(input_path)