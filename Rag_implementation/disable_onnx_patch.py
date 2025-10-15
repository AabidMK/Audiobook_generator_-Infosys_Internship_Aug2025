import os

# 🧠 Force Chroma to skip ONNX entirely
os.environ["CHROMA_DEFAULT_EMBEDDING_FUNCTION"] = "sentence-transformers/all-MiniLM-L6-v2"

# 🪄 Monkey-patch Chroma to stop it from loading ONNXMiniLM_L6_V2
import chromadb.utils.embedding_functions as ef
ef.DefaultEmbeddingFunction = lambda: ef.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

print("✅ ONNX disabled globally — patched Chroma to use SentenceTransformer backend.")
