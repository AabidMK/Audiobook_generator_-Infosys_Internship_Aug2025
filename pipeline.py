from text_extraction import extract_text
from text_enrichment import enrich_text
from audio_generation import generate_audio

def main():
    # Step 1: Extract text
    file_path = input("Enter the file path (.pdf, .docx, .png, .jpg): ")
    extracted_text, error = extract_text(file_path)

    if error:
        print(f"❌ Error: {error}")
        return
    print("✅ Text extracted successfully.")

    # Step 2: Enrich text with Gemini
    enriched_text = enrich_text(extracted_text)
    print("✅ Text enriched for audiobook narration.")

    #Step 3: Generate audio with Coqui tts
    generate_audio(enriched_text)

if __name__ == "__main__":
    main()