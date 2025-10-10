import os
from dotenv import load_dotenv
import google.generativeai as genai

def enrich_text(input_text):
# Load environment variables
    load_dotenv()
    API_KEY = os.getenv("GEMINI_API_KEY")

    if not API_KEY:
        raise ValueError("API key not found. Make sure GEMINI_API_KEY is set in your .env file.")
# Configure Gemini
    genai.configure(api_key=API_KEY,transport="rest")

# Choose a Gemini model (text-only model)
    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = f"""
You are an expert audiobook narrator.  
Your task is to transform the extracted text into listener-friendly *audiobook-ready narration* without leaving out details.  

🔹 Guidelines:
- Do NOT summarize or cut down the content. Keep all important details from the original.  
-Begin with a warm greeting such as :"Hello listeners ,welcome ...".
-Provide a short summary of what the listener will learn before diving into the content.
-Make it engaging and conversational ,not just a direct copy
- Rewrite the text so it flows naturally when spoken aloud.  
- Break down long or complex sentences into *clear, shorter sentences*.  
- Add natural *pauses* using "..." or line breaks for rhythm and engagement.  
- Remove raw Markdown symbols (#, *, -, etc.), but keep all information they represent.  
- Rewrite bullet points or lists into *spoken style*. For example: "First..., then..., finally...". 
- Expand abbreviations (e.g., "e.g." → "for example", "etc." → "and so on").  
- Just make it more engaging, warm, and listener-friendly.  

 Here is the extracted content:
{input_text}
"""
    response = model.generate_content(prompt)
    return response.text
