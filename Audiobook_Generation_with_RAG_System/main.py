import asyncio
import os
import time
import argparse
import json
import traceback
from datetime import datetime
from typing import Dict, Any, List

from enhanced_extraction import EnhancedTextExtraction
from audiobook_generator import StateOfTheArtAudiobookGenerator

try:
    import edge_tts
    TTS_AVAILABLE = True
    print("✅ Edge-TTS detected – audio generation ready")
except ImportError:
    TTS_AVAILABLE = False
    print("⚠️  Edge-TTS not installed (pip install edge-tts) – audio disabled")

try:
    from rag_system import Phase2RAGSystem
    RAG_AVAILABLE = True
    print("✅ RAG system with Groq detected – Q&A ready")
except ImportError:
    RAG_AVAILABLE = False
    print("⚠️  RAG system not available – Q&A features disabled")

class CompleteAudiobookPipeline:
    """
    COMPLETE STATE-OF-THE-ART AUDIOBOOK PIPELINE
    - PDF text extraction
    - Enhanced audiobook text generation (LLM)
    - Human-like audio generation (Edge TTS)
    - Intelligent document Q&A (RAG + Groq)
    """
    
    def __init__(
        self,
        enable_rag: bool = True,
        enable_tts: bool = True,
        local_only_llm: bool = False
    ):
        self.enable_rag = enable_rag and RAG_AVAILABLE
        self.enable_tts = enable_tts and TTS_AVAILABLE
        self.local_only_llm = local_only_llm

        # Components
        self.audiobook_generator = None
        self.rag_system = None

        # Session statistics
        self.stats = {
            "documents_processed": 0,
            "audiobooks_generated": 0,
            "audio_files_created": 0,
            "questions_answered": 0,
            "total_processing_sec": 0.0,
            "session_start": datetime.now().isoformat(),
            "components": {
                "audiobook_generator": "pending",
                "rag_system": "pending" if self.enable_rag else "disabled",
                "edge_tts": "pending" if self.enable_tts else "disabled"
            }
        }

    async def init_components(self) -> bool:
        """Initialize all pipeline components"""
        try:
            print("🔧 Initializing pipeline components...")
            
            # Initialize audiobook generator
            print("📚 Loading audiobook generator...")
            self.audiobook_generator = StateOfTheArtAudiobookGenerator(
                local_only=self.local_only_llm
            )
            self.stats["components"]["audiobook_generator"] = "ready"
            print("✅ Audiobook generator ready")
            
            # Initialize RAG system
            if self.enable_rag:
                print("🧠 Loading RAG system with Groq...")
                self.rag_system = Phase2RAGSystem(
    groq_api_key="",
    groq_model="mixtral-8x7b-32768"
)
                self.stats["components"]["rag_system"] = "ready"
                print("✅ RAG system ready")
            
            # Check Edge TTS
            if self.enable_tts:
                if hasattr(self.audiobook_generator, 'generate_audio_from_audiobook'):
                    self.stats["components"]["edge_tts"] = "ready"
                    print("✅ Edge TTS audio generation ready")
                else:
                    self.stats["components"]["edge_tts"] = "missing_method"
                    print("⚠️  Edge TTS method missing in audiobook generator")
            
            print("🚀 All components initialized successfully")
            return True
            
        except Exception as exc:
            print(f"❌ Component initialization failed: {exc}")
            traceback.print_exc()
            return False

    async def process_document_complete(
        self,
        pdf_path: str,
        generate_audio: bool = False,
        voice_style: str = "storytelling",
        audio_length_limit: int = 25000,
        index_in_rag: bool = True
    ) -> Dict[str, Any]:
        """Complete document processing pipeline"""

        pipeline_start = time.time()
        filename = os.path.basename(pdf_path)
        
        print(f"\n🚀 PROCESSING DOCUMENT: {filename}")
        print("=" * 60)
        
        result = {
            "file_path": pdf_path,
            "filename": filename,
            "started": datetime.now().isoformat(),
            "status": "processing",
            "components": {}
        }

        try:
            print("📖 STEP 1: Enhanced text extraction...")
            step1_start = time.time()
            
            extracted_text = EnhancedTextExtraction.extract_text_from_any(pdf_path)
            
            if extracted_text.startswith("Error"):
                result.update(
                    status="failed",
                    error=f"Text extraction failed: {extracted_text}",
                    total_time=time.time() - pipeline_start
                )
                return result
            
            step1_time = time.time() - step1_start
            result["components"]["text_extraction"] = {
                "status": "success",
                "characters_extracted": len(extracted_text),
                "processing_time": round(step1_time, 2)
            }
            print(f"✅ Extracted {len(extracted_text):,} characters in {step1_time:.1f}s")

            print("\n📚 STEP 2: Enhanced audiobook text generation...")
            step2_start = time.time()
            
            audiobook_file = await self.audiobook_generator.generate_audiobook_text_complete(pdf_path)
            
            if audiobook_file.startswith("❌"):
                result["components"]["audiobook_generation"] = {
                    "status": "failed",
                    "error": audiobook_file
                }
                print(f"❌ Audiobook generation failed: {audiobook_file}")
            else:
                step2_time = time.time() - step2_start
                result["components"]["audiobook_generation"] = {
                    "status": "success",
                    "output_file": audiobook_file,
                    "processing_time": round(step2_time, 2)
                }
                self.stats["audiobooks_generated"] += 1
                print(f"✅ Audiobook generated in {step2_time:.1f}s: {os.path.basename(audiobook_file)}")

            if generate_audio and self.enable_tts and not audiobook_file.startswith("❌"):
                print(f"\n🎙️  STEP 3: Audio generation ({voice_style} voice)...")
                step3_start = time.time()
                
                audio_result = await self.audiobook_generator.generate_audio_from_audiobook(
                    audiobook_file,
                    voice_style=voice_style,
                    audio_length_limit=audio_length_limit
                )
                
                step3_time = time.time() - step3_start
                result["components"]["audio_generation"] = {
                    **audio_result,
                    "processing_time": round(step3_time, 2)
                }
                
                if audio_result.get('success'):
                    self.stats["audio_files_created"] += 1
                    print(f"✅ Audio generated in {step3_time:.1f}s: {os.path.basename(audio_result['audio_file'])}")
                    print(f"🎭 Voice: {audio_result['voice']} | Size: {audio_result['file_size_mb']}MB | Duration: ~{audio_result['estimated_duration_min']}min")
                else:
                    print(f"❌ Audio generation failed: {audio_result.get('error')}")

            if index_in_rag and self.enable_rag:
                print(f"\n🧠 STEP 4: RAG indexing for intelligent Q&A...")
                step4_start = time.time()
                
                rag_result = self.rag_system.ingest_document_complete(pdf_path, extracted_text)
                step4_time = time.time() - step4_start
                
                result["components"]["rag_indexing"] = {
                    **rag_result,
                    "processing_time": round(step4_time, 2)
                }
                
                if rag_result.get('status') == 'success':
                    print(f"✅ RAG indexing completed in {step4_time:.1f}s: {rag_result['chunks_created']} chunks indexed")
                else:
                    print(f"❌ RAG indexing failed: {rag_result.get('error')}")

            pipeline_time = time.time() - pipeline_start
            
            result.update({
                "status": "success",
                "total_processing_time": round(pipeline_time, 2),
                "completed": datetime.now().isoformat()
            })
            
            # Update session stats
            self.stats["documents_processed"] += 1
            self.stats["total_processing_sec"] += pipeline_time
            
            print(f"\n🎉 DOCUMENT PROCESSING COMPLETE!")
            print(f"⏱️  Total time: {pipeline_time:.1f}s")
            print("=" * 60)
            
            return result

        except Exception as e:
            pipeline_time = time.time() - pipeline_start
            result.update({
                "status": "failed",
                "error": str(e),
                "total_processing_time": round(pipeline_time, 2),
                "completed": datetime.now().isoformat()
            })
            print(f"❌ Document processing failed: {e}")
            traceback.print_exc()
            return result

    async def interactive_qa_session(self):
        """Interactive Q&A session using RAG system"""
        
        if not self.enable_rag:
            print("❌ RAG system disabled. Enable with --rag to use Q&A features.")
            return
        
        # Get knowledge base stats
        stats = self.rag_system.get_knowledge_base_stats_complete()
        
        print(f"\n🧠 INTERACTIVE Q&A SESSION")
        print("=" * 60)
        print(f"📚 Knowledge base: {stats['total_documents']} documents indexed")
        print(f"⚡ Powered by: {stats.get('llm_model', 'Groq API')} (ultra-fast)")
        print(f"🎯 Embedding model: {stats.get('embedding_model', 'BGE-large-en-v1.5')}")
        
        if not stats.get('ready_for_qa', False):
            print("\n⚠️  No documents indexed yet. Process documents first with:")
            print("   python main.py document.pdf")
            return
        
        print(f"📋 Available sources:")
        for i, source in enumerate(stats.get('source_files', [])[:5], 1):
            print(f"   {i}. {source}")
        if len(stats.get('source_files', [])) > 5:
            print(f"   ... and {len(stats['source_files']) - 5} more")
        
        print(f"\n💡 Ask questions about your documents (type 'quit' to exit)")
        print("─" * 60)
        
        question_count = 0
        try:
            while True:
                question = input(f"\n❓ Your question: ").strip()
                
                if question.lower() in ['quit', 'exit', 'q', '']:
                    break
                
                if len(question) < 5:
                    print("💬 Please ask a more specific question.")
                    continue
                
                # Process question with timing
                print(f"🔄 Processing with Groq (ultra-fast)...")
                qa_start = time.time()
                
                result = await self.rag_system.ask_question_complete(question)
                qa_time = time.time() - qa_start
                
                question_count += 1
                self.stats["questions_answered"] += 1
                
                # Display results
                if result.get('error'):
                    print(f"❌ Error: {result['error']}")
                    continue
                
                print(f"\n💡 Answer:")
                print(f"   {result['answer']}")
                
                print(f"\n📊 Details:")
                print(f"   • Confidence: {result['confidence']:.1%}")
                print(f"   • Sources used: {len(result.get('citations', []))}")
                print(f"   • Processing time: {qa_time:.2f}s")
                print(f"   • Model: {result.get('groq_model', 'Groq API')}")
                
                # Show sources
                if result.get('citations'):
                    print(f"\n📚 Sources:")
                    for citation in result['citations'][:3]:  # Show top 3
                        print(f"   • {citation['file_name']} (similarity: {citation['similarity']:.1%})")
                
                print("─" * 60)
                
        except KeyboardInterrupt:
            print(f"\n👋 Q&A session interrupted")
        except Exception as e:
            print(f"❌ Q&A session error: {e}")
        
        if question_count > 0:
            avg_time = (time.time() - qa_start) / question_count if question_count > 0 else 0
            print(f"\n📊 Session summary: {question_count} questions answered")
            print(f"⚡ Average response time: {avg_time:.2f}s per question")

    def get_session_stats(self) -> Dict[str, Any]:
        """Get comprehensive session statistics"""
        session_duration = (datetime.now() - datetime.fromisoformat(self.stats['session_start'])).total_seconds()
        
        return {
            **self.stats,
            "session_duration_minutes": round(session_duration / 60, 1),
            "avg_processing_time_per_doc": (
                round(self.stats['total_processing_sec'] / self.stats['documents_processed'], 1)
                if self.stats['documents_processed'] > 0 else 0
            ),
            "system_info": {
                "rag_available": RAG_AVAILABLE,
                "tts_available": TTS_AVAILABLE,
                "groq_api": bool(os.getenv('GROQ_API_KEY')) if RAG_AVAILABLE else False,
                "edge_tts": TTS_AVAILABLE
            }
        }

    async def close(self):
        """Clean up all resources"""
        try:
            if self.audiobook_generator:
                await self.audiobook_generator.close()
            
            if self.enable_rag and self.rag_system:
                await self.rag_system.close()
        except Exception as e:
            print(f"⚠️  Cleanup warning: {e}")

async def main():
    """Complete main function with full CLI support"""
    
    parser = argparse.ArgumentParser(
        prog="audiobook_pipeline",
        description="Complete State-of-the-Art Audiobook Pipeline with RAG Q&A",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
🚀 EXAMPLES:
  python main.py document.pdf                           # Generate audiobook text
  python main.py document.pdf --generate-audio          # + Generate MP3 audio  
  python main.py document.pdf --generate-audio --qa     # + Interactive Q&A
  python main.py *.pdf --generate-audio --voice storytelling  # Process multiple files
  python main.py --qa-only                              # Q&A mode (existing documents)
  python main.py document.pdf --no-rag                  # Disable Q&A features
  python main.py --stats                                # Show system statistics
        
🎭 VOICE STYLES: storytelling, authoritative, conversational, narrative, dramatic
⚡ POWERED BY: Groq API (ultra-fast Q&A) + Edge TTS (human-like audio)
        """
    )
    
    # File arguments
    parser.add_argument('files', nargs='*', help='PDF files to process')
    
    # Audio options
    parser.add_argument('--generate-audio', action='store_true',
                       help='Generate MP3 audio using Edge TTS')
    parser.add_argument('--voice-style',
                       choices=['storytelling', 'authoritative', 'conversational', 
                               'narrative', 'dramatic'],
                       default='storytelling',
                       help='Edge TTS voice style (default: storytelling)')
    parser.add_argument('--audio-length', type=int, default=25000,
                       help='Max characters for audio generation (default: 25000)')
    
    # RAG options
    parser.add_argument('--no-rag', action='store_true',
                       help='Disable RAG indexing and Q&A features')
    parser.add_argument('--qa', '--interactive', action='store_true',
                       help='Start interactive Q&A session after processing')
    parser.add_argument('--qa-only', action='store_true',
                       help='Start in Q&A-only mode (skip document processing)')
    
    # System options  
    parser.add_argument('--local-only', action='store_true',
                       help='Use only local LLMs (no Gemini/Groq APIs)')
    parser.add_argument('--stats', action='store_true',
                       help='Show system statistics and exit')
    
    args = parser.parse_args()
    
    # Header
    print("🚀 COMPLETE STATE-OF-THE-ART AUDIOBOOK PIPELINE")
    print("📚 PDF → Enhanced Text → 🎙️ Edge TTS Audio → 🧠 RAG Q&A")
    print("=" * 80)
    
    # Initialize pipeline
    pipeline = CompleteAudiobookPipeline(
        enable_rag=not args.no_rag,
        enable_tts=args.generate_audio,
        local_only_llm=args.local_only
    )
    
    # Initialize components
    if not await pipeline.init_components():
        print("❌ Pipeline initialization failed")
        return
    
    try:
        # Stats mode
        if args.stats:
            stats = pipeline.get_session_stats()
            print(f"\n📊 SYSTEM STATISTICS")
            print("=" * 60)
            print(json.dumps(stats, indent=2, default=str))
            
            if pipeline.enable_rag:
                rag_stats = pipeline.rag_system.get_knowledge_base_stats_complete()
                print(f"\n🧠 RAG SYSTEM STATISTICS")
                print("=" * 60)
                print(json.dumps(rag_stats, indent=2, default=str))
            return
        
        # Q&A-only mode
        if args.qa_only:
            await pipeline.interactive_qa_session()
            return
        
        # Document processing mode
        if not args.files:
            # Default test file
            test_files = ["testing.pdf"]
            if not os.path.exists("testing.pdf"):
                print("❌ No files specified and testing.pdf not found")
                print("💡 Usage: python main.py document.pdf --generate-audio --qa")
                return
        else:
            test_files = args.files
        
        # Process each file
        all_results = []
        for file_path in test_files:
            if not os.path.isfile(file_path):
                print(f"⚠️  File not found: {file_path}")
                continue
            
            result = await pipeline.process_document_complete(
                file_path,
                generate_audio=args.generate_audio,
                voice_style=args.voice_style,
                audio_length_limit=args.audio_length,
                index_in_rag=not args.no_rag
            )
            all_results.append(result)
        
        # Session summary
        if all_results:
            successful = len([r for r in all_results if r.get('status') == 'success'])
            total_time = sum(r.get('total_processing_time', 0) for r in all_results)
            
            print(f"\n📊 PROCESSING SUMMARY")
            print("=" * 60)
            print(f"📄 Documents processed: {successful}/{len(all_results)}")
            print(f"⏱️  Total processing time: {total_time:.1f}s")
            
            session_stats = pipeline.get_session_stats()
            print(f"📚 Audiobooks generated: {session_stats['audiobooks_generated']}")
            print(f"🎵 Audio files created: {session_stats['audio_files_created']}")
            
            # Offer Q&A session
            if args.qa and pipeline.enable_rag and successful > 0:
                print(f"\n💡 Starting interactive Q&A session...")
                await pipeline.interactive_qa_session()
            elif pipeline.enable_rag and successful > 0:
                print(f"\n💡 Documents indexed! Start Q&A with: python main.py --qa-only")
    
    except KeyboardInterrupt:
        print(f"\n👋 Pipeline interrupted by user")
    except Exception as e:
        print(f"\n❌ Pipeline error: {e}")
        traceback.print_exc()
    finally:
        await pipeline.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        traceback.print_exc()
