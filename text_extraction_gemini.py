# text_extraction_gemini.py
import os
import sys
import re
import time
import glob
import google.generativeai as genai
from dotenv import load_dotenv

# ---------------- Load API key from .env ----------------
load_dotenv()  # expects a .env with GOOGLE_API_KEY=...

TEMPERATURE = 0.4
MAX_CHARS = 12000            # per-request chunk size
BACKOFF_BASE = 6             # seconds for simple backoff

# If you want to bias toward a model, put it first here; the code
# will still verify availability via list_models().
PREFERRED_MODELS = [
    "gemini-1.5-flash-8b",
    "gemini-1.5-flash-latest",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-2.0-flash-lite-preview-02-05",  # sometimes available for free tier
]

REWRITE_PROMPT = (
    "Rewrite the following text for clear, engaging narration suitable for an audiobook listener. "
    "Keep factual content, do not invent details, improve flow and coherence, use concise sentences, "
    "and keep or enhance Markdown headings and bullet lists where helpful. "
    "Normalize spacing and punctuation. Return only the rewritten text."
)


# ---------------- Helpers ----------------
def ensure_api_key():
    api_key = os.getenv("GOOGLE_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY not found. Create a .env file with:\n"
            "GOOGLE_API_KEY=your_key_here"
        )
    # Configure the SDK (defaults to v1 API in recent versions)
    genai.configure(api_key=api_key)


def normalize(s: str) -> str:
    s = s.replace("\u00A0", " ")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\r?\n\s*", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def chunk_text(s: str, max_chars: int):
    s = s.strip()
    start = 0
    while start < len(s):
        end = min(start + max_chars, len(s))
        # Prefer to cut on a paragraph boundary if possible
        cut = s.rfind("\n\n", start, end)
        if cut == -1 or cut <= start + 1000:
            cut = end
        yield s[start:cut]
        start = cut


def pick_available_model():
    """
    Query the project’s available models and pick one that supports generateContent.
    Falls back sensibly if listing is restricted.
    """
    try:
        available = genai.list_models()
        names = []
        for m in available:
            # m.name is like "models/gemini-1.5-flash-8b"
            short = m.name.split("/")[-1]
            if "generateContent" in getattr(m, "supported_generation_methods", []):
                names.append(short)

        # Prefer one from our preferred list
        for cand in PREFERRED_MODELS:
            if cand in names:
                return cand

        # Otherwise, take any that supports generateContent
        if names:
            print("No preferred model found; using:", names[0])
            return names[0]

        # As a last resort, try a commonly-available short name
        print("No listable models found; attempting gemini-1.5-flash-8b")
        return "gemini-1.5-flash-8b"

    except Exception as e:
        # If list_models fails (permissions, network), try a sane default
        print(f"Model listing failed ({e}); attempting gemini-1.5-flash-8b")
        return "gemini-1.5-flash-8b"


def rewrite_chunk(model, text: str, attempt: int = 1) -> str:
    prompt = f"{REWRITE_PROMPT}\n\n---\n{text}"
    try:
        resp = model.generate_content(
            prompt,
            generation_config={"temperature": TEMPERATURE},
        )
        return (resp.text or "").strip()
    except Exception as e:
        # simple backoff on quotas/timeouts
        wait_s = BACKOFF_BASE * attempt
        msg = str(e)
        m = re.search(r"retry_delay\s*{\s*seconds:\s*(\d+)", msg)
        if m:
            wait_s = max(wait_s, int(m.group(1)))
        if attempt >= 3:
            raise
        print(f"[rewrite backoff] waiting {wait_s}s then retrying...")
        time.sleep(wait_s)
        return rewrite_chunk(model, text, attempt + 1)


def rewrite_file(raw_md_path: str) -> str:
    ensure_api_key()

    base = os.path.basename(raw_md_path)
    if not base.endswith("_raw.md"):
        raise ValueError("Input must be a '*_raw.md' file")
    out_path = raw_md_path[:-7] + "_rewritten.md"  # replace _raw.md

    # Load and normalize the raw text
    with open(raw_md_path, "r", encoding="utf-8") as f:
        raw = normalize(f.read())

    # Pick a working model dynamically
    model_name = pick_available_model()
    print(f"Using model: {model_name}")
    model = genai.GenerativeModel(model_name)

    # Start output
    with open(out_path, "w", encoding="utf-8") as out:
        out.write(f"# Rewritten Text ({base[:-7]})\n\n")

    # Chunk + rewrite
    idx = 1
    for chunk in chunk_text(raw, MAX_CHARS):
        print(f"Rewriting chunk {idx}...")
        rewritten = rewrite_chunk(model, chunk)
        with open(out_path, "a", encoding="utf-8") as out:
            out.write(f"\n\n## Rewritten chunk {idx}\n\n{rewritten}\n")
        idx += 1

    print(f"Saved rewritten: {out_path}")
    return out_path


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        in_path = sys.argv[1]
    else:
        raws = glob.glob("*_raw.md")
        if not raws:
            print("No *_raw.md found.")
            sys.exit(1)
        in_path = max(raws, key=os.path.getmtime)

    rewrite_file(os.path.abspath(in_path))
