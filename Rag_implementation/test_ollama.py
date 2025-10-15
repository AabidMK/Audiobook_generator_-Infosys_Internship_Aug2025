import requests
import json

def query_ollama(model: str, prompt: str):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    resp = requests.post(url, json=payload)
    resp.raise_for_status()
    data = resp.json()
    return data.get("response", "")

if __name__ == "__main__":
    model = "gemma3:1b"
    prompt = "Hello, can you explain what an audiobook is in 2 sentences?"
    print("Sending prompt to Ollama:", prompt)
    answer = query_ollama(model, prompt)
    print("\n=== Ollama Response ===")
    print(answer)
