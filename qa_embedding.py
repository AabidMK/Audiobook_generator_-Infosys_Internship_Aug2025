import os
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader
import docx
from PIL import Image
import pytesseract

class EmbeddingModule:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        print(f"[Embedding] Loading model: {model_name}")
        self.model = SentenceTransformer(model_name)

    # --- File extractors ---
    def extract_text(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        text = ""

        if ext == ".pdf":
            reader = PdfReader(file_path)
            for page in reader.pages:
                text += page.extract_text() or ""
        elif ext == ".docx":
            doc = docx.Document(file_path)
            text = "\n".join([p.text for p in doc.paragraphs])
        elif ext in [".png", ".jpg", ".jpeg"]:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
        else:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

        return text.strip()

    # --- Chunk text ---
    def chunk_text(self, text, chunk_size=500, overlap=100):
        chunks = []
        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunks.append(text[start:end])
            start += chunk_size - overlap
        return chunks

    # --- Process & embed ---
    def process_and_embed(self, file_path, chunk_size=500, overlap=100):
        text = self.extract_text(file_path)
        chunks = self.chunk_text(text, chunk_size, overlap)
        embeddings = self.model.encode(chunks)

        # ✅ Metadata for each chunk
        metadatas = []
        for i, _ in enumerate(chunks):
            metadatas.append({
                "file_path": os.path.basename(file_path),
                "chunk_id": i
            })

        return chunks, embeddings, metadatas

    def embed_query(self, query):
        return self.model.encode([query])[0]
