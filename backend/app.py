import os
import shutil
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import gtts.lang

from rag_utils import load_document, create_vector_store, create_rag_chain, store_rag_answer
from tts_conversion import convert_text_to_audio

# =====================================
# FASTAPI APP CONFIGURATION
# =====================================
app = FastAPI(title="RAG Document AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================
# GLOBAL STATE
# =====================================
STATE = {
    "uploaded_filename": None,
    "uploaded_filepath": None,
    "vector_store": None,
    "rag_chain": None,
    "user_logged_in": False,
    "auth_token": None,
    "qa_history": []
}

# =====================================
# MODELS
# =====================================
class LoginPayload(BaseModel):
    username: str
    password: str

class QuestionPayload(BaseModel):
    question: str

class AudiobookPayload(BaseModel):
    lang_code: Optional[str] = "en"

# =====================================
# AUTH DEPENDENCY
# =====================================
def require_login(authorization: Optional[str] = Header(None)):
    """Check Bearer token before allowing access."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header format")

    token = parts[1]
    if not STATE["user_logged_in"] or token != STATE["auth_token"]:
        raise HTTPException(status_code=401, detail="Unauthorized. Please log in first.")

    return True

# =====================================
# ROUTES
# =====================================

@app.get("/")
def root():
    return {"msg": "Backend is running 🚀"}

# ---------- LOGIN ----------
@app.post("/api/login")
def login(payload: LoginPayload):
    """Simple fixed-credential login"""
    if payload.username == "admin" and payload.password == "password123":
        token = uuid.uuid4().hex
        STATE["user_logged_in"] = True
        STATE["auth_token"] = token
        return {"status": "ok", "token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# ---------- Q&A HISTORY ----------
@app.get("/api/qa-history")
def get_qa_history(auth: bool = Depends(require_login)):
    """Return stored QA history"""
    return {"qa_pairs": STATE.get("qa_history", [])}

# ---------- UPLOAD DOCUMENT ----------
@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...), auth: bool = Depends(require_login)):
    """Upload a document and create RAG chain"""
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()
    if ext not in [".pdf", ".txt", ".docx"]:
        raise HTTPException(status_code=400, detail="Only .pdf, .txt, .docx allowed")

    save_dir = os.path.join(os.path.dirname(__file__), "temp_files")
    os.makedirs(save_dir, exist_ok=True)
    unique_name = f"{uuid.uuid4().hex}_{filename}"
    save_path = os.path.join(save_dir, unique_name)
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    docs = load_document(save_path)
    if not docs:
        raise HTTPException(status_code=500, detail="Failed to load document")

    vector_store = create_vector_store(
        docs, persist_directory=os.path.join(os.path.dirname(__file__), "chroma_db")
    )
    rag_chain = create_rag_chain(vector_store)

    STATE.update({
        "uploaded_filename": filename,
        "uploaded_filepath": save_path,
        "vector_store": vector_store,
        "rag_chain": rag_chain,
    })

    return {"status": "ok", "filename": filename}

# ---------- ANSWER QUESTIONS ----------
@app.post("/api/answer")
async def get_answer(payload: QuestionPayload, auth: bool = Depends(require_login)):
    """Ask a question using RAG"""
    if not STATE.get("rag_chain"):
        raise HTTPException(status_code=400, detail="No document uploaded yet")

    question = payload.question
    chain = STATE["rag_chain"]

    try:
        print(f"🧠 /api/answer request: {question}")
        response = chain.invoke({"query": question})
        answer = response.get("result") or response.get("answer") or str(response)

        # Save to history
        STATE["qa_history"].append([question, answer])

        # Store in RAG vector store
        store_rag_answer(
            STATE["vector_store"], answer, question, STATE["uploaded_filename"]
        )

        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting answer: {e}")

# ---------- AUDIOBOOK GENERATION ----------
@app.post("/api/audiobook")
async def generate_audiobook(payload: AudiobookPayload, auth: bool = Depends(require_login)):
    """Convert uploaded text into audio"""
    if not STATE.get("uploaded_filepath"):
        raise HTTPException(status_code=400, detail="No document uploaded yet")

    lang_code = payload.lang_code or "en"
    try:
        docs = load_document(STATE["uploaded_filepath"])
        raw_text = "\n\n".join([getattr(d, "page_content", str(d)) for d in docs])

        save_dir = os.path.join(os.path.dirname(__file__), "temp_files")
        os.makedirs(save_dir, exist_ok=True)

        base_name = os.path.splitext(STATE["uploaded_filename"])[0]
        audio_filename = f"{base_name}_audiobook.mp3"
        audio_path = os.path.join(save_dir, audio_filename)

        audio_path = convert_text_to_audio(
            raw_text, output_filename=audio_path, lang_code=lang_code
        )

        if not audio_path or not os.path.exists(audio_path):
            raise HTTPException(status_code=500, detail="Audio generation failed")

        return FileResponse(audio_path, media_type="audio/mpeg", filename=audio_filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio generation error: {e}")

# ---------- LANGUAGES ----------
@app.get("/api/langs")
def list_languages():
    """List supported TTS languages"""
    return {"langs": gtts.lang.tts_langs()}


# import os
# import shutil
# import uuid
# import traceback
# from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Header
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import FileResponse
# from pydantic import BaseModel
# from typing import Optional
# import gtts.lang
# import json

# from rag_utils import load_document, create_vector_store, create_rag_chain, store_rag_answer
# from tts_conversion import convert_text_to_audio

# # FastAPI app
# app = FastAPI(title="RAG Document AI Backend")

# # Allow frontend (React) to talk to backend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # In production, restrict to your domain
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # -------------------
# # STATE & AUTH
# # -------------------
# STATE = {
#     "uploaded_filename": None,
#     "uploaded_filepath": None,
#     "vector_store": None,
#     "rag_chain": None,
#     "user_logged_in": False,
#     "auth_token": None,
#     "qa_history": []
# }

# HISTORY_PATH = os.path.join(os.path.dirname(__file__), "qa_history.json")


# # -------------------
# # MODELS
# # -------------------
# class LoginPayload(BaseModel):
#     username: str
#     password: str


# class QuestionPayload(BaseModel):
#     question: str


# class AudiobookPayload(BaseModel):
#     lang_code: Optional[str] = "en"


# # -------------------
# # Helper functions
# # -------------------
# def require_login(token: Optional[str] = Header(None)):
#     """Dependency to enforce login"""
#     if not STATE["user_logged_in"] or token != STATE["auth_token"]:
#         raise HTTPException(status_code=401, detail="Unauthorized. Please log in first.")
#     return True


# def save_history():
#     """Persist Q&A history to a JSON file"""
#     try:
#         with open(HISTORY_PATH, "w", encoding="utf-8") as f:
#             json.dump(STATE["qa_history"], f, ensure_ascii=False, indent=2)
#     except Exception as e:
#         print(f"⚠️ Could not save history: {e}")


# def load_history():
#     """Load persisted Q&A history if file exists"""
#     if os.path.exists(HISTORY_PATH):
#         try:
#             with open(HISTORY_PATH, "r", encoding="utf-8") as f:
#                 STATE["qa_history"] = json.load(f)
#         except Exception as e:
#             print("⚠️ Could not load history (corrupt?), starting empty:", e)
#             STATE["qa_history"] = []


# load_history()

# # -------------------
# # Routes
# # -------------------
# @app.get("/")
# def root():
#     return {"msg": "Backend is running 🚀"}


# @app.post("/api/login")
# def login(payload: LoginPayload):
#     """Simple login with fixed username/password"""
#     # NOTE: For production, replace with secure auth and hashed password from env
#     if payload.username == "admin" and payload.password == "password123":
#         token = uuid.uuid4().hex
#         STATE["user_logged_in"] = True
#         STATE["auth_token"] = token
#         return {"status": "ok", "token": token}
#     raise HTTPException(status_code=401, detail="Invalid credentials")


# @app.post("/api/upload")
# async def upload_document(file: UploadFile = File(...), auth: bool = Depends(require_login)):
#     """Upload a document and build vector store for RAG"""
#     filename = file.filename
#     ext = os.path.splitext(filename)[1].lower()
#     if ext not in [".pdf", ".txt", ".docx"]:
#         raise HTTPException(status_code=400, detail="Only .pdf, .txt, .docx allowed.")

#     # Save uploaded file
#     save_dir = os.path.join(os.path.dirname(__file__), "temp_files")
#     os.makedirs(save_dir, exist_ok=True)
#     unique_name = f"{uuid.uuid4().hex}_{filename}"
#     save_path = os.path.join(save_dir, unique_name)
#     with open(save_path, "wb") as f:
#         shutil.copyfileobj(file.file, f)

#     # Load docs + create vector store
#     docs = load_document(save_path)
#     if not docs:
#         raise HTTPException(status_code=500, detail="Failed to load document.")

#     vector_store = create_vector_store(
#         docs, persist_directory=os.path.join(os.path.dirname(__file__), "chroma_db")
#     )
#     rag_chain = create_rag_chain(vector_store)

#     # Save state
#     STATE["uploaded_filename"] = filename
#     STATE["uploaded_filepath"] = save_path
#     STATE["vector_store"] = vector_store
#     STATE["rag_chain"] = rag_chain

#     return {"status": "ok", "filename": filename}


# def _extract_answer_from_response(response):
#     """
#     Given a response (possibly dict or string), try to extract the best textual answer.
#     """
#     if isinstance(response, dict):
#         # common keys to check
#         for k in ("answer", "output", "result", "text", "content"):
#             if k in response and response[k]:
#                 return response[k]
#         # sometimes nested candidate structures:
#         # try to find text in response.candidates... for LLM providers
#         try:
#             # safe navigate a few levels
#             cand = response.get("candidates") or response.get("choices") or response.get("outputs")
#             if isinstance(cand, list) and len(cand) > 0:
#                 first = cand[0]
#                 # try several nested paths
#                 if isinstance(first, dict):
#                     for path in ("text", "content", "message", "output_text"):
#                         if path in first and first[path]:
#                             return first[path]
#                     # check deeper
#                     parts = first.get("content", {}).get("parts") if isinstance(first.get("content"), dict) else None
#                     if parts and isinstance(parts, list) and len(parts) and isinstance(parts[0], dict):
#                         if "text" in parts[0]:
#                             return parts[0]["text"]
#                 elif isinstance(first, str):
#                     return first
#         except Exception:
#             pass
#         # fallback: stringify
#         return str(response)
#     else:
#         return str(response)


# @app.post("/api/answer")
# async def get_answer(payload: QuestionPayload, auth: bool = Depends(require_login)):
#     """Ask a question to the RAG chain. This tries multiple invocation styles for LangChain compatibility."""
#     if not STATE.get("rag_chain"):
#         raise HTTPException(status_code=400, detail="No document uploaded yet")

#     question = payload.question
#     chain = STATE["rag_chain"]

#     # Debug print
#     print("\n🧠 /api/answer request:", question)

#     tried = []
#     response = None
#     answer = None
#     last_exc = None

#     # Sequence of call patterns to try (most compatible across LangChain versions)
#     call_attempts = [
#         ("chain.run(question)", lambda: chain.run(question)),
#         ("chain.invoke({'query': question})", lambda: chain.invoke({"query": question})),
#         ("chain.invoke({'input': question})", lambda: chain.invoke({"input": question})),
#         ("chain({'query': question})", lambda: chain({"query": question})),
#         ("chain({'input': question})", lambda: chain({"input": question})),
#         ("chain.__call__({'query': question})", lambda: chain.__call__({"query": question})),
#         ("chain.__call__({'input': question})", lambda: chain.__call__({"input": question})),
#     ]

#     for label, fn in call_attempts:
#         try:
#             tried.append(label)
#             print(f"Trying: {label}")
#             response = fn()
#             print("Raw response:", repr(response)[:1000])
#             # If result is a dict-like LangChain response containing nested fields, normalize it
#             if isinstance(response, dict) and "answer" in response and response["answer"]:
#                 answer = _extract_answer_from_response(response)
#             else:
#                 # extract generically
#                 candidate = _extract_answer_from_response(response)
#                 if candidate and len(candidate) > 0:
#                     answer = candidate
#             # If answer is still numeric/empty string, keep trying
#             if answer is not None and str(answer).strip() != "":
#                 break
#         except Exception as e:
#             last_exc = e
#             print(f"Attempt {label} failed: {e}")
#             traceback.print_exc()

#     if answer is None:
#         # nothing worked
#         err_msg = f"No usable response from RAG chain. Attempts: {tried}. Last error: {last_exc}"
#         print("❌", err_msg)
#         raise HTTPException(status_code=500, detail=err_msg)

#     # ensure string
#     answer = str(answer)

#     # Save to in-memory history & persist
#     try:
#         STATE["qa_history"].append([question, answer])
#         save_history()
#     except Exception as e:
#         print("⚠️ Could not save to qa_history:", e)

#     # Persist Q/A to vector store if possible
#     try:
#         store_rag_answer(
#             STATE.get("vector_store"), answer, question, STATE.get("uploaded_filename")
#         )
#     except Exception as e:
#         print("⚠️ store_rag_answer failed:", e)

#     print("✅ Final answer:", answer[:300])
#     return {"answer": answer}


# @app.post("/api/audiobook")
# async def generate_audiobook(payload: AudiobookPayload, auth: bool = Depends(require_login)):
#     if not STATE.get("uploaded_filepath"):
#         raise HTTPException(status_code=400, detail="No document uploaded yet")

#     lang_code = payload.lang_code or "en"
#     try:
#         docs = load_document(STATE["uploaded_filepath"])
#         raw_text = "\n\n".join([getattr(d, "page_content", str(d)) for d in docs])

#         save_dir = os.path.join(os.path.dirname(__file__), "temp_files")
#         os.makedirs(save_dir, exist_ok=True)
#         audio_path = os.path.join(save_dir, "audiobook.mp3")

#         audio_path = convert_text_to_audio(raw_text, output_filename=audio_path, lang_code=lang_code)

#         if not os.path.exists(audio_path):
#             raise HTTPException(status_code=500, detail="Audio file not found")

#         # ✅ Return the audio file directly to React
#         return FileResponse(audio_path, media_type="audio/mpeg", filename="audiobook.mp3")

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Audio generation error: {e}")

# @app.get("/api/langs")
# def list_languages():
#     """Return supported languages for TTS"""
#     return {"langs": gtts.lang.tts_langs()}


# @app.get("/api/qa-history")
# def get_qa_history(auth: bool = Depends(require_login)):
#     """Return stored Q&A pairs"""
#     return {"qa_pairs": STATE["qa_history"]}


# import os
# import shutil
# import uuid
# from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Header
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import FileResponse
# from pydantic import BaseModel
# from typing import Optional
# import gtts.lang

# from rag_utils import load_document, create_vector_store, create_rag_chain, store_rag_answer
# from tts_conversion import convert_text_to_audio

# # FastAPI app
# app = FastAPI(title="RAG Document AI Backend")

# # Allow frontend (React) to talk to backend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # In production, restrict: ["http://localhost:3000"]
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # -------------------
# # STATE & AUTH
# # -------------------
# STATE = {
#     "uploaded_filename": None,
#     "uploaded_filepath": None,
#     "vector_store": None,
#     "rag_chain": None,
#     "user_logged_in": False,   # 👈 track login status
#     "auth_token": None,        # 👈 store session token
#     "qa_history": []           # 👈 store question-answer history
# }

# # -------------------
# # MODELS
# # -------------------
# class LoginPayload(BaseModel):
#     username: str
#     password: str

# class QuestionPayload(BaseModel):
#     question: str

# class AudiobookPayload(BaseModel):
#     lang_code: Optional[str] = "en"

# # -------------------
# # AUTH HELPERS
# # -------------------
# def require_login(token: Optional[str] = Header(None)):
#     """Dependency to enforce login"""
#     if not STATE["user_logged_in"] or token != STATE["auth_token"]:
#         raise HTTPException(status_code=401, detail="Unauthorized. Please log in first.")
#     return True

# # -------------------
# # ROUTES
# # -------------------
# @app.get("/")
# def root():
#     return {"msg": "Backend is running 🚀"}

# @app.post("/api/login")
# def login(payload: LoginPayload):
#     """Simple login with fixed username/password"""
#     if payload.username == "admin" and payload.password == "password123":
#         token = uuid.uuid4().hex
#         STATE["user_logged_in"] = True
#         STATE["auth_token"] = token
#         return {"status": "ok", "token": token}
#     raise HTTPException(status_code=401, detail="Invalid credentials")

# @app.post("/api/upload")
# async def upload_document(file: UploadFile = File(...), auth: bool = Depends(require_login)):
#     """Upload a document and build vector store for RAG"""
#     filename = file.filename
#     ext = os.path.splitext(filename)[1].lower()
#     if ext not in [".pdf", ".txt", ".docx"]:
#         raise HTTPException(status_code=400, detail="Only .pdf, .txt, .docx allowed.")

#     # Save uploaded file
#     save_dir = os.path.join(os.path.dirname(__file__), "temp_files")
#     os.makedirs(save_dir, exist_ok=True)
#     unique_name = f"{uuid.uuid4().hex}_{filename}"
#     save_path = os.path.join(save_dir, unique_name)
#     with open(save_path, "wb") as f:
#         shutil.copyfileobj(file.file, f)

#     # Load docs + create vector store
#     docs = load_document(save_path)
#     if not docs:
#         raise HTTPException(status_code=500, detail="Failed to load document.")

#     vector_store = create_vector_store(
#         docs, persist_directory=os.path.join(os.path.dirname(__file__), "chroma_db")
#     )
#     rag_chain = create_rag_chain(vector_store)

#     # Save state
#     STATE["uploaded_filename"] = filename
#     STATE["uploaded_filepath"] = save_path
#     STATE["vector_store"] = vector_store
#     STATE["rag_chain"] = rag_chain

#     return {"status": "ok", "filename": filename}

# @app.post("/api/answer")
# async def get_answer(payload: QuestionPayload, auth: bool = Depends(require_login)):
#     """Ask a question to the RAG chain"""
#     if not STATE.get("rag_chain"):
#         raise HTTPException(status_code=400, detail="No document uploaded yet")

#     question = payload.question
#     try:
#         chain = STATE["rag_chain"]

#         # ✅ Use the modern invoke() method safely
#         response = chain.invoke({"input": question})
#         if isinstance(response, dict):
#             answer = (
#                 response.get("answer")
#                 or response.get("output")
#                 or response.get("result")
#                 or str(response)
#             )
#         else:
#             answer = str(response)

#         # Store in-memory history
#         STATE["qa_history"].append([question, answer])

#         # Persist Q&A pair
#         store_rag_answer(
#             STATE["vector_store"], answer, question, STATE["uploaded_filename"]
#         )

#         return {"answer": answer}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error getting answer: {e}")

# @app.post("/api/audiobook")
# async def generate_audiobook(payload: AudiobookPayload, auth: bool = Depends(require_login)):
#     """Convert uploaded document into audiobook MP3"""
#     if not STATE.get("uploaded_filepath"):
#         raise HTTPException(status_code=400, detail="No document uploaded yet")

#     lang_code = payload.lang_code or "en"
#     try:
#         docs = load_document(STATE["uploaded_filepath"])
#         raw_text = "\n\n".join([getattr(d, "page_content", str(d)) for d in docs])

#         save_dir = os.path.join(os.path.dirname(__file__), "temp_files")
#         os.makedirs(save_dir, exist_ok=True)
#         audio_path = os.path.join(save_dir, "audiobook.mp3")

#         audio_path = convert_text_to_audio(
#             raw_text, output_filename=audio_path, lang_code=lang_code
#         )

#         if not audio_path or not os.path.exists(audio_path):
#             raise HTTPException(status_code=500, detail="Audio generation failed")

#         return FileResponse(audio_path, media_type="audio/mpeg", filename="audiobook.mp3")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Audio generation error: {e}")

# @app.get("/api/langs")
# def list_languages():
#     """Return supported languages for TTS"""
#     return {"langs": gtts.lang.tts_langs()}

# @app.get("/api/qa-history")
# def get_qa_history(auth: bool = Depends(require_login)):
#     """Return stored Q&A pairs"""
#     return {"qa_pairs": STATE["qa_history"]}


# import os
# import shutil
# import uuid
# from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Header
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import FileResponse
# from pydantic import BaseModel
# from typing import Optional
# import gtts.lang

# from rag_utils import load_document, create_vector_store, create_rag_chain, store_rag_answer
# from tts_conversion import convert_text_to_audio

# # FastAPI app
# app = FastAPI(title="RAG Document AI Backend")

# # Allow frontend (React) to talk to backend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # In production, restrict: ["http://localhost:3000"]
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # -------------------
# # STATE & AUTH
# # -------------------
# STATE = {
#     "uploaded_filename": None,
#     "uploaded_filepath": None,
#     "vector_store": None,
#     "rag_chain": None,
#     "user_logged_in": False,   # 👈 track login status
#     "auth_token": None         # 👈 store session token
# }

# # -------------------
# # MODELS
# # -------------------
# class LoginPayload(BaseModel):
#     username: str
#     password: str

# class QuestionPayload(BaseModel):
#     question: str

# class AudiobookPayload(BaseModel):
#     lang_code: Optional[str] = "en"

# # -------------------
# # AUTH HELPERS
# # -------------------
# def require_login(token: Optional[str] = Header(None)):
#     """Dependency to enforce login"""
#     if not STATE["user_logged_in"] or token != STATE["auth_token"]:
#         raise HTTPException(status_code=401, detail="Unauthorized. Please log in first.")
#     return True

# # -------------------
# # ROUTES
# # -------------------
# @app.get("/")
# def root():
#     return {"msg": "Backend is running 🚀"}

# @app.post("/api/login")
# def login(payload: LoginPayload):
#     """Simple login with fixed username/password"""
#     if payload.username == "admin" and payload.password == "password123":
#         token = uuid.uuid4().hex
#         STATE["user_logged_in"] = True
#         STATE["auth_token"] = token
#         return {"status": "ok", "token": token}
#     raise HTTPException(status_code=401, detail="Invalid credentials")

# @app.post("/api/upload")
# async def upload_document(file: UploadFile = File(...), auth: bool = Depends(require_login)):
#     """Upload a document and build vector store for RAG"""
#     filename = file.filename
#     ext = os.path.splitext(filename)[1].lower()
#     if ext not in [".pdf", ".txt", ".docx"]:
#         raise HTTPException(status_code=400, detail="Only .pdf, .txt, .docx allowed.")

#     # Save uploaded file
#     save_dir = os.path.join(os.path.dirname(__file__), "temp_files")
#     os.makedirs(save_dir, exist_ok=True)
#     unique_name = f"{uuid.uuid4().hex}_{filename}"
#     save_path = os.path.join(save_dir, unique_name)
#     with open(save_path, "wb") as f:
#         shutil.copyfileobj(file.file, f)

#     # Load docs + create vector store
#     docs = load_document(save_path)
#     if not docs:
#         raise HTTPException(status_code=500, detail="Failed to load document.")

#     vector_store = create_vector_store(
#         docs, persist_directory=os.path.join(os.path.dirname(__file__), "chroma_db")
#     )
#     rag_chain = create_rag_chain(vector_store)

#     # Save state
#     STATE["uploaded_filename"] = filename
#     STATE["uploaded_filepath"] = save_path
#     STATE["vector_store"] = vector_store
#     STATE["rag_chain"] = rag_chain

#     return {"status": "ok", "filename": filename}

# @app.post("/api/answer")
# async def get_answer(payload: QuestionPayload, auth: bool = Depends(require_login)):
#     """Ask a question to the RAG chain"""
#     if not STATE.get("rag_chain"):
#         raise HTTPException(status_code=400, detail="No document uploaded yet")

#     question = payload.question
#     try:
#         chain = STATE["rag_chain"]

#         try:
#             answer = chain.run(question)
#         except Exception:
#             response = chain.invoke({"input": question})
#             answer = response.get("answer") if isinstance(response, dict) else str(response)

#         store_rag_answer(
#             STATE["vector_store"], answer, question, STATE["uploaded_filename"]
#         )

#         return {"answer": answer}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error getting answer: {e}")

# @app.post("/api/audiobook")
# async def generate_audiobook(payload: AudiobookPayload, auth: bool = Depends(require_login)):
#     """Convert uploaded document into audiobook MP3"""
#     if not STATE.get("uploaded_filepath"):
#         raise HTTPException(status_code=400, detail="No document uploaded yet")

#     lang_code = payload.lang_code or "en"
#     try:
#         docs = load_document(STATE["uploaded_filepath"])
#         raw_text = "\n\n".join([getattr(d, "page_content", str(d)) for d in docs])

#         save_dir = os.path.join(os.path.dirname(__file__), "temp_files")
#         os.makedirs(save_dir, exist_ok=True)
#         audio_path = os.path.join(save_dir, "audiobook.mp3")

#         audio_path = convert_text_to_audio(
#             raw_text, output_filename=audio_path, lang_code=lang_code
#         )

#         if not audio_path or not os.path.exists(audio_path):
#             raise HTTPException(status_code=500, detail="Audio generation failed")

#         return FileResponse(audio_path, media_type="audio/mpeg", filename="audiobook.mp3")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Audio generation error: {e}")

# @app.get("/api/langs")
# def list_languages():
#     """Return supported languages for TTS"""
#     return {"langs": gtts.lang.tts_langs()}

# import os
# import shutil
# import uuid
# from fastapi import FastAPI, UploadFile, File, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import FileResponse
# from pydantic import BaseModel
# from typing import Optional
# import gtts.lang

# from rag_utils import load_document, create_vector_store, create_rag_chain, store_rag_answer
# from tts_conversion import convert_text_to_audio

# # FastAPI app
# app = FastAPI(title="RAG Document AI Backend")

# # Allow frontend (React) to talk to backend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # change to ["http://localhost:3000"] in production
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Global state (stores last uploaded doc info in memory)
# STATE = {
#     "uploaded_filename": None,
#     "uploaded_filepath": None,
#     "vector_store": None,
#     "rag_chain": None
# }

# # Pydantic models
# class QuestionPayload(BaseModel):
#     question: str

# class AudiobookPayload(BaseModel):
#     lang_code: Optional[str] = "en"


# @app.get("/")
# def root():
#     return {"msg": "Backend is running 🚀"}


# @app.post("/api/upload")
# async def upload_document(file: UploadFile = File(...)):
#     """Upload a document and build vector store for RAG"""
#     filename = file.filename
#     ext = os.path.splitext(filename)[1].lower()
#     if ext not in [".pdf", ".txt", ".docx"]:
#         raise HTTPException(status_code=400, detail="Only .pdf, .txt, .docx allowed.")

#     # Save uploaded file
#     save_dir = os.path.join(os.path.dirname(__file__), "temp_files")
#     os.makedirs(save_dir, exist_ok=True)
#     unique_name = f"{uuid.uuid4().hex}_{filename}"
#     save_path = os.path.join(save_dir, unique_name)
#     with open(save_path, "wb") as f:
#         shutil.copyfileobj(file.file, f)

#     # Load docs + create vector store
#     docs = load_document(save_path)
#     if not docs:
#         raise HTTPException(status_code=500, detail="Failed to load document.")

#     vector_store = create_vector_store(docs, persist_directory=os.path.join(os.path.dirname(__file__), "chroma_db"))
#     rag_chain = create_rag_chain(vector_store)

#     # Save state
#     STATE["uploaded_filename"] = filename
#     STATE["uploaded_filepath"] = save_path
#     STATE["vector_store"] = vector_store
#     STATE["rag_chain"] = rag_chain

#     return {"status": "ok", "filename": filename}


# @app.post("/api/answer")
# async def get_answer(payload: QuestionPayload):
#     """Ask a question to the RAG chain"""
#     if not STATE.get("rag_chain"):
#         raise HTTPException(status_code=400, detail="No document uploaded yet")

#     question = payload.question
#     try:
#         chain = STATE["rag_chain"]

#         # Try chain.run first
#         try:
#             answer = chain.run(question)
#         except Exception:
#             response = chain.invoke({"input": question})
#             answer = response.get("answer") if isinstance(response, dict) else str(response)

#         # Store QA pair for persistence
#         store_rag_answer(STATE["vector_store"], answer, question, STATE["uploaded_filename"])

#         return {"answer": answer}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error getting answer: {e}")


# @app.post("/api/audiobook")
# async def generate_audiobook(payload: AudiobookPayload):
#     """Convert uploaded document into audiobook MP3"""
#     if not STATE.get("uploaded_filepath"):
#         raise HTTPException(status_code=400, detail="No document uploaded yet")

#     lang_code = payload.lang_code or "en"
#     try:
#         docs = load_document(STATE["uploaded_filepath"])
#         raw_text = "\n\n".join([getattr(d, "page_content", str(d)) for d in docs])

#         audio_path = os.path.join(os.path.dirname(__file__), "temp_files", "audiobook.mp3")
#         audio_path = convert_text_to_audio(raw_text, output_filename=audio_path, lang_code=lang_code)

#         if not audio_path or not os.path.exists(audio_path):
#             raise HTTPException(status_code=500, detail="Audio generation failed")

#         return FileResponse(audio_path, media_type="audio/mpeg", filename="audiobook.mp3")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Audio generation error: {e}")


# @app.get("/api/langs")
# def list_languages():
#     """Return supported languages for TTS"""
#     return {"langs": gtts.lang.tts_langs()}
