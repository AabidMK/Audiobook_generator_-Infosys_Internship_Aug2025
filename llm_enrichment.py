import requests
import textwrap
from utils import load_config

config = load_config()

def build_prompt(text):
    return textwrap.dedent(f"""
    Rewrite the following text for an engaging audiobook narration.
    - Tone: warm, conversational
    - Pace: moderate
    - Audience: general
    - Do NOT invent facts.
    - Make it clear, engaging, and easy to listen to.

    Text:
    \"\"\"{text}\"\"\"
    """)

def enrich_text(text):
    url = config['llm']['api_url']
    model = config['llm']['model_name']
    prompt = build_prompt(text)
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, json=data, timeout=600)
    response.raise_for_status()
    return response.json().get("response", "")
