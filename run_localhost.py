#!/usr/bin/env python3
"""
Simple script to run the project on localhost
"""

import os
import sys
import subprocess
import time
from unicode_utils import safe_print

def check_frontend():
    """Check if frontend exists"""
    frontend_dir = "frontend"
    if os.path.exists(frontend_dir):
        safe_print(f"[OK] Frontend directory found: {frontend_dir}")
        
        # Check for package.json
        if os.path.exists(os.path.join(frontend_dir, "package.json")):
            safe_print("[OK] Frontend appears to be a Node.js project")
            return True
        else:
            safe_print("[INFO] Frontend directory exists but no package.json found")
            return False
    else:
        safe_print("[INFO] No frontend directory found")
        return False

def start_backend():
    """Start the backend API"""
    safe_print("\n[STARTING] Backend API on http://localhost:8000")
    try:
        # Run the API
        subprocess.run([sys.executable, "start_api.py"], check=True)
    except KeyboardInterrupt:
        safe_print("\n[STOPPED] Backend stopped by user")
    except Exception as e:
        safe_print(f"[ERROR] Backend failed: {e}")

def start_frontend():
    """Start the frontend (if available)"""
    if not check_frontend():
        return False
    
    frontend_dir = "frontend"
    safe_print(f"\n[STARTING] Frontend from {frontend_dir}")
    
    try:
        # Change to frontend directory
        os.chdir(frontend_dir)
        
        # Try to install dependencies if node_modules doesn't exist
        if not os.path.exists("node_modules"):
            safe_print("[INFO] Installing frontend dependencies...")
            subprocess.run(["npm", "install"], check=True)
        
        # Start the frontend
        safe_print("[INFO] Starting frontend server...")
        subprocess.run(["npm", "run", "dev"], check=True)
        
    except FileNotFoundError:
        safe_print("[ERROR] Node.js/npm not found. Please install Node.js")
        return False
    except subprocess.CalledProcessError as e:
        safe_print(f"[ERROR] Frontend start failed: {e}")
        return False
    except KeyboardInterrupt:
        safe_print("\n[STOPPED] Frontend stopped by user")
        return True
    
    return True

def main():
    safe_print("AudioBook Generator - Localhost Setup")
    safe_print("=" * 50)
    
    # Check environment
    api_key = os.getenv('GEMINI_API_KEY', '')
    if not api_key:
        safe_print("[ERROR] GEMINI_API_KEY not found in .env file")
        safe_print("[INFO] Please set your Gemini API key in .env file")
        return False
    
    safe_print(f"[OK] Gemini API key configured")
    
    # Check if frontend exists
    has_frontend = check_frontend()
    
    if has_frontend:
        safe_print("\n[CHOICE] You have a frontend. Choose an option:")
        safe_print("1. Start backend only (API at http://localhost:8000)")
        safe_print("2. Start frontend only (you'll need to start backend separately)")
        safe_print("3. Instructions for manual setup")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            start_backend()
        elif choice == "2":
            start_frontend()
        elif choice == "3":
            safe_print("\n[INSTRUCTIONS] Manual Setup:")
            safe_print("1. Terminal 1: python start_api.py")
            safe_print("2. Terminal 2: cd frontend && npm run dev")
            safe_print("3. Open your frontend URL (usually http://localhost:3000 or http://localhost:5173)")
        else:
            safe_print("[INFO] Invalid choice. Starting backend only...")
            start_backend()
    else:
        safe_print("\n[INFO] No frontend detected. Starting backend API only...")
        safe_print("[INFO] API will be available at http://localhost:8000")
        safe_print("[INFO] API docs at http://localhost:8000/docs")
        start_backend()

if __name__ == "__main__":
    main()