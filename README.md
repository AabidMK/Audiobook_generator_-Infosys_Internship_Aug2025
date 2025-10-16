**🎧✨ AUDIOBOOK GENERATOR & AI ASSISTANT**

🔊 Transform your text into lifelike speech.
An intelligent system that converts text documents into human-like audiobooks using advanced NLP and Text-to-Speech (TTS) technologies.
It also supports transcription, summarization, and AI-based enrichment, making it an all-in-one audio reading and assistant platform.

**🗂️ PROJECT STRUCTURE**

AUDIOBOOK/

│
├──  audio_output/          # Generated audiobook files  
├──  chroma_db/             # Vector database for embeddings  
├──  input_files/           # Input text or document files  
├──  output/                # Processed output data  
├──  rag/                   # Retrieval-Augmented Generation components  
├──  venv/                  # Virtual environment  
│
├──  .env                   # Environment variables (API keys, config)  
├──  enricher.py            # Enhances text context before audio generation  
├──  extractor.py           # Extracts text/content from input files  
├──  list_models.py         # Lists available models for TTS/NLP  
├──  main.py                # Main entry point of the application  
├──  requirements.txt       # Project dependencies  
├──  transcribe.py          # Converts speech/audio to text  
├──  tts.py                 # Text-to-Speech configuration  
├──  tts_generator.py       # Core TTS and audiobook generation logic  
├──  output_audio.mp3       # Example generated audiobook  
└──  README.md              # Project documentation  




**⚙️ FEATURES**

✨ Text-to-Speech Conversion — Generate natural audiobook-style audio from any document

🧠 AI-Powered Enrichment — Enhance or summarize text using intelligent NLP models

🎤 Speech-to-Text Transcription — Convert voice recordings back into text

📚 RAG Integration — Contextualized responses using retrieval-augmented generation

🧩 Modular Architecture — Separate, reusable modules for extraction, enrichment, and generation


**🚀 HOW TO RUN**

📥 Clone the Repository

git clone https://github.com/yourusername/AUDIOBOOK.git
cd AUDIOBOOK


⚙️ Install Dependencies

pip install -r requirements.txt


🔐 Set Up Environment Variables

Create a .env file and add your API keys (if required).

▶️ Run the Application

python main.py


📂 View Output

Generated audiobooks will be saved in the audio_output/ folder.


**🧠 TECHNOLOGIES USED
Category	Tools / Frameworks**

💻 Programming	Python 3

🗣️ NLP	SpaCy, NER Models

🎧 Audio	OpenAI / Other TTS Engines

🌐 Interface	Streamlit (optional UI)

🧮 Data	ChromaDB (for vector embeddings)


**🎯 USE CASES**

🎓 Convert textbooks, notes, or articles into clear spoken audio

📰 Summarize large documents into short, easy-to-listen segments

♿ Enhance accessibility for visually impaired users

🤖 Build intelligent voice assistants for education or productivity

**🖼️ PREVIEW**

📁 Folder Snapshot:


**🎵 Sample Output:**
output_audio.mp3 — Generated audiobook file available in audio_output/


**💡 FUTURE ENHANCEMENTS**

🌍 Multilingual voice support

🧩 Integration with GPT-powered summarization

🎚️ Custom voice and tone settings

☁️ Cloud-based audiobook storage
