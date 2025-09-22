
def extract_text_from_txt(txt_path: str) -> str:
    try:
        with open(txt_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception:
        # fallback: return empty string
        return ""
