import google.generativeai as genai
import os

# Set your API key from an environment variable
# The environment variable for Google's API is typically GOOGLE_API_KEY
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def enrich_text_with_llm(text):
    """
    Rewrites the given text for an engaging audiobook narration using the Gemini API.
    """
    if not os.getenv("GOOGLE_API_KEY"):
        print("API key not found. Please set the GOOGLE_API_KEY environment variable.")
        return text  # Return original text or handle error appropriately

    try:
        # Initialize the generative model
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Generate content with the specified prompt
        response = model.generate_content(
            f"Rewrite this text for an engaging audiobook narration, focusing on clarity and a conversational tone. The text is:\n\n{text}"
        )

        # Access and return the rewritten text from the response
        enriched_text = response.text
        return enriched_text

    except Exception as e:
        print(f"An error occurred during LLM enrichment: {e}")
        return text  # Return the original text in case of an error