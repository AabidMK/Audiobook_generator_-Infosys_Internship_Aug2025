import os
from tomarkdown import extract_to_markdown
from dotenv import load_dotenv
import google.generativeai as genai
from TTS.api import TTS
# Extract to Markdown
extract_to_markdown(
    r"F:\Internship\1.5 Basics of Neural Network.pptx",
    "F:/Internship/output (4).md"
)

#  Load API keys from .env
load_dotenv(dotenv_path=r"F:\Internship\secrets.env")

google_api_key = os.getenv("GOOGLE_API_KEY")

# Configure Gemini
genai.configure(api_key=google_api_key)

#  Read the extracted Markdown content
with open("F:/Internship/output (4).md", "r", encoding="utf-8") as f:
    markdown_content = f.read()

#Prompt for Gemini text generation
prompt = f"""
You are an expert Conceptual Explainer and Professional Audiobook Narrator.
I will provide you with raw, parsed text extracted from a document.
Your job is to transform this text into a polished, audiobook-ready narration that is clear, deeply understandable, and fully engaging for listeners.

Guidelines to Follow:

1. Preserve Completeness:
    - Do not shorten, summarize, or omit any part of the original text.
    - Every concept and detail must remain fully intact and accurately conveyed.

2. Clean the Text:
    - Remove irrelevant elements such as headers, footers, page numbers, references, and formatting artifacts.
    - Fix broken sentences or parsing issues so they form complete, natural-sounding statements.

3. Ensure Deep Understanding:
    - Rewrite the content into clear, listener-friendly language that teaches or explains concepts thoroughly.
    - Break down complex ideas step-by-step so they are easy to grasp.
    - Use smooth transitions to maintain a logical flow and keep the listener engaged.

4. Expand for Clarity (When Needed):
    - If a sentence or idea is vague or confusing, slightly expand it for better understanding while staying true to the original meaning.
    - Do not add external information or personal commentary — only clarify what is present in the source text.

5. Audiobook Flow:
    - Ensure the narration flows naturally as if being read aloud, with consistent pacing and tone.
    - The style should feel like a knowledgeable teacher guiding the listener through the material.

6. Final Output:
    - Provide only the finalized audiobook narration, ready for direct Text-to-Speech (TTS) conversion.
    - Do not include instructions, notes, or metadata — just the clean narration.

Here is the parsed text:

{markdown_content}
"""

#  Generate audiobook text using Gemini
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(prompt)

cleaned_text = response.text


with open(r"F:\Internship\llmoutput.txt", "w", encoding="utf-8") as f:
    f.write(cleaned_text)
    
def generate_tts(cleaned_text):
    tts = TTS(model_name="tts_models/en/ljspeech/glow-tts")

    tts.tts_to_file(text=cleaned_text, file_path="voice_change.wav")
generate_tts(cleaned_text)


