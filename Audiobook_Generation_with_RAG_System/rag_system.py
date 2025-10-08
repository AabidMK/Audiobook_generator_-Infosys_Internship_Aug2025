import os
import re
import json
import hashlib
from datetime import datetime
from typing import List, Dict, Optional, Any, Tuple
import numpy as np
import requests
import asyncio
try:
    import chromadb
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False


class Phase2RAGSystem:
    def __init__(self, 
                 persist_directory: str = "phase2_rag_db",
                 groq_api_key: str = None,
                 groq_model: str = "mixtral-8x7b-32768",
                 max_context_tokens: int = 3000):
        
        self.persist_directory = persist_directory
        os.makedirs(self.persist_directory, exist_ok=True)
        
        # Groq API Configuration
        self.groq_api_key = groq_api_key or os.getenv("GROQ_API_KEY")
        self.groq_model = groq_model
        
        # Token budget for context
        self.max_context_tokens = max_context_tokens
        
        # Initialize components
        self.collection = None
        self.model = None
        self.document_chunks = {}
        
        if CHROMADB_AVAILABLE:
            self.client = chromadb.PersistentClient(path=self.persist_directory)
            self.collection = self._get_or_create_collection()
        
        if EMBEDDINGS_AVAILABLE:
            try:
                # Use same embedding model for consistency
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
            except:
                self.model = None

    def _get_or_create_collection(self):
        if not CHROMADB_AVAILABLE:
            return None
        
        try:
            return self.client.get_collection(name="phase2_documents")
        except:
            return self.client.create_collection(
                name="phase2_documents",
                metadata={"hnsw:space": "cosine"}
            )

    def ingest_document_complete(self, file_path: str, text: str) -> Dict[str, Any]:
        """Phase 1: Index document with embeddings"""
        if not text or len(text) < 100:
            return {'status': 'failed', 'error': 'Text too short'}
        
        cleaned_text = self._clean_text(text)
        chunks = self._create_chunks(cleaned_text)
        
        if not chunks:
            return {'status': 'failed', 'error': 'No chunks created'}
        
        if CHROMADB_AVAILABLE and self.collection and self.model:
            return self._store_with_chromadb(file_path, chunks)
        else:
            return self._store_simple(file_path, chunks)

    def _clean_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()

    def _create_chunks(self, text: str, chunk_size: int = 1000) -> List[str]:
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i + chunk_size])
            if len(chunk) > 50:
                chunks.append(chunk)
        
        return chunks

    def _store_with_chromadb(self, file_path: str, chunks: List[str]) -> Dict[str, Any]:
        try:
            # Step: Create embeddings using same model used for querying
            embeddings = self.model.encode(chunks)
            
            ids = []
            metadatas = []
            
            file_hash = hashlib.md5(file_path.encode()).hexdigest()[:8]
            
            for i, chunk in enumerate(chunks):
                chunk_id = f"{file_hash}_{i}"
                ids.append(chunk_id)
                metadatas.append({
                    'source_file': os.path.basename(file_path),
                    'source_path': file_path,
                    'chunk_index': i,
                    'chunk_length': len(chunk)
                })
            
            self.collection.add(
                ids=ids,
                documents=chunks,
                metadatas=metadatas,
                embeddings=embeddings.tolist()
            )
            
            return {
                'status': 'success',
                'chunks_created': len(chunks),
                'storage_method': 'chromadb_with_embeddings'
            }
        
        except Exception as e:
            return {'status': 'failed', 'error': str(e)}

    def _store_simple(self, file_path: str, chunks: List[str]) -> Dict[str, Any]:
        file_id = hashlib.md5(file_path.encode()).hexdigest()[:8]
        
        self.document_chunks[file_id] = {
            'file_path': file_path,
            'file_name': os.path.basename(file_path),
            'chunks': chunks,
            'created': datetime.now().isoformat()
        }
        
        storage_file = os.path.join(self.persist_directory, 'simple_storage.json')
        
        try:
            with open(storage_file, 'w', encoding='utf-8') as f:
                json.dump(self.document_chunks, f, indent=2, ensure_ascii=False)
        except:
            pass
        
        return {
            'status': 'success',
            'chunks_created': len(chunks),
            'storage_method': 'simple_json'
        }

    async def ask_question_complete(self, question: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Phase 2 RAG: Complete pipeline
        1. Take user question
        2. Create embedding for question
        3. Query ChromaDB for top-K nearest items
        4. Assemble context with token budget
        5. Build anti-hallucination prompt
        6. Call Groq LLM with prompt
        7. Return answer with citations
        """
        
        if not question or not question.strip():
            return {'error': 'Empty question'}
        
        # Step 1: User question received
        question = question.strip()
        
        if CHROMADB_AVAILABLE and self.collection and self.model:
            return await self._phase2_rag_pipeline(question, top_k)
        else:
            return await self._fallback_pipeline(question)

    async def _phase2_rag_pipeline(self, question: str, top_k: int) -> Dict[str, Any]:
        """Complete Phase 2 RAG implementation"""
        
        try:
            # Step 2: Create embedding for question using same model/config
            question_embedding = self.model.encode([question])
            
            # Step 3: Query ChromaDB for top-K nearest items (similarities/distances)
            results = self.collection.query(
                query_embeddings=question_embedding.tolist(),
                n_results=top_k,
                include=["documents", "metadatas", "distances"]
            )
            
            if not results['documents'] or not results['documents'][0]:
                return {
                    'question': question,
                    'answer': 'No relevant information found in the knowledge base.',
                    'confidence': 0.0,
                    'citations': [],
                    'method': 'phase2_rag_no_results'
                }
            
            # Step 4: Assemble retrieved chunks into context string with token budget
            context, citations = self._assemble_context_with_budget(
                results['documents'][0],
                results['metadatas'][0],
                results['distances'][0]
            )
            
            # Step 5: Build prompt that instructs LLM to use context and avoid hallucination
            prompt = self._build_anti_hallucination_prompt(question, context)
            
            # Step 6: Call Groq LLM with the prompt
            llm_answer, method_used = await self._call_llm(prompt)
            
            # Step 7: Return answer with citations (file_path, chunk_index, distance)
            return {
                'question': question,
                'answer': llm_answer,
                'confidence': 0.9,
                'citations': citations,
                'method': f'phase2_rag_{method_used}',
                'context_chunks_used': len(citations),
                'total_context_chars': len(context)
            }
            
        except Exception as e:
            return {'error': f'Phase 2 RAG pipeline failed: {str(e)}'}

    def _assemble_context_with_budget(self, 
                                    documents: List[str], 
                                    metadatas: List[Dict], 
                                    distances: List[float]) -> Tuple[str, List[Dict]]:
        """Step 4: Assemble context string trimmed to LLM token budget"""
        
        # Rough token estimation: ~4 chars per token
        max_context_chars = self.max_context_tokens * 4
        
        context_parts = []
        citations = []
        current_length = 0
        
        for i, (doc, metadata, distance) in enumerate(zip(documents, metadatas, distances)):
            # Add citation info
            citation = {
                'citation_id': i + 1,
                'file_path': metadata['source_path'],
                'file_name': metadata['source_file'],
                'chunk_index': metadata['chunk_index'],
                'distance': distance,
                'similarity': 1 - distance  # Convert distance to similarity
            }
            
            # Check if adding this chunk exceeds token budget
            chunk_with_header = f"\n--- Source {i+1}: {metadata['source_file']} (chunk {metadata['chunk_index']}) ---\n{doc}\n"
            
            if current_length + len(chunk_with_header) > max_context_chars:
                if not context_parts:  # At least include one chunk
                    context_parts.append(chunk_with_header[:max_context_chars])
                    citations.append(citation)
                break
            
            context_parts.append(chunk_with_header)
            citations.append(citation)
            current_length += len(chunk_with_header)
        
        context = "".join(context_parts)
        return context, citations

    def _build_anti_hallucination_prompt(self, question: str, context: str) -> str:
        """Step 5: Build prompt that instructs LLM to use context and avoid hallucination"""
        
        prompt = f"""You are a helpful AI assistant that answers questions based on provided context. Follow these rules strictly:

1. ONLY use information from the provided context below
2. If the context doesn't contain enough information to answer the question, say "I don't have enough information in the provided context to answer this question"
3. Do not make up or invent any information
4. Do not use your general knowledge beyond what's in the context
5. If you're uncertain, express that uncertainty
6. Provide a clear, concise answer based solely on the context

CONTEXT:
{context}

QUESTION: {question}

ANSWER (based only on the provided context):"""

        return prompt

    async def _call_llm(self, prompt: str) -> Tuple[str, str]:
        """Step 6: Call Groq LLM with the prompt and return answer"""
        
        # Try Groq first
        if self.groq_api_key:
            try:
                answer = await self._call_groq(prompt)
                return answer, "groq"
            except Exception as e:
                print(f"Groq call failed: {e}")
        
        # Try local LLM as fallback
        try:
            answer = await self._call_local_llm(prompt)
            return answer, "local_llm"
        except Exception as e:
            print(f"Local LLM call failed: {e}")
        
        return "I apologize, but I'm unable to process your question at the moment due to LLM service unavailability.", "fallback"

    async def _call_groq(self, prompt: str) -> str:
        """Call Groq Cloud API"""
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.groq_model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 512,
            "temperature": 0.3
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        else:
            raise Exception(f"Groq API error: {response.status_code} - {response.text}")

    async def _call_local_llm(self, prompt: str) -> str:
        """Call local LLM (Ollama/LM Studio) as fallback"""
        
        # Try Ollama first
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3.2:3b",
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.3}
                },
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json()["response"].strip()
        except:
            pass
        
        # Try LM Studio
        response = requests.post(
            "http://localhost:1234/v1/chat/completions",
            headers={"Content-Type": "application/json"},
            json={
                "model": "local-model",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": 500
            },
            timeout=60
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            raise Exception(f"Local LLM error: {response.status_code}")

    async def _fallback_pipeline(self, question: str) -> Dict[str, Any]:
        """Fallback when ChromaDB/embeddings not available"""
        return {
            'question': question,
            'answer': 'RAG system requires ChromaDB and sentence-transformers to be installed for Phase 2 functionality.',
            'confidence': 0.0,
            'citations': [],
            'method': 'fallback_no_dependencies'
        }

    def get_knowledge_base_stats_complete(self) -> Dict[str, Any]:
        """Get system statistics"""
        if CHROMADB_AVAILABLE and self.collection:
            try:
                count = self.collection.count()
                return {
                    'total_chunks': count,
                    'ready_for_qa': count > 0,
                    'storage_method': 'chromadb_with_embeddings',
                    'embedding_model': 'all-MiniLM-L6-v2' if self.model else 'none',
                    'llm_available': bool(self.groq_api_key),
                    'llm_provider': 'groq',
                    'groq_model': self.groq_model,
                    'max_context_tokens': self.max_context_tokens
                }
            except:
                pass
        
        return {
            'total_chunks': 0,
            'ready_for_qa': False,
            'storage_method': 'none',
            'embedding_model': 'none',
            'llm_available': False
        }

    async def close(self):
        """Cleanup resources"""
        pass


import asyncio

# ---- Your Phase2RAGSystem class code is above this ----

if __name__ == "__main__":
    rag = Phase2RAGSystem(
        groq_api_key="",
        groq_model="mixtral-8x7b-32768"
    )
    
    # Index documents (not async)
    extracted_text = open("document.txt", "r", encoding="utf-8").read()  # Or your method
    result = rag.ingest_document_complete("document.txt", extracted_text)
    print(f"Indexed: {result}")

    # Async main function for querying
    async def main():
        answer = await rag.ask_question_complete("What is the main topic?")
        print(f"Answer: {answer['answer']}")
        print(f"Citations: {answer['citations']}")
        print(f"Method: {answer['method']}")

    asyncio.run(main())
