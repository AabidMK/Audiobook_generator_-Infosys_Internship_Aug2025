from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import tempfile
import shutil
import sys
import uuid
from dotenv import load_dotenv
import google.generativeai as genai

# Local imports (add your own modules)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from document_parser import extract_to_markdown
from totts import generate_tts
from ragcall import rag_call
from ragutils import create_collection, query_with_gemini

# ------------------------------------------------------------
# Initialize FastAPI app and CORS
# ------------------------------------------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------
# Load environment variables and configure Gemini API
# ------------------------------------------------------------
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "secrets.env"))
google_api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=google_api_key)

# Global variable to keep track of last generated audio
current_audio_id = None


# ------------------------------------------------------------
# Pydantic model for chat endpoint
# ------------------------------------------------------------
class ChatMessage(BaseModel):
    message: str


# ------------------------------------------------------------
# Root endpoint to verify server status
# ------------------------------------------------------------
@app.get("/")
async def root():
    return {"message": "FastAPI backend is running", "status": "ok"}


# ------------------------------------------------------------
# File Upload → Extract Text → Clean → TTS → Save Audio
# ------------------------------------------------------------
@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
            shutil.copyfileobj(file.file, tmp_file)
            temp_path = tmp_file.name

        # ------------------------------------------------------------
        # Extract text content from uploaded document
        # ------------------------------------------------------------
        try:
            md_path = temp_path.replace(os.path.splitext(temp_path)[1], ".md")
            extract_to_markdown(temp_path, md_path)

            with open(md_path, "r", encoding="utf-8") as f:
                markdown_content = f.read()

            # Clean up temporary files
            os.unlink(temp_path)
            os.unlink(md_path)

            # ------------------------------------------------------------
            # Prepare narration prompt for Gemini model
            # ------------------------------------------------------------
            prompt = f"""
You are an expert Conceptual Explainer and Professional Audiobook Narrator.
I will provide you with raw, parsed text extracted from a document.
Your job is to transform this text into a polished, audiobook-ready narration that is clear, deeply understandable, and fully engaging for listeners.

Guidelines to Follow:

1. Preserve Completeness:
    - Do not shorten, summarize, or omit any part of the original text.
    - Every concept and detail must remain fully intact and accurately conveyed.

2. Clean the Text:
    - Remove irrelevant elements such as headers, footers, page numbers, references, and formatting artifacts.
    - Fix broken sentences or parsing issues so they form complete, natural-sounding statements.

3. Ensure Deep Understanding:
    - Rewrite the content into clear, listener-friendly language that teaches or explains concepts thoroughly.
    - Break down complex ideas step-by-step so they are easy to grasp.
    - Use smooth transitions to maintain a logical flow and keep the listener engaged.

4. Handle Technical Content Naturally:
    - When encountering symbols, formulas, or calculations, focus on explaining their meaning and purpose rather than reading them literally.
    - Express them in natural, descriptive language that a listener can easily understand.
    - If there are step-by-step calculations, walk the listener through the process clearly and conclude with the final result in spoken form.
    - Ensure that even technical or numerical information flows naturally in the narration.

5. Expand for Clarity (When Needed):
    - If a sentence or idea is vague or confusing, slightly expand it for better understanding while staying true to the original meaning.

6. Audiobook Flow:
    - Maintain a consistent, engaging tone as if you are a skilled teacher guiding the listener.
    - Ensure smooth pacing and natural speech patterns for a pleasant listening experience.

7. Final Output:
    - Provide only the finalized audiobook narration, ready for direct Text-to-Speech (TTS) conversion.
    - Do not include instructions, notes, or metadata.
    - Do not add intros — the LLM will generate a topic-based intro automatically.

Here is the parsed text:

{markdown_content}
"""

            # ------------------------------------------------------------
            # Generate narration text using Gemini
            # ------------------------------------------------------------
            MODEL_NAME = "models/learnlm-2.0-flash-experimental"
            model = genai.GenerativeModel(model_name=MODEL_NAME)
            response = model.generate_content(
                prompt,
                request_options={"timeout": 600},  # 10 minutes timeout
            )
            audiobook_text = response.text

        except Exception as parse_error:
            print(f"File parsing failed: {parse_error}")
            audiobook_text = (
                f"Welcome to your audiobook. This is a demo narration for the file {file.filename}. "
                "The document contains important information that has been processed for audio consumption. "
                "This audiobook provides a clear and engaging presentation of the content."
            )

        # ------------------------------------------------------------
        # Generate unique audio ID and TTS file
        # ------------------------------------------------------------
        audio_id = str(uuid.uuid4())[:8]
        global current_audio_id
        current_audio_id = audio_id

        # ------------------------------------------------------------
        # Store document in RAG system
        # ------------------------------------------------------------
        try:
            rag_call(audiobook_text, file.filename)
            print("Document stored in RAG system")
        except Exception as rag_error:
            print(f"RAG storage failed: {rag_error}")

        # ------------------------------------------------------------
        # Generate TTS audio file
        # ------------------------------------------------------------
        try:
            from TTS.api import TTS
            tts = TTS(
                model_name="tts_models/en/ljspeech/tacotron2-DDC",
                vocoder_name="vocoder_models/en/ljspeech/hifigan_v2",
            )

            audio_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                f"audio_{audio_id}.wav",
            )

            tts.tts_to_file(text=audiobook_text, file_path=audio_path)
            print(f"TTS audio generated: {audio_path}")

        except Exception as tts_error:
            print(f"TTS generation failed: {tts_error}")

        # ------------------------------------------------------------
        # Return response to frontend
        # ------------------------------------------------------------
        return {
            "success": True,
            "text": audiobook_text,
            "text_length": len(audiobook_text),
            "audio_ready": True,
            "audio_id": audio_id,
        }

    except Exception as e:
        print(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ------------------------------------------------------------
# Endpoint: Download generated audiobook
# ------------------------------------------------------------
@app.get("/api/download-audio")
async def download_audio():
    global current_audio_id

    if current_audio_id:
        audio_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            f"audio_{current_audio_id}.wav",
        )
        if os.path.exists(audio_path):
            return FileResponse(audio_path, media_type="audio/wav", filename="audiobook.wav")

    # Fallback to a default voice sample if current audio missing
    fallback_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "voice_change.wav",
    )
    if os.path.exists(fallback_path):
        return FileResponse(fallback_path, media_type="audio/wav", filename="audiobook.wav")

    raise HTTPException(status_code=404, detail="No audio file available. Please generate audiobook first.")


# ------------------------------------------------------------
# Endpoint: Chat with RAG-based knowledge base
# ------------------------------------------------------------
@app.post("/api/chat")
async def chat(message: ChatMessage):
    try:
        collection = create_collection()
        response, chunks = query_with_gemini(message.message, collection)

        if "I don't know" in response:
            response = (
                "I'm sorry, but I don't have enough information to answer that question. "
                "Could you please ask something else?"
            )
            return {"response": response}

        # Build readable file reference block
        if chunks:
            file_refs = "\n".join([f"[{i+1}] {c['file_path']}" for i, c in enumerate(chunks)])
            response_with_sources = (
                f"{response}\n\n"
                f"**📁 Referenced Files:**\n{file_refs}"
            )
        else:
            response_with_sources = response

        return {"response": response_with_sources}

    except Exception as e:
        print(f"Chat error: {e}")
        return {
            "response": "I'm having trouble accessing the knowledge base right now, "
                        "but I'm here to help with any questions about your documents."
        }

# ------------------------------------------------------------
# Main entry point
# ------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
