import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("API key not found. Make sure GEMINI_API_KEY is set in your .env file.")
# Configure Gemini
genai.configure(api_key=API_KEY)

# Choose a Gemini model (text-only model)
model = genai.GenerativeModel("gemini-1.5-flash")

# Step 1: Read extracted Markdown file
with open("llm_input.md", "r", encoding="utf-8") as f:
    md_content = f.read()

# Step 2: Send content to Gemini for better extraction/cleanup
prompt = f"""
You are an expert audiobook script editor.  
Your task is to transform the extracted text into *audiobook-ready narration* without leaving out details.  

🔹 Guidelines:
- Do NOT summarize or cut down the content. Keep all important details from the original.  
- Rewrite the text so it flows naturally when spoken aloud.  
- Break down long or complex sentences into *clear, shorter sentences*.  
- Add natural *pauses* using "..." or line breaks for rhythm and engagement.  
- Remove raw Markdown symbols (#, *, -, etc.), but keep all information they represent.  
- Rewrite bullet points or lists into *spoken style*. For example: "First..., then..., finally...". 
- Expand abbreviations (e.g., "e.g." → "for example", "etc." → "and so on").  
- Maintain the same depth of information, just make it more engaging, warm, and listener-friendly.  

Here is the extracted content:
{md_content}
"""

response = model.generate_content(prompt)

# Step 3: Save the improved output
output_file = "llm_extraction.md"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(response.text)

print(f"✅ Improved extraction saved to {output_file}")