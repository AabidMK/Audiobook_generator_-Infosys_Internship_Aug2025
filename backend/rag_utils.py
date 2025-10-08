import os
import json
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredWordDocumentLoader,
)
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter

# ------------------------------------
# Document Loader
# ------------------------------------
def load_document(file_path: str):
    """Load documents from PDF, TXT, or DOCX."""
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext == ".pdf":
            print(f"📘 Loading PDF: {file_path}")
            loader = PyPDFLoader(file_path)
        elif ext == ".txt":
            print(f"📄 Loading TXT: {file_path}")
            loader = TextLoader(file_path)
        elif ext == ".docx":
            print(f"📝 Loading DOCX: {file_path}")
            loader = UnstructuredWordDocumentLoader(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

        docs = loader.load()

        # Split into chunks for embedding
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(docs)
        print(f"✅ Loaded {len(chunks)} chunks.")
        return chunks
    except Exception as e:
        print(f"❌ Document loading failed: {e}")
        return []


# ------------------------------------
# Vector Store
# ------------------------------------
def create_vector_store(docs, persist_directory="chroma_db"):
    """Create a Chroma vector store with Ollama embeddings."""
    try:
        embeddings = OllamaEmbeddings(model="nomic-embed-text")

        os.makedirs(persist_directory, exist_ok=True)
        print("🧠 Creating or connecting to Chroma vector store...")

        # The new Chroma client doesn't require .persist()
        vector_store = Chroma(
            collection_name="rag_collection",
            embedding_function=embeddings,
            persist_directory=persist_directory,
        )

        if docs:
            print(f"➕ Adding {len(docs)} documents to Chroma collection...")
            vector_store.add_documents(docs)

        # Custom history tracking
        vector_store.qa_history = []

        print("✅ Vector store ready.")
        return vector_store

    except Exception as e:
        print(f"❌ Vector store creation failed: {e}")
        return None


# ------------------------------------
# RAG Chain
# ------------------------------------
def create_rag_chain(vector_store):
    """Create a retrieval-based QA chain."""
    try:
        if vector_store is None:
            raise ValueError("Vector store not initialized")

        print("🧩 Building RetrievalQA chain...")
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})
        llm = OllamaLLM(model="llama3")

        chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            chain_type="stuff",
            input_key="query",
            return_source_documents=True,
        )

        print("✅ RAG chain created successfully.")
        return chain
    except Exception as e:
        print(f"❌ RAG chain creation failed: {e}")
        return None


# ------------------------------------
# Store Q&A History
# ------------------------------------
def store_rag_answer(vector_store, answer: str, question: str, filename: str):
    """Save question-answer pairs in memory and optionally to disk."""
    try:
        if not hasattr(vector_store, "qa_history"):
            vector_store.qa_history = []
        vector_store.qa_history.append((question, answer))

        os.makedirs("temp_files", exist_ok=True)
        history_path = os.path.join("temp_files", f"{filename}_qa_history.json")

        with open(history_path, "w", encoding="utf-8") as f:
            json.dump(vector_store.qa_history, f, ensure_ascii=False, indent=2)

        print(f"💾 Saved Q&A history → {history_path}")
    except Exception as e:
        print(f"⚠️ Failed to store Q&A history: {e}")


# import os
# import time
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.document_loaders import PyPDFLoader, TextLoader
# from langchain_community.vectorstores import Chroma
# from langchain.docstore.document import Document
# from langchain_community.llms import Ollama
# from langchain_community.embeddings import OllamaEmbeddings
# from langchain.chains import RetrievalQA

# def load_document(file_path: str):
#     """
#     Load PDF, TXT, or DOCX into LangChain Document objects.
#     """
#     ext = os.path.splitext(file_path)[1].lower()
#     try:
#         if ext == ".pdf":
#             loader = PyPDFLoader(file_path)
#             docs = loader.load()
#             return docs
#         elif ext == ".txt":
#             loader = TextLoader(file_path, encoding="utf-8")
#             docs = loader.load()
#             return docs
#         elif ext == ".docx":
#             from docx import Document as DocxDocument
#             doc = DocxDocument(file_path)
#             all_text = "\n".join([p.text for p in doc.paragraphs])
#             return [Document(page_content=all_text, metadata={"source": file_path})]
#         else:
#             return []
#     except Exception as e:
#         print("❌ Error loading document:", e)
#         return []


# def create_vector_store(docs, persist_directory="./chroma_db"):
#     """
#     Split docs into chunks and create Chroma vector store with Ollama embeddings.
#     """
#     embeddings = OllamaEmbeddings(model="nomic-embed-text")  # run with Ollama

#     os.makedirs(persist_directory, exist_ok=True)

#     if os.path.exists(persist_directory) and os.listdir(persist_directory):
#         print("📂 Loading existing Chroma DB...")
#         vector_store = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
#     else:
#         print("⚡ Creating new Chroma DB...")
#         splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#         splits = splitter.split_documents(docs)
#         vector_store = Chroma.from_documents(
#             documents=splits,
#             embedding=embeddings,
#             persist_directory=persist_directory
#         )
#         vector_store.persist()
#         print("✅ Vector store created and persisted.")
#     return vector_store


# def create_rag_chain(vector_store):
#     """
#     Create RetrievalQA chain with Ollama as the LLM.
#     """
#     llm = Ollama(model="llama3")  # Change to "mistral" or any model you pulled
#     retriever = vector_store.as_retriever()
#     qa_chain = RetrievalQA.from_chain_type(
#         llm=llm,
#         chain_type="stuff",
#         retriever=retriever
#     )
#     return qa_chain


# def store_rag_answer(vector_store, answer, user_question, source_document):
#     """
#     Store Q&A pair into Chroma DB for history.
#     """
#     try:
#         qa_id = f"qa-{int(time.time())}"
#         vector_store.add_texts(
#             texts=[user_question, answer],
#             metadatas=[
#                 {"type": "user_question", "source_doc": source_document, "qa_id": qa_id},
#                 {"type": "rag_answer", "source_doc": source_document, "qa_id": qa_id}
#             ],
#             ids=[f"q-{qa_id}", f"a-{qa_id}"]
#         )
#         vector_store.persist()
#         print(f"💾 Stored Q&A pair {qa_id}")
#     except Exception as e:
#         print("❌ Error storing QA:", e)
