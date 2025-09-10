from gtts import gTTS

text = "Welcome to our audiobook generator. This is GTTS , We are exploring advanced text-to-speech systems to make audio sound more natural, emotional, and pleasant to listen to."

# Generate
tts = gTTS(text=text, lang="en")

# Save
tts.save("gtts_sample.mp3")

print("Done! Saved as gtts_sample.mp3")

