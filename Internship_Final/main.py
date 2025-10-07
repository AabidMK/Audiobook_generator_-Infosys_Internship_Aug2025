import os
from document_parser import extract_to_markdown
from dotenv import load_dotenv
import google.generativeai as genai
from totts import generate_tts
from ragcall import rag_call
file_path = r"F:\Internship\1.5 Basics of Neural Network.pptx"
# Extract to Markdown
extract_to_markdown(
    file_path,
    "F:/Internship/output (4).md"
)

# Load API keys from .env
load_dotenv(dotenv_path=r"F:\Internship\secrets.env")
google_api_key = os.getenv("GOOGLE_API_KEY")


# Configure Gemini
genai.configure(api_key=google_api_key)

# Read the extracted Markdown content
with open("F:/Internship/output (4).md", "r", encoding="utf-8") as f:
    markdown_content = f.read()

# Prompt for Gemini text generation
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

4. Handle Technical Content Naturally:
    - When encountering symbols, formulas, or calculations, focus on explaining their meaning and purpose rather than reading them literally.
    - Express them in natural, descriptive language that a listener can easily understand.
    - If there are step-by-step calculations, walk the listener through the process clearly and conclude with the final result in spoken form.
    - Ensure that even technical or numerical information flows naturally in the narration and avoids awkward or robotic phrasing.

5. Expand for Clarity (When Needed):
    - If a sentence or idea is vague or confusing, slightly expand it for better understanding while staying true to the original meaning.
    - Do not add external information or personal commentary — only clarify what is present in the source text.

6. Audiobook Flow:
    - Maintain a consistent, engaging tone as if you are a skilled teacher guiding the listener.
    - Ensure smooth pacing and natural speech patterns to create a pleasant listening experience.

7. Final Output:
    - Provide only the finalized audiobook narration, ready for direct Text-to-Speech (TTS) conversion.
    - Do not include instructions, notes, or metadata — just the clean narration.
    - also dont add intro as llm make intro as topic based intro

Here is the parsed text:

{markdown_content}

"""
# print(markdown_content)

MODEL_NAME = "models/learnlm-2.0-flash-experimental"

# Instantiate the model without the timeout parameter
model = genai.GenerativeModel(model_name=MODEL_NAME)

# Now, generate content and set the timeout within request_options
response = model.generate_content(
    prompt,
    request_options={"timeout": 600}  # Set the timeout in seconds here
)
cleaned_text = response.text

# Save the generated text
with open(r"F:\Internship\llmoutput.txt", "w", encoding="utf-8") as f:
    f.write(cleaned_text)

# Call TTS and RAG functions
generate_tts(cleaned_text)
rag_call(cleaned_text,file_path)
