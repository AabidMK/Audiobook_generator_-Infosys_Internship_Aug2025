# rag/src/ollama_llm.py
from openai import OpenAI

class LMStudioClient:
    def __init__(self, model="meta-llama/Meta-Llama-3-8B-Instruct"):
        # Point the client to the LM Studio local server
        self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
        self.model = model
        self.system_prompt = (
            "You are an expert Q&A assistant. You are given a context and a question. "
            "Your task is to answer the question based *only* on the provided context. "
            "If the context does not contain the answer, state that the information is not available in the provided documents. "
            "Do not use any external knowledge."
        )

    def generate(self, context, query):
        prompt = f"Context:\n{context}\n\nQuestion: {query}"
        
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return completion.choices[0].message.content