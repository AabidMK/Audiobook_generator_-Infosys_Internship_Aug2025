from pathlib import Path

def save_text_output(text: str, input_file: str, output_dir: str = "outputs"):
    """Save extracted text into a .txt file"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    output_path = Path(output_dir) / (Path(input_file).stem + "_extracted.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"[+] Extracted text saved at: {output_path}")
    return str(output_path)
