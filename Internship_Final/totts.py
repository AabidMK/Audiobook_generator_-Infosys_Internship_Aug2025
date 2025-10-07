from TTS.api import TTS
# Generate TTS using English model
def generate_tts(cleaned_text):
    # Use Tacotron2-DDC as TTS model and HifiGAN vocoder for clear English voice
    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", 
              vocoder_name="vocoder_models/en/ljspeech/hifigan_v2")
    
    tts.tts_to_file(text=cleaned_text, file_path="voice_change.wav")