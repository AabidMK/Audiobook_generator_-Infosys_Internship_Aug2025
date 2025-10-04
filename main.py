from parsing import parse_text
from chunking import chunk_text
from embedding import generate_embeddings
from storage import save_chunks_to_chromadb

def run_pipeline(input_file: str):
    with open(input_file, "r", encoding="utf-8") as f:
        raw_text = f.read()

    parsed_text = parse_text(raw_text)
    chunks = chunk_text(parsed_text)
    embeddings = generate_embeddings(chunks)
    save_chunks_to_chromadb(chunks, embeddings)

if __name__ == "__main__":
    run_pipeline("rewritten_output.md")



