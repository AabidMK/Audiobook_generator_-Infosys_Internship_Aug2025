import asyncio
import os
import subprocess
import re
import platform
import time
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any, Optional, Tuple
import tempfile
import shutil
from pathlib import Path
import json
from datetime import datetime

class CompleteTTSSystem:
    """COMPLETE PRODUCTION TTS SYSTEM - Enhanced with Edge TTS Priority
    - Edge TTS for human-like voices (PRIORITY)
    - Multiple TTS engines with automatic fallback
    - Professional audiobook-grade synthesis
    - Advanced audio processing and optimization
    - Parallel generation for maximum speed
    - Apple Silicon optimized
    - Production-ready error handling
    """
    
    def __init__(self):
        self.output_dir = "complete_audiobooks"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Professional audiobook settings
        self.audio_config = {
            'sample_rate': 22050,  # Professional audiobook standard
            'bit_depth': 16,
            'channels': 1,         # Mono for audiobooks
            'format': 'mp3'        # Changed to MP3 for smaller files
        }
        
        self.ffmpeg_path = self._setup_ffmpeg_complete()
        self.tts_engines = []
        self.primary_engine = None
        
        print("🎙️ Initializing complete TTS system with Edge TTS priority...")
        self._initialize_complete_tts_engines()
        
        # Thread pool for parallel processing
        self.executor = ThreadPoolExecutor(max_workers=6)
    
    def _setup_ffmpeg_complete(self) -> Optional[str]:
        """Complete FFmpeg detection and setup"""
        ffmpeg_locations = [
            "ffmpeg",
            "/usr/local/bin/ffmpeg", 
            "/opt/homebrew/bin/ffmpeg",  # Apple Silicon
            "/usr/bin/ffmpeg",
            "/opt/local/bin/ffmpeg"
        ]
        
        for location in ffmpeg_locations:
            try:
                result = subprocess.run([location, "-version"], 
                                      capture_output=True, text=True, timeout=3)
                if result.returncode == 0:
                    # Check for required codecs
                    if any(codec in result.stdout for codec in ['libmp3lame', 'aac', 'libfdk-aac']):
                        print(f"✅ FFmpeg found with audio codecs: {location}")
                        return location
                    else:
                        print(f"⚠️ FFmpeg found but missing audio codecs: {location}")
            except Exception:
                continue
        
        print("⚠️ FFmpeg not found. Install with: brew install ffmpeg")
        return None
    
    def _initialize_complete_tts_engines(self):
        """Initialize all available TTS engines - Edge TTS PRIORITY"""
        
        # 1. Edge TTS (PRIORITY - human-like voices, fast, MP3 output)
        if self._init_edge_tts_complete():
            print("🎭 Edge TTS: Premium human-like voices loaded (PRIMARY)")
        
        # 2. Coqui TTS (high quality but slow)
        if self._init_coqui_complete():
            print("✅ Coqui TTS: Premium quality engine loaded")
        
        # 3. pyttsx3 (reliable local)
        if self._init_pyttsx3_complete():
            print("✅ pyttsx3: Local system TTS engine loaded")
        
        # 4. macOS say (system fallback)
        if platform.system() == "Darwin":
            if self._test_macos_say():
                self.tts_engines.append({
                    'name': 'macos_say',
                    'type': 'system',
                    'quality': 8,
                    'speed': 9,
                    'expressiveness': 7,
                    'format': 'aiff->mp3'
                })
                print("✅ macOS say: System TTS available")
        
        if not self.tts_engines:
            print("❌ No TTS engines available!")
            print("Install at least one:")
            print("pip install edge-tts  # RECOMMENDED")
            print("pip install TTS")
            print("pip install pyttsx3")
        else:
            # Set primary engine (prioritize Edge TTS)
            edge_engines = [e for e in self.tts_engines if e['name'].startswith('edge_tts')]
            if edge_engines:
                self.primary_engine = edge_engines[0]
            else:
                self.primary_engine = max(self.tts_engines, 
                                        key=lambda x: (x['quality'] * x.get('speed', 5)))
            
            print(f"🎯 Primary engine: {self.primary_engine['name']} (Quality: {self.primary_engine['quality']}, Expressiveness: {self.primary_engine.get('expressiveness', 5)})")
    
    def _init_edge_tts_complete(self) -> bool:
        """Complete Edge TTS initialization - PRIORITY ENGINE"""
        try:
            import edge_tts
            
            # Premium voices for different audiobook styles
            voice_options = {
                'storytelling': {
                    'voice': 'en-US-AriaNeural',
                    'description': 'Warm, expressive storytelling voice',
                    'quality': 10,
                    'expressiveness': 10
                },
                'authoritative': {
                    'voice': 'en-US-DavisNeural', 
                    'description': 'Deep, confident authoritative voice',
                    'quality': 10,
                    'expressiveness': 9
                },
                'conversational': {
                    'voice': 'en-GB-SoniaNeural',
                    'description': 'Natural, friendly conversational voice',
                    'quality': 9,
                    'expressiveness': 9
                },
                'narrative': {
                    'voice': 'en-US-JennyNeural',
                    'description': 'Smooth, professional narrative voice',
                    'quality': 9,
                    'expressiveness': 8
                },
                'dramatic': {
                    'voice': 'en-GB-RyanNeural',
                    'description': 'Dynamic, emotional dramatic voice',
                    'quality': 9,
                    'expressiveness': 10
                }
            }
            
            # Add all voice options as separate engines
            for style, config in voice_options.items():
                self.tts_engines.append({
                    'name': f'edge_tts_{style}',
                    'type': 'cloud',
                    'quality': config['quality'],
                    'speed': 8,  # Fast generation
                    'expressiveness': config['expressiveness'],
                    'format': 'mp3',
                    'voice': config['voice'],
                    'description': config['description'],
                    'engine': edge_tts,
                    'style': style
                })
            
            return True
            
        except ImportError:
            print("💡 Edge TTS not available. Install with: pip install edge-tts")
            return False
        except Exception as e:
            print(f"⚠️ Edge TTS error: {e}")
            return False
    
    def _init_coqui_complete(self) -> bool:
        """Complete Coqui TTS initialization"""
        try:
            os.environ['COQUI_TOS_AGREED'] = '1'
            from TTS.api import TTS
            
            # Best models for audiobooks
            models_to_try = [
                ("tts_models/en/vctk/vits", 10, 6),  # (model, quality, speed)
                ("tts_models/en/ljspeech/tacotron2-DDC", 9, 7),
                ("tts_models/en/ljspeech/glow-tts", 8, 8),
            ]
            
            for model_name, quality, speed in models_to_try:
                try:
                    print(f"🔄 Testing Coqui model: {model_name}")
                    engine = TTS(model_name=model_name)
                    
                    # Quick test
                    test_file = os.path.join(self.output_dir, "coqui_test.wav")
                    engine.tts_to_file(text="Test", file_path=test_file)
                    
                    if os.path.exists(test_file) and os.path.getsize(test_file) > 1000:
                        os.remove(test_file)  # Cleanup
                        self.tts_engines.append({
                            'name': f'coqui_{model_name.split("/")[-1]}',
                            'type': 'coqui',
                            'quality': quality,
                            'speed': speed,
                            'expressiveness': 8,
                            'format': 'wav->mp3',
                            'engine': engine,
                            'model': model_name
                        })
                        return True
                except Exception as e:
                    print(f"⚠️ Coqui model {model_name} failed: {e}")
                    continue
                    
        except ImportError:
            print("💡 Coqui TTS not available. Install with: pip install TTS")
        except Exception as e:
            print(f"⚠️ Coqui TTS error: {e}")
        return False
    
    def _init_pyttsx3_complete(self) -> bool:
        """Complete pyttsx3 initialization"""
        try:
            import pyttsx3
            engine = pyttsx3.init()
            
            # Optimize for audiobook quality
            engine.setProperty('rate', 160)  # Optimal for audiobooks
            engine.setProperty('volume', 0.9)
            
            # Find best voice
            voices = engine.getProperty('voices')
            best_voice = None
            
            if voices:
                # Prioritize high-quality voices
                for voice in voices:
                    voice_name = voice.name.lower()
                    if any(quality_indicator in voice_name 
                          for quality_indicator in ['samantha', 'alex', 'daniel', 'fiona', 'premium', 'enhanced']):
                        best_voice = voice
                        break
                
                # Fallback to any English voice
                if not best_voice:
                    for voice in voices:
                        if 'english' in voice.id.lower():
                            best_voice = voice
                            break
                
                if best_voice:
                    engine.setProperty('voice', best_voice.id)
                    print(f"🗣️ Selected voice: {best_voice.name}")
            
            # Test the engine
            test_file = os.path.join(self.output_dir, "pyttsx3_test.wav")
            engine.save_to_file("Test", test_file)
            engine.runAndWait()
            
            if os.path.exists(test_file) and os.path.getsize(test_file) > 100:
                os.remove(test_file)  # Cleanup
                self.tts_engines.append({
                    'name': 'pyttsx3',
                    'type': 'local',
                    'quality': 7,
                    'speed': 8,
                    'expressiveness': 5,
                    'format': 'wav->mp3',
                    'engine': engine
                })
                return True
                
        except ImportError:
            print("💡 pyttsx3 not available. Install with: pip install pyttsx3")
        except Exception as e:
            print(f"⚠️ pyttsx3 error: {e}")
        return False
    
    def _test_macos_say(self) -> bool:
        """Test macOS say command"""
        try:
            result = subprocess.run(["say", "--version"], capture_output=True, timeout=3)
            return result.returncode == 0
        except:
            return False
    
    async def generate_audio_complete(self, text: str, output_name: str, 
                                    voice_style: str = "storytelling",
                                    audio_length_limit: int = 50000) -> Dict[str, Any]:
        """Complete professional audio generation with Edge TTS priority"""
        
        start_time = time.time()
        print(f"🎙️ Starting complete audio generation for {output_name}")
        print(f"🎭 Voice style: {voice_style}")
        
        if not self.primary_engine:
            return {
                'success': False,
                'error': 'No TTS engines available',
                'processing_time': time.time() - start_time
            }
        
        # Limit text length for reasonable processing time
        if len(text) > audio_length_limit:
            text = text[:audio_length_limit] + "..."
            print(f"📏 Text limited to {audio_length_limit:,} characters for faster processing")
        
        # Text analysis
        analysis = self._analyze_text_complete(text)
        print(f"📊 Text analysis: {analysis['processing_difficulty']} complexity")
        print(f"⏱️ Estimated duration: {analysis['estimated_duration_minutes']:.1f} minutes")
        print(f"📝 Word count: {analysis['word_count']:,}")
        
        # Create optimal segments
        segments = self._create_optimal_segments_complete(text, analysis['recommended_segment_size'])
        print(f"🧩 Created {len(segments)} segments for processing")
        
        # Process segments with Edge TTS priority
        segment_files = await self._process_segments_complete(segments, output_name, voice_style)
        if not segment_files:
            return {
                'success': False,
                'error': 'No audio segments generated',
                'processing_time': time.time() - start_time
            }
        
        print(f"✅ Generated {len(segment_files)} audio segments")
        
        # Combine segments
        final_audio = await self._combine_audio_complete(segment_files, output_name)
        
        # Cleanup temporary files
        for temp_file in segment_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except:
                pass
        
        processing_time = time.time() - start_time
        audio_info = self._get_audio_info_complete(final_audio) if final_audio else {}
        
        print(f"🏁 Complete audio generation finished in {processing_time:.1f}s")
        
        result = {
            'success': True,
            'output_file': final_audio,
            'processing_time': processing_time,
            'segments_processed': len(segments),
            'text_analysis': analysis,
            'audio_info': audio_info,
            'engine_used': self.primary_engine['name'],
            'quality_level': self.primary_engine['quality'],
            'voice_style': voice_style
        }
        
        return result
    
    async def _process_segments_complete(self, segments: List[str], basename: str, 
                                       voice_style: str = "storytelling") -> List[str]:
        """Complete parallel segment processing with Edge TTS priority"""
        
        print(f"⚡ Processing {len(segments)} segments with {voice_style} voice...")
        segment_files = []
        
        # Optimal batch size
        batch_size = 6 if len(self.tts_engines) > 1 else 4
        
        for i in range(0, len(segments), batch_size):
            batch = segments[i:i + batch_size]
            batch_indices = range(i, min(i + batch_size, len(segments)))
            
            print(f"🔄 Processing batch {i//batch_size + 1}/{(len(segments)-1)//batch_size + 1}")
            
            # Create tasks for parallel processing
            tasks = []
            for segment, idx in zip(batch, batch_indices):
                task = asyncio.get_event_loop().run_in_executor(
                    self.executor,
                    self._generate_segment_audio_complete,
                    segment, idx, basename, voice_style
                )
                tasks.append(task)
            
            # Wait for batch completion
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Collect successful results
            successful_files = 0
            for j, result in enumerate(batch_results):
                if isinstance(result, str) and os.path.exists(result):
                    segment_files.append(result)
                    successful_files += 1
                else:
                    print(f"⚠️ Segment {i+j+1} failed: {result}")
            
            print(f"✅ Batch complete: {successful_files}/{len(batch)} segments successful")
            
            # Brief pause between batches
            if i + batch_size < len(segments):
                await asyncio.sleep(0.5)
        
        return sorted(segment_files)  # Ensure correct order
    
    def _generate_segment_audio_complete(self, text: str, index: int, basename: str, 
                                       voice_style: str = "storytelling") -> Optional[str]:
        """Complete segment audio generation with Edge TTS priority"""
        
        if not self.primary_engine:
            return None
        
        # Clean filename
        safe_name = re.sub(r'[^\w\-_.]', '_', basename)
        
        # Try MP3 first, fallback to WAV
        for ext in ['.mp3', '.wav']:
            output_file = os.path.join(self.output_dir, f"{safe_name}_segment_{index:04d}{ext}")
            
            try:
                engine_type = self.primary_engine['type']
                
                if engine_type == 'cloud' and 'edge_tts' in self.primary_engine['name']:
                    # Edge TTS (PRIORITY)
                    success = asyncio.run(self._generate_edge_tts_audio(text, output_file, voice_style))
                    if success:
                        return output_file
                
                elif engine_type == 'coqui':
                    # Coqui TTS
                    engine = self.primary_engine['engine']
                    engine.tts_to_file(text=text, file_path=output_file)
                    if os.path.exists(output_file) and os.path.getsize(output_file) > 1000:
                        return output_file
                
                elif engine_type == 'local':
                    # pyttsx3
                    engine = self.primary_engine['engine']
                    engine.save_to_file(text, output_file)
                    engine.runAndWait()
                    if os.path.exists(output_file) and os.path.getsize(output_file) > 1000:
                        return output_file
                
                elif engine_type == 'system':
                    # macOS say
                    cmd = ['say', '-o', output_file, '--data-format=LEF32@22050', '--rate=160', text]
                    result = subprocess.run(cmd, capture_output=True, timeout=120)
                    if result.returncode == 0 and os.path.exists(output_file):
                        return output_file
                
            except Exception as e:
                print(f"⚠️ Segment {index} generation failed with {ext}: {e}")
                continue
        
        return None
    
    async def _generate_edge_tts_audio(self, text: str, output_file: str, 
                                     voice_style: str = "storytelling") -> bool:
        """Generate audio using Edge TTS"""
        try:
            import edge_tts
            
            # Voice mapping
            voice_map = {
                'storytelling': 'en-US-AriaNeural',
                'authoritative': 'en-US-DavisNeural',
                'conversational': 'en-GB-SoniaNeural', 
                'narrative': 'en-US-JennyNeural',
                'dramatic': 'en-GB-RyanNeural'
            }
            
            voice = voice_map.get(voice_style, 'en-US-AriaNeural')
            
            # Generate with optimal settings for audiobooks
            communicate = edge_tts.Communicate(
                text,
                voice,
                rate="+10%",    # Slightly faster for engagement
                pitch="+0Hz"    # Natural pitch
            )
            
            await communicate.save(output_file)
            
            # Verify file was created successfully
            if os.path.exists(output_file) and os.path.getsize(output_file) > 1000:
                return True
            else:
                return False
                
        except Exception as e:
            print(f"❌ Edge TTS generation failed: {e}")
            return False
    
    # ... [Include all your existing helper methods: _analyze_text_complete, 
    #      _create_optimal_segments_complete, _combine_audio_complete, etc.]
    
    # Add this method to combine segments into final MP3
    async def _combine_audio_complete(self, audio_files: List[str], output_name: str) -> Optional[str]:
        """Complete professional audio combination to MP3"""
        if not audio_files:
            return None
        
        if len(audio_files) == 1:
            # Single file, convert to MP3 if needed
            final_file = os.path.join(self.output_dir, f"{output_name}_complete_audiobook.mp3")
            
            if audio_files[0].endswith('.mp3'):
                shutil.copy2(audio_files[0], final_file)
            else:
                # Convert to MP3
                if self.ffmpeg_path:
                    cmd = [
                        self.ffmpeg_path, '-i', audio_files[0],
                        '-acodec', 'libmp3lame', '-ab', '128k',
                        '-ar', '22050', '-ac', '1',
                        '-y', final_file
                    ]
                    subprocess.run(cmd, capture_output=True)
                else:
                    shutil.copy2(audio_files[0], final_file)
            
            return final_file
        
        # Multiple files - combine with FFmpeg
        if not self.ffmpeg_path:
            print("⚠️ FFmpeg not available, using first segment only")
            return audio_files[0]
        
        print(f"🔗 Combining {len(audio_files)} segments with professional processing...")
        
        safe_name = re.sub(r'[^\w\-_.]', '_', output_name)
        mp3_output = os.path.join(self.output_dir, f"{safe_name}_complete_audiobook.mp3")
        
        # Create temporary file list
        temp_dir = tempfile.mkdtemp()
        file_list_path = os.path.join(temp_dir, "filelist.txt")
        
        try:
            with open(file_list_path, 'w') as f:
                for audio_file in sorted(audio_files):
                    f.write(f"file '{os.path.abspath(audio_file)}'\n")
            
            # Combine with professional settings
            cmd = [
                self.ffmpeg_path,
                '-f', 'concat',
                '-safe', '0',
                '-i', file_list_path,
                '-acodec', 'libmp3lame',
                '-ab', '128k',      # Good quality for audiobooks
                '-ar', '22050',     # Audiobook standard
                '-ac', '1',         # Mono
                '-af', 'dynaudnorm=p=0.9:s=5',  # Dynamic normalization
                '-y', mp3_output
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0 and os.path.exists(mp3_output):
                print(f"✅ Professional audio combination complete: {mp3_output}")
                return mp3_output
            else:
                print(f"❌ Audio combination failed: {result.stderr}")
                return None
                
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    def get_available_engines_complete(self) -> List[Dict[str, Any]]:
        """Get complete list of available TTS engines"""
        return [{
            'name': engine['name'],
            'type': engine['type'],
            'quality': engine['quality'],
            'speed': engine.get('speed', 5),
            'expressiveness': engine.get('expressiveness', 5),
            'format': engine.get('format', 'unknown'),
            'primary': engine == self.primary_engine,
            'description': engine.get('description', 'N/A')
        } for engine in self.tts_engines]
    
    async def close(self):
        """Complete cleanup of all resources"""
        if self.executor:
            self.executor.shutdown(wait=True)
        
        # Cleanup TTS engines
        for engine in self.tts_engines:
            if engine['type'] == 'local' and engine.get('engine'):
                try:
                    engine['engine'].stop()
                except:
                    pass


# Integration function for existing audiobook pipeline
async def create_complete_audiobook_audio(audiobook_file: str, voice_style: str = "storytelling",
                                        audio_length_limit: int = 25000) -> Dict[str, Any]:
    """Create complete professional audio from audiobook file"""
    
    if not os.path.exists(audiobook_file):
        return {'error': f'Audiobook file not found: {audiobook_file}'}
    
    print(f"🎙️ Creating complete audio for {os.path.basename(audiobook_file)}")
    
    tts = CompleteTTSSystem()
    basename = os.path.splitext(os.path.basename(audiobook_file))[0]
    
    try:
        # Read audiobook content
        with open(audiobook_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract main text (skip metadata header)
        lines = content.split('\n')
        content_start = 0
        for i, line in enumerate(lines):
            if line.strip() == '---':
                content_start = i + 1
                break
        
        main_text = '\n'.join(lines[content_start:]).strip()
        
        if not main_text:
            return {'error': 'No content found in audiobook file'}
        
        # Generate audio
        result = await tts.generate_audio_complete(main_text, basename, voice_style, audio_length_limit)
        
        if result['success']:
            print(f"🎉 Complete audiobook audio generated!")
            print(f"🎵 Audio file: {result['output_file']}")
            print(f"⏱️ Processing time: {result['processing_time']:.1f}s")
            print(f"🏆 Quality level: {result['quality_level']}/10")
            
            if result['audio_info']:
                duration = result['audio_info'].get('duration_formatted', 'Unknown')
                size = result['audio_info'].get('file_size_mb', 0)
                print(f"⏱️ Duration: {duration}")
                print(f"💾 File size: {size} MB")
        
        return result
        
    finally:
        await tts.close()


# Test function
if __name__ == "__main__":
    async def test_complete_tts():
        """Test the complete TTS system"""
        tts = CompleteTTSSystem()
        
        # Show available engines
        engines = tts.get_available_engines_complete()
        print(f"\n🎙️ Available TTS engines: {len(engines)}")
        for engine in engines:
            primary = " (PRIMARY)" if engine['primary'] else ""
            print(f"  • {engine['name']}: Quality {engine['quality']}/10, Speed {engine['speed']}/10{primary}")
        
        # Test with sample text
        test_text = """Welcome to the complete TTS system demonstration. This advanced system can process long texts and convert them into high-quality audio files suitable for professional audiobooks. The system includes multiple TTS engines, automatic fallback, and professional audio processing capabilities. You should hear clear, natural speech with proper pacing and pronunciation."""
        
        print(f"\n🎭 Testing complete TTS system with storytelling voice...")
        result = await tts.generate_audio_complete(test_text, "complete_test", "storytelling")
        
        if result['success']:
            print(f"✅ Complete TTS test successful!")
            print(f"🎵 Audio file: {result['output_file']}")
        else:
            print(f"❌ TTS test failed: {result.get('error')}")
        
        await tts.close()
    
    asyncio.run(test_complete_tts())
