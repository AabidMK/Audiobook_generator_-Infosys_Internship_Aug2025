
import logging
from typing import List
import torch
try:
    from sentence_transformers import SentenceTransformer
except ImportError as e:
    SentenceTransformer = None
    IMPORT_ERROR = e

class EmbeddingManager:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        if SentenceTransformer is None:
            raise RuntimeError("Install sentence-transformers first!") from IMPORT_ERROR
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = SentenceTransformer(model_name, device=self.device)
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"EmbeddingManager using {model_name} on {self.device}")

    def embed(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        if not texts:
            return []
        return self.model.encode(texts, convert_to_numpy=True, show_progress_bar=True, batch_size=batch_size).tolist()
