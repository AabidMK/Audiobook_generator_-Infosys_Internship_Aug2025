import os
import asyncio
import aiohttp
import fitz
import docx
import edge_tts

#TEXT EXTRACTION

class TextExtraction:
    @staticmethod
    def extract_text_from_pdf(file_path):
        text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        return text

    @staticmethod
    def extract_text_from_docx(file_path):
        doc_obj = docx.Document(file_path)
        return "\n".join([p.text for p in doc_obj.paragraphs])

    @staticmethod
    def extract_text_from_txt(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def extract_text(file_path):
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            return TextExtraction.extract_text_from_pdf(file_path)
        elif ext == ".docx":
            return TextExtraction.extract_text_from_docx(file_path)
        elif ext == ".txt":
            return TextExtraction.extract_text_from_txt(file_path)
        else:
            return f"Error: Unsupported file type {ext}"


# GEMINI REWRITER

class GeminiRewriter:
    def __init__(self, api_key):
        self.api_key = api_key
        if not self.api_key:
            raise ValueError("❌ Missing GEMINI_API_KEY")

        self.prompt = """You are an expert audiobook narrator. 
Rewrite the following text into engaging, listener-friendly audiobook style, 
keeping all key information accurate:"""

    async def rewrite(self, text: str) -> str:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
        payload = {
            "contents": [{"parts": [{"text": f"{self.prompt}\n\n{text}"}]}],
            "generationConfig": {"maxOutputTokens": 2048}
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, timeout=60) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data["candidates"][0]["content"]["parts"][0]["text"].strip()
                else:
                    raise RuntimeError(f"Gemini API error {resp.status}: {await resp.text()}")


#EDGE TTS SYNTHESIS

class EdgeTTS:
    def __init__(self, voice="en-US-AriaNeural", rate="+0%", volume="+0%"):
        self.voice = voice
        self.rate = rate
        self.volume = volume

    async def speak_to_file(self, text: str, out_file: str):
        tts = edge_tts.Communicate(text, voice=self.voice, rate=self.rate, volume=self.volume)
        await tts.save(out_file)
        print(f"🎧 Audio saved: {out_file}")


# MAIN PIPELINE

async def main():

    input_file = "AI AudioBook Generator.pdf"
    output_dir = "audiobook_output"
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Extract text
    raw_text = TextExtraction.extract_text(input_file)
    print(f"📖 Extracted {len(raw_text)} characters")

    # Step 2: Rewrite with Gemini (pass your API key here)
    GEMINI_API_KEY = "AIzaSyCcW4Uob-viODFMxoyXU571bHig6A9D0b4"
    rewriter = GeminiRewriter(api_key=GEMINI_API_KEY)
    rewritten_text = await rewriter.rewrite(raw_text)
    print("✅ Text rewritten by Gemini")

    # Save rewritten text
    md_file = os.path.join(output_dir, "audiobook_text.md")
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(rewritten_text)
    print(f"📂 Saved audiobook text: {md_file}")

    # Step 3: Convert to audio with Edge TTS
    tts = EdgeTTS(voice="en-US-AriaNeural")
    audio_file = os.path.join(output_dir, "audiobook.mp3")
    await tts.speak_to_file(rewritten_text, audio_file)



if __name__ == "__main__":
    asyncio.run(main())
