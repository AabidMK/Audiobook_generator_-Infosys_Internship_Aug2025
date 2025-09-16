import asyncio
import edge_tts
from pypdf import PdfReader

async def text_to_speech(text, output_file, voice="en-US-AriaNeural"):
    """Convert text to speech and save as MP3"""
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)
    print(f"✅ Audio saved at {output_file}")

def extract_text_from_pdf(pdf_path):
    """Extract text from all pages of a PDF"""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

if __name__ == "__main__":
    pdf_file = "AI AudioBook Generator.pdf"     
    output_file = "book_audio.mp3"  

    # Step 1: Extract text
    text = extract_text_from_pdf(pdf_file)

    # Optional: Limit text length (Edge TTS works best with smaller chunks)
    # For big books, you should split text into parts
    text = text[:4000]   # first 4000 characters (avoid too long requests)

    # Step 2: Convert to speech
    asyncio.run(text_to_speech(text, output_file))
