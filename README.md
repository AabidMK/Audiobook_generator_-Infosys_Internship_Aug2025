🎧 Audiobook Generator & AI Assistant

An intelligent system that converts text documents into human-like audiobooks using advanced NLP and text-to-speech technologies. The assistant also supports transcription, summarization, and text enrichment — providing an all-in-one audio reading experience.

📁 Project Structure
AUDIOBOOK/
│
├── audio_output/          # Generated audiobook files
├── chroma_db/             # Vector database for embeddings
├── input_files/           # Input text or document files
├── output/                # Processed output data
├── rag/                   # Retrieval-Augmented Generation components
├── venv/                  # Virtual environment
│
├── .env                   # Environment variables (API keys, config)
├── enricher.py            # Enhances text context before audio generation
├── extractor.py           # Extracts text/content from input files
├── list_models.py         # Lists available models for TTS or NLP
├── main.py                # Main entry point of the application
├── requirements.txt       # Project dependencies
├── transcribe.py          # Converts speech/audio to text
├── tts.py                 # Text-to-Speech configuration
├── tts_generator.py       # Core TTS and audiobook generation logic
├── output_audio.mp3       # Example generated audiobook
└── README.md              # Project documentation

⚙️ Features

🎙 Text-to-Speech Conversion: Generate realistic audiobook audio from any text or document

🧠 AI-Powered Enrichment: Automatically enhance, clean, or summarize text

🔊 Speech-to-Text Transcription: Convert recorded audio back into readable text

📚 RAG Integration: Provides contextual responses and smart content generation

🧩 Modular Architecture: Separate modules for extraction, enrichment, and generation

🚀 How to Run

Clone the Repository

git clone https://github.com/yourusername/AUDIOBOOK.git
cd AUDIOBOOK


Install Dependencies

pip install -r requirements.txt


Set Up Environment Variables

Create a .env file and add your API keys (if required)

Run the Application

python main.py


View Output

Generated audiobooks will be saved inside the audio_output/ folder

🧠 Technologies Used

Python 3

SpaCy / NLP Models

OpenAI or Other TTS Engines

Streamlit (optional UI)

ChromaDB for Embedding Storage

🎯 Use Cases

Convert e-books, PDFs, or articles into spoken audio

Generate summarized audiobook versions of large documents

Build educational or accessibility-focused audio assistants

🖼️ Preview

🗂 Folder Snapshot:


🎧 Sample Output:
output_audio.mp3 — Generated audiobook file located in audio_output/
