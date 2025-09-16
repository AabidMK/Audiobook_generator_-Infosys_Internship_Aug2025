import asyncio
import edge_tts
from pathlib import Path
from tkinter import Tk, filedialog

# 🔹 Convert text to speech
async def text_to_speech(text: str, output_file: str, voice: str = "en-US-AriaNeural"):
    tts = edge_tts.Communicate(text, voice)
    await tts.save(output_file)
    print(f"[+] Saved: {output_file}")

def main():
    # 🔹 Ask user to upload a text file
    Tk().withdraw()  # hide tkinter window
    file_path = filedialog.askopenfilename(
        title="Select a text file",
        filetypes=[("Text Files", "*.txt"), ("Markdown Files", "*.md")]
    )

    if not file_path:
        print("No file selected.")
        return

    # 🔹 Read the uploaded text
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    if not text.strip():
        print("[!] The file is empty.")
        return

    # 🔹 Output audio filename
    output_file = Path(file_path).stem + "_audiobook.mp3"

    # Run async TTS
    asyncio.run(text_to_speech(text, output_file))

if __name__ == "__main__":
    main()
