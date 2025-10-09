"""
Test script to diagnose RAG endpoint issues
"""
import os
import sys

print("=" * 70)
print("RAG SYSTEM DIAGNOSTIC TEST")
print("=" * 70)

# Test 1: Check if .env file exists
print("\n[TEST 1] Checking for .env file...")
if os.path.exists(".env"):
    print("✓ .env file found")
    with open(".env", "r") as f:
        content = f.read()
        if "GEMINI_API_KEY" in content:
            print("✓ GEMINI_API_KEY found in .env")
        else:
            print("✗ GEMINI_API_KEY NOT found in .env")
else:
    print("✗ .env file NOT found")

# Test 2: Check ChromaDB
print("\n[TEST 2] Checking ChromaDB...")
try:
    import chromadb
    client = chromadb.PersistentClient(path="chroma_db")
    collection = client.get_collection("documents")
    count = collection.count()
    print(f"✓ ChromaDB connected successfully")
    print(f"✓ Collection 'documents' has {count} chunks")
except Exception as e:
    print(f"✗ ChromaDB error: {e}")

# Test 3: Check embedding model
print("\n[TEST 3] Checking embedding model...")
try:
    from sentence_transformers import SentenceTransformer
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    print("✓ Embedding model loaded successfully")
except Exception as e:
    print(f"✗ Embedding model error: {e}")

# Test 4: Check Gemini API
print("\n[TEST 4] Checking Gemini API configuration...")
try:
    from dotenv import load_dotenv
    import google.generativeai as genai
    
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if api_key:
        print("✓ GEMINI_API_KEY loaded from environment")
        genai.configure(api_key=api_key)
        print("✓ Gemini API configured")
    else:
        print("✗ GEMINI_API_KEY not found in environment")
except Exception as e:
    print(f"✗ Gemini API error: {e}")

# Test 5: Test RAG pipeline directly
print("\n[TEST 5] Testing RAG pipeline directly...")
try:
    from backend.rag.rag_pipeline import backend.rag.rag_pipeline as rag_pipeline
    
    test_question = "What is this document about?"
    print(f"Question: {test_question}")
    
    answer, citations = rag_pipeline(test_question, top_k=3)
    
    print("\n✓ RAG pipeline executed successfully!")
    print(f"\nAnswer preview: {answer[:200]}...")
    print(f"\nNumber of citations: {len(citations)}")
    
except Exception as e:
    print(f"✗ RAG pipeline error: {e}")
    import traceback
    traceback.print_exc()

# Test 6: Check if server is running
print("\n[TEST 6] Checking if Flask server is accessible...")
try:
    import requests
    response = requests.get("http://localhost:8080/health", timeout=2)
    if response.status_code == 200:
        print("✓ Flask server is running and accessible")
    else:
        print(f"✗ Flask server returned status code: {response.status_code}")
except requests.exceptions.ConnectionError:
    print("✗ Flask server is NOT running (connection refused)")
except Exception as e:
    print(f"✗ Error checking server: {e}")

# Test 7: Test RAG endpoint if server is running
print("\n[TEST 7] Testing /rag-query/ endpoint...")
try:
    import requests
    
    payload = {"question": "audiobook_chunks"}
    response = requests.post(
        "http://localhost:8080/rag-query/",
        data=payload,
        timeout=30
    )
    
    if response.status_code == 200:
        data = response.json()
        print("✓ /rag-query/ endpoint responded successfully")
        print(f"Answer preview: {data.get('answer', '')[:200]}...")
    else:
        print(f"✗ /rag-query/ endpoint returned status {response.status_code}")
        print(f"Response: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("✗ Cannot test endpoint - server not running")
except Exception as e:
    print(f"✗ Endpoint test error: {e}")

print("\n" + "=" * 70)
print("DIAGNOSTIC TEST COMPLETE")
print("=" * 70)

print("\n[RECOMMENDATIONS]")
print("1. Ensure .env file exists with GEMINI_API_KEY")
print("2. Ensure ChromaDB has indexed documents")
print("3. Start Flask server: python pipeline_orchestrator.py serve")
print("4. Check browser console for frontend errors")
