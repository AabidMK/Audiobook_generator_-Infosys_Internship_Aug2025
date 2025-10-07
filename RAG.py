from sentence_transformers import SentenceTransformer
import chromadb
from openai import OpenAI  # LM Studio exposes OpenAI-compatible API

# Initialize embedding model
embedding_model = SentenceTransformer("intfloat/e5-large-v2")

# Connect to ChromaDB
chroma_client = chromadb.PersistentClient(path="chroma_db")
collection = chroma_client.get_or_create_collection("audiobook_chunks")

# Connect to LM Studio (OpenAI-compatible endpoint)
client = OpenAI(
    base_url="http://localhost:1234/v1",  # LM Studio API URL
    api_key="not-needed"                  # LM Studio doesn’t need a real key
)

def rag_query(user_query):
    # Encode query into embeddings
    query_emb = embedding_model.encode([user_query], convert_to_numpy=True)[0]

    # Retrieve top matching chunks from Chroma
    results = collection.query(
        query_embeddings=[query_emb.tolist()],
        n_results=3
    )

    context = "\n".join(results["documents"][0])

    # Construct RAG prompt
    prompt = f"""
    You are a helpful assistant helping with audiobook summarization.
    Do NOT guess or make up any content not present in the context.
    Use ONLY the context below to answer the question.
    If the context does not contain the answer, say "I don't know."
    Context:
    {context}

    Question: {user_query}
    Answer:
    """

    # Call LM Studio (OpenAI-style)
    response = client.chat.completions.create(
        model="mistral-7b-instruct-v0.3",  # use your LM Studio model
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )

    return response.choices[0].message.content


# Example
print(rag_query("Summarize this research paper in simple words"))


# text_extraction_module.py
# import fitz
# import docx
# import pytesseract
# import easyocr
# from PIL import Image
# import os

# reader = easyocr.Reader(['en'])

# def extract_text_from_pdf(pdf_path, output_txt="output.txt"):
#     doc = fitz.open(pdf_path)
#     with open(output_txt, "w", encoding="utf-8") as f:
#         for page_num in range(len(doc)):
#             page = doc[page_num]

#             text = page.get_text()
#             f.write(f"\n--- Page {page_num+1} ---\n")
#             f.write(text + "\n")

#             for img_index, img in enumerate(page.get_images(full=True)):
#                 xref = img[0]
#                 base_image = doc.extract_image(xref)
#                 image_bytes = base_image["image"]

#                 image_path = f"temp_img_{page_num+1}_{img_index}.png"
#                 with open(image_path, "wb") as img_file:
#                     img_file.write(image_bytes)

#                 ocr_text_tess = pytesseract.image_to_string(Image.open(image_path))

#                 ocr_text_easy = reader.readtext(image_path, detail=0)

#                 f.write(f"\n[Image {img_index+1} OCR - Tesseract]:\n{ocr_text_tess}\n")
#                 f.write(f"\n[Image {img_index+1} OCR - EasyOCR]:\n{' '.join(ocr_text_easy)}\n")

#                 os.remove(image_path) 

# def extract_text_from_docx(docx_path, output_txt="output.txt"):
#     doc = docx.Document(docx_path)
#     with open(output_txt, "w", encoding="utf-8") as f:
#         for para in doc.paragraphs:
#             f.write(para.text + "\n")

# def extract_text_from_txt(txt_path, output_txt="output.txt"):
#     with open(txt_path, "r", encoding="utf-8") as infile, open(output_txt, "w", encoding="utf-8") as outfile:
#         outfile.write(infile.read())

# def extract_text(file_path, output_txt="output.txt"):
#     ext = file_path.split(".")[-1].lower()
#     if ext == "pdf":
#         extract_text_from_pdf(file_path, output_txt)
#     elif ext == "docx":
#         extract_text_from_docx(file_path, output_txt)
#     elif ext == "txt":
#         extract_text_from_txt(file_path, output_txt)
#     else:
#         raise ValueError("Unsupported file format. Use PDF, DOCX, or TXT.")
#     print(f"✅ Extracted text saved to {output_txt}")

# extract_text("./LLM based project titles_250918_142744.pdf", "extracted_text1.txt")

# Mistral.py
# # audiobook_api.py

# import os
# from urllib import response
# import requests
# from Text_Extraction_Module import extract_text

# # CONFIG
# LM_API_URL = "http://localhost:1234/v1/chat/completions"  # Change based on LM Studio settings
# MODEL_ID = "mistral-7b-instruct-v0.3"
# CHUNK_SIZE = 2048  # adjust based on model's context window (tokens)
# SYSTEM_PROMPT = (""" You are a professional audiobook narrator tasked with converting the following text into an engaging, fun, and easy-to-listen-to audiobook-style narration. Your task is to:
#     - Carefully preserve at least 80 percent of the original text content by character length, without summarizing, deleting, or omitting important text.
#     - Clearly announce section titles such as "Abstract", "Introduction", "Chapter X", "Conclusion", and distinctly mark them with engaging phrasing and natural pauses.
#     - Emphasize important concepts, facts, or emotional points to create a lively and immersive listening experience.
#     - Maintain smooth continuity with what was narrated previously, incorporating previous context seamlessly to avoid any abrupt changes or repetitions.
#     - Use varied sentence structures, tone, and pacing to keep the listener's attention.
#     - Do not add unrelated content, questions, or answers not found in the original.
#     - Treat the given text as the authoritative source and enrich only the style and presentation without altering the meaning.
#     Below is the text for narration:""")
# # ("Convert the following text into engaging audiobook-style narration without summarizing or deleting any of the information mentioned. "
# #     "Make it fun, interesting, and easy to listen to:\n")
# # """Convert the following academic text into engaging audiobook-style narration. Make it fun, interesting, and easy to listen to. Clearly announce section titles (e.g., 'Abstract', 'Introduction', 'Conclusion') and differentiate sections using phrasing and pauses. Emphasize important parts. without summarizing or deleting any of the information mentioned. Here is the text:"""

# def chunk_text(text, chunk_size=CHUNK_SIZE):
#     """Splits text into chunks under model's token/context window."""
#     paragraphs = text.split('\n\n')
#     chunks, curr_chunk = [], ""
#     for para in paragraphs:
#         if len(curr_chunk) + len(para) < chunk_size:
#             curr_chunk += para + "\n\n"
#         else:
#             chunks.append(curr_chunk.strip())
#             curr_chunk = para + "\n\n"
#     if curr_chunk.strip(): chunks.append(curr_chunk.strip())
#     return chunks

# def get_context_summary(text, max_length=300):
#     """
#     Extract a summary or last portion of the previous enriched text to carry over as context.
#     Keeps max_length characters to fit in context window.
#     """
#     # Simple approach: get last max_length characters, feel free to replace with summarization
#     return text[-max_length:] if len(text) > max_length else text

# def run_mistral_on_chunk(input_text, api_url=LM_API_URL):
#     headers = {"Content-Type": "application/json"}

#     payload = {
#         "model": MODEL_ID,
#         "messages": [
#             {"role": "user", "content": SYSTEM_PROMPT + input_text}
#         ],
#         "max_tokens": CHUNK_SIZE,
#         "temperature": 0.85
#     }
#     response = requests.post(api_url, json=payload, headers=headers)
#     if not response.ok:
#         print(f"API error details: {response.status_code} {response.text}")
#     response.raise_for_status()
#     return response.json()['choices'][0]['message']['content']

# def process_book_to_audiobook(input_file, output_file):
#     with open(input_file, "r", encoding="utf-8") as f:
#         raw_text = f.read()

#     chunks = chunk_text(raw_text)
#     enriched_chunks = []
#     carried_context = ""  # Store previous enriched content snippet

#     for idx, chunk in enumerate(chunks):
#         print(f"Processing chunk {idx+1}/{len(chunks)}")

#         # Concatenate carried context summary with current chunk text
#         prompt_input = ""
#         if carried_context:
#             prompt_input += f"Previously narrated excerpt:\n{carried_context}\n\n"
#         prompt_input += chunk

#         enriched_text = run_mistral_on_chunk(prompt_input)
#         enriched_chunks.append(enriched_text + "\n\n")

#         # Update carried context for next chunk processing
#         carried_context = get_context_summary(enriched_text, max_length=300)

#     enriched_book = "".join(enriched_chunks)
#     with open(output_file, "w", encoding="utf-8") as out_f:
#         out_f.write(enriched_book)

#     print(f"Enriched audiobook narration saved to {output_file}")

# # Usage example pointing to the extracted text file
# process_book_to_audiobook("extracted_text.md", "enriched_text.md")

# print("Context used:\n", context[:1000])  # preview first 1000 chars

# TTS_test.py
# import os
# import re
# import base64
# from sarvamai import SarvamAI
# from pydub import AudioSegment

# AudioSegment.converter = r"C:\\Users\\Hardik Rokde\\Downloads\\ffmpeg-8.0-essentials_build\\ffmpeg-8.0-essentials_build\\bin\\ffmpeg.exe"  # update path

# def preprocess_markdown(md_text: str) -> str:
#     md_text = re.sub(r"```.*?```", "", md_text, flags=re.DOTALL)
#     md_text = re.sub(r"#+\s*(.*)", r"\1. ", md_text)
#     md_text = re.sub(r"^\s*[-*]\s+", "- ", md_text, flags=re.MULTILINE)
#     md_text = md_text.replace("- ", "• ")
#     md_text = re.sub(r"[>*_`#]", "", md_text)
#     md_text = re.sub(r"\s+", " ", md_text)
#     return md_text.strip()

# def split_text(text: str, max_chars: int = 2400):
#     parts = []
#     while len(text) > max_chars:
#         split_at = text.rfind('.', 0, max_chars)
#         if split_at == -1:
#             split_at = max_chars
#         parts.append(text[:split_at+1].strip())
#         text = text[split_at+1:].strip()
#     if text:
#         parts.append(text)
#     return parts

# # --- Main Script ---
# with open("enriched_text.md", "r", encoding="utf-8") as f:
#     raw_text = f.read()

# clean_text = preprocess_markdown(raw_text)
# chunks = split_text(clean_text)

# client = SarvamAI(api_subscription_key="sk_vf4ahup5_2al499Fw3mxnX1iTN02C45Y9")

# audio_files = []
# for i, chunk in enumerate(chunks):
#     response = client.text_to_speech.convert(
#         text=chunk,
#         target_language_code="en-IN",
#         speaker="manisha",
#         pitch=0,
#         pace=1,
#         loudness=1.5,
#         speech_sample_rate=22050,
#         enable_preprocessing=True,
#         model="bulbul:v2"
#     )

#     # Access the base64 audio from the 'audios' list
#     base64_audio = response.audios[0]  # assume one chunk → one audio
#     audio_bytes = base64.b64decode(base64_audio)

#     filename = f"chunk_{i}.wav"
#     with open(filename, "wb") as f_out:
#         f_out.write(audio_bytes)
#     audio_files.append(filename)
#     print(f"✅ Saved {filename} ({len(chunk)} chars)")

# # Merge the chunks
# final_audio = AudioSegment.empty()
# for af in audio_files:
#     final_audio += AudioSegment.from_file(af, format="wav")

# final_audio.export("output_sarvam.mp3", format="mp3")
# print("🎉 Final audiobook: output_sarvam.mp3")

# text_chunking.py
# from langchain.text_splitter import RecursiveCharacterTextSplitter

# def chunk_text(text, chunk_size=1000, chunk_overlap=100):
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=chunk_size,
#         chunk_overlap=chunk_overlap
#     )
#     return splitter.split_text(text)

# # Example usage
# with open("enriched_text.md", "r", encoding="utf-8") as f:
#     raw_text = f.read()

# chunks = chunk_text(raw_text)
# print(f"✅ Split into {len(chunks)} chunks")

# from sentence_transformers import SentenceTransformer

# # Load embedding model
# embedding_model = SentenceTransformer("BAAI/bge-large-en")

# # Convert chunks to embeddings
# embeddings = embedding_model.encode(chunks, convert_to_numpy=True, show_progress_bar=True)

# print(f"✅ Generated {len(embeddings)} embeddings of dimension {embeddings.shape[1]}")

# import chromadb
# from chromadb.utils import embedding_functions

# # Create Chroma client (local storage)
# client = chromadb.PersistentClient(path="./chroma_store")

# # Define collection
# collection = client.get_or_create_collection(
#     name="audiobook_chunks"
# )

# # Add chunks with embeddings
# for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
#     collection.add(
#         ids=[f"chunk_{i}"],
#         embeddings=[emb.tolist()],
#         documents=[chunk],
#         metadatas=[{"chunk_id": i}]
#     )

# print("✅ Stored chunks in ChromaDB")


# query = "Explain the main idea of the introduction chapter."

# query_emb = embedding_model.encode([query], convert_to_numpy=True)[0]

# results = collection.query(
#     query_embeddings=[query_emb.tolist()],
#     n_results=3
# )

# print("🔎 Retrieved Chunks:")
# for doc in results["documents"][0]:
#     print("-", doc[:200], "...")

# tess.py
# import pytesseract
# print(pytesseract.get_tesseract_version())

# RAG.py
# from sentence_transformers import SentenceTransformer
# import chromadb
# from openai import OpenAI  # LM Studio exposes OpenAI-compatible API

# # Initialize embedding model
# embedding_model = SentenceTransformer("intfloat/e5-large-v2")

# # Connect to ChromaDB
# chroma_client = chromadb.PersistentClient(path="chroma_db")
# collection = chroma_client.get_or_create_collection("audiobook_chunks")

# # Connect to LM Studio (OpenAI-compatible endpoint)
# client = OpenAI(
#     base_url="http://localhost:1234/v1",  # LM Studio API URL
#     api_key="not-needed"                  # LM Studio doesn’t need a real key
# )

# def rag_query(user_query):
#     # Encode query into embeddings
#     query_emb = embedding_model.encode([user_query], convert_to_numpy=True)[0]

#     # Retrieve top matching chunks from Chroma
#     results = collection.query(
#         query_embeddings=[query_emb.tolist()],
#         n_results=3
#     )

#     context = "\n".join(results["documents"][0])

#     # Construct RAG prompt
#     prompt = f"""
#     You are an assistant helping with audiobook summarization.
#     Use ONLY the context below to answer the question.
#     If the context does not contain the answer, say "I don’t know."
#     Context:
#     {context}

#     Question: {user_query}
#     Answer:
#     """

#     # Call LM Studio (OpenAI-style)
#     response = client.chat.completions.create(
#         model="mistral-7b-instruct-v0.3",  # use your LM Studio model
#         messages=[{"role": "user", "content": prompt}]
#     )

#     return response.choices[0].message.content


# # Example
# print(rag_query("Summarize this research paper in simple words"))


# so this my entire project code done till now. Suggest me where to do the changes and what changes should I do such that the model doesn't halucinate because when I used mistral.py, firstly it generates a few lines of irrelevant random text(changes evertime i run it) and then even if i remove it from the enriched_text.md, the rag qna model when asked to summarize the introduction or the whole research paper, it is giving random answers completely irrelevant to the document.