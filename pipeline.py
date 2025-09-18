# pipeline.py

from extraction import extract_text
from enrichment import rewrite_text_with_gemini as enrich_text
from coqui import generate_audio

def main(file_path, output_audio):
    print("🚀 Starting Audiobook Generator Pipeline")

    # Step 1: Extract text
    print("📄 Extracting text...")
    raw_text = extract_text(file_path)

    # Step 2: Enrich text (cleaning, summarization, etc.)
    print("✨ Enriching text...")
    enriched_text = enrich_text(raw_text)

    # Step 3: Generate audio
    print("🎧 Generating audio...")
    generate_audio(enriched_text, output_audio)

    print("✅ Pipeline completed. Audio saved at:", output_audio)

if __name__ == "__main__":
    # Example usage
    input_file = "ronaldo.pdf"
    output_audio = "output.mp3"
    main(input_file, output_audio)


