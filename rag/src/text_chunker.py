import logging

logger = logging.getLogger(__name__)

class TextChunk:
    def __init__(self, text: str, chunk_index: int, source_file: str):
        self.text = text
        self.chunk_index = chunk_index
        self.source_file = source_file

class TextChunker:
    def __init__(self, chunk_size=500, chunk_overlap=100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(self, text: str):
        words = text.split()
        chunks = []
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk_words = words[i:i + self.chunk_size]
            context_start = max(0, i - self.chunk_overlap)
            context = words[context_start:i]
            chunk_text = " ".join(context + chunk_words).strip()
            chunks.append(chunk_text)
        return chunks

    def process_documents(self, documents):
        all_chunks = []
        for filename, text in documents:
            chunks = self.chunk_text(text)
            for i, chunk_text in enumerate(chunks):
                all_chunks.append(TextChunk(text=chunk_text, chunk_index=i, source_file=filename))
            logger.info(f"Document {filename} split into {len(chunks)} chunks")
        return all_chunks
