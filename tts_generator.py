from TTS.api import TTS
from utils import load_config

config = load_config()

def text_to_speech(text, output_file):
    tts = TTS(model_name=config['tts']['model_name'], gpu=config['tts']['use_gpu'], progress_bar=True)
    tts.tts_to_file(text=text, file_path=output_file)
    print(f"✅ Audio saved at {output_file}")
