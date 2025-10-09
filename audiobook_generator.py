import re
import asyncio
import json
import os
import time
import platform
import subprocess
from typing import Optional, Dict, Any, List
import requests
from datetime import datetime
import hashlib
import aiohttp
import traceback

from enhanced_extraction import EnhancedTextExtraction

# ═══════════════════════════════════════════════════════════════════
# LLM MANAGER - UNCHANGED
# ═══════════════════════════════════════════════════════════════════
class StateOfTheArtLLMManager:
    def __init__(self, local_only=False):
        self.gemini_api_key = ""
        self.lm_studio_base_url = "http://localhost:1234"
        self.lm_studio_models = [
            "meta-llama-3-8b-instruct", "llama-3.2-3b-instruct", 
            "mistral-7b-instruct-v0.3", "qwen2.5-7b-instruct", "llama-3.1-8b-instruct"
        ]
        self.current_lm_model = None
        self.gemini_models = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]
        self.current_gemini_model = self.gemini_models[0]
        self.gemini_requests_today = 0
        self.gemini_daily_limit = 2000
        self.fallback_active = local_only
        self.cache_dir = "complete_llm_cache"
        self.local_only_mode = local_only
        os.makedirs(self.cache_dir, exist_ok=True)
        
        self.complete_audiobook_prompt = """Transform the given text into premium audiobook content.

TRANSFORMATION RULES:
- Create conversational flow with natural transitions
- Use engaging phrases: "Here's what's fascinating...", "This brings us to..."
- Address listener directly: "As you can imagine...", "You might wonder..."
- Break complex ideas into digestible segments
- Maintain factual accuracy and technical precision
- Expand content by 40-80% for optimal pacing

Transform this text: {text}"""

        self.session = None
        self.initialize_session()

    def initialize_session(self):
        try:
            timeout = aiohttp.ClientTimeout(total=120)
            connector = aiohttp.TCPConnector(
                limit=20, limit_per_host=10, ttl_dns_cache=300,
                use_dns_cache=True, keepalive_timeout=60
            )
            self.session = aiohttp.ClientSession(timeout=timeout, connector=connector)
        except Exception:
            pass

    def get_cache_key(self, text: str) -> str:
        content = f"lm_studio_audiobook_v4_{text}"
        return hashlib.sha256(content.encode()).hexdigest()

    def load_from_cache(self, cache_key: str) -> Optional[Dict[str, Any]]:
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                cache_age = time.time() - data.get('timestamp', 0)
                if cache_age < 86400:  # 24 hours
                    return data
            except Exception:
                pass
        return None

    def save_to_cache(self, cache_key: str, original_text: str, rewritten_text: str, quality_score: float, method: str):
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        try:
            data = {
                'timestamp': time.time(),
                'processing_date': datetime.now().isoformat(),
                'original_length': len(original_text),
                'rewritten_length': len(rewritten_text),
                'rewritten_text': rewritten_text,
                'quality_score': quality_score,
                'method': method,
                'processing_mode': 'local_only' if self.local_only_mode else 'hybrid',
                'version': 'lm_studio_v4'
            }
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    async def call_lm_studio_complete(self, text: str) -> Optional[Dict[str, Any]]:
        # Health check
        try:
            health_response = requests.get(f"{self.lm_studio_base_url}/v1/models", timeout=5)
            if health_response.status_code != 200:
                return None
        except Exception:
            return None

        # Get available models
        try:
            models = health_response.json().get('data', [])
            available_models = [model.get('id', '') for model in models]
            if not available_models:
                return None

            best_model = None
            for preferred_model in self.lm_studio_models:
                for available_model in available_models:
                    if preferred_model in available_model.lower():
                        best_model = available_model
                        break
                if best_model:
                    break
            
            if not best_model:
                best_model = available_models[0]
            
            self.current_lm_model = best_model

        except Exception:
            return None

        # Generate content
        try:
            url = f"{self.lm_studio_base_url}/v1/chat/completions"
            payload = {
                "model": best_model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a professional audiobook narrator. Transform text into engaging, conversational audiobook content."
                    },
                    {
                        "role": "user", 
                        "content": f"Transform this text into engaging audiobook content:\n\n{text[:2500]}"
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 2048,
                "top_p": 0.9,
                "frequency_penalty": 0.1,
                "presence_penalty": 0.1,
                "stream": False
            }

            if not self.session:
                self.initialize_session()

            timeout = aiohttp.ClientTimeout(total=45)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        if 'choices' in data and len(data['choices']) > 0:
                            content = data['choices'][0]['message']['content']
                            if content and content.strip():
                                result_text = content.strip()
                                quality_score = self.calculate_enhanced_quality_score(text, result_text)
                                return {
                                    'text': result_text,
                                    'quality_score': quality_score,
                                    'method': f'lm_studio_{best_model.replace("-", "_").replace(".", "_")}'
                                }
        except Exception:
            pass
        
        return None

    async def call_gemini_api_complete(self, text: str) -> Optional[Dict[str, Any]]:
        if self.local_only_mode or not self.gemini_api_key or self.gemini_requests_today >= self.gemini_daily_limit:
            return None

        if not self.session:
            self.initialize_session()

        for model_name in self.gemini_models:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.gemini_api_key}"
                payload = {
                    "contents": [{
                        "parts": [{"text": f"Transform this text into engaging audiobook content:\n\n{text[:2500]}"}]
                    }],
                    "generationConfig": {
                        "temperature": 0.7,
                        "topK": 40,
                        "topP": 0.9,
                        "maxOutputTokens": 2048,
                        "candidateCount": 1
                    }
                }

                async with self.session.post(url, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        if 'candidates' in data and data['candidates']:
                            rewritten_text = data['candidates'][0]['content']['parts'][0]['text']
                            self.gemini_requests_today += 1
                            self.current_gemini_model = model_name
                            quality_score = self.calculate_enhanced_quality_score(text, rewritten_text)
                            return {
                                'text': rewritten_text.strip(),
                                'quality_score': quality_score,
                                'method': f'gemini_{model_name.replace("-", "_")}'
                            }
                    elif response.status == 404:
                        continue
                    elif response.status == 403:
                        self.fallback_active = True
                        break
                    elif response.status == 429:
                        await asyncio.sleep(2)
                        continue
                    else:
                        continue
            except Exception:
                continue

        return None

    def calculate_enhanced_quality_score(self, original: str, rewritten: str) -> float:
        if not rewritten or len(rewritten) < 50:
            return 0.1
        
        length_ratio = len(rewritten) / len(original) if len(original) > 0 else 0
        if length_ratio > 1.2:
            length_score = min(1.0, 0.5 + (length_ratio - 1.2) * 0.5)
        else:
            length_score = length_ratio * 0.4
        
        # Engagement indicators
        engagement_words = [
            'fascinating', 'remarkable', 'important', 'consider', 'imagine', 'discover', 
            'explore', 'understand', 'realize', 'notice', 'interesting', 'significant',
            'now', 'let\'s', 'you might', 'what\'s more', 'crucially', 'essentially',
            'particularly', 'notably', 'surprisingly', 'importantly', 'here\'s'
        ]
        engagement_count = sum(1 for word in engagement_words if word.lower() in rewritten.lower())
        engagement_score = min(1.0, engagement_count / 8)
        
        # Transition words
        transitions = [
            'however', 'moreover', 'furthermore', 'in addition', 'meanwhile', 'consequently',
            'therefore', 'as a result', 'for example', 'specifically', 'what\'s interesting',
            'here\'s the thing', 'this brings us to', 'to put it simply', 'in other words',
            'most importantly', 'and', 'but', 'so'
        ]
        transition_count = sum(1 for trans in transitions if trans.lower() in rewritten.lower())
        transition_score = min(1.0, transition_count / 5)
        
        # Audio-friendly phrases
        audio_phrases = [
            'as you can imagine', 'you might be wondering', 'picture this', 'think about',
            'consider this', 'notice how', 'imagine', 'you', 'we', 'this'
        ]
        audio_count = sum(1 for phrase in audio_phrases if phrase.lower() in rewritten.lower())
        audio_score = min(1.0, audio_count / 3)
        
        # Narrative elements
        narrative_words = [
            'story', 'journey', 'experience', 'discovery', 'reveals', 'unfolds',
            'demonstrates', 'illustrates', 'shows', 'tells', 'explains', 'describes'
        ]
        narrative_count = sum(1 for word in narrative_words if word.lower() in rewritten.lower())
        narrative_score = min(1.0, narrative_count / 4)
        
        # Sentence structure
        sentences = [s for s in rewritten.split('.') if s.strip()]
        avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        structure_bonus = 0.2 if 10 <= avg_sentence_length <= 25 else 0.1
        
        quality_score = (
            length_score * 0.20 + 
            engagement_score * 0.20 + 
            transition_score * 0.15 + 
            audio_score * 0.15 + 
            narrative_score * 0.15 + 
            structure_bonus * 0.15
        )
        
        if length_ratio < 1.1:
            quality_score = max(quality_score, 0.5)
        
        return min(1.0, quality_score)

    async def rewrite_text_chunk_complete(self, text: str, chunk_index: int = 0) -> Dict[str, Any]:
        cache_key = self.get_cache_key(text)
        cached_result = self.load_from_cache(cache_key)
        
        if cached_result:
            return {
                'text': cached_result['rewritten_text'],
                'quality_score': cached_result.get('quality_score', 0.8),
                'method': 'cache',
                'chunk_index': chunk_index
            }

        # Try LM Studio first
        result = await self.call_lm_studio_complete(text)
        if result:
            self.save_to_cache(cache_key, text, result['text'], result['quality_score'], result['method'])
            result['chunk_index'] = chunk_index
            return result

        # Try Gemini as fallback
        if not self.local_only_mode and not self.fallback_active:
            result = await self.call_gemini_api_complete(text)
            if result:
                self.save_to_cache(cache_key, text, result['text'], result['quality_score'], result['method'])
                result['chunk_index'] = chunk_index
                return result

        # Enhanced basic processing fallback
        enhanced_text = self.apply_enhanced_basic_enhancement(text)
        return {
            'text': enhanced_text,
            'quality_score': 0.65,
            'method': 'enhanced_basic_processing',
            'chunk_index': chunk_index
        }

    def apply_enhanced_basic_enhancement(self, text: str) -> str:
        enhanced = text
        
        # Basic enhancements
        enhancements = {
            '. ': '. Now, ',
            'However, ': 'However, here\'s what\'s particularly interesting: ',
            'Therefore, ': 'So here\'s what this means: ',
            'Important ': 'What\'s particularly important ',
            'For example, ': 'To illustrate this point, ',
            'Additionally, ': 'Building on this idea, '
        }
        
        for old, new in enhancements.items():
            enhanced = enhanced.replace(old, new)
        
        # Split overly long sentences
        sentences = enhanced.split('. ')
        improved_sentences = []
        for sentence in sentences:
            if len(sentence) > 180 and ', ' in sentence:
                parts = sentence.split(', ', 1)
                if len(parts) == 2:
                    improved_sentences.append(parts[0] + '.')
                    improved_sentences.append('Moreover, ' + parts[1])
                else:
                    improved_sentences.append(sentence)
            else:
                improved_sentences.append(sentence)
        
        return '. '.join(improved_sentences)

    def smart_chunk_text(self, text: str, max_chunk_size: int = 2500) -> List[str]:
        sections = text.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for section in sections:
            if len(section) > max_chunk_size:
                sentences = section.split('. ')
                for sentence in sentences:
                    candidate = current_chunk + sentence + '. '
                    if len(candidate) <= max_chunk_size:
                        current_chunk = candidate
                    else:
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                        current_chunk = sentence + '. '
            else:
                candidate = (current_chunk + '\n\n' + section) if current_chunk else section
                if len(candidate) <= max_chunk_size:
                    current_chunk = candidate
                else:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = section
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return [chunk for chunk in chunks if len(chunk.split()) >= 20]

    async def process_document_complete(self, extracted_text: str) -> Dict[str, Any]:
        chunks = self.smart_chunk_text(extracted_text)
        chunk_results = []
        quality_scores = []
        
        batch_size = 3
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            batch_indices = list(range(i, min(i + batch_size, len(chunks))))
            
            batch_tasks = [
                self.rewrite_text_chunk_complete(chunk, idx) 
                for chunk, idx in zip(batch, batch_indices)
            ]
            batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
            
            for j, result in enumerate(batch_results):
                chunk_idx = i + j
                if isinstance(result, Exception):
                    chunk_results.append(chunks[chunk_idx])
                    quality_scores.append(0.3)
                else:
                    chunk_results.append(result['text'])
                    quality_scores.append(result['quality_score'])
            
            if i + batch_size < len(chunks):
                await asyncio.sleep(1)
        
        final_text = '\n\n'.join(chunk_results)
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        expansion_ratio = len(final_text) / len(extracted_text) if len(extracted_text) > 0 else 0
        
        return {
            'final_text': final_text,
            'quality_scores': quality_scores,
            'average_quality': avg_quality,
            'expansion_ratio': expansion_ratio,
            'chunk_count': len(chunks),
            'original_length': len(extracted_text),
            'final_length': len(final_text),
            'lm_studio_model': self.current_lm_model,
            'gemini_model': self.current_gemini_model
        }

    async def close(self):
        if self.session:
            await self.session.close()

# ═══════════════════════════════════════════════════════════════════
# EDGE TTS INTEGRATION - NEW!
# ═══════════════════════════════════════════════════════════════════
class EdgeTTSManager:
    """Manages Edge TTS for human-like audio generation"""
    
    @staticmethod
    def is_available() -> bool:
        """Check if Edge TTS is available"""
        try:
            import edge_tts  # noqa: F401
            return True
        except ImportError:
            return False
    
    @staticmethod
    async def install_if_needed() -> bool:
        """Install Edge TTS if not available"""
        if EdgeTTSManager.is_available():
            return True
        
        try:
            import subprocess
            result = subprocess.run(
                ["pip", "install", "edge-tts"], 
                capture_output=True, text=True
            )
            if result.returncode == 0:
                print("✅ Edge TTS installed successfully")
                return True
            else:
                print(f"❌ Edge TTS installation failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Edge TTS installation error: {e}")
            return False
    
    @staticmethod
    def get_voice_styles() -> Dict[str, Dict[str, str]]:
        """Get available voice styles and their configurations"""
        return {
            'storytelling': {
                'voice': 'en-US-AriaNeural',
                'description': 'Warm, expressive storytelling voice',
                'rate': '+15%',
                'pitch': '+5Hz'
            },
            'authoritative': {
                'voice': 'en-US-DavisNeural', 
                'description': 'Deep, confident authoritative voice',
                'rate': '+10%',
                'pitch': '+0Hz'
            },
            'conversational': {
                'voice': 'en-GB-SoniaNeural',
                'description': 'Natural, friendly conversational voice',
                'rate': '+20%',
                'pitch': '+8Hz'
            },
            'narrative': {
                'voice': 'en-US-JennyNeural',
                'description': 'Smooth, professional narrative voice',
                'rate': '+12%',
                'pitch': '+3Hz'
            },
            'dramatic': {
                'voice': 'en-GB-RyanNeural',
                'description': 'Dynamic, emotional dramatic voice',
                'rate': '+5%',
                'pitch': '+10Hz'
            }
        }
    
    @staticmethod
    async def generate_audio(
        text: str, 
        output_file: str, 
        voice_style: str = "storytelling"
    ) -> Dict[str, Any]:
        """Generate audio using Edge TTS"""
        
        if not EdgeTTSManager.is_available():
            if not await EdgeTTSManager.install_if_needed():
                return {
                    'success': False,
                    'error': 'Edge TTS not available and installation failed'
                }
        
        try:
            import edge_tts
            
            voice_configs = EdgeTTSManager.get_voice_styles()
            config = voice_configs.get(voice_style, voice_configs['storytelling'])
            
            print(f"🎭 Using voice: {config['voice']} ({config['description']})")
            
            communicate = edge_tts.Communicate(
                text,
                config['voice'],
                rate=config['rate'],
                pitch=config['pitch']
            )
            
            start_time = time.time()
            await communicate.save(output_file)
            generation_time = time.time() - start_time
            
            if os.path.exists(output_file) and os.path.getsize(output_file) > 5000:
                file_size_mb = os.path.getsize(output_file) / 1024 / 1024
                estimated_duration = len(text) // 150  # Rough estimate
                
                return {
                    'success': True,
                    'output_file': output_file,
                    'voice': config['voice'],
                    'voice_style': voice_style,
                    'file_size_mb': round(file_size_mb, 1),
                    'estimated_duration_min': estimated_duration,
                    'generation_time_sec': round(generation_time, 1),
                    'content_length': len(text)
                }
            else:
                return {
                    'success': False,
                    'error': 'Audio file was not created or is too small'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Edge TTS generation failed: {str(e)}'
            }

# ═══════════════════════════════════════════════════════════════════
# CROSS-PLATFORM TTS (LEGACY - KEPT FOR COMPATIBILITY)
# ═══════════════════════════════════════════════════════════════════
class CrossPlatformTTS:
    @staticmethod
    def get_available_engines():
        engines = []
        
        # Check Edge TTS
        if EdgeTTSManager.is_available():
            engines.append('edge_tts')
        
        try:
            import pyttsx3  # noqa: F401
            engines.append('pyttsx3')
        except ImportError:
            pass
        
        try:
            from gtts import gTTS  # noqa: F401
            engines.append('gtts')
        except ImportError:
            pass
        
        if platform.system() == "Darwin":
            engines.append('macos_say')
        elif platform.system() == "Windows":
            engines.append('windows_sapi')
        elif platform.system() == "Linux":
            engines.append('espeak')
        
        return engines
    
    @staticmethod 
    def generate_audio_pyttsx3(text: str, output_file: str, voice_rate: int = 180) -> bool:
        try:
            import pyttsx3
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            if voices:
                engine.setProperty('voice', voices[0].id)
            engine.setProperty('rate', voice_rate)
            engine.setProperty('volume', 0.9)
            engine.save_to_file(text, output_file)
            engine.runAndWait()
            return os.path.exists(output_file) and os.path.getsize(output_file) > 1000
        except Exception:
            return False
    
    @staticmethod
    def generate_audio_gtts(text: str, output_file: str, lang: str = 'en') -> bool:
        try:
            from gtts import gTTS
            import io
            from pydub import AudioSegment  # noqa: F401
            
            tts = gTTS(text=text, lang=lang, slow=False)
            
            temp_mp3 = output_file.replace('.wav', '_temp.mp3')
            tts.save(temp_mp3)
            
            if output_file.endswith('.wav'):
                audio = AudioSegment.from_mp3(temp_mp3)
                audio.export(output_file, format='wav')
                os.remove(temp_mp3)
            else:
                os.rename(temp_mp3, output_file)
            
            return os.path.exists(output_file) and os.path.getsize(output_file) > 1000
        except Exception:
            return False
    
    @staticmethod
    def generate_audio_macos_say(text: str, output_file: str, voice: str = 'Daniel', rate: int = 180) -> bool:
        try:
            if platform.system() != "Darwin":
                return False
            
            temp_text_file = output_file.replace('.wav', '_temp.txt').replace('.aiff', '_temp.txt')
            with open(temp_text_file, 'w', encoding='utf-8') as f:
                f.write(text)
            
            cmd = ['say', '-f', temp_text_file, '-o', output_file, '-r', str(rate), '-v', voice]
            result = subprocess.run(cmd, capture_output=True, text=True)
            os.remove(temp_text_file)
            
            return result.returncode == 0 and os.path.exists(output_file)
        except Exception:
            return False
    
    @classmethod
    def generate_audio(cls, text: str, output_file: str, preferred_engine: str = None) -> Dict[str, Any]:
        available_engines = cls.get_available_engines()
        
        if not available_engines:
            return {'success': False, 'engine': None, 'error': 'No TTS engines available'}
        
        engines_to_try = []
        if preferred_engine and preferred_engine in available_engines:
            engines_to_try.append(preferred_engine)
        
        for engine in available_engines:
            if engine not in engines_to_try:
                engines_to_try.append(engine)
        
        for engine in engines_to_try:
            try:
                success = False
                
                if engine == 'edge_tts':
                    # This should not be used here - EdgeTTSManager handles it
                    continue
                elif engine == 'pyttsx3':
                    success = cls.generate_audio_pyttsx3(text, output_file)
                elif engine == 'gtts':
                    success = cls.generate_audio_gtts(text, output_file)
                elif engine == 'macos_say':
                    success = cls.generate_audio_macos_say(text, output_file)
                
                if success:
                    return {
                        'success': True,
                        'engine': engine,
                        'file_path': output_file,
                        'file_size': os.path.getsize(output_file)
                    }
            except Exception as e:
                continue
        
        return {'success': False, 'engine': None, 'error': 'All TTS engines failed'}

# ═══════════════════════════════════════════════════════════════════
# MAIN AUDIOBOOK GENERATOR - ENHANCED WITH EDGE TTS
# ═══════════════════════════════════════════════════════════════════
class StateOfTheArtAudiobookGenerator:
    def __init__(self, local_only=False):
        self.llm_manager = StateOfTheArtLLMManager(local_only=local_only)
        self.output_dir = "complete_audiobooks"
        os.makedirs(self.output_dir, exist_ok=True)
        self.tts = CrossPlatformTTS()
        self.edge_tts = EdgeTTSManager()

    # ────────────────────────────────────────────────────────────────
    # EXISTING METHODS - UNCHANGED  
    # ────────────────────────────────────────────────────────────────
    async def generate_audiobook_text_complete(self, file_path: str) -> str:
        """Generate enhanced audiobook text from PDF"""
        try:
            extracted_text = EnhancedTextExtraction.extract_text_from_any(file_path)
            if extracted_text.startswith("Error"):
                return f"❌ Extraction failed: {extracted_text}"
            
            transformation_result = await self.llm_manager.process_document_complete(extracted_text)
            audiobook_text = transformation_result['final_text']
            
            basename = os.path.splitext(os.path.basename(file_path))[0]
            output_dir = os.path.abspath(self.output_dir)
            os.makedirs(output_dir, exist_ok=True)
            
            safe_basename = re.sub(r'[^\w\-_.]', '_', basename)
            output_file = os.path.join(output_dir, f"{safe_basename}_COMPLETE_audiobook.md")
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            processing_mode = "LM Studio Advanced" if self.llm_manager.local_only_mode else "Hybrid (Gemini + LM Studio)"
            
            header = f"""# COMPLETE AudioBook: {basename}

**Source**: {os.path.basename(file_path)}
**Generated**: {timestamp}
**System**: {processing_mode}
**Quality Score**: {transformation_result['average_quality']:.2f}/1.0
**Enhancement Ratio**: {transformation_result['expansion_ratio']:.1f}x

---

"""
            
            final_content = header + audiobook_text
            
            save_successful = False
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(final_content)
                if os.path.exists(output_file) and os.path.getsize(output_file) >= len(final_content) * 0.8:
                    save_successful = True
            except Exception:
                pass
            
            if not save_successful:
                fallback_dir = os.path.join(os.getcwd(), "audiobooks_fallback")
                os.makedirs(fallback_dir, exist_ok=True)
                fallback_file = os.path.join(fallback_dir, f"{safe_basename}_audiobook.md")
                try:
                    with open(fallback_file, 'w', encoding='utf-8') as f:
                        f.write(final_content)
                    if os.path.exists(fallback_file):
                        output_file = fallback_file
                        save_successful = True
                except Exception:
                    pass
            
            if not save_successful:
                desktop_path = os.path.expanduser("~/Desktop")
                if os.path.exists(desktop_path):
                    desktop_file = os.path.join(desktop_path, f"{safe_basename}_audiobook.md")
                    try:
                        with open(desktop_file, 'w', encoding='utf-8') as f:
                            f.write(final_content)
                        if os.path.exists(desktop_file):
                            output_file = desktop_file
                            save_successful = True
                    except Exception:
                        pass
            
            if save_successful:
                try:
                    txt_file = output_file.replace('.md', '.txt')
                    with open(txt_file, 'w', encoding='utf-8') as f:
                        f.write(final_content)
                except:
                    pass
                return output_file
            else:
                return "❌ Failed to save audiobook file"
                
        except Exception as e:
            return f"❌ Audiobook generation failed: {e}"

    # ────────────────────────────────────────────────────────────────
    # NEW EDGE TTS INTEGRATION METHODS
    # ────────────────────────────────────────────────────────────────
    async def generate_audio_from_audiobook(
        self, 
        audiobook_file: str, 
        voice_style: str = "storytelling", 
        audio_length_limit: int = 25000
    ) -> Dict[str, Any]:
        """Convert audiobook text to speech using Edge TTS - NEW METHOD"""
        
        if not os.path.exists(audiobook_file):
            return {
                'success': False, 
                'error': f'Audiobook file not found: {audiobook_file}'
            }
        
        print(f"🎙️ Generating audio from: {os.path.basename(audiobook_file)}")
        
        try:
            # Read audiobook content
            with open(audiobook_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract main content (remove metadata header)
            if '---' in content:
                parts = content.split('---', 2)
                content = parts[2].strip() if len(parts) >= 3 else content
            
            # Apply length limit
            original_length = len(content)
            if len(content) > audio_length_limit:
                content = content[:audio_length_limit] + "..."
                print(f"📏 Content limited to {audio_length_limit:,} characters (was {original_length:,})")
            
            # Generate audio file name
            base_name = os.path.splitext(os.path.basename(audiobook_file))[0]
            audio_file = f"{base_name}_AUDIO_{voice_style}.mp3"
            
            print(f"🎭 Generating with {voice_style} voice...")
            print(f"📝 Content: {len(content):,} characters")
            print(f"🎵 Output: {audio_file}")
            
            # Generate with Edge TTS
            result = await self.edge_tts.generate_audio(content, audio_file, voice_style)
            
            if result['success']:
                print(f"🎉 Audio generation successful!")
                print(f"   File: {result['output_file']}")
                print(f"   Size: {result['file_size_mb']} MB")
                print(f"   Duration: ~{result['estimated_duration_min']} minutes")
                print(f"   Generation time: {result['generation_time_sec']}s")
                
                return {
                    'success': True,
                    'audio_file': result['output_file'],
                    'engine': f"edge_tts_{voice_style}",
                    'voice': result['voice'],
                    'file_size_mb': result['file_size_mb'],
                    'estimated_duration_min': result['estimated_duration_min'],
                    'generation_time_sec': result['generation_time_sec'],
                    'content_length': result['content_length']
                }
            else:
                return {
                    'success': False,
                    'error': result['error']
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Audio generation error: {str(e)}'
            }

    async def generate_complete_audiobook_with_fast_audio(
        self, 
        file_path: str, 
        generate_audio: bool = True, 
        voice_style: str = "storytelling", 
        audio_length_limit: int = 25000
    ) -> Dict[str, Any]:
        """Complete pipeline: PDF → Enhanced Audiobook Text → Edge TTS Audio - NEW METHOD"""
        
        print(f"🚀 COMPLETE AUDIOBOOK PIPELINE WITH EDGE TTS")
        print("=" * 60)
        
        start_time = time.time()
        
        # Step 1: Generate audiobook text
        print("📚 Step 1: Generating enhanced audiobook text...")
        audiobook_file = await self.generate_audiobook_text_complete(file_path)
        
        if audiobook_file.startswith("❌"):
            return {
                'success': False,
                'error': audiobook_file,
                'status': 'text_generation_failed'
            }
        
        text_time = time.time() - start_time
        print(f"✅ Audiobook text generated in {text_time:.1f}s: {audiobook_file}")
        
        # Step 2: Generate audio (if requested)
        audio_result = None
        if generate_audio:
            print(f"\n🎙️ Step 2: Generating audio with {voice_style} voice...")
            audio_result = await self.generate_audio_from_audiobook(
                audiobook_file, 
                voice_style=voice_style,
                audio_length_limit=audio_length_limit
            )
        
        total_time = time.time() - start_time
        
        # Step 3: Compile final result
        result = {
            'success': True,
            'audiobook_file': audiobook_file,
            'text_generation_time': round(text_time, 1),
            'total_time': round(total_time, 1),
            'voice_style': voice_style,
            'status': 'complete_with_text'
        }
        
        if audio_result:
            if audio_result['success']:
                result.update({
                    'audio_file': audio_result['audio_file'],
                    'audio_engine': audio_result['engine'],
                    'audio_voice': audio_result['voice'],
                    'audio_size_mb': audio_result['file_size_mb'],
                    'estimated_duration_min': audio_result['estimated_duration_min'],
                    'audio_generation_time': audio_result['generation_time_sec'],
                    'status': 'complete_with_audio'
                })
                print(f"\n🎉 COMPLETE SUCCESS!")
                print(f"📚 Audiobook: {result['audiobook_file']}")
                print(f"🎵 Audio: {result['audio_file']}")
                print(f"⏱️ Total time: {result['total_time']}s")
            else:
                result.update({
                    'audio_error': audio_result['error'],
                    'status': 'complete_with_text_only'
                })
                print(f"\n⚠️ Text generation successful, audio failed: {audio_result['error']}")
        
        print("=" * 60)
        return result

    # ────────────────────────────────────────────────────────────────
    # LEGACY METHOD - KEPT FOR COMPATIBILITY  
    # ────────────────────────────────────────────────────────────────
    async def generate_complete_audiobook_with_audio(
        self, 
        file_path: str, 
        generate_audio: bool = True,
        audio_length_limit: int = 50000, 
        preferred_tts_engine: str = None
    ) -> Dict[str, Any]:
        """Legacy method - redirects to new Edge TTS pipeline"""
        
        # Map old engine preferences to new voice styles
        voice_style_map = {
            'edge_tts': 'storytelling',
            'pyttsx3': 'authoritative', 
            'gtts': 'conversational'
        }
        
        voice_style = voice_style_map.get(preferred_tts_engine, 'storytelling')
        
        return await self.generate_complete_audiobook_with_fast_audio(
            file_path=file_path,
            generate_audio=generate_audio,
            voice_style=voice_style,
            audio_length_limit=audio_length_limit
        )

    async def close(self):
        """Close all resources"""
        await self.llm_manager.close()

# ═══════════════════════════════════════════════════════════════════
# TEST FUNCTIONALITY
# ═══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    async def test_audiobook_generator_with_edge_tts():
        generator = StateOfTheArtAudiobookGenerator(local_only=False)
        test_file = "testing.pdf"
        
        if os.path.exists(test_file):
            result = await generator.generate_complete_audiobook_with_fast_audio(
                test_file, 
                generate_audio=True,
                voice_style='storytelling',
                audio_length_limit=15000  # Small test
            )
            
            print("🎬 Generation Results:")
            print(f"📚 Audiobook file: {result.get('audiobook_file')}")
            print(f"🎵 Audio file: {result.get('audio_file')}")
            print(f"📊 Status: {result.get('status')}")
            print(f"⏱️ Total time: {result.get('total_time')}s")
            
            if result.get('audio_file'):
                print(f"🎭 Voice: {result.get('audio_voice')}")
                print(f"💾 Audio size: {result.get('audio_size_mb')} MB")
        
        await generator.close()
    
    asyncio.run(test_audiobook_generator_with_edge_tts())
