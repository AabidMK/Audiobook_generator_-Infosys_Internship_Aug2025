import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ragutils import create_collection, query_with_gemini
from ragcall import rag_call

# Test RAG system
print("Testing RAG system...")

# Store some test content
test_content = "Neural networks are computational models inspired by biological neural networks. They consist of interconnected nodes called neurons that process information."
rag_call(test_content, "test_document.txt")

# Test querying
collection = create_collection()
print(f"Collection count: {collection.count()}")

# Test query
try:
    response, chunks = query_with_gemini("What are neural networks?", collection)
    print(f"Response: {response}")
except Exception as e:
    print(f"Query failed: {e}")