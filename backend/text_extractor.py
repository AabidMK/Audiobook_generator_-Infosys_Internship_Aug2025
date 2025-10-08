import PyPDF2
import docx
import io

def extract_text_from_pdf(file_stream):
    """Extracts text from a PDF file stream using PyPDF2."""
    try:
        reader = PyPDF2.PdfReader(file_stream)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error extracting text from PDF: {e}"

def extract_text_from_docx(file_stream):
    """Extracts text from a DOCX file stream using python-docx."""
    try:
        doc = docx.Document(file_stream)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        return f"Error extracting text from DOCX: {e}"

def extract_text_from_txt(file_stream):
    """Extracts text from a TXT file stream."""
    try:
        # Decode the file stream as UTF-8
        return file_stream.read().decode('utf-8')
    except Exception as e:
        return f"Error extracting text from TXT: {e}"

def extract_text(file, file_type):
    """
    Main function to handle text extraction based on file type.
    It takes a file object and its type and calls the appropriate function.
    """
    file_stream = io.BytesIO(file.read())
    if file_type == 'pdf':
        return extract_text_from_pdf(file_stream)
    elif file_type == 'docx':
        return extract_text_from_docx(file_stream)
    elif file_type == 'txt':
        return extract_text_from_txt(file_stream)
    else:
        return "Unsupported file type"