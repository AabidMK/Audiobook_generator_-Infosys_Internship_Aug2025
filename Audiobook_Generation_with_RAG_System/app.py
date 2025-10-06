import streamlit as st
import asyncio
import os
import time
import json
from datetime import datetime
from pathlib import Path
import tempfile
import base64
from typing import Dict, Any

st.set_page_config(
    page_title="🎙️ AI Audiobook Studio",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

try:
    from enhanced_extraction import EnhancedTextExtraction
    from audiobook_generator import StateOfTheArtAudiobookGenerator
    from rag_system import SimpleRAGSystem
    COMPONENTS_AVAILABLE = True
except ImportError as e:
    st.error(f"Missing components: {e}")
    COMPONENTS_AVAILABLE = False

def init_session_state():
    if 'pipeline' not in st.session_state:
        st.session_state.pipeline = None
    if 'rag_system' not in st.session_state:
        st.session_state.rag_system = None
    if 'processing_history' not in st.session_state:
        st.session_state.processing_history = []
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 'upload'

async def initialize_components():
    if st.session_state.pipeline is None:
        with st.spinner("🔄 Initializing AI components..."):
            try:
                st.session_state.pipeline = StateOfTheArtAudiobookGenerator(local_only=False)
                st.session_state.rag_system = SimpleRAGSystem()
                st.success("✅ Components initialized successfully!")
                return True
            except Exception as e:
                st.error(f"❌ Failed to initialize: {e}")
                return False
    return True

def get_file_download_link(file_path: str, filename: str) -> str:
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            bytes_data = f.read()
        b64 = base64.b64encode(bytes_data).decode()
        return f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">📥 Download {filename}</a>'
    return ""

def main():
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <h1>🎙️ AI Audiobook Studio</h1>
        <p style="font-size: 1.2em; color: #666;">Transform PDFs into Professional Audiobooks with AI</p>
    </div>
    """, unsafe_allow_html=True)

    if not COMPONENTS_AVAILABLE:
        st.error("⚠️ Required components not available. Please install dependencies.")
        return

    init_session_state()

    with st.sidebar:
        st.markdown("### 🛠️ Controls")
        
        if st.button("🔄 Reset Session", type="secondary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        st.markdown("### 📊 System Status")
        
        if st.session_state.pipeline:
            st.success("🤖 Audiobook Generator: Ready")
        else:
            st.warning("🤖 Audiobook Generator: Not initialized")
            
        if st.session_state.rag_system:
            st.success("🧠 RAG System: Ready")
            stats = st.session_state.rag_system.get_knowledge_base_stats_complete()
            st.metric("📚 Documents Indexed", stats.get('total_documents', 0))
        else:
            st.warning("🧠 RAG System: Not initialized")
        
        st.markdown("### 📈 Session Stats")
        total_processed = len(st.session_state.processing_history)
        st.metric("📄 Files Processed", total_processed)

    tab1, tab2, tab3, tab4 = st.tabs(["📄 Document Upload", "🎙️ Generate Audiobook", "🧠 Ask Questions", "📊 Analytics"])

    with tab1:
        st.markdown("## 📤 Upload & Process Document")
        
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=['pdf'],
            help="Upload a PDF document to convert into an audiobook"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            generate_audio = st.checkbox("🎵 Generate Audio", value=True)
            voice_style = st.selectbox(
                "🎭 Voice Style",
                ["storytelling", "authoritative", "conversational", "narrative", "dramatic"],
                index=0
            )
        
        with col2:
            audio_length = st.slider("📏 Audio Length (chars)", 5000, 50000, 25000, 5000)
            enable_rag = st.checkbox("🧠 Enable Q&A Indexing", value=True)

        if uploaded_file is not None:
            st.success(f"📁 File uploaded: {uploaded_file.name} ({uploaded_file.size:,} bytes)")
            
            if st.button("🚀 Process Document", type="primary"):
                if not asyncio.run(initialize_components()):
                    st.stop()
                
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    temp_path = tmp_file.name

                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    status_text.text("🔍 Extracting text...")
                    progress_bar.progress(10)
                    
                    extracted_text = EnhancedTextExtraction.extract_text_from_any(temp_path)
                    
                    if extracted_text.startswith("Error"):
                        st.error(f"❌ Text extraction failed: {extracted_text}")
                        return
                    
                    st.success(f"✅ Extracted {len(extracted_text):,} characters")
                    progress_bar.progress(30)
                    
                    status_text.text("🤖 Generating enhanced audiobook text...")
                    
                    audiobook_file = asyncio.run(
                        st.session_state.pipeline.generate_audiobook_text_complete(temp_path)
                    )
                    
                    if audiobook_file.startswith("❌"):
                        st.error(f"❌ Audiobook generation failed: {audiobook_file}")
                        return
                    
                    progress_bar.progress(60)
                    
                    result = {
                        'filename': uploaded_file.name,
                        'timestamp': datetime.now().isoformat(),
                        'extracted_chars': len(extracted_text),
                        'audiobook_file': audiobook_file,
                        'audio_file': None,
                        'rag_indexed': False
                    }
                    
                    if generate_audio:
                        status_text.text("🎙️ Generating audio...")
                        
                        try:
                            audio_result = asyncio.run(
                                st.session_state.pipeline.generate_audio_from_audiobook(
                                    audiobook_file, voice_style, audio_length
                                )
                            )
                            
                            if audio_result.get('success'):
                                result['audio_file'] = audio_result['audio_file']
                                st.success(f"🎵 Audio generated: {audio_result['file_size_mb']}MB")
                            else:
                                st.warning(f"⚠️ Audio generation failed: {audio_result.get('error')}")
                        
                        except Exception as e:
                            st.warning(f"⚠️ Audio generation error: {e}")
                    
                    progress_bar.progress(80)
                    
                    if enable_rag:
                        status_text.text("🧠 Indexing for Q&A...")
                        
                        try:
                            rag_result = st.session_state.rag_system.ingest_document_complete(
                                temp_path, extracted_text
                            )
                            
                            if rag_result.get('status') == 'success':
                                result['rag_indexed'] = True
                                st.success(f"🧠 Indexed {rag_result['chunks_created']} chunks")
                            else:
                                st.warning(f"⚠️ RAG indexing failed: {rag_result.get('error')}")
                        
                        except Exception as e:
                            st.warning(f"⚠️ RAG indexing error: {e}")
                    
                    progress_bar.progress(100)
                    status_text.text("✅ Processing complete!")
                    
                    st.session_state.processing_history.append(result)
                    
                    st.success("🎉 Document processed successfully!")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if os.path.exists(audiobook_file):
                            st.markdown(get_file_download_link(
                                audiobook_file, 
                                f"{Path(uploaded_file.name).stem}_audiobook.md"
                            ), unsafe_allow_html=True)
                    
                    with col2:
                        if result['audio_file'] and os.path.exists(result['audio_file']):
                            st.markdown(get_file_download_link(
                                result['audio_file'],
                                f"{Path(uploaded_file.name).stem}_audio.mp3"
                            ), unsafe_allow_html=True)
                
                except Exception as e:
                    st.error(f"❌ Processing failed: {e}")
                    import traceback
                    st.code(traceback.format_exc())
                
                finally:
                    if os.path.exists(temp_path):
                        os.unlink(temp_path)

    with tab2:
        st.markdown("## 🎙️ Generated Audiobooks")
        
        if st.session_state.processing_history:
            for i, item in enumerate(reversed(st.session_state.processing_history)):
                with st.expander(f"📄 {item['filename']} - {item['timestamp'][:16]}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("📝 Characters", f"{item['extracted_chars']:,}")
                    
                    with col2:
                        st.metric("🎵 Audio", "✅" if item['audio_file'] else "❌")
                    
                    with col3:
                        st.metric("🧠 Q&A Ready", "✅" if item['rag_indexed'] else "❌")
                    
                    if item['audiobook_file'] and os.path.exists(item['audiobook_file']):
                        st.markdown("**📖 Enhanced Text Preview:**")
                        try:
                            with open(item['audiobook_file'], 'r', encoding='utf-8') as f:
                                content = f.read()
                                preview = content[:1000] + "..." if len(content) > 1000 else content
                                st.text_area("", preview, height=150, key=f"preview_{i}")
                        except:
                            st.error("Could not load audiobook file")
                    
                    if item['audio_file'] and os.path.exists(item['audio_file']):
                        st.audio(item['audio_file'])
        else:
            st.info("📝 No audiobooks generated yet. Upload a document in the first tab!")

    with tab3:
        st.markdown("## 🧠 Ask Questions About Your Documents")
        
        if not st.session_state.rag_system:
            st.warning("🧠 RAG system not initialized")
        else:
            stats = st.session_state.rag_system.get_knowledge_base_stats_complete()
            
            if stats.get('ready_for_qa', False):
                st.success(f"📚 Knowledge base ready with {stats['total_documents']} documents")
                
                question = st.text_input(
                    "❓ Ask a question about your documents:",
                    placeholder="What is the main topic of the document?"
                )
                
                if question and st.button("🔍 Get Answer", type="primary"):
                    with st.spinner("🤔 Thinking..."):
                        try:
                            answer_result = asyncio.run(
                                st.session_state.rag_system.ask_question_complete(question)
                            )
                            
                            st.markdown("### 💡 Answer:")
                            st.markdown(answer_result['answer'])
                            
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                confidence = answer_result.get('confidence', 0)
                                st.metric("🎯 Confidence", f"{confidence:.1%}")
                            
                            with col2:
                                sources = answer_result.get('sources_used', 0)
                                st.metric("📚 Sources", sources)
                            
                            with col3:
                                method = answer_result.get('method', 'unknown')
                                st.metric("🔧 Method", method)
                        
                        except Exception as e:
                            st.error(f"❌ Q&A failed: {e}")
                
                if 'chat_history' not in st.session_state:
                    st.session_state.chat_history = []
                
                st.markdown("### 💬 Recent Questions")
                for i, (q, a) in enumerate(reversed(st.session_state.chat_history[-5:])):
                    with st.expander(f"Q: {q[:50]}..."):
                        st.markdown(f"**Question:** {q}")
                        st.markdown(f"**Answer:** {a}")
            else:
                st.info("📚 No documents indexed yet. Process documents with Q&A enabled first!")

    with tab4:
        st.markdown("## 📊 Analytics & System Info")
        
        if st.session_state.processing_history:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_files = len(st.session_state.processing_history)
                st.metric("📄 Total Files", total_files)
            
            with col2:
                total_chars = sum(item['extracted_chars'] for item in st.session_state.processing_history)
                st.metric("📝 Total Characters", f"{total_chars:,}")
            
            with col3:
                audio_files = sum(1 for item in st.session_state.processing_history if item['audio_file'])
                st.metric("🎵 Audio Files", audio_files)
            
            with col4:
                rag_files = sum(1 for item in st.session_state.processing_history if item['rag_indexed'])
                st.metric("🧠 Q&A Ready", rag_files)
            
            st.markdown("### 📈 Processing History")
            
            import pandas as pd
            
            df_data = []
            for item in st.session_state.processing_history:
                df_data.append({
                    'Filename': item['filename'],
                    'Timestamp': item['timestamp'][:16],
                    'Characters': item['extracted_chars'],
                    'Audio': '✅' if item['audio_file'] else '❌',
                    'Q&A': '✅' if item['rag_indexed'] else '❌'
                })
            
            if df_data:
                df = pd.DataFrame(df_data)
                st.dataframe(df, use_container_width=True)
        
        else:
            st.info("📊 No analytics data available yet")
        
        st.markdown("### 🔧 System Information")
        
        sys_info = {
            "Pipeline Status": "✅ Ready" if st.session_state.pipeline else "❌ Not Ready",
            "RAG Status": "✅ Ready" if st.session_state.rag_system else "❌ Not Ready",
            "Session Started": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        for key, value in sys_info.items():
            st.text(f"{key}: {value}")

if __name__ == "__main__":
    main()
