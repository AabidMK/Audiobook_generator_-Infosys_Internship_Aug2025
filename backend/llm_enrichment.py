import google.generativeai as genai
import os

def enrich_text_with_llm(text, lang_code="en"):
    """
    Rewrites the given text for an engaging audiobook narration 
    using the Gemini API, ensuring it's in the correct language.

    Args:
        text (str): The text to enrich.
        lang_code (str): Target language (default: 'en').
    """
    if not os.getenv("GOOGLE_API_KEY"):
        print("API key not found. Please set the GOOGLE_API_KEY environment variable.")
        return text 

    try:
        genai.api_key = os.getenv("GOOGLE_API_KEY")
        model_name = "gemini-2.5-flash-preview-05-20"
        model = genai.GenerativeModel(model_name)

        response = model.generate_content(
            f"Rewrite the following text in {lang_code} for an engaging audiobook narration. "
            f"Make it clear, expressive, and conversational. Keep the language strictly {lang_code}:\n\n{text}"
        )

        if response.candidates and response.candidates[0].content.parts:
            return response.candidates[0].content.parts[0].text
        return text

    except Exception as e:
        print(f"An error occurred during LLM enrichment: {e}")
        return text