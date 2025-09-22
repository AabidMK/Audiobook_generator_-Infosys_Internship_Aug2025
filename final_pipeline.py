import logging
from pathlib import Path
import sys

from rag_project.src.text_extraction import extract
from text_enrichment import enrich_text, save_markdown
from audio_generation import generate_audiobook

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("audiobook_pipeline.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

class AudiobookPipeline:
    def __init__(self, input_file: str, output_folder: str = None):
        self.input_file = Path(input_file)
        self.output_folder = Path(output_folder) if output_folder else self.input_file.parent / "Output"
        self.output_folder.mkdir(parents=True, exist_ok=True)

        # Base name for audio and markdown
        self.basename = self.output_folder / self.input_file.stem
        self.md_path = self.output_folder / f"{self.input_file.stem}_enriched.md"

    def run_extraction(self) -> str:
        """Extract text from PDF/DOCX."""
        logging.info(f"Extracting text from {self.input_file.name}")
        text = extract(str(self.input_file))
        if not text.strip():
            logging.error("No text extracted. Aborting pipeline.")
            sys.exit(1)
        return text

    def run_enrichment(self, text: str) -> str:
        """Enrich extracted text and save markdown."""
        logging.info("Enriching text for audiobook")
        enriched_text = enrich_text(text)
        save_markdown(enriched_text, str(self.md_path))
        return enriched_text

    def run_audio_generation(self, enriched_text: str):
        """Generate audiobook audio using Coqui TTS."""
        logging.info("Generating audiobook audio")
        generate_audiobook(enriched_text, str(self.basename))

    def run(self):
        logging.info(f"Starting audiobook pipeline for {self.input_file.name}")
        raw_text = self.run_extraction()
        enriched_text = self.run_enrichment(raw_text)
        self.run_audio_generation(enriched_text)
        logging.info(f"Audiobook pipeline completed successfully!\nAll outputs saved in: {self.output_folder}")


# ----------------------
# Example usage
# ----------------------
if __name__ == "__main__":
    input_path = "C:/Users/kjish/Downloads/AI AudioBook Generator.pdf"
    pipeline = AudiobookPipeline(input_path)
    pipeline.run()
