# rag_query.py — Gemini + ChromaDB RAG (token-trim, robust query + citations)
import os
import sys
import textwrap
from typing import List, Tuple

import chromadb
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

# Optional but strongly recommended: token-accurate trimming
try:
    import tiktoken
    enc = tiktoken.get_encoding("cl100k_base")
    def token_len(s: str) -> int: return len(enc.encode(s))
except Exception:
    enc = None
    def token_len(s: str) -> int: return len(s) // 4  # rough fallback

# ---------------- Config ----------------
PERSIST_PATH = "vector_db"
COLLECTION_NAME = "audiobook_chunks"
EMBED_MODEL = "intfloat/e5-base-v2"

PREFERRED_MODELS = [
    "gemini-2.5-flash",
    "gemini-flash-latest",
    "gemini-2.0-flash",
    "gemini-2.0-flash-001",
    "gemini-2.5-pro",
]

MAX_CONTEXT_TOKENS = 6000
TEMPERATURE = 0.2

# ---------------- Helpers ----------------
def ensure_api_key():
    api_key = os.environ.get("GOOGLE_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY is not set.\n"
            "Windows PowerShell:\n  setx GOOGLE_API_KEY \"YOUR_GEMINI_API_KEY\"\n"
            "Then open a new terminal."
        )
    genai.configure(api_key==api_key)

def pick_available_model(preferred_list):
    models = [
        m.name.split("/")[-1]
        for m in genai.list_models()
        if "generateContent" in getattr(m, "supported_generation_methods", [])
    ]
    for m in preferred_list:
        if m in models:
            return m
    if models:
        return models[0]
    raise RuntimeError("No suitable Gemini model found for generateContent in this project.")

def flatten_chroma(results) -> Tuple[List[str], List[dict], List[float]]:
    docs, metas, dists = [], [], []
    for group_docs, group_meta, group_dist in zip(
        results.get("documents", []),
        results.get("metadatas", []),
        results.get("distances", []),
    ):
        for d, m, dist in zip(group_docs, group_meta, group_dist):
            docs.append(d)
            metas.append(m)
            dists.append(float(dist))
    return docs, metas, dists

def trim_to_tokens(parts: List[str], max_tokens: int) -> List[str]:
    out, used = [], 0
    for p in parts:
        t = token_len(p)
        if used + t > max_tokens:
            break
        out.append(p)
        used += t
    return out

# ---------------- Main ----------------
def main():
    # 1) Read question
    question = "What is Dracula’s main theme?"
    if len(sys.argv) >= 2:
        question = " ".join(sys.argv[1:]).strip()
    print("STEP 1: Question OK")

    # 2) Init embedder + Chroma
    embedder = SentenceTransformer(EMBED_MODEL)
    client = chromadb.PersistentClient(path=PERSIST_PATH)
    try:
        collection = client.get_collection(COLLECTION_NAME)
    except Exception:
        raise RuntimeError(f"Chroma collection '{COLLECTION_NAME}' not found. Run index_embeddings.py first.")
    print(f"STEP 2: Embedding model OK ({EMBED_MODEL})")

    # 3) Embed query and retrieve top-K with full fields
    q_emb = embedder.encode([question], normalize_embeddings=True)
    res = collection.query(
        query_embeddings=q_emb.tolist(),
        n_results=5,
        include=["documents", "metadatas", "distances"],
    )
    docs, metas, dists = flatten_chroma(res)
    if not docs:
        print("No results returned from Chroma.")
        return
    print(f"STEP 3: Vector search OK ({len(docs)} hits)")

    # 4) Build trimmed context (token budget)
    parts = trim_to_tokens(docs, MAX_CONTEXT_TOKENS)
    context = "\n\n---\n\n".join(parts)
    print(f"STEP 4: Context assembled OK (~{sum(token_len(p) for p in parts)} tokens)")

    # 5) Prepare prompt (anti-hallucination)
    prompt = textwrap.dedent(f"""
    You are a retrieval-augmented QA assistant. Use ONLY the context below.
    If the answer is not in the context, say: "I don't know."

    # Context
    {context}

    # Task
    Answer the user's question strictly using the Context. Be concise.

    # Question
    {question}

    # Answer
    """).strip()
    print("STEP 5: Prompt built OK")

    # 6) Call Gemini
    ensure_api_key()
    model_name = pick_available_model(PREFERRED_MODELS)
    model = genai.GenerativeModel(model_name)
    resp = model.generate_content(prompt, generation_config={"temperature": TEMPERATURE})
    answer = (getattr(resp, "text", None) or "").strip()
    print("STEP 6: LLM call OK")

    # Output answer
    print("\n--- Answer ---\n")
    print(answer or "I don't know.")

    # 7) Citations
    print("\n--- Citations ---\n")
    for m, dist in zip(metas, dists):
        fp = m.get("file_path", "unknown")
        cid = m.get("chunk_id", "n/a")
        sim = 1.0 - float(dist)
        print(f"- {fp} (chunk {cid}), distance={dist:.4f}, similarity={sim:.4f}")
    print("STEP 7: Citations attached OK")

if __name__ == "__main__":
    main()
