def extract_text_from_plaintext(path):
    """Extract raw text from a .txt file."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()