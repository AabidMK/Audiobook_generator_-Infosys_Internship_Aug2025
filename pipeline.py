import os
import argparse
import subprocess

def run_step(command, description):
    print(f"\n🚀 {description}...")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"❌ Failed at step: {description}")
        exit(1)

def main():
    parser = argparse.ArgumentParser(description="Full Audiobook Pipeline")
    parser.add_argument("input", help="Input file (PDF, DOCX, or image)")
    parser.add_argument("-o", "--output", default="audiobook.wav", help="Output audio file")
    args = parser.parse_args()

    # Step 1: Extract text
    extracted_file = "extracted.txt"
    run_step(f"python text_extractor.py {args.input} -o {extracted_file}", "Extracting text")

    # Step 2: Enrich text into Markdown with voices
    enriched_file = "enriched.md"
    run_step(f"python text_llm.py {extracted_file} -o {enriched_file}", "Enriching text into Markdown")

    # Step 3: Generate audiobook with voices
    run_step(f"python multivoiceTTS.py {enriched_file} -o {args.output}", "Generating audiobook")

    print(f"\n✅ Pipeline completed successfully! Audiobook saved to {args.output}")

if __name__ == "__main__":
    main()