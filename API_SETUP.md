# API Keys & Configuration Setup

## Required API Keys

### 1. Gemini API Key (Required for RAG Q&A)
- **Purpose**: Powers the RAG question-answering system
- **Get it from**: [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Free tier**: 60 requests per minute, 1500 requests per day
- **Setup**: Add to `.env` file as `GEMINI_API_KEY=your_key_here`

### 2. LM Studio (Optional - for local LLM)
- **Purpose**: Local text enhancement for audiobook generation
- **Download**: [LM Studio](https://lmstudio.ai/)
- **Models**: Llama 3, Mistral, Qwen2.5 (recommended)
- **Setup**: Start LM Studio server on `http://localhost:1234`

## Configuration Steps

### Step 1: Get Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the generated key

### Step 2: Configure Environment
1. Open `.env` file in project root
2. Replace `your_gemini_api_key_here` with your actual key:
   ```
   GEMINI_API_KEY=AIzaSyC-your-actual-key-here
   ```

### Step 3: Install Additional Dependencies
```bash
pip install edge-tts google-generativeai python-dotenv
```

## Features by Configuration

### With Gemini API Key:
✅ RAG question-answering  
✅ Basic audiobook text generation  
✅ Edge TTS audio generation  

### With LM Studio + Gemini:
✅ Enhanced audiobook text generation  
✅ RAG question-answering  
✅ Edge TTS audio generation  
✅ Local processing (privacy)  

### Minimal Setup (No API keys):
✅ Basic text extraction  
✅ Simple text enhancement  
✅ Edge TTS audio generation  
❌ No RAG Q&A functionality  

## Troubleshooting

### Gemini API Issues:
- Check API key is valid
- Verify daily quota not exceeded
- Ensure internet connection

### LM Studio Issues:
- Start LM Studio application
- Load a model (Llama 3.2 recommended)
- Start local server
- Check `http://localhost:1234/v1/models` responds

### Edge TTS Issues:
- Automatically installs when needed
- Requires internet connection
- No API key required

## Cost Information

### Gemini API:
- **Free tier**: 15 RPM, 1500 RPD
- **Paid**: $0.00015 per 1K characters input
- **Typical usage**: ~$0.01-0.05 per document

### LM Studio:
- **Free**: Completely free
- **Requirements**: 8GB+ RAM recommended
- **Models**: 3-8GB disk space per model

### Edge TTS:
- **Free**: Microsoft's free service
- **No limits**: Unlimited usage
- **Quality**: High-quality neural voices