#!/usr/bin/env python3
"""
Setup verification script for AI Audiobook Generator
Checks if all dependencies and configurations are properly set up
"""

import os
import sys
import subprocess
import importlib.util

def check_python_version():
    """Check if Python version is 3.8+"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print("✅ Python version:", f"{version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print("❌ Python 3.8+ required. Current version:", f"{version.major}.{version.minor}.{version.micro}")
        return False

def check_python_packages():
    """Check if required Python packages are installed"""
    required_packages = [
        'fastapi', 'uvicorn', 'python-multipart', 'python-dotenv',
        'google.generativeai', 'TTS', 'PyPDF2', 'docx', 'pptx', 'PIL'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            if package == 'google.generativeai':
                import google.generativeai
            elif package == 'docx':
                import docx
            elif package == 'pptx':
                import pptx
            elif package == 'PIL':
                import PIL
            else:
                importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    return len(missing_packages) == 0, missing_packages

def check_node_version():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Node.js version: {version}")
            return True
        else:
            print("❌ Node.js not found")
            return False
    except FileNotFoundError:
        print("❌ Node.js not installed")
        return False

def check_npm_packages():
    """Check if frontend dependencies are installed"""
    frontend_path = os.path.join(os.path.dirname(__file__), 'frontend')
    node_modules_path = os.path.join(frontend_path, 'node_modules')
    
    if os.path.exists(node_modules_path):
        print("✅ Frontend dependencies installed")
        return True
    else:
        print("❌ Frontend dependencies not installed")
        return False

def check_env_file():
    """Check if environment file exists"""
    env_path = os.path.join(os.path.dirname(__file__), 'secrets.env')
    if os.path.exists(env_path):
        print("✅ Environment file (secrets.env) found")
        
        # Check if Google API key is set
        with open(env_path, 'r') as f:
            content = f.read()
            if 'GOOGLE_API_KEY=' in content and 'your_google_api_key_here' not in content:
                print("✅ Google API key configured")
                return True
            else:
                print("⚠️  Google API key not configured in secrets.env")
                return False
    else:
        print("❌ Environment file (secrets.env) not found")
        return False

def check_project_structure():
    """Check if project structure is correct"""
    base_path = os.path.dirname(__file__)
    required_paths = [
        'frontend/src/App.js',
        'frontend/package.json',
        'main.py',
        'tomarkdown.py'
    ]
    
    all_exist = True
    for path in required_paths:
        full_path = os.path.join(base_path, path)
        if os.path.exists(full_path):
            print(f"✅ {path}")
        else:
            print(f"❌ {path}")
            all_exist = False
    
    return all_exist

def main():
    print("🔍 AI Audiobook Generator - Setup Verification")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Python Packages", lambda: check_python_packages()[0]),
        ("Node.js", check_node_version),
        ("Frontend Dependencies", check_npm_packages),
        ("Environment Configuration", check_env_file),
        ("Project Structure", check_project_structure)
    ]
    
    print("\n📋 Checking Requirements:")
    print("-" * 30)
    
    all_passed = True
    for name, check_func in checks:
        print(f"\n{name}:")
        try:
            result = check_func()
            if not result:
                all_passed = False
        except Exception as e:
            print(f"❌ Error checking {name}: {e}")
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All checks passed! You're ready to start development.")
        print("\nTo start the application:")
        print("1. Run: python main.py")
        print("2. Run: cd frontend && npm start (in another terminal)")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        
        # Show installation commands for missing packages
        _, missing_packages = check_python_packages()
        if missing_packages:
            print(f"\nTo install missing Python packages:")
            print(f"pip install {' '.join(missing_packages)}")
        
        if not check_npm_packages():
            print(f"\nTo install frontend dependencies:")
            print(f"cd frontend && npm install")

if __name__ == "__main__":
    main()