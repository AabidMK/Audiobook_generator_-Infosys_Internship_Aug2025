import os
import google.genai as genai

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("API key not found! Set GEMINI_API_KEY as an environment variable.")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-1.5-flash",
    contents="Explain how AI works in a simple way"
)

print(response.text)
