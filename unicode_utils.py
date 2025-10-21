"""
Unicode utilities to handle encoding issues
"""
import re

def clean_unicode_text(text):
    """Remove problematic Unicode characters and emojis"""
    if not text:
        return text
    
    # Remove emojis and symbols
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    
    text = emoji_pattern.sub('', text)
    
    # Replace common problematic characters
    replacements = {
        '🚀': '',
        '📚': '',
        '🎙️': '',
        '🎭': '',
        '📝': '',
        '🎵': '',
        '🎉': '',
        '✅': '',
        '❌': '',
        '⚠️': '',
        '📏': '',
        '⏱️': '',
        '💾': '',
        '📊': '',
        '🎬': '',
        '🔧': '',
        '📋': '',
        '📍': '',
        '🔍': '',
        '📁': '',
        '💬': '',
        '🎧': '',
        '📖': '',
        '🔊': '',
        '⬇️': '',
        '📄': '',
        '🎤': '',
        '🔄': '',
        '💡': '',
        '🎯': '',
        '📈': '',
        '🔗': '',
        '📌': '',
        '🎪': '',
        '🌟': '',
        '🔥': '',
        '💯': '',
        '🚨': '',
        '⭐': '',
        '🎨': '',
        '🔔': '',
        '📢': '',
        '🎺': '',
        '🎸': '',
        '🥁': '',
        '🎹': '',
        '🎼': '',
        '🎶': '',
        '🎵': '',
        '🔈': '',
        '🔉': '',
        '🔊': '',
        '📻': '',
        '🎚️': '',
        '🎛️': '',
        '🎧': '',
        '📱': '',
        '💻': '',
        '🖥️': '',
        '⌨️': '',
        '🖱️': '',
        '🖨️': '',
        '💽': '',
        '💾': '',
        '💿': '',
        '📀': '',
        '🧮': '',
        '🎥': '',
        '📹': '',
        '📷': '',
        '📸': '',
        '📺': '',
        '📼': '',
        '🔍': '',
        '🔎': '',
        '🕯️': '',
        '💡': '',
        '🔦': '',
        '🏮': '',
        '🪔': '',
        '📔': '',
        '📕': '',
        '📖': '',
        '📗': '',
        '📘': '',
        '📙': '',
        '📚': '',
        '📓': '',
        '📒': '',
        '📃': '',
        '📜': '',
        '📄': '',
        '📰': '',
        '🗞️': '',
        '📑': '',
        '🔖': '',
        '🏷️': '',
        '💰': '',
        '🪙': '',
        '💴': '',
        '💵': '',
        '💶': '',
        '💷': '',
        '💸': '',
        '💳': '',
        '🧾': '',
        '💹': '',
        '✉️': '',
        '📧': '',
        '📨': '',
        '📩': '',
        '📤': '',
        '📥': '',
        '📦': '',
        '📫': '',
        '📪': '',
        '📬': '',
        '📭': '',
        '📮': '',
        '🗳️': '',
        '✏️': '',
        '✒️': '',
        '🖋️': '',
        '🖊️': '',
        '🖌️': '',
        '🖍️': '',
        '📝': '',
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text

def clean_list_strings(text_list):
    """Clean a list of strings from Unicode issues"""
    if not text_list:
        return text_list
    return [clean_unicode_text(str(text)) for text in text_list]

def clean_dict_values(data_dict):
    """Clean dictionary values from Unicode issues"""
    if not data_dict:
        return data_dict
    cleaned = {}
    for key, value in data_dict.items():
        if isinstance(value, str):
            cleaned[key] = clean_unicode_text(value)
        elif isinstance(value, list):
            cleaned[key] = clean_list_strings(value)
        else:
            cleaned[key] = value
    return cleaned

def safe_print(text):
    """Print text safely without Unicode errors"""
    try:
        print(clean_unicode_text(str(text)))
    except UnicodeEncodeError:
        # Fallback to ASCII-only
        print(str(text).encode('ascii', 'ignore').decode('ascii'))