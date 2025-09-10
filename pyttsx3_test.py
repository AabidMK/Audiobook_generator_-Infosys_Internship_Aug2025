import pyttsx3

# Initialize the engine
engine = pyttsx3.init()

# Set speaking rate and volume
engine.setProperty("rate", 170)     # Speed (default ~200)
engine.setProperty("volume", 0.9)   # Volume (0.0 – 1.0)

# (Optional) Choose a voice (0 for male, 1 for female usually on Windows)
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)

# Text to convert
text = (
    "Welcome to our audiobook generator. This is PYTTSX3"
    "We are testing different text to speech systems to find which one "
    "sounds the most natural, pleasant, and engaging for long listening sessions."
)

# Save output to file
engine.save_to_file(text, "pyttsx3_sample.mp3")

# Run the speech engine
engine.runAndWait()

print("Audio saved as pyttsx3_sample.mp3")
