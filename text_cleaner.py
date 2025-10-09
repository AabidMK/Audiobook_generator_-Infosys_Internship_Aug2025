import re

def clean_text(text):
    """
    Cleans the input text by:
    - Lowercasing
    - Removing special characters and extra spaces
    """
    text = text.lower()  # lowercase
    text = re.sub(r'\s+', ' ', text)  # remove extra spaces
    text = re.sub(r'[^a-z0-9\s]', '', text)  # remove punctuation/special chars
    return text
