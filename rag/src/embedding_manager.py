import logging
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel

logger = logging.getLogger(__name__)

class GemmaEmbedder:
    def __init__(self, model_name="google/embeddinggemma-300m"):
        self.device = "mps" if torch.backends.mps.is_available() else "cpu"
        logger.info(f"Using device: {self.device}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, token=True)
        self.model = AutoModel.from_pretrained(model_name, token=True).to(self.device)

    def mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output.last_hidden_state
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, dim=1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    def encode(self, texts, batch_size=8):
        embeddings = []
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            encoded_input = self.tokenizer(batch_texts, padding=True, truncation=True, return_tensors="pt").to(self.device)
            with torch.no_grad():
                model_output = self.model(**encoded_input)
            batch_embeddings = self.mean_pooling(model_output, encoded_input["attention_mask"])
            batch_embeddings = F.normalize(batch_embeddings, p=2, dim=1)
            embeddings.append(batch_embeddings.cpu())
        return torch.cat(embeddings, dim=0)
