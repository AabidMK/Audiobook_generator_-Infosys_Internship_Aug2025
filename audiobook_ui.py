import os
import tempfile
import hashlib
import logging
from typing import List, Tuple

import streamlit as st
from dotenv import load_dotenv

# Load .env but DO NOT display keys in UI
load_dotenv()

# Import backend functions 
try:
    from pipeline_extraction import extract_text
    from pipeline_enrichment import enrich_text
    from pipeline_chunking import chunk_multiple_documents
    from pipeline_embedding import initialize_embedding_model, embed_chunks_for_pipeline
    from pipeline_chroma import get_chroma_client, get_or_create_collection, store_chunks, persist_client
    from pipeline_audio_edgetts import generate_audio
    from pipeline_rag import run_qna_session, initialize_qna_pipeline, trim_to_budget
except Exception as e:
    raise ImportError(f"Failed to import backend modules. Ensure backend files are present and importable. Original error: {e}")

# Ensure embedding model is loaded for the session
if 'embedding_model' not in st.session_state:
    st.session_state['embedding_model'] = initialize_embedding_model()

# Initialize ChromaDB collection if not already
if 'chroma_collection' not in st.session_state:
    try:
        client = get_chroma_client()
        collection = get_or_create_collection(client)
        st.session_state['chroma_collection'] = collection
        st.session_state['collection_ready'] = True
    except Exception as e:
        st.session_state['chroma_collection'] = None
        st.session_state['collection_ready'] = False
        st.warning("ChromaDB collection could not be initialized yet.")

# Logger
logger = logging.getLogger("audiobook_studio")
logger.setLevel(logging.INFO)

# Streamlit config
st.set_page_config(page_title="Audiobook Studio", layout="wide", initial_sidebar_state="collapsed")

# CSS styling
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    html, body, [class*="css"]  { font-family: 'Inter', sans-serif; background: linear-gradient(180deg, #f7f8fa 0%, #ffffff 100%); color: #1f2937; }
    .top-nav { display:flex; justify-content:flex-end; gap:12px; padding: 18px 28px 6px 28px; align-items:center; }
    .nav-btn { background: linear-gradient(180deg, #ffffff 0%, #f1f5f9 100%); border: 1px solid #e6e9ee; padding: 8px 16px; border-radius: 10px; box-shadow: 0 6px 18px rgba(30,41,59,0.04); cursor: pointer; font-weight: 600; color: #0f172a; }
    .nav-btn.active { background: linear-gradient(180deg, #eef2ff 0%, #e9f0ff 100%); border: 1px solid #dbeafe; box-shadow: 0 8px 24px rgba(59,130,246,0.08); }
    .logo-wrap { display:flex; flex-direction:column; align-items:center; justify-content:center; margin-top: 24px; margin-bottom: 12px; }
    .logo-card { width:120px; height:120px; background: linear-gradient(180deg, #ffffff 0%, #f7f7f7 100%); border-radius: 20px; box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06); display:flex; align-items:center; justify-content:center; border: 1px solid rgba(15,23,42,0.04); }
    .logo-text { margin-top:12px; font-size:20px; font-weight:700; color:#0f172a; letter-spacing:0.2px; }
    .panel { background: white; border-radius: 14px; padding: 20px; box-shadow: 0 10px 30px rgba(15,23,42,0.04); border: 1px solid rgba(15,23,42,0.03); }
    .msg-row { display:flex; margin-bottom: 10px; }
    .msg-user { margin-left:auto; background: linear-gradient(180deg,#eef2ff,#e6f0ff); padding:10px 14px; border-radius:14px 14px 6px 14px; max-width:70%; }
    .msg-assistant { margin-right:auto; background:#f3f4f6; padding:10px 14px; border-radius:14px 14px 14px 6px; max-width:70%; }
    .chat-input { display:flex; gap:8px; margin-top:12px; }
    .send-btn { background: linear-gradient(180deg,#4f46e5,#6366f1); color: white; padding:10px 12px; border-radius: 10px; border: none; cursor: pointer; font-weight:700; }
    .muted { color: #6b7280; font-size: 13px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Logo
logo_svg = """
<div class="logo-wrap">
  <div class="logo-card">
    <svg width="72" height="72" viewBox="0 0 72 72" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="36" cy="36" r="28" fill="white" stroke="#e6e9ee" stroke-width="1.5"/>
      <path d="M26 36c1.5-6 6-10 10-10" stroke="#9ca3af" stroke-width="2.4" stroke-linecap="round"/>
      <path d="M30 36c1-3.5 3-6 6-6" stroke="#c7cbd1" stroke-width="2.2" stroke-linecap="round"/>
      <path d="M38 36c1.5 6 6 10 10 10" stroke="#9ca3af" stroke-width="2.4" stroke-linecap="round"/>
    </svg>
  </div>
  <div class="logo-text">Audiobook Studio</div>
</div>
"""
st.markdown(logo_svg, unsafe_allow_html=True)

# Navigation buttons
if 'view' not in st.session_state:
    st.session_state['view'] = 'generate'

nav_col1, nav_col2, nav_col3 = st.columns([1,1,6])
with nav_col2:
    if st.button("Generate Audio"):
        st.session_state['view'] = 'generate'
with nav_col3:
    if st.button("Chat"):
        st.session_state['view'] = 'chat'

st.write("")  # divider

main_col1, main_col2, main_col3 = st.columns([1,6,1])
with main_col2:

    if st.session_state['view'] == 'generate':
        # Generate Audio panel
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("Generate Audio")
        uploaded_files = st.file_uploader("Upload one or more files", accept_multiple_files=True, type=['pdf','docx','png','jpg','jpeg','bmp','tiff'])
        start_clicked = st.button("Start & Generate")
        if start_clicked:
            if not uploaded_files:
                st.error("Please upload at least one file to proceed.")
            else:
                temp_paths = []
                documents_for_chunks = []
                for f in uploaded_files:
                    suffix = os.path.splitext(f.name)[1] or ""
                    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
                    tmp.write(f.read())
                    tmp.close()
                    temp_paths.append(tmp.name)
                    try:
                        text, err = extract_text(tmp.name)
                    except Exception as e:
                        logger.exception("Extraction failure")
                        text, err = "", str(e)
                    if err:
                        logger.warning(f"Extraction warning for {f.name}: {err}")
                    if text.strip():
                        documents_for_chunks.append((text, f.name, tmp.name))
                if not documents_for_chunks:
                    st.error("No valid text extracted from uploaded files.")
                else:
                    with st.spinner("Processing..."):
                        try:
                            enriched_text = enrich_text("\n\n".join([d[0] for d in documents_for_chunks]))
                        except Exception:
                            logger.exception("Enrichment failed; using raw text")
                            enriched_text = "\n\n".join([d[0] for d in documents_for_chunks])
                        chunks = chunk_multiple_documents(documents_for_chunks)
                        if st.session_state.get('embedding_model') is None:
                            st.session_state['embedding_model'] = initialize_embedding_model()
                        embedding_model = st.session_state['embedding_model']
                        texts, embeddings, metadatas, ids = embed_chunks_for_pipeline(chunks, embedding_model)
                        try:
                            client = get_chroma_client()
                            collection = get_or_create_collection(client)
                            store_chunks(collection, texts, metadatas, ids, embeddings)
                            persist_client(client)
                            st.session_state['chroma_collection'] = collection
                            st.session_state['collection_ready'] = True
                        except Exception:
                            logger.exception("Chroma store failed")
                            st.session_state['collection_ready'] = False
                        try:
                            first_file_name = uploaded_files[0].name.rsplit('.',1)[0]
                            audio_file_name = f"{first_file_name}_output.wav"
                            os.makedirs("generated_audio", exist_ok=True)
                            out_path = os.path.join("generated_audio", audio_file_name)
                            generate_audio(enriched_text, output_file=out_path)
                            st.session_state['audio_file'] = out_path
                        except Exception:
                            logger.exception("Audio generation failed")
                            st.session_state['audio_file'] = None
        if st.session_state.get('audio_file'):
            st.audio(st.session_state['audio_file'])
            with open(st.session_state['audio_file'], "rb") as af:
                st.download_button("Download Audiobook (.wav)", data=af, file_name=os.path.basename(st.session_state['audio_file']))
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        # Chat panel using run_qna_session logic
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("Chat")
        st.markdown("<div class='muted'>Ask questions about uploaded documents. Chat history preserved for this session.</div>", unsafe_allow_html=True)

        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = []

        chat_box = st.empty()
        def render_chat():
            with chat_box.container():
                for turn in st.session_state['chat_history']:
                    st.markdown(f"<div class='msg-row'><div class='msg-user'>{turn['q']}</div></div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='msg-row'><div class='msg-assistant'>{turn['a']}</div></div>", unsafe_allow_html=True)
                    if 'citations' in turn:
                        for c in turn['citations']:
                            st.markdown(f"<div class='muted'>Citation: {c}</div>", unsafe_allow_html=True)
        render_chat()

        col_inp, col_send = st.columns([12,1])
        with col_inp:
            user_q = st.text_input("", key="chat_input", placeholder="Type your question here")
        with col_send:
            send = st.button("↑", key="send_btn")

        if send and user_q.strip():
            try:
                collection = st.session_state.get('chroma_collection', None)
                embedding_model = st.session_state.get('embedding_model', None)
                if  not collection  or not embedding_model:
                    st.error("No indexed documents found. Run Generate Audio first.")
                else:
                    answer, citations = run_qna_session( question=user_q, collection=collection,embedding_model=embedding_model)
                    st.session_state['chat_history'].append({'q': user_q, 'a': answer, 'citations': citations})
                    render_chat()
            except Exception:
                logger.exception("Chat failed")
                st.error("Failed to get answer. Check backend logs.")

        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("<div style='text-align:center; margin-top:18px; color:#9ca3af; font-size:13px;'>Audiobook Studio • Minimal white/silver theme</div>", unsafe_allow_html=True)