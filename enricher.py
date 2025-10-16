# enricher.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

# ✅ Load .env file automatically
load_dotenv()

# ✅ Read API key from .env
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file")

genai.configure(api_key=api_key)

# ✅ Prefer Pro model, fallback to Flash if unavailable
def get_model():
    try:
        return genai.GenerativeModel("gemini-2.5-pro")
    except Exception:
        print("⚠️ Falling back to gemini-2.5-flash")
        return genai.GenerativeModel("gemini-2.5-flash")

model = get_model()

def enrich_text(text: str) -> str:
    """
    Takes raw extracted text and enhances it for audiobook narration.
    Example: fixing grammar, making sentences smoother, etc.
    """
    prompt = f"""
    You are an audiobook text enhancer.
    Improve this text for clarity and narration while keeping meaning intact.
    Input:
    {text}
    """

    try:
        response = model.generate_content(prompt)
        # Some responses may be in .text or in candidates
        if hasattr(response, "text") and response.text:
            return response.text.strip()
        elif hasattr(response, "candidates") and response.candidates:
            return response.candidates[0].content.parts[0].text.strip()
        else:
            return text  # fallback
    except Exception as e:
        print(f"⚠️ Enrichment failed: {e}")
        return text  # fallback
