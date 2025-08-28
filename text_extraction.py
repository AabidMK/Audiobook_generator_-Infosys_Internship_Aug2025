import os
from PyPDF2 import PdfReader

def extract_text_from_file(file_path):
    """
    Extracts text from a .txt or .pdf file on the local machine.

    Args:
        file_path (str): The full path to the input file.

    Returns:
        str: The extracted text content.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found at '{file_path}'")
        return None

    file_extension = os.path.splitext(file_path)[1].lower()

    text_content = ""
    try:
        if file_extension == '.txt':
            with open(file_path, 'r', encoding='utf-8') as file:
                text_content = file.read()
        elif file_extension == '.pdf':
            with open(file_path, 'rb') as file:
                pdf_reader = PdfReader(file)
                for page in pdf_reader.pages:
                    text_content += page.extract_text() or ""
        else:
            print(f"Error: Unsupported file type '{file_extension}'. Only .txt and .pdf are supported.")
            return None
    except Exception as e:
        print(f"Error extracting text from file: {e}")
        return None

    return text_content

def save_text_to_file(text, output_file_path):
    """
    Saves the given text content to a new .txt file.

    Args:
        text (str): The text content to save.
        output_file_path (str): The path to the new output file.

    Returns:
        bool: True if the file was saved successfully, False otherwise.
    """
    try:
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(text)
        return True
    except Exception as e:
        print(f"Error saving file: {e}")
        return False

# --- Main execution block ---
if __name__ == "__main__":
    # Prompt the user for the input file path
    input_file_path = input("Enter the path to your .txt or .pdf file: ")

    # Extract the text
    extracted_text = extract_text_from_file(input_file_path)

    if extracted_text is not None:
        print("\n--- Extracted Text ---")
        print(extracted_text)

        # Prompt the user for the output file name
        output_file_name = input("\nEnter a filename to save the extracted text (e.g., extracted_text.txt): ")
        output_file_path = os.path.join(os.path.dirname(input_file_path), output_file_name)

        # Save the extracted text to the specified file
        if save_text_to_file(extracted_text, output_file_path):
            print(f"\nSuccess! The extracted text has been saved to '{output_file_path}'.")
        else:
            print("\nFailed to save the file. Please check the provided filename and permissions.")