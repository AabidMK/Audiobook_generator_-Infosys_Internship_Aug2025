
import logging
import docx

def extract_text_from_docx(docx_path: str) -> str:
    try:
        doc = docx.Document(docx_path)
        text = "\\n\\n".join(p.text.strip() for p in doc.paragraphs if p.text.strip())
        if not text:
            logging.warning(f"No text extracted from {docx_path}")
        return text
    except Exception as e:
        logging.error(f"DOCX Extraction Error for {docx_path}: {e}", exc_info=True)
        return ""
