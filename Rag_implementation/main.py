import argparse
import logging
import time
from pathlib import Path
from typing import Dict, Any
from src.document_parser import parse_dir, parse_file
from src.text_chunker import TextChunker
from src.embedding_manager import EmbeddingManager
from src.vector_store import VectorStoreManager
from src.ollama_llm import OllamaLLMAnswerGenerator
import os


def index_documents(input_path,
                    backend="chroma",
                    model="sentence-transformers/all-MiniLM-L6-v2"):
    """Index documents into Chroma with embeddings for similarity search."""
    docs = []
    p = Path(input_path)

    if not p.exists():
        logging.error(f"Path does not exist: {p}")
        return 0

    # Parse either a single file or a directory of files
    if p.is_file():
        docs.append(parse_file(p))
    else:
        docs = parse_dir(p)

    # Filter out empty documents
    docs = [(t, s, f) for (t, s, f) in docs if t and t.strip()]
    if not docs:
        logging.error("No valid documents found with extractable text.")
        return 0

    # Chunk documents
    chunker = TextChunker()
    chunks = chunker.chunk_multiple_documents(docs)
    texts = [c.text for c in chunks if c.text.strip()]

    # Generate embeddings
    embedder = EmbeddingManager(model_name=model)
    embeddings = embedder.embed(texts)
    dim = len(embeddings[0]) if embeddings else 384

    # Store embeddings in Chroma with cosine similarity as metric
    store = VectorStoreManager(backend=backend, dim=dim, metric="cosine")
    store.add_embeddings(
        ids=[str(i) for i in range(len(texts))],
        embeddings=embeddings,
        metadatas=[{"file": c.file_path, "chunk": idx} for idx, c in enumerate(chunks)],
        documents=texts,
    )

    logging.info(f"Indexing complete. Added {len(texts)} chunks.")
    return len(texts)

def query_docs(question: str,
               backend: str = "chroma",
               model: str = "sentence-transformers/all-MiniLM-L6-v2",
               topk: int = 5,
               llm_model: str = "gemma2:1b") -> Dict[str, Any]:
    """
    Retrieve top-k similar chunks (cosine similarity) and generate an answer using Ollama.
    """
    try:
        # Embed the question
        embedder = EmbeddingManager(model_name=model)
        q_emb = embedder.embed([question])[0]

        # Retrieve top-k similar chunks using Chroma (default = cosine)
        store = VectorStoreManager(backend=backend)
        res = store.query(q_emb, n_results=topk)

        chunks = []
        if backend == "chroma":
            docs = res.get("documents", [[]])[0]
            metas = res.get("metadatas", [[]])[0]
            distances = res.get("distances", [[]])[0]
            # Lower distance = higher similarity for cosine
            for d, m, dist in zip(docs, metas, distances):
                chunks.append({
                    "text": d,
                    "meta": m,
                    "score": dist
                })

        if not chunks:
            return {
                "answer": "No relevant information found.",
                "sources": []
            }

        context = "\n\n".join([
            f"[Source {idx + 1}]: {chunk['text'].strip()}"
            for idx, chunk in enumerate(chunks)
        ])

        llm = OllamaLLMAnswerGenerator(model_name=llm_model)
        prompt = (
            "Based on the provided context, give a detailed and accurate answer. "
            "Use only the information found in the context. "
            "If no relevant information is available, say so clearly.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {question}\n\n"
            "Answer:"
        )

        max_retries = 3
        answer = None

        for attempt in range(max_retries):
            try:
                answer = llm.generate(question=question, context=context)
                if answer and not answer.startswith("Error"):
                    break
                time.sleep(2)
            except Exception as e:
                logging.warning(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(2)

        if not answer:
            return {
                "answer": "No relevant answer could be generated.",
                "sources": []
            }

        return {
            "answer": answer,
            "sources": [{
                "file": chunk["meta"].get("file"),
                "chunk": chunk["meta"].get("chunk", 0),
                "score": chunk["score"]
            } for chunk in chunks]
        }

    except Exception as e:
        logging.error(f"Error during query: {str(e)}", exc_info=True)
        return {
            "answer": f"Error: {str(e)}",
            "sources": []
        }

def show_results(result: Dict[str, Any]):
    """Display results with cosine similarity scores."""
    print("\n=== Best Answer ===")
    print(result["answer"].strip())
    
    if result["sources"]:
        print("\n=== Sources Used (by Similarity) ===")
        # Use 'score' instead of 'similarity' since that's what we store
        for source in sorted(result["sources"], key=lambda x: x["score"]):
            filename = os.path.basename(source["file"])
            # Convert cosine distance to similarity percentage (lower distance = higher similarity)
            similarity_pct = (1 - source["score"]) * 100
            print(f"- {filename} (chunk {source['chunk']})")
            print(f"  Similarity: {similarity_pct:.1f}% (cosine distance: {source['score']:.3f})")
    print()

def main():
    parser = argparse.ArgumentParser(description="Document Q&A System with cosine similarity")
    sub = parser.add_subparsers(dest="cmd")

    # Index sub-command
    p_index = sub.add_parser("index", help="Index documents for searching")
    p_index.add_argument("-i", "--input", required=True, help="Input file or directory path")
    p_index.add_argument("--backend", default="chroma", help="Vector store backend")
    p_index.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2",
                         help="Embedding model name")

    # Query sub-command
    p_query = sub.add_parser("query", help="Ask questions about documents")
    p_query.add_argument("question", help="Your question about the documents")
    p_query.add_argument("--backend", default="chroma", help="Vector store backend")
    p_query.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2",
                         help="Embedding model name")
    p_query.add_argument("--topk", type=int, default=5,
                         help="Number of relevant chunks to retrieve (default=5)")
    p_query.add_argument("--llm", default="gemma2:1b",
                         help="Ollama model to use")

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(message)s")

    try:
        if args.cmd == "index":
            num_chunks = index_documents(
                args.input,
                backend=args.backend,
                model=args.model
            )
            print(f"\nIndexed {num_chunks} chunks successfully!")

        elif args.cmd == "query":
            result = query_docs(
                args.question,
                backend=args.backend,
                model=args.model,
                topk=args.topk,
                llm_model=args.llm
            )
            show_results(result)

        else:
            parser.print_help()

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        print("\nMake sure you have:")
        print("1. Indexed some documents first using the 'index' command")
        print("2. Installed all required packages")
        print("3. Started the Ollama server (ollama serve)")


if __name__ == "__main__":
    main()
