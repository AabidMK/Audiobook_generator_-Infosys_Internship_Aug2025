import requests
import logging

class OllamaLLMAnswerGenerator:
    """Call Ollama locally (Gemma3, Llama, Mistral, etc.)"""

    def __init__(self, model_name: str = "gemma3:1b", host: str = "http://localhost:11434"):
        self.model_name = model_name
        self.url = f"{host}/api/generate"
        logging.info(f"Loaded local LLM: {self.model_name} (via Ollama)")

    def generate(self, question: str, context: str, max_tokens: int = 1500) -> str:
        """Send prompt + context to Ollama and return best answer."""
        prompt = f"""
You are an assistant answering questions using ONLY the provided context. 
Do not invent information. 
Always answer concisely in 2–4 sentences.

Context:
{context}

Question: {question}

Answer:
"""
        try:
            resp = requests.post(self.url, json={
                "model": self.model_name,
                "prompt": prompt,
                "stream": False
            })
            resp.raise_for_status()
            data = resp.json()
            return data.get("response", "").strip()
        except Exception as e:
            logging.error(f"Ollama request failed: {e}")
            return "Error: could not get answer from Ollama."
