import requests
import logging

class OllamaLLMAnswerGenerator:
    def __init__(self, model_name="gemma3:1b", base_url="http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        logging.info(f"Initialized Ollama with model: {self.model_name}")

    def generate(self, question: str, context: str) -> str:
        prompt = (
            "Use the provided context to answer the question. "
            "Do not hallucinate. If not found, say clearly.\n\n"
            f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
        )
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={"model": self.model_name, "prompt": prompt, "stream": False},
            )
            response.raise_for_status()
            data = response.json()
            return data.get("response", "").strip()
        except Exception as e:
            logging.error(f"Generation error: {e}")
            return "Error: could not generate answer."
