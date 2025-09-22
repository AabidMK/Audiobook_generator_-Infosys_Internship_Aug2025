
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class TextChunk:
    text: str
    chunk_index: int
    total_chunks: int
    source: str
    file_path: str

class TextChunker:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(self, text: str, source: str, file_path: str) -> List[TextChunk]:
        words = text.split()
        if not words:
            return []
        chunks = []
        start = 0
        idx = 0
        while start < len(words):
            end = min(start + self.chunk_size, len(words))
            chunk_words = words[start:end]
            chunk_text = " ".join(chunk_words)
            chunks.append(TextChunk(chunk_text, idx, 0, source, file_path))
            start += self.chunk_size - self.chunk_overlap
            idx += 1
        total = len(chunks)
        for c in chunks:
            c.total_chunks = total
        return chunks

    def chunk_multiple_documents(self, documents: List[Tuple[str, str, str]]):
        all_chunks = []
        for text, source, file_path in documents:
            all_chunks.extend(self.chunk_text(text, source, file_path))
        return all_chunks
