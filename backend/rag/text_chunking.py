import logging
from typing import List, Dict, Any, Tuple

# Set up basic logging for pipeline messages
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')
self_logger = logging.getLogger(__name__)

def chunk_text(text: str, chunk_size: int = 500, chunk_overlap: int = 100) -> List[Dict[str, Any]]:
    """
    Chunks a single text document into smaller pieces with metadata.
    
    Args:
        text: The input text to be chunked.
        chunk_size: The maximum number of characters per chunk.
        chunk_overlap: The number of characters to overlap between chunks.
            
    Returns:
        A list of dictionaries, where each dictionary represents a chunk
        with its text and metadata.
    """
    if not text:
        return []

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size to avoid infinite loop.")

    chunks = []
    start = 0
    text_len = len(text)
    
    while start < text_len:
        end = min(start + chunk_size, text_len)
        chunk_content = text[start:end]   # renamed to avoid shadowing function name
        
        chunk_metadata = {
            'text': chunk_content,
            'chunk_index': len(chunks),
        }
        chunks.append(chunk_metadata)

        if end == text_len:
            break
        
        start += chunk_size - chunk_overlap
            
    self_logger.info(f"Created {len(chunks)} chunks from text of length {text_len}")
    return chunks

def chunk_multiple_documents(documents: List[Tuple[str, str, str]], chunk_size: int = 500, chunk_overlap: int = 100) -> List[Dict[str, Any]]:
    """
    Chunks multiple documents.
    
    Args:
        documents: A list of tuples, where each tuple is
                   (text, source, file_path).
        chunk_size: The maximum number of characters per chunk.
        chunk_overlap: The number of characters to overlap between chunks.
            
    Returns:
        A list of all chunk dictionaries from all documents.
    """
    all_chunks = []
    for doc_text, doc_source, doc_file_path in documents:
        # Pass chunk_size and chunk_overlap to the single-document function
        chunks = chunk_text(doc_text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        
        # Add source and file_path metadata to each chunk
        for chunk in chunks:
            chunk['source'] = doc_source
            chunk['file_path'] = doc_file_path
            chunk['total_chunks'] = len(chunks)
            all_chunks.append(chunk)
            
    self_logger.info(f"Total chunks created from {len(documents)} documents: {len(all_chunks)}")
    return all_chunks