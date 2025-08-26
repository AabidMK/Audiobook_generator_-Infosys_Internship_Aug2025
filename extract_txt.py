def extract_text_file(file_path: str) -> str:
    """Extract text from plain .txt file"""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
