from pathlib import Path
from typing import List, Tuple
from .extract_pdf import extract_text_from_pdf
from .extract_docx import extract_text_from_docx
from .extract_txt import extract_text_from_txt
from .extract_image import extract_text_from_image

SUPPORTED = [".pdf", ".docx", ".txt", ".png", ".jpg", ".jpeg", ".tiff"]

def parse_file(path: Path) -> Tuple[str, str, str]:
    """
    Parse a single file and extract its text content.
    Returns a tuple of (filename, file extension, extracted text)
    """
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    ext = path.suffix.lower()
    if ext not in SUPPORTED:
        raise ValueError(f"Unsupported file format: {ext}")
    
    try:
        if ext == '.pdf':
            text = extract_text_from_pdf(path)
        elif ext == '.docx':
            text = extract_text_from_docx(path)
        elif ext == '.txt':
            text = extract_text_from_txt(path)
        else:  # Image files
            text = extract_text_from_image(path)
           
        return (path.name, ext, text)
    
    except Exception as e:
        raise Exception(f"Error processing {path.name}: {str(e)}")

def parse_dir(root_path: Path) -> List[Tuple[str,str,str]]:
    """
    Parse all supported files in a directory.
    Returns a list of tuples (filename, file extension, extracted text)
    """
    if not root_path.exists() or not root_path.is_dir():
        raise NotADirectoryError(f"Invalid directory path: {root_path}")
    
    results = []
    for file_path in root_path.glob("*"):
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED:
            try:
                result = parse_file(file_path)
                results.append(result)
            except Exception as e:
                print(f"Warning: Skipping {file_path.name} - {str(e)}")
                
    return results