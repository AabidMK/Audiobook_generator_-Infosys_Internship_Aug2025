import os
import re
import json
import hashlib
from datetime import datetime
from typing import List, Dict, Optional, Any
import numpy as np

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

class SimpleRAGSystem:
    def __init__(self, persist_directory: str = "simple_rag_db"):
        self.persist_directory = persist_directory
        os.makedirs(self.persist_directory, exist_ok=True)
        
        self.collection = None
        self.model = None
        self.documents = []
        self.document_chunks = {}
        
        if CHROMADB_AVAILABLE:
            self.client = chromadb.PersistentClient(path=self.persist_directory)
            self.collection = self._get_or_create_collection()
        
        if EMBEDDINGS_AVAILABLE:
            try:
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
            except:
                self.model = None
    
    def _get_or_create_collection(self):
        if not CHROMADB_AVAILABLE:
            return None
        
        try:
            return self.client.get_collection(name="simple_documents")
        except:
            return self.client.create_collection(
                name="simple_documents",
                metadata={"hnsw:space": "cosine"}
            )
    
    def ingest_document_complete(self, file_path: str, text: str) -> Dict[str, Any]:
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
                    'chunk_index': i
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
                'storage_method': 'chromadb'
            }
        
        except Exception as e:
            return self._store_simple(file_path, chunks)
    
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
    
    async def ask_question_complete(self, question: str) -> Dict[str, Any]:
        if CHROMADB_AVAILABLE and self.collection and self.model:
            return await self._query_chromadb(question)
        else:
            return await self._query_simple(question)
    
    async def _query_chromadb(self, question: str) -> Dict[str, Any]:
        try:
            question_embedding = self.model.encode([question])
            
            results = self.collection.query(
                query_embeddings=question_embedding.tolist(),
                n_results=5,
                include=["documents", "metadatas", "distances"]
            )
            
            if not results['documents'] or not results['documents'][0]:
                return {
                    'question': question,
                    'answer': 'No relevant information found.',
                    'confidence': 0.0,
                    'method': 'chromadb_search'
                }
            
            best_chunks = results['documents'][0][:3]
            context = '\n\n'.join(best_chunks)
            
            answer = self._generate_simple_answer(question, context)
            
            return {
                'question': question,
                'answer': answer,
                'confidence': 0.7,
                'sources_used': len(best_chunks),
                'method': 'chromadb_search'
            }
        
        except Exception as e:
            return await self._query_simple(question)
    
    async def _query_simple(self, question: str) -> Dict[str, Any]:
        if not self.document_chunks:
            storage_file = os.path.join(self.persist_directory, 'simple_storage.json')
            try:
                with open(storage_file, 'r', encoding='utf-8') as f:
                    self.document_chunks = json.load(f)
            except:
                pass
        
        if not self.document_chunks:
            return {
                'question': question,
                'answer': 'No documents have been indexed yet.',
                'confidence': 0.0,
                'method': 'simple_search'
            }
        
        question_words = set(question.lower().split())
        best_chunks = []
        
        for doc_data in self.document_chunks.values():
            for chunk in doc_data['chunks']:
                chunk_words = set(chunk.lower().split())
                overlap = len(question_words & chunk_words)
                
                if overlap > 0:
                    score = overlap / len(question_words)
                    best_chunks.append((chunk, score))
        
        best_chunks.sort(key=lambda x: x[1], reverse=True)
        
        if not best_chunks:
            return {
                'question': question,
                'answer': 'No relevant information found in the documents.',
                'confidence': 0.0,
                'method': 'simple_search'
            }
        
        context = '\n\n'.join([chunk[0] for chunk in best_chunks[:3]])
        answer = self._generate_simple_answer(question, context)
        
        return {
            'question': question,
            'answer': answer,
            'confidence': 0.6,
            'sources_used': min(3, len(best_chunks)),
            'method': 'simple_search'
        }
    
    def _generate_simple_answer(self, question: str, context: str) -> str:
        question_lower = question.lower()
        context_sentences = re.split(r'[.!?]+', context)
        
        relevant_sentences = []
        
        for sentence in context_sentences:
            if len(sentence.strip()) < 10:
                continue
            
            sentence_lower = sentence.lower()
            question_words = question_lower.split()
            
            relevance_score = 0
            for word in question_words:
                if len(word) > 3 and word in sentence_lower:
                    relevance_score += 1
            
            if relevance_score > 0:
                relevant_sentences.append((sentence.strip(), relevance_score))
        
        if not relevant_sentences:
            return "I found some information but couldn't extract a specific answer to your question."
        
        relevant_sentences.sort(key=lambda x: x[1], reverse=True)
        
        answer_parts = []
        for sentence, score in relevant_sentences[:3]:
            if sentence not in answer_parts:
                answer_parts.append(sentence)
        
        return '. '.join(answer_parts) + '.' if answer_parts else "No specific answer found."
    
    def get_knowledge_base_stats_complete(self) -> Dict[str, Any]:
        if CHROMADB_AVAILABLE and self.collection:
            try:
                count = self.collection.count()
                return {
                    'total_documents': count,
                    'ready_for_qa': count > 0,
                    'storage_method': 'chromadb',
                    'embedding_model': 'all-MiniLM-L6-v2' if self.model else 'none'
                }
            except:
                pass
        
        if not self.document_chunks:
            storage_file = os.path.join(self.persist_directory, 'simple_storage.json')
            try:
                with open(storage_file, 'r', encoding='utf-8') as f:
                    self.document_chunks = json.load(f)
            except:
                pass
        
        total_chunks = sum(len(doc['chunks']) for doc in self.document_chunks.values())
        
        return {
            'total_documents': len(self.document_chunks),
            'total_chunks': total_chunks,
            'ready_for_qa': len(self.document_chunks) > 0,
            'storage_method': 'simple_json',
            'embedding_model': 'keyword_matching'
        }
    
    async def close(self):
        pass
