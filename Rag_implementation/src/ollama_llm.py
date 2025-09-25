import requests
import logging

class OllamaLLMAnswerGenerator:
    def __init__(self, model_name: str = "gemma3:1b", host: str = "http://localhost:11434"):
        self.model_name = model_name
        self.url = f"{host}/api/generate"
        self.verify_ollama()

    def verify_ollama(self) -> None:
        try:
            resp = requests.get("http://localhost:11434/api/tags")
            resp.raise_for_status()
            logging.info(f"Initialized Ollama with model: {self.model_name}")
        except Exception as e:
            raise RuntimeError(f"Ollama service not available: {e}")

    def generate(self, question: str, context: str) -> str:
        try:
            # Simplified prompt template
            prompt = (
                f"Context:\n{context}\n\n"
                f"Question: {question}\n\n"
                f"Answer:"
            )

            resp = requests.post(
                self.url,
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.7,
                    "num_predict": 2000  # Using num_predict instead of max_tokens
                },
                timeout=30
            )
            resp.raise_for_status()
            return resp.json()["response"].strip()
        except Exception as e:
            logging.error(f"Generation error: {e}")
            raise