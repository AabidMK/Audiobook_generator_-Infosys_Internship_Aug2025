#!/usr/bin/env python3
"""Test script to verify file upload functionality"""

import requests
import os

def test_file_upload():
    """Test the file upload endpoint"""
    
    # Check if test file exists
    test_file = "test_document.txt"
    if not os.path.exists(test_file):
        print(f"Test file {test_file} not found")
        return False
    
    # Test the endpoint
    url = "http://localhost:8080/generate-audiobook/"
    
    try:
        with open(test_file, 'rb') as f:
            files = {'file': f}
            data = {'question': 'What is this document about?'}
            
            print(f"Uploading {test_file} to {url}")
            response = requests.post(url, files=files, data=data, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                print("Upload successful!")
                print(f"Response: {result}")
                return True
            else:
                print(f"Upload failed with status {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
    except Exception as e:
        print(f"Error during upload: {e}")
        return False

if __name__ == "__main__":
    print("Testing File Upload Functionality")
    print("=" * 50)
    
    # Test backend health first
    try:
        health_response = requests.get("http://localhost:8080/health")
        if health_response.status_code == 200:
            print("Backend server is running")
        else:
            print("Backend server is not responding")
            exit(1)
    except Exception as e:
        print(f"Cannot connect to backend: {e}")
        exit(1)
    
    # Test file upload
    success = test_file_upload()
    
    if success:
        print("\nFile upload test PASSED!")
    else:
        print("\nFile upload test FAILED!")
    
    print("=" * 50)
