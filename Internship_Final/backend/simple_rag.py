import os
import json
from typing import List, Dict

# Simple in-memory document store
documents = {}
document_counter = 0

def store_document(content: str, filename: str) -> str:
    """Store document content with a unique ID"""
    global document_counter
    doc_id = f"doc_{document_counter}"
    documents[doc_id] = {
        "content": content,
        "filename": filename,
        "chunks": content.split('. ')  # Simple sentence splitting
    }
    document_counter += 1
    print(f"Stored document {doc_id}: {filename}")
    return doc_id

def search_documents(query: str) -> List[Dict]:
    """Simple keyword-based search"""
    results = []
    query_words = query.lower().split()
    
    for doc_id, doc in documents.items():
        for i, chunk in enumerate(doc["chunks"]):
            chunk_lower = chunk.lower()
            score = sum(1 for word in query_words if word in chunk_lower)
            
            if score > 0:
                results.append({
                    "doc_id": doc_id,
                    "chunk": chunk,
                    "filename": doc["filename"],
                    "score": score
                })
    
    # Sort by score
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:3]  # Top 3 results

def generate_response(query: str, context_chunks: List[Dict]) -> str:
    """Generate response using context"""
    if not context_chunks:
        return "I don't have enough context to answer that question. Please upload a document first."
    
    context = " ".join([chunk["chunk"] for chunk in context_chunks])
    
    # Simple response generation
    response = f"Based on the uploaded documents, here's what I found: {context[:300]}..."
    
    return response

def chat_with_documents(query: str) -> str:
    """Main chat function"""
    if not documents:
        return "No documents found. Please upload a document first to enable document-based chat."
    
    # Search for relevant chunks
    relevant_chunks = search_documents(query)
    
    # Generate response
    response = generate_response(query, relevant_chunks)
    
    return response