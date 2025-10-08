def chunk_text(text, chunk_size=500, chunk_overlap=100):
    text = text.strip()
    if not text:
        return []

    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - chunk_overlap
    return chunks

if __name__ == "__main__":
    sample_text = "This is a sample text. " * 50
    chunks = chunk_text(sample_text, chunk_size=100, chunk_overlap=20)
    print(f"Total chunks created: {len(chunks)}")
    print(chunks[:2])