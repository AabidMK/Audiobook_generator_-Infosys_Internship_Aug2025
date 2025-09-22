import argparse, logging, os
from pathlib import Path
from src.document_parser import parse_dir, parse_file
from src.text_chunker import TextChunker
from src.embedding_manager import EmbeddingManager
from src.vector_store import VectorStoreManager


def index_documents(input_path, backend="chroma", model="sentence-transformers/all-MiniLM-L6-v2"):
    docs = []
    p = Path(input_path)
    if p.is_file():
        docs.append(parse_file(p))   
    else:
        docs = parse_dir(p)

    # filter empty docs
    docs = [(t, s, f) for (t, s, f) in docs if t and t.strip()]
    if not docs:
        logging.error("No valid documents found with extractable text. Exiting.")
        return 0

    # chunk documents
    chunker = TextChunker()
    chunks = chunker.chunk_multiple_documents(docs)
    texts = [c.text for c in chunks if c.text.strip()]

    # embeddings
    embedder = EmbeddingManager(model_name=model)
    embeddings = embedder.embed(texts)
    dim = len(embeddings[0]) if embeddings else 384

    # vector store
    store = VectorStoreManager(backend=backend, dim=dim)
    store.add_embeddings(
        ids=[str(i) for i in range(len(texts))],
        embeddings=embeddings,
        metadatas=[{"file": c.file_path} for c in chunks],
        documents=texts,
    )

    logging.info("Indexing complete. Added %d chunks." % len(texts))
    return len(texts)


def query_docs(question, backend="chroma", model="sentence-transformers/all-MiniLM-L6-v2", topk=3):
    embedder = EmbeddingManager(model_name=model)
    q_emb = embedder.embed([question])[0]
    store = VectorStoreManager(backend=backend)
    res = store.query(q_emb, n_results=topk)

    out = []
    if backend == "chroma":
        docs = res.get("documents", [[]])[0]
        metas = res.get("metadatas", [[]])[0]
        for d, m in zip(docs, metas):
            out.append({"text": d, "meta": m})
    else:
        for hit in res:
            out.append({"text": hit.payload.get("doc"), "meta": hit.payload})
    return out


def show_results(results):
    for i, r in enumerate(results):
        print(f"--- RESULT {i+1} ---")
        print("SOURCE:", r["meta"].get("file"))
        print()
        print(r["text"][:800])
        print()


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")

    # Index command
    p_index = sub.add_parser("index")
    p_index.add_argument("-i", "--input", required=True)
    p_index.add_argument("--backend", default="chroma")
    p_index.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2")

    # Query command
    p_query = sub.add_parser("query")
    p_query.add_argument("question")
    p_query.add_argument("--backend", default="chroma")
    p_query.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2")
    p_query.add_argument("--topk", type=int, default=3)

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)

    if args.cmd == "index":
        index_documents(args.input, backend=args.backend, model=args.model)
    elif args.cmd == "query":
        res = query_docs(args.question, backend=args.backend, model=args.model, topk=args.topk)
        show_results(res)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
