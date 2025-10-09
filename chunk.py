def chunk_text(text, chunk_size=500, overlap=50):
    """
    Split text into overlapping chunks.
    Example: chunk_size=500, overlap=50 → chunks of 500 tokens with 50 overlap
    """
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks
