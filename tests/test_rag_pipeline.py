"""
Quick test script to verify RAG functionality
"""
from backend.rag.rag_pipeline import backend.rag.rag_pipeline as rag_pipeline

# Test questions
test_questions = [
    "What is the main topic of the document?",
    "Can you summarize the key points?",
    "What are the important concepts discussed?"
]

print("=" * 60)
print("RAG FUNCTIONALITY TEST")
print("=" * 60)

for i, question in enumerate(test_questions, 1):
    print(f"\n\n{'='*60}")
    print(f"TEST {i}: {question}")
    print('='*60)
    
    try:
        answer, citations = rag_pipeline(question, top_k=3)
        
        print("\n--- ANSWER ---")
        print(answer)
        
        print("\n--- CITATIONS ---")
        for j, cite in enumerate(citations, 1):
            print(f"{j}. File: {cite.get('file_path', 'N/A')}")
            print(f"   Chunk Index: {cite.get('chunk_index', 'N/A')}")
            print(f"   Distance: {cite.get('distance', 'N/A'):.4f}")
        
        print("\n✓ Test passed - Answer received successfully")
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

print("\n\n" + "=" * 60)
print("RAG TEST COMPLETE")
print("=" * 60)
