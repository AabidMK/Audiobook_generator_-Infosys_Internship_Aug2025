import os
import json

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

def create_output_dir(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

def validate_file(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    if ext not in ['.pdf', '.docx', '.txt']:
        raise ValueError("Unsupported file type")
    return True
