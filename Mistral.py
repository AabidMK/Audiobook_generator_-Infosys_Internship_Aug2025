# audiobook_api.py

import os
from urllib import response
import requests
from Text_Extraction_Module import extract_text

# CONFIG
LM_API_URL = "http://localhost:1234/v1/chat/completions"  # Change based on LM Studio settings
MODEL_ID = "mistral-7b-instruct-v0.3"
CHUNK_SIZE = 2048  # adjust based on model's context window (tokens)
SYSTEM_PROMPT = (""" You are a professional audiobook narrator tasked with converting the following text into an engaging, fun, and easy-to-listen-to audiobook-style narration. Your task is to:
    - Carefully preserve at least 80 percent of the original text content by character length, without summarizing, deleting, or omitting important text.
    - Clearly announce section titles such as "Abstract", "Introduction", "Chapter X", "Conclusion", and distinctly mark them with engaging phrasing and natural pauses.
    - Emphasize important concepts, facts, or emotional points to create a lively and immersive listening experience.
    - Maintain smooth continuity with what was narrated previously, incorporating previous context seamlessly to avoid any abrupt changes or repetitions.
    - Use varied sentence structures, tone, and pacing to keep the listener's attention.
    - Do not add unrelated content, questions, or answers not found in the original.
    - Treat the given text as the authoritative source and enrich only the style and presentation without altering the meaning.
    Below is the text for narration:""")
# ("Convert the following text into engaging audiobook-style narration without summarizing or deleting any of the information mentioned. "
#     "Make it fun, interesting, and easy to listen to:\n")
# """Convert the following academic text into engaging audiobook-style narration. Make it fun, interesting, and easy to listen to. Clearly announce section titles (e.g., 'Abstract', 'Introduction', 'Conclusion') and differentiate sections using phrasing and pauses. Emphasize important parts. without summarizing or deleting any of the information mentioned. Here is the text:"""

def chunk_text(text, chunk_size=CHUNK_SIZE):
    """Splits text into chunks under model's token/context window."""
    paragraphs = text.split('\n\n')
    chunks, curr_chunk = [], ""
    for para in paragraphs:
        if len(curr_chunk) + len(para) < chunk_size:
            curr_chunk += para + "\n\n"
        else:
            chunks.append(curr_chunk.strip())
            curr_chunk = para + "\n\n"
    if curr_chunk.strip(): chunks.append(curr_chunk.strip())
    return chunks

def get_context_summary(text, max_length=300):
    """
    Extract a summary or last portion of the previous enriched text to carry over as context.
    Keeps max_length characters to fit in context window.
    """
    # Simple approach: get last max_length characters, feel free to replace with summarization
    return text[-max_length:] if len(text) > max_length else text

def run_mistral_on_chunk(input_text, api_url=LM_API_URL):
    headers = {"Content-Type": "application/json"}

    payload = {
        "model": MODEL_ID,
        "messages": [
            {"role": "user", "content": SYSTEM_PROMPT + input_text}
        ],
        "max_tokens": CHUNK_SIZE,
        "temperature": 0.85
    }
    response = requests.post(api_url, json=payload, headers=headers)
    if not response.ok:
        print(f"API error details: {response.status_code} {response.text}")
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']

def process_book_to_audiobook(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        raw_text = f.read()

    chunks = chunk_text(raw_text)
    enriched_chunks = []
    carried_context = ""  # Store previous enriched content snippet

    for idx, chunk in enumerate(chunks):
        print(f"Processing chunk {idx+1}/{len(chunks)}")

        # Concatenate carried context summary with current chunk text
        prompt_input = ""
        if carried_context:
            prompt_input += f"Previously narrated excerpt:\n{carried_context}\n\n"
        prompt_input += chunk

        enriched_text = run_mistral_on_chunk(prompt_input)
        enriched_chunks.append(enriched_text + "\n\n")

        # Update carried context for next chunk processing
        carried_context = get_context_summary(enriched_text, max_length=300)

    enriched_book = "".join(enriched_chunks)
    with open(output_file, "w", encoding="utf-8") as out_f:
        out_f.write(enriched_book)

    print(f"Enriched audiobook narration saved to {output_file}")

# Usage example pointing to the extracted text file
process_book_to_audiobook("extracted_text.md", "enriched_text.md")

