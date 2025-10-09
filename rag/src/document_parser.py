import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class DocumentParser:
    def __init__(self, encoding="utf-8"):
        self.encoding = encoding

    def read_text_files(self, directory: str):
        documents = []
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                file_path = os.path.join(directory, filename)
                try:
                    text = Path(file_path).read_text(encoding=self.encoding)
                    documents.append((filename, text))
                    logger.info(f"Loaded file: {filename}")
                except Exception as e:
                    logger.error(f"Error reading {filename}: {e}")
        return documents
