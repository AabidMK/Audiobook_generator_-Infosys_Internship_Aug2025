# run_pipeline.py
import os
import subprocess
import glob
from dotenv import load_dotenv

def run_pipeline():
    load_dotenv()

    # STEP 1: Text extraction (choose source and produce *_raw.md)
    print("\n=== STEP 1: Text Extraction ===")
    subprocess.run(["python", "text_extraction.py"], check=True)

    raws = glob.glob("*_raw.md")
    if not raws:
        print(" No *_raw.md produced, aborting.")
        return
    latest_raw = max(raws, key=os.path.getmtime)
    print(f"Found raw file: {latest_raw}")

    # STEP 2: Rewrite the raw with Gemini => *_rewritten.md
    print("\n=== STEP 2: Rewriting with Gemini ===")
    subprocess.run(["python", "text_extraction_gemini.py", latest_raw], check=True)

    rews = glob.glob("*_rewritten.md")
    if not rews:
        print(" No *_rewritten.md produced, aborting.")
        return
    latest_rew = max(rews, key=os.path.getmtime)
    print(f"Found rewritten file: {latest_rew}")

    # STEP 3: (Optional) TTS -> audiobook
    print("\n=== STEP 3: Generating Audiobook (Edge TTS) ===")
    try:
        subprocess.run(["python", "edge_tts_convert.py"], check=True)
    except Exception as e:
        print(f" TTS step skipped or failed: {e}")

    # STEP 4: Index embeddings into ChromaDB
    print("\n=== STEP 4: Index embeddings ===")
    subprocess.run(["python", "index_embeddings.py"], check=True)

    print("\nPipeline complete!")

if __name__ == "__main__":
    run_pipeline()
