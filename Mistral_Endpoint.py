from flask import Flask, request, jsonify
import os
from Text_Extraction_Module import extract_text
import requests

LMSTUDIO_API_URL = "http://192.168.56.1:1234/v1/chat/completions"  # LM Studio endpoint
MODEL_NAME = "mistral-7b-instruct-v0.3"
CHUNK_SIZE = 12000  # Approx 12k tokens per chunk, adjust per model context limit

def chunk_text(text, chunk_size):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i:i + chunk_size])

def enrich_text(text_chunk):
    try:
        prompt = f"[INST] Please convert the following book text into engaging audiobook-style narration. Keep the output lively, fun and interesting to hear. Here is the text:\n\n{text_chunk}\n[/INST]"
        payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 2048  # Adjust as needed
        }
        response = requests.post(LMSTUDIO_API_URL, json=payload)
        response.raise_for_status()  # Raise error if status != 200
        response_json = response.json()
        # Correct access to the API response
        return response_json['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error calling LM Studio API: {e}")
        return ""


app = Flask(__name__)

@app.route('/enriched_book', methods=['POST'])
def enrich_book():
    uploaded_file = request.files['file']
    save_path = os.path.join(os.getcwd(), uploaded_file.filename)
    uploaded_file.save(save_path)

    # Step 1: Extract text
    extracted_text = extract_text(save_path)  # Your function, returns plain text
    with open("extracted_text.md", "w", encoding="utf-8") as f:
        f.write(extracted_text)
    
    # Step 2: Chunk and enrich
    enriched_chunks = []
    for chunk in chunk_text(extracted_text, CHUNK_SIZE):
        enriched = enrich_text(chunk)
        print("Enriched chunk preview:", enriched[:200])
        enriched_chunks.append(enriched)
    
    enriched_text = "\n\n".join(enriched_chunks)
    with open("enriched_text.md", "w", encoding="utf-8") as f:
        f.write(enriched_text)

    return jsonify({"status": "success", "output": "enriched_text.md"})

if __name__ == '__main__':
    app.run(port=8000)
