import asyncio
import json
import os
import time
from typing import Optional, Dict, Any
import requests
from datetime import datetime
import hashlib
import aiohttp  # Add this import for async HTTP

# Import your existing text extraction
from enhanced_extraction import EnhancedTextExtraction

class HybridLLMManager:
    """
    Hybrid LLM system that tries Gemini API first, falls back to local Ollama
    """
    
    def __init__(self, local_only=False):  # Changed default to False for Gemini first
        self.gemini_api_key = ''
        self.ollama_base_url = "http://localhost:11434"
        self.ollama_model = "llama3:8b-instruct-q4_K_M"
        
        # Track usage and fallback state
        self.gemini_requests_today = 0
        self.gemini_daily_limit = 1000
        self.fallback_active = local_only
        self.cache_dir = "llm_cache"
        self.local_only_mode = local_only
        
        # Create cache directory
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Enhanced audiobook-specific prompts for better results
        self.audiobook_system_prompt = """You are an expert audiobook narrator and content rewriter. Transform the given text into engaging, listener-friendly audiobook content.

Guidelines:
- Rewrite in a warm, conversational tone perfect for audio narration
- Break up complex sentences into shorter, clearer ones
- Add smooth transitions between ideas using phrases like "Now," "Here's what's interesting," "Let's explore"
- Maintain all key information and technical accuracy
- Use active voice and present tense where appropriate
- Introduce technical terms naturally: "This process, known as machine learning, works by..."
- Create natural pauses and emphasis for better audio flow

Transform this text for audiobook narration:"""

        if self.local_only_mode:
            print("🏠 Running in LOCAL-ONLY mode (Ollama only)")
        else:
            print("☁️ Running in HYBRID mode (Gemini API + Ollama fallback)")
        
    def _get_cache_key(self, text: str, style: str) -> str:
        """Generate cache key for text rewriting"""
        content = f"{text}_{style}"
        return hashlib.md5(content.encode()).hexdigest()

    def _load_from_cache(self, cache_key: str) -> Optional[str]:
        """Load cached rewritten text"""
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('rewritten_text')
            except Exception as e:
                print(f"Cache read error: {e}")
        return None

    def _save_to_cache(self, cache_key: str, original_text: str, rewritten_text: str):
        """Save rewritten text to cache"""
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        try:
            data = {
                'timestamp': datetime.now().isoformat(),
                'original_length': len(original_text),
                'rewritten_length': len(rewritten_text),
                'rewritten_text': rewritten_text,
                'processing_mode': 'local_only' if self.local_only_mode else 'hybrid'
            }
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Cache write error: {e}")

    async def call_gemini_api(self, text: str) -> Optional[str]:
        """Call Gemini API for text rewriting using async HTTP"""
        if self.local_only_mode:
            print("🏠 Skipping Gemini API (local-only mode)")
            return None
            
        if not self.gemini_api_key:
            print("⚠️ No Gemini API key found")
            return None
            
        if self.gemini_requests_today >= self.gemini_daily_limit:
            print("⚠️ Gemini daily limit reached")
            return None

        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"
            
            headers = {
                'Content-Type': 'application/json',
            }
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": f"{self.audiobook_system_prompt}\n\n{text}"
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 2048,
                }
            }
            
            print(f"☁️ Processing with Gemini API... (2-5 seconds)")
            
            # Use aiohttp for async HTTP request
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload, timeout=30) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if 'candidates' in data and data['candidates']:
                            rewritten_text = data['candidates'][0]['content']['parts'][0]['text']
                            self.gemini_requests_today += 1
                            print(f"✅ Gemini API success ({self.gemini_requests_today}/{self.gemini_daily_limit} today)")
                            return rewritten_text.strip()
                        else:
                            print(f"❌ No candidates in Gemini response: {data}")
                    else:
                        print(f"❌ Gemini API error: {response.status}")
                        error_text = await response.text()
                        print(f"Error details: {error_text}")
                        
                        if "quota" in error_text.lower() or "limit" in error_text.lower():
                            self.fallback_active = True
                            print("🔄 Activating fallback to local LLM")
                            
        except aiohttp.ClientError as e:
            print(f"❌ Gemini API connection error: {e}")
            self.fallback_active = True
        except asyncio.TimeoutError:
            print("❌ Gemini API timeout")
            self.fallback_active = True
        except Exception as e:
            print(f"❌ Gemini processing error: {e}")
            
        return None

    async def call_ollama_local(self, text: str) -> Optional[str]:
        """Call local Ollama for text rewriting"""
        try:
            print("🔍 Checking Ollama connection...")
            
            # Check if Ollama is running
            health_response = requests.get(f"{self.ollama_base_url}/api/tags", timeout=5)
            if health_response.status_code != 200:
                print("❌ Ollama not running. Start with: ollama serve")
                return None
            
            # Check if our model is available
            models = health_response.json().get('models', [])
            model_names = [model.get('name', '') for model in models]
            
            if not any(self.ollama_model in name for name in model_names):
                print(f"❌ Model {self.ollama_model} not found.")
                print(f"📥 Available models: {', '.join(model_names)}")
                print(f"💡 Download with: ollama pull {self.ollama_model}")
                return None
            
            print(f"✅ Using model: {self.ollama_model}")
            
            url = f"{self.ollama_base_url}/api/generate"
            
            payload = {
                "model": self.ollama_model,
                "prompt": f"{self.audiobook_system_prompt}\n\n{text}",
                "options": {
                    "temperature": 1,
                    "top_p": 0.9,
                    "top_k": 40,
                    "num_predict": 2048,
                    "stop": ["Human:", "Assistant:", "---"]
                },
                "stream": False
            }
            
            print(f"🤖 Processing with Ollama... (this may take 30-60 seconds)")
            response = requests.post(url, json=payload, timeout=180)
            response.raise_for_status()
            
            data = response.json()
            if 'response' in data:
                result = data['response'].strip()
                print(f"✅ Ollama success! Generated {len(result)} characters")
                return result
                
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to Ollama.")
            print("💡 Make sure Ollama is running: ollama serve")
        except requests.exceptions.Timeout:
            print("❌ Ollama timeout - try shorter text or check system resources")
        except Exception as e:
            print(f"❌ Ollama error: {e}")
            
        return None

    async def rewrite_text_chunk(self, text: str, style: str = "audiobook") -> str:
        """
        Main method: Try Gemini first, fallback to Ollama
        """
        # Check cache first
        cache_key = self._get_cache_key(text, style)
        cached_result = self._load_from_cache(cache_key)
        if cached_result:
            print("📦 Using cached result")
            return cached_result
        
        print(f"🔄 Processing chunk ({len(text)} chars)...")
        
        # Try Gemini API first (unless local-only mode or fallback is active)
        if not self.local_only_mode and not self.fallback_active:
            result = await self.call_gemini_api(text)
            if result:
                self._save_to_cache(cache_key, text, result)
                return result
        
        # Fallback to local Ollama
        print("🔄 Switching to local LLM...")
        result = await self.call_ollama_local(text)
        if result:
            self._save_to_cache(cache_key, text, result)
            return result
        
        # If both fail, return original text with warning
        print("⚠️ Both LLMs failed, returning original text")
        return f"[UNPROCESSED] {text}"

    def chunk_text(self, text: str, max_chunk_size: int = 4000) -> list:
        """Split text into chunks suitable for LLM processing"""
        # Split by paragraphs first
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            # If single paragraph is too long, split by sentences
            if len(paragraph) > max_chunk_size:
                sentences = paragraph.split('. ')
                for sentence in sentences:
                    if len(current_chunk + sentence) > max_chunk_size:
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                            current_chunk = sentence + ". "
                        else:
                            # Single sentence is very long, force split
                            chunks.append(sentence[:max_chunk_size])
                            current_chunk = sentence[max_chunk_size:] + ". "
                    else:
                        current_chunk += sentence + ". "
            else:
                # Normal paragraph
                if len(current_chunk + paragraph) > max_chunk_size:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                        current_chunk = paragraph + "\n\n"
                    else:
                        chunks.append(paragraph)
                else:
                    current_chunk += paragraph + "\n\n"
        
        # Add final chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks

    async def process_document(self, extracted_text: str) -> str:
        """Process entire document with chunking"""
        print(f"\n🎯 Starting audiobook rewriting for {len(extracted_text)} characters")
        
        # Chunk the text
        chunks = self.chunk_text(extracted_text)
        print(f"📝 Split into {len(chunks)} chunks")
        
        rewritten_chunks = []
        
        for i, chunk in enumerate(chunks, 1):
            print(f"\n--- Processing chunk {i}/{len(chunks)} ---")
            rewritten_chunk = await self.rewrite_text_chunk(chunk)
            rewritten_chunks.append(rewritten_chunk)
            
            # Brief pause between chunks (shorter for API calls)
            if not self.fallback_active:
                await asyncio.sleep(0.5)  # Faster for API
            else:
                await asyncio.sleep(2)    # Longer for local processing
        
        # Combine all rewritten chunks
        final_text = "\n\n".join(rewritten_chunks)
        
        print(f"\n✅ Audiobook rewriting complete!")
        print(f"📊 Original: {len(extracted_text)} chars → Rewritten: {len(final_text)} chars")
        
        return final_text

class AudiobookGenerator:
    """Main class that combines text extraction with LLM rewriting"""
    
    def __init__(self, local_only=False):  # Changed default to use Gemini API first
        self.llm_manager = HybridLLMManager(local_only=local_only)
        self.output_dir = "audiobook_output"
        os.makedirs(self.output_dir, exist_ok=True)
    
    async def generate_audiobook_text(self, file_path: str) -> str:
        """Complete pipeline: extract text -> rewrite for audiobook"""
        print(f"🚀 Starting AudioBook generation for: {os.path.basename(file_path)}")
        
        # Step 1: Extract text using your existing code
        print("\n📖 Step 1: Extracting text...")
        extracted_text = EnhancedTextExtraction.extract_text_from_any(file_path)
        
        if extracted_text.startswith("Error"):
            return f"Extraction failed: {extracted_text}"
        
        # Limit to first 10k characters for testing (remove this for full processing)
        #extracted_text = extracted_text[:10000]
        
        print(f"✅ Extracted {len(extracted_text)} characters (limited to first 10k for testing)")
        
        # Step 2: Rewrite for audiobook style
        print("\n🎤 Step 2: Rewriting for audiobook narration...")
        audiobook_text = await self.llm_manager.process_document(extracted_text)
        
        # Step 3: Save the result
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_file = os.path.join(self.output_dir, f"{base_name}_audiobook.md")
        
        # Create enhanced audiobook markdown
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        processing_mode = "Local Ollama Only" if self.llm_manager.local_only_mode else "Hybrid LLM (Gemini + Ollama)"
        
        header = f"""# AudioBook Version: {base_name}

**Original Source**: {os.path.basename(file_path)}  
**Generated**: {timestamp}  
**System**: {processing_mode}  
**Original Length**: {len(extracted_text):,} characters  
**Audiobook Length**: {len(audiobook_text):,} characters  

---

"""
        
        final_content = header + audiobook_text
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_content)
        
        print(f"\n✅ AudioBook text saved: {output_file}")
        return output_file

# Test your complete system with Gemini API
async def main():
    """Test the complete audiobook generation pipeline"""
    
    print("☁️ HYBRID MODE: Using Gemini API with Ollama fallback")
    print("=" * 60)
    
    # Your test files
    test_files = [
        # Add more files here
    ]
    
    generator = AudiobookGenerator(local_only=False)  # Enable Gemini API
    
    for file_path in test_files:
        if os.path.isfile(file_path):
            try:
                result_file = await generator.generate_audiobook_text(file_path)
                print(f"🎉 Success! AudioBook text ready: {result_file}")
            except Exception as e:
                print(f"❌ Failed processing {file_path}: {e}")
        else:
            print(f"⚠️ File not found: {file_path}")

if __name__ == "__main__":
    print("🚀 Starting AudioBook Generator (Gemini API + Ollama Hybrid)")
    print("💡 Set GEMINI_API_KEY environment variable for best performance")
    print("💡 Ollama fallback available if needed")
    asyncio.run(main())
