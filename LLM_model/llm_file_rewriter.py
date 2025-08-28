import requests
import json
import time
import os
from PyPDF2 import PdfReader

def get_api_key():
    """
    Retrieves the Gemini API key.
    
    In a real-world application, you would load this from a secure
    environment variable. For this example, we'll use a placeholder.
    """
    # The API key is left as an empty string and will be provided by the Canvas environment.
    return "AIzaSyC7T8OZKNnelTGygPLqR1jSb7bY31suX1s" # Your API key goes here

def read_file_content(file_path):
    """
    Reads the content from a .txt or .pdf file.
    
    Args:
        file_path (str): The path to the file on the user's device.
        
    Returns:
        tuple: A tuple containing (content, status, message).
               - content (str): The extracted text content.
               - status (bool): True if successful, False otherwise.
               - message (str): A message describing the outcome.
    """
    if not os.path.exists(file_path):
        return "", False, f"Error: File not found at '{file_path}'."
    
    file_extension = os.path.splitext(file_path)[1].lower()
    
    try:
        if file_extension == '.txt':
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read(), True, "Text content read successfully."
        elif file_extension == '.pdf':
            with open(file_path, 'rb') as file:
                pdf_reader = PdfReader(file)
                text_content = ""
                for page in pdf_reader.pages:
                    text_content += page.extract_text() or ""
                return text_content, True, "PDF content extracted successfully."
        else:
            return "", False, f"Error: Unsupported file type '{file_extension}'. Only .txt and .pdf are supported."
    except Exception as e:
        return "", False, f"Error reading file: {e}"

def rewrite_text_with_gemini(text_to_rewrite):
    """
    Rewrites text for better narration using the Google Gemini API.
    
    Args:
        text_to_rewrite (str): The input text to be rewritten.
        
    Returns:
        str: The rewritten text, or an error message if the API call fails.
    """
    api_key = get_api_key()
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"
    
    # Prompt to guide the LLM's rewriting process
    prompt = f"Rewrite the following text for better narration, improved flow, and an engaging listener experience. Use a natural, conversational tone and make it easy to follow:\n\n{text_to_rewrite}"
    
    # Payload for the API request
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    
    # Exponential backoff retry mechanism
    max_retries = 5
    attempt = 0
    while attempt < max_retries:
        try:
            response = requests.post(api_url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
            response.raise_for_status()
            
            result = response.json()
            
            if 'candidates' in result and result['candidates']:
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                return "Error: No candidates found in the API response."
        except requests.exceptions.HTTPError as errh:
            if errh.response.status_code == 429 and attempt < max_retries - 1:
                delay = 2 ** attempt
                print(f"Rate limit exceeded. Retrying in {delay} seconds...")
                time.sleep(delay)
                attempt += 1
            else:
                return f"HTTP Error: {errh}"
        except requests.exceptions.RequestException as err:
            return f"An unexpected error occurred: {err}"
    
    return "Failed to get a response after multiple retries due to rate limiting."

def save_text_to_file(text, output_file_path):
    """
    Saves the given text to a specified file.
    
    Args:
        text (str): The text content to save.
        output_file_path (str): The path to the output file.
        
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
    file_path = input("Please enter the path to your .txt or .pdf file: ")# "C:\\Users\\SAI PAVAN\\Downloads\\"

    content, status, message = read_file_content(file_path)
    
    if not status:
        print(message)
    else:
        print("\n--- Reading file... Done. ---")
        
        if not content.strip():
            print("Error: The file is empty or contains no readable text.")
        else:
            print("\n--- Sending to Gemini API for rewriting... ---")
            rewritten_text = rewrite_text_with_gemini(content)
            
            print("\n--- Rewritten Text ---")
            print(rewritten_text)

            output_filename = input("\nEnter a filename to save the rewritten text (e.g., rewritten_output.txt): ") #"D:\\Infosys spring\\rewritten_output.txt")

            if save_text_to_file(rewritten_text, output_filename):
                print(f"\nSuccess! The rewritten text has been saved to '{output_filename}'.")
            else:
                print("\nFailed to save the file. Please check the provided filename and permissions.")