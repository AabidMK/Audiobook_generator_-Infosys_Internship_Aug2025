import requests

# Test backend connectivity
try:
    response = requests.get("http://localhost:8000")
    print(f"Backend status: {response.status_code}")
except Exception as e:
    print(f"Backend connection failed: {e}")

# Test upload endpoint
try:
    with open("../sample.png", "rb") as f:
        files = {"file": f}
        response = requests.post("http://localhost:8000/api/upload", files=files)
        print(f"Upload status: {response.status_code}")
        print(f"Upload response: {response.json()}")
except Exception as e:
    print(f"Upload test failed: {e}")

# Test chat endpoint
try:
    response = requests.post("http://localhost:8000/api/chat", 
                           json={"message": "test"})
    print(f"Chat status: {response.status_code}")
    print(f"Chat response: {response.json()}")
except Exception as e:
    print(f"Chat test failed: {e}")