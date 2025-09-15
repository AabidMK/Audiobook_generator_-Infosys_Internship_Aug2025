import asyncio
import os
import subprocess
import re
import platform
from audiobook_generator import AudiobookGenerator

class QualityAudiobookTTS:
    """High-quality TTS optimized for professional audiobook results"""
    
    def __init__(self):
        self.output_dir = "creative_audiobooks"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Setup FFmpeg
        self.ffmpeg_available = self._setup_ffmpeg()
        
        # Load best quality TTS
        self.tts_engine = None
        self.tts_type = None
        self._load_quality_tts()
        
    def _setup_ffmpeg(self):
        """Setup FFmpeg"""
        for ffmpeg_path in ['ffmpeg', '/opt/homebrew/bin/ffmpeg', '/usr/local/bin/ffmpeg']:
            try:
                result = subprocess.run([ffmpeg_path, '-version'], 
                                      capture_output=True, text=True, timeout=3)
                if result.returncode == 0:
                    print(f"✅ FFmpeg: {ffmpeg_path}")
                    return ffmpeg_path
            except:
                continue
        
        print("❌ FFmpeg not found")
        return None
    
    def _load_quality_tts(self):
        """Load highest quality TTS available"""
        
        os.environ["COQUI_TOS_AGREED"] = "1"
        
        # Try best Coqui models first
        quality_models = [
            "tts_models/en/ljspeech/glow-tts",        # High quality, natural
            "tts_models/en/ljspeech/tacotron2-DDC",   # Good quality, stable
            "tts_models/en/ljspeech/speedy-speech"    # Fast but decent quality
        ]
        
        for model_name in quality_models:
            try:
                from TTS.api import TTS
                
                print(f"🎨 Loading {model_name.split('/')[-1]}...")
                self.tts_engine = TTS(model_name=model_name)
                self.tts_type = "coqui_quality"
                self.model_name = model_name.split('/')[-1]
                print(f"✅ High-quality TTS loaded: {self.model_name}")
                return
                
            except Exception as e:
                print(f"⚠️ {model_name} failed: {e}")
                continue
        
        # Fallback to well-configured pyttsx3
        try:
            import pyttsx3
            
            print("🎙️ Loading pyttsx3 with quality settings...")
            engine = pyttsx3.init()
            if engine:
                self.tts_engine = engine
                self.tts_type = "pyttsx3_quality"
                self._configure_quality_pyttsx3()
                print("✅ pyttsx3 loaded with quality optimization")
                return
                
        except Exception as e:
            print(f"⚠️ pyttsx3 failed: {e}")
        
        print("❌ No quality TTS engines available")
    
    def _configure_quality_pyttsx3(self):
        """Configure pyttsx3 for maximum audiobook quality"""
        try:
            voices = self.tts_engine.getProperty('voices')
            
            if voices:
                # Score voices for audiobook quality
                voice_scores = []
                
                for voice in voices:
                    score = 0
                    name_lower = voice.name.lower()
                    
                    # Prefer certain high-quality voices
                    quality_voices = [
                        'zira', 'hazel', 'alex', 'samantha', 'daniel',
                        'karen', 'moira', 'tessa', 'fiona', 'veena'
                    ]
                    
                    for quality_voice in quality_voices:
                        if quality_voice in name_lower:
                            score += 10
                            break
                    
                    # Prefer female voices for audiobooks (generally more pleasant)
                    if any(word in name_lower for word in ['female', 'woman', 'zira', 'hazel', 'samantha']):
                        score += 5
                    
                    # Prefer English voices
                    if any(word in voice.id.lower() for word in ['en', 'english', 'us', 'uk']):
                        score += 3
                    
                    voice_scores.append((voice, score))
                
                # Select highest scoring voice
                best_voice = max(voice_scores, key=lambda x: x[1])[0]
                self.tts_engine.setProperty('voice', best_voice.id)
                print(f"🎭 Selected quality voice: {best_voice.name}")
            
            # Optimize settings for audiobook quality
            self.tts_engine.setProperty('rate', 160)    # Professional audiobook pace
            self.tts_engine.setProperty('volume', 0.95) # Clear, strong voice
            
        except Exception as e:
            print(f"⚠️ pyttsx3 quality configuration failed: {e}")
    
    def analyze_text_for_quality(self, text):
        """Professional audiobook emotion and pacing analysis"""
        
        text_lower = text.lower()
        
        # Detect dialogue vs narration
        has_dialogue = '"' in text or "'" in text
        dialogue_ratio = (text.count('"') + text.count("'")) / len(text) * 100
        
        # Detect action vs description
        action_words = ['suddenly', 'quickly', 'ran', 'jumped', 'rushed', 'burst', 'grabbed']
        action_score = sum(1 for word in action_words if word in text_lower)
        
        # Detect emotional content
        emotions = {
            'excitement': {
                'keywords': ['excited', 'amazing', 'wonderful', 'fantastic', 'thrilled', 'incredible', '!'],
                'speed_modifier': 1.15,
                'quality_setting': 'expressive'
            },
            'sadness': {
                'keywords': ['sad', 'crying', 'tears', 'sorrow', 'mourning', 'grief', 'lonely'],
                'speed_modifier': 0.85,
                'quality_setting': 'gentle'
            },
            'anger': {
                'keywords': ['angry', 'furious', 'rage', 'shouted', 'yelled', 'mad'],
                'speed_modifier': 1.2,
                'quality_setting': 'intense'
            },
            'fear': {
                'keywords': ['scared', 'afraid', 'terrified', 'frightened', 'panic', 'horror'],
                'speed_modifier': 1.1,
                'quality_setting': 'tense'
            },
            'mystery': {
                'keywords': ['mysterious', 'secret', 'hidden', 'whisper', 'shadow', 'strange'],
                'speed_modifier': 0.9,
                'quality_setting': 'mysterious'
            },
            'joy': {
                'keywords': ['happy', 'joy', 'laugh', 'smile', 'cheerful', 'delighted'],
                'speed_modifier': 1.08,
                'quality_setting': 'warm'
            },
            'romance': {
                'keywords': ['love', 'heart', 'kiss', 'embrace', 'tender', 'gentle'],
                'speed_modifier': 0.95,
                'quality_setting': 'intimate'
            }
        }
        
        # Calculate emotion scores
        emotion_scores = {}
        for emotion, data in emotions.items():
            score = sum(1 for keyword in data['keywords'] if keyword in text_lower)
            if emotion == 'excitement':
                score += text.count('!')  # Extra weight for exclamations
            emotion_scores[emotion] = score
        
        # Determine primary emotion
        primary_emotion = max(emotion_scores, key=emotion_scores.get) if max(emotion_scores.values()) > 0 else 'neutral'
        emotion_intensity = min(emotion_scores[primary_emotion], 3) / 3.0
        
        # Determine content type and pacing
        if has_dialogue and dialogue_ratio > 20:
            content_type = 'dialogue_heavy'
            base_speed = 1.05  # Slightly faster for dialogue
        elif action_score > 2:
            content_type = 'action'
            base_speed = 1.1   # Faster for action
        elif any(word in text_lower for word in ['chapter', 'part', 'section']):
            content_type = 'chapter_heading'
            base_speed = 0.9   # Slower, more formal
        else:
            content_type = 'narrative'
            base_speed = 1.0   # Standard narrative pace
        
        # Get emotion settings
        emotion_data = emotions.get(primary_emotion, {'speed_modifier': 1.0, 'quality_setting': 'neutral'})
        
        return {
            'primary_emotion': primary_emotion,
            'emotion_intensity': emotion_intensity,
            'content_type': content_type,
            'has_dialogue': has_dialogue,
            'dialogue_ratio': dialogue_ratio,
            'action_score': action_score,
            'speed': base_speed * emotion_data['speed_modifier'],
            'quality_setting': emotion_data['quality_setting'],
            'text_length': len(text)
        }
    
    def enhance_text_for_quality(self, text, analysis):
        """Enhance text for better TTS quality"""
        
        # Smart text processing based on content
        enhanced_text = text
        
        # Handle dialogue better
        if analysis['has_dialogue']:
            # Add slight pauses before dialogue
            enhanced_text = re.sub(r'(")', r' \1', enhanced_text)
            enhanced_text = re.sub(r'(.")', r'\1 ', enhanced_text)
        
        # Handle chapter headings
        if analysis['content_type'] == 'chapter_heading':
            # Add pauses around chapter titles
            enhanced_text = re.sub(r'(Chapter\s+\d+)', r' \1 ', enhanced_text, flags=re.IGNORECASE)
        
        # Improve punctuation handling
        enhanced_text = re.sub(r'\.\.\.', ' ... ', enhanced_text)  # Ellipsis pauses
        enhanced_text = re.sub(r'--', ' -- ', enhanced_text)       # Em dash pauses
        
        # Clean up formatting
        enhanced_text = re.sub(r'\s+', ' ', enhanced_text)
        
        return enhanced_text.strip()
    
    def clean_text_for_professional_tts(self, text):
        """Professional-grade text cleaning"""
        
        # Comprehensive character replacement
        replacements = {
            '"': '"', '"': '"', ''': "'", ''': "'",
            '—': ' -- ', '–': ' - ', '…': ' ... ',
            '\n': ' ', '\t': ' ', '\r': ' ',
            '&': ' and ', '@': ' at ', '#': ' number ',
            '%': ' percent ', '$': ' dollars ',
            '€': ' euros ', '£': ' pounds '
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        # Remove problematic characters that break TTS
        text = re.sub(r'[^\w\s\.,!?;:\-\'\"()\[\]{}]', ' ', text)
        
        # Smart abbreviation handling
        abbreviations = {
            'Mr.': 'Mister', 'Mrs.': 'Misses', 'Ms.': 'Miss', 'Dr.': 'Doctor',
            'Prof.': 'Professor', 'St.': 'Saint', 'Ave.': 'Avenue',
            'etc.': 'etcetera', 'vs.': 'versus', 'e.g.': 'for example',
            'i.e.': 'that is', 'Ph.D.': 'PhD'
        }
        
        for abbrev, full in abbreviations.items():
            text = text.replace(abbrev, full)
        
        # Clean multiple spaces and normalize
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def split_into_quality_segments(self, text, optimal_size=4000):
        """Split text optimally for quality while maintaining reasonable speed"""
        
        segments = []
        
        # Try to split by chapters first
        if "Chapter" in text or "CHAPTER" in text:
            print("📖 Detected chapters - splitting by chapter boundaries")
            chapters = re.split(r'(?i)(chapter\s+\d+)', text)
            
            current_segment = ""
            for i, part in enumerate(chapters):
                if re.match(r'(?i)chapter\s+\d+', part):
                    # This is a chapter heading
                    if current_segment:
                        segments.append(current_segment.strip())
                    current_segment = part + " "
                else:
                    # This is chapter content
                    if len(current_segment + part) <= optimal_size:
                        current_segment += part
                    else:
                        if current_segment:
                            segments.append(current_segment.strip())
                        
                        # Split large content by scenes/paragraphs
                        if len(part) > optimal_size:
                            scene_segments = self._split_by_scenes(part, optimal_size)
                            segments.extend(scene_segments)
                            current_segment = ""
                        else:
                            current_segment = part
            
            if current_segment.strip():
                segments.append(current_segment.strip())
        
        else:
            # Split by scenes/paragraphs
            print("📄 No chapters detected - splitting by scenes and paragraphs")
            segments = self._split_by_scenes(text, optimal_size)
        
        # Filter and validate segments
        quality_segments = []
        for segment in segments:
            cleaned = segment.strip()
            if len(cleaned) > 50:  # Minimum viable segment length
                quality_segments.append(cleaned)
        
        print(f"✅ Created {len(quality_segments)} quality segments")
        print(f"📊 Average segment length: {sum(len(s) for s in quality_segments) // len(quality_segments):,} characters")
        
        return quality_segments
    
    def _split_by_scenes(self, text, optimal_size):
        """Split text by scenes and paragraph breaks"""
        
        segments = []
        
        # Try scene breaks first (double newline + common scene indicators)
        scene_patterns = [
            r'\n\n\*\*\*\n\n',  # *** scene break
            r'\n\n---\n\n',     # --- scene break
            r'\n\n\s*\n\n',     # Multiple newlines
        ]
        
        scenes = [text]  # Start with full text
        
        for pattern in scene_patterns:
            new_scenes = []
            for scene in scenes:
                new_scenes.extend(re.split(pattern, scene))
            scenes = new_scenes
        
        # Now split scenes that are too long
        for scene in scenes:
            if len(scene) <= optimal_size:
                if scene.strip():
                    segments.append(scene.strip())
            else:
                # Split by paragraphs
                paragraphs = scene.split('\n\n')
                current_segment = ""
                
                for para in paragraphs:
                    if len(current_segment + para) <= optimal_size:
                        current_segment += para + "\n\n"
                    else:
                        if current_segment:
                            segments.append(current_segment.strip())
                        
                        # If single paragraph is too long, split by sentences
                        if len(para) > optimal_size:
                            sentences = re.split(r'(?<=[.!?])\s+', para)
                            temp_segment = ""
                            
                            for sentence in sentences:
                                if len(temp_segment + sentence) <= optimal_size:
                                    temp_segment += sentence + " "
                                else:
                                    if temp_segment:
                                        segments.append(temp_segment.strip())
                                    temp_segment = sentence + " "
                            
                            current_segment = temp_segment
                        else:
                            current_segment = para + "\n\n"
                
                if current_segment.strip():
                    segments.append(current_segment.strip())
        
        return segments
    
    async def generate_quality_audio(self, text_segment, output_file, segment_num, total_segments):
        """Generate high-quality audio with professional settings"""
        
        try:
            # Professional analysis
            analysis = self.analyze_text_for_quality(text_segment)
            
            # Enhance text for quality
            enhanced_text = self.enhance_text_for_quality(text_segment, analysis)
            
            # Professional cleaning
            clean_text = self.clean_text_for_professional_tts(enhanced_text)
            
            if len(clean_text.strip()) < 20:
                return False
            
            # Progress with quality info
            progress = (segment_num / total_segments) * 100
            print(f"🎨 Segment {segment_num}/{total_segments} ({progress:.1f}%)")
            print(f"   📝 {len(clean_text):,} chars | 🎭 {analysis['primary_emotion']} | ⚡ {analysis['speed']:.2f}x")
            print(f"   🎬 {analysis['content_type']} | 🎨 {analysis['quality_setting']}")
            
            temp_audio = output_file.replace('.mp3', '_temp.wav')
            
            # Generate with quality settings
            if self.tts_type == "coqui_quality":
                # High-quality Coqui TTS
                self.tts_engine.tts_to_file(
                    text=clean_text,
                    file_path=temp_audio,
                    speed=analysis['speed']
                )
                
            elif self.tts_type == "pyttsx3_quality":
                # Quality-configured pyttsx3
                rate = max(140, min(200, int(160 * analysis['speed'])))
                volume = 0.95 if analysis['quality_setting'] in ['expressive', 'intense'] else 0.85
                
                self.tts_engine.setProperty('rate', rate)
                self.tts_engine.setProperty('volume', volume)
                
                self.tts_engine.save_to_file(clean_text, temp_audio)
                self.tts_engine.runAndWait()
            
            # Verify quality
            if not os.path.exists(temp_audio):
                print("   ❌ Audio file not created")
                return False
            
            audio_size = os.path.getsize(temp_audio)
            if audio_size < 5000:  # Require minimum quality threshold
                print(f"   ❌ Audio quality too low: {audio_size} bytes")
                os.remove(temp_audio)
                return False
            
            print(f"   ✅ Quality audio: {audio_size:,} bytes")
            
            # High-quality MP3 conversion
            if self.ffmpeg_available:
                mp3_output = output_file.replace('.wav', '.mp3')
                
                # Use higher bitrate for quality
                bitrate = '96k' if analysis['quality_setting'] in ['expressive', 'mysterious'] else '64k'
                
                conv_cmd = [
                    self.ffmpeg_available, '-i', temp_audio,
                    '-codec:a', 'libmp3lame', '-b:a', bitrate,
                    '-ar', '22050', '-ac', '1', '-y', mp3_output
                ]
                
                result = subprocess.run(conv_cmd, capture_output=True, timeout=60)
                
                if result.returncode == 0 and os.path.exists(mp3_output):
                    os.remove(temp_audio)
                    print(f"   ✅ High-quality MP3: {bitrate} bitrate")
                    return mp3_output
            
            return temp_audio
            
        except Exception as e:
            print(f"   ❌ Quality generation failed: {e}")
            return False
    
    def combine_with_quality(self, audio_files, final_output):
        """Combine audio with quality preservation"""
        
        if not audio_files or not self.ffmpeg_available:
            return False
        
        print(f"\n🎵 Combining {len(audio_files)} segments with quality preservation...")
        
        # Create file list
        filelist_path = os.path.join(self.output_dir, "quality_segments.txt")
        
        with open(filelist_path, 'w', encoding='utf-8') as f:
            for audio_file in audio_files:
                abs_path = os.path.abspath(audio_file).replace('\\', '/')
                f.write(f"file '{abs_path}'\n")
        
        # High-quality combination
        cmd = [
            self.ffmpeg_available, '-f', 'concat', '-safe', '0',
            '-i', filelist_path,
            '-c', 'copy',  # Preserve quality
            '-y', final_output
        ]
        
        result = subprocess.run(cmd, capture_output=True, timeout=600)
        
        if os.path.exists(filelist_path):
            os.remove(filelist_path)
        
        if result.returncode == 0 and os.path.exists(final_output):
            print(f"✅ High-quality audiobook created")
            return final_output
        
        return False

async def convert_quality_audiobook():
    """Generate professional-quality audiobook"""
    
    audiobook_file = "audiobook_output/just_mytype_audiobook.md"
    
    if not os.path.exists(audiobook_file):
        print(f"❌ Audiobook file not found: {audiobook_file}")
        return
    
    print("🎨 PROFESSIONAL QUALITY AUDIOBOOK GENERATOR")
    print("=" * 60)
    print("🎭 High-quality voice synthesis")
    print("🎬 Professional emotion and pacing control")
    print("📚 Optimized for audiobook listening experience")
    print("⚖️ Balanced quality vs speed")
    print("=" * 60)
    
    # Read audiobook
    with open(audiobook_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    text_start = content.find('---\n\n') + 5
    audiobook_text = content[text_start:] if text_start > 4 else content
    
    if len(audiobook_text.strip()) < 100:
        print("❌ Not enough text content")
        return
    
    print(f"\n📝 Processing {len(audiobook_text):,} characters for quality generation")
    
    # Initialize quality TTS
    tts = QualityAudiobookTTS()
    
    if not tts.tts_engine:
        print("❌ No quality TTS engine available")
        print("💡 Try: pip install TTS")
        print("💡 Or: pip install pyttsx3")
        return
    
    print(f"🎨 Using quality engine: {tts.tts_type}")
    if hasattr(tts, 'model_name'):
        print(f"🎙️ Model: {tts.model_name}")
    
    # Create quality-optimized segments
    print("\n📚 Creating professional segments...")
    segments = tts.split_into_quality_segments(audiobook_text, optimal_size=4000)
    
    # Estimate time and quality
    estimated_minutes = len(segments) * 2.5  # ~2.5 minutes per quality segment
    estimated_hours = estimated_minutes / 60
    
    print(f"⏱️ Estimated generation time: {estimated_hours:.1f} hours")
    print(f"🎯 Target quality: Professional audiobook standard")
    
    # Confirm generation
    proceed = input(f"\n🎨 Generate high-quality audiobook with {len(segments)} segments? (y/n): ").lower()
    if proceed != 'y':
        print("Generation cancelled")
        return
    
    print(f"\n🎨 Starting QUALITY audiobook generation...\n")
    
    # Generate with quality focus
    audio_files = []
    failed_segments = []
    
    start_time = asyncio.get_event_loop().time()
    
    for i, segment in enumerate(segments, 1):
        segment_filename = f"quality_segment_{i:03d}"
        output_file = f"creative_audiobooks/{segment_filename}.wav"
        
        audio_file = await tts.generate_quality_audio(segment, output_file, i, len(segments))
        
        if audio_file:
            audio_files.append(audio_file)
            print()  # Clean spacing
        else:
            failed_segments.append(i)
            print()
        
        # Progress update every 10 segments
        if i % 10 == 0:
            elapsed = (asyncio.get_event_loop().time() - start_time) / 60
            remaining_estimate = ((len(segments) - i) * elapsed / i)
            print(f"📊 Progress: {i}/{len(segments)} | ⏱️ Remaining: ~{remaining_estimate:.0f} minutes\n")
    
    # Final summary
    elapsed_total = (asyncio.get_event_loop().time() - start_time) / 60
    success_rate = (len(audio_files) / len(segments)) * 100
    
    print(f"📊 QUALITY Generation Summary:")
    print(f"✅ Success rate: {len(audio_files)}/{len(segments)} ({success_rate:.1f}%)")
    print(f"⏱️ Total time: {elapsed_total:.1f} minutes")
    print(f"🎨 Quality: Professional audiobook standard")
    
    if audio_files:
        # Quality combination
        base_name = os.path.splitext(os.path.basename(audiobook_file))[0]
        final_audiobook = f"creative_audiobooks/{base_name}_QUALITY_AUDIOBOOK.mp3"
        
        combined_file = tts.combine_with_quality(audio_files, final_audiobook)
        
        if combined_file:
            file_size = os.path.getsize(combined_file) / (1024*1024)
            duration_hours = len(audio_files) * 6 / 60  # ~6 minutes per 4000-char segment
            
            print(f"\n🎉 SUCCESS! Professional audiobook ready:")
            print(f"📂 Location: {combined_file}")
            print(f"📁 File size: {file_size:.1f} MB")
            print(f"⏱️ Duration: ~{duration_hours:.1f} hours")
            print(f"🎨 Quality: Professional audiobook standard")
            print(f"🎭 Features: Emotion control, proper pacing, dialogue handling")
            
            # Cleanup option
            cleanup = input("\n🗑️ Delete individual segment files to save space? (y/n): ").lower()
            if cleanup == 'y':
                for audio_file in audio_files:
                    try:
                        os.remove(audio_file)
                    except:
                        pass
                print("✅ Segment files cleaned up")
            
            print(f"\n🎊 Your professional-quality audiobook is ready!")
            print(f"🎧 Enjoy natural, expressive narration!")
            
        else:
            print("❌ Failed to combine segments")
    else:
        print("❌ No quality segments generated")

if __name__ == "__main__":
    print("🎨 PROFESSIONAL QUALITY AUDIOBOOK GENERATOR")
    print("📚 Audiobook Standard • 🎭 Natural Expression • ⚖️ Quality/Speed Balance")
    asyncio.run(convert_quality_audiobook())
