import docx

def extract_docx(file_path: str) -> str:
    """Extract text from .docx file"""
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])
