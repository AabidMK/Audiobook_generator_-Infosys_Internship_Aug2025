# edge_tts_convert.py
import os
import sys
import glob
import asyncio
import edge_tts

VOICE = "en-GB-SoniaNeural"   # or en-US-AriaNeural, en-IN-NeerjaNeural, etc.
RATE = "-10%"                 # a bit slower, nicer for narration

async def md_to_speech(md_path: str) -> str:
    base = os.path.basename(md_path)
    if not base.endswith("_rewritten.md"):
        raise ValueError("Input must be a *_rewritten.md file")
    mp3 = base.replace("_rewritten.md", ".mp3")

    with open(md_path, "r", encoding="utf-8") as f:
        text = f.read()

    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE,
        rate=RATE
    )
    await communicate.save(mp3)
    print(f"Saved audio: {mp3}")
    return mp3

async def main():
    if len(sys.argv) >= 2:
        md_path = sys.argv[1]
    else:
        files = glob.glob("*_rewritten.md")
        if not files:
            print("No *_rewritten.md found.")
            return
        md_path = max(files, key=os.path.getmtime)

    mp3 = await md_to_speech(os.path.abspath(md_path))
    # auto-play on Windows
    os.system(f"start {mp3}")

if __name__ == "__main__":
    asyncio.run(main())
