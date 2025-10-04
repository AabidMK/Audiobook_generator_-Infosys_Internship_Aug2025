import os
import argparse
from datetime import datetime

# =====================
# Import project modules
# =====================
from Text_extractor import extract_text
from text_llm import rewrite_with_lmstudio
from multivoiceTTS import synthesize_chunks, split_into_chunks
from index_builder import index_chunks
from rag_pipeline import answer_question

# =====================
# Helper: Generate unique file names
# =====================
def make_unique_filename(base_name: str, suffix: str, ext: str):
    """
    Create a unique filename with timestamp.
    Example: IOT_assig_05_07_20251004_212130_raw.txt
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_{timestamp}_{suffix}{ext}"

# =====================
# Pipeline Orchestrator
# =====================
def run_extract(input_file, output_file=None):
    print("\n📘 Extracting text...")

    # Generate dynamic output filename if not provided
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = output_file or make_unique_filename(base_name, "raw", ".txt")

    extracted = extract_text(input_file)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(extracted)

    print(f"✅ Extracted text saved to {output_file}")
    return output_file


def run_enrich(input_file, output_file=None):
    print("\n✨ Enriching text...")

    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = output_file or make_unique_filename(base_name, "rewritten", ".md")

    with open(input_file, "r", encoding="utf-8") as f:
        raw_text = f.read()

    enriched = rewrite_with_lmstudio(raw_text)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(enriched)

    print(f"✅ Enriched markdown saved to {output_file}")
    return output_file


def run_narrate(input_file, output_file=None):
    print("\n🎤 Narrating enriched text...")

    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = output_file or make_unique_filename(base_name, "audiobook", ".wav")

    with open(input_file, "r", encoding="utf-8") as f:
        enriched_text = f.read()

    chunks = split_into_chunks(enriched_text)
    synthesize_chunks(chunks, output_file)

    print(f"✅ Audiobook narration saved to {output_file}")
    return output_file


def run_index(input_file, collection="audiobook_chunks"):
    print(f"\n📦 Indexing into Qdrant collection '{collection}'...")
    index_chunks(input_file, collection)
    print(f"✅ Indexed {input_file} into collection '{collection}'")


def run_rag(question, collection="audiobook_chunks", top_k=5):
    print(f"\n🔍 Running RAG query on collection '{collection}'...")
    answer, citations, context = answer_question(question, collection, top_k=top_k)
    print("\n📝 Answer:\n", answer)
    print("\n📌 Citations:")
    for c in citations:
        print("-", c)
    print("\n📄 Context:\n", context)
    return answer


def run_full(input_file, question, collection="audiobook_chunks"):
    base_name = os.path.splitext(os.path.basename(input_file))[0]

    # Step 1: Extract
    raw_txt = run_extract(input_file)

    # Step 2: Enrich
    enriched_md = run_enrich(raw_txt)

    # Step 3: Narrate
    run_narrate(enriched_md)

    # Step 4: Index
    run_index(enriched_md, collection)

    # Step 5: RAG
    run_rag(question, collection)

# =====================
# CLI Entry Point
# =====================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Unified pipeline for audiobook + RAG system")
    parser.add_argument("--mode", required=True, choices=["extract", "enrich", "narrate", "index", "rag", "full"],
                        help="Which stage of the pipeline to run")
    parser.add_argument("--input", help="Input file (PDF, DOCX, image, or markdown depending on mode)")
    parser.add_argument("--output", help="Optional output file")
    parser.add_argument("--question", help="User question for RAG query")
    parser.add_argument("--collection", default="audiobook_chunks", help="Qdrant collection name (default: audiobook_chunks)")
    parser.add_argument("--top_k", type=int, default=5, help="Number of chunks to retrieve in RAG")
    args = parser.parse_args()

    if args.mode == "extract":
        run_extract(args.input, args.output)

    elif args.mode == "enrich":
        run_enrich(args.input, args.output)

    elif args.mode == "narrate":
        run_narrate(args.input, args.output)

    elif args.mode == "index":
        run_index(args.input, args.collection)

    elif args.mode == "rag":
        if not args.question:
            raise ValueError("❌ You must provide --question for rag mode")
        run_rag(args.question, args.collection, top_k=args.top_k)

    elif args.mode == "full":
        if not args.input or not args.question:
            raise ValueError("❌ You must provide both --input and --question for full mode")
        run_full(args.input, args.question, args.collection)