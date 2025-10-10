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
MAX_RETRIES = 3

# Try these in order; we’ll verify availability via list_models()
PREFERRED_MODELS = [
    "gemini-2.5-flash",
    "gemini-flash-latest",
    "gemini-2.0-flash",
    "gemini-1.5-flash-8b",
    "gemini-1.5-flash-latest",
    "gemini-1.5-pro",
    "gemini-2.0-flash-lite-preview-02-05",
]

# Strictly ask for plain paragraphs only
REWRITE_PROMPT = (
    "Rewrite the text for clear, engaging audiobook narration. "
    "Keep factual content, improve flow and coherence, use concise sentences. "
    "Output PLAIN PARAGRAPHS ONLY. "
    "Do NOT add headings, lists, bullets, numbering, hashtags, code fences, or any labels. "
    "Do NOT write phrases like 'rewritten text' or 'chunk'. "
    "Preserve paragraph breaks but otherwise just return the narrative as clean text."
)

# ---------------- Helpers ----------------
def ensure_api_key():
    api_key = os.getenv("GOOGLE_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY not found. Create a .env file with:\n"
            "GOOGLE_API_KEY=your_key_here"
        )
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
        cut = s.rfind("\n\n", start, end)  # prefer to cut at paragraph boundary
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
            short = m.name.split("/")[-1]
            if "generateContent" in getattr(m, "supported_generation_methods", []):
                names.append(short)

        for cand in PREFERRED_MODELS:
            if cand in names:
                return cand

        if names:
            print("No preferred model found; using:", names[0])
            return names[0]

        print("No listable models found; attempting gemini-2.5-flash")
        return "gemini-2.5-flash"

    except Exception as e:
        print(f"Model listing failed ({e}); attempting gemini-2.5-flash")
        return "gemini-2.5-flash"

def strip_markup(text: str) -> str:
    """
    Remove accidental headings, bullets, numbered lists, hashtags, code fences, and labels.
    Keep paragraph breaks. Normalize to at most double newlines.
    """
    lines = text.splitlines()
    cleaned = []
    for ln in lines:
        l = ln.strip()

        # Ignore code fences entirely
        if l.startswith("```"):
            continue

        # Remove typical headers, bullets, numbered prefixes, hashtags
        l = re.sub(r"^\s*#+\s*", "", l)                   # markdown headers
        l = re.sub(r"^\s*[-*•·]\s+", "", l)               # bullets
        l = re.sub(r"^\s*\d+[\.\)\-]\s+", "", l)          # numbered bullets (1., 1), 1-)
        l = re.sub(r"^\s*#\s*", "", l)                    # leading hashtag marker
        l = re.sub(r"^\s*rewritten\s*chunk.*$", "", l, flags=re.IGNORECASE)
        l = re.sub(r"^\s*chunk\s*\d+.*$", "", l, flags=re.IGNORECASE)
        l = re.sub(r"^\s*rewritten\s*text.*$", "", l, flags=re.IGNORECASE)

        cleaned.append(l)

    text2 = "\n".join(cleaned)
    text2 = re.sub(r"\n{3,}", "\n\n", text2).strip()
    return text2

def rewrite_chunk(model, text: str, attempt: int = 1) -> str:
    prompt = f"{REWRITE_PROMPT}\n\n---\n{text}"
    try:
        resp = model.generate_content(
            prompt,
            generation_config={"temperature": TEMPERATURE},
        )
        raw = (resp.text or "").strip()
        return strip_markup(raw)
    except Exception as e:
        wait_s = BACKOFF_BASE * attempt
        msg = str(e)
        m = re.search(r"retry_delay\s*{\s*seconds:\s*(\d+)", msg)
        if m:
            wait_s = max(wait_s, int(m.group(1)))
        if attempt >= MAX_RETRIES:
            raise
        print(f"[rewrite backoff] waiting {wait_s}s then retrying...")
        time.sleep(wait_s)
        return rewrite_chunk(model, text, attempt + 1)

# ---------------- Main entry ----------------
def rewrite_file(raw_md_path: str) -> str:
    """
    Input:  <base>_raw.md
    Output: <base>_rewritten.md
    Writes plain paragraphs only (no headers, bullets, chunk labels).
    """
    ensure_api_key()

    base = os.path.basename(raw_md_path)
    if not base.endswith("_raw.md"):
        raise ValueError("Input must be a '*_raw.md' file")
    out_path = raw_md_path[:-7] + "_rewritten.md"  # replace _raw.md

    with open(raw_md_path, "r", encoding="utf-8") as f:
        raw = normalize(f.read())

    model_name = pick_available_model()
    print(f"Using model: {model_name}")
    model = genai.GenerativeModel(model_name)

    # Start with an empty file; we do not reveal it's rewritten
    open(out_path, "w", encoding="utf-8").close()

    idx = 1
    for chunk in chunk_text(raw, MAX_CHARS):
        print(f"Rewriting chunk {idx}...")
        rewritten = rewrite_chunk(model, chunk)
        if rewritten:
            with open(out_path, "a", encoding="utf-8") as out:
                if os.path.getsize(out_path) > 0:
                    out.write("\n\n")  # keep paragraph spacing between chunks
                out.write(rewritten)
        idx += 1

    # Final sanitize pass on full output
    with open(out_path, "r", encoding="utf-8") as f:
        final_text = strip_markup(f.read())
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(final_text)

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
