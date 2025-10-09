"""
Main Server Entry Point
Run this file to start the audiobook generator backend server
"""
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Change to project root directory for relative paths
os.chdir(project_root)

try:
    # Try new structure first
    from backend.pipeline.orchestrator import main
    print("✓ Using reorganized structure")
except ImportError:
    # Fall back to old structure
    try:
        from pipeline_orchestrator import main
        print("✓ Using original structure")
    except ImportError as e:
        print(f"❌ Error: Could not import orchestrator module")
        print(f"   {e}")
        print("\n💡 Try running: python pipeline_orchestrator.py serve")
        sys.exit(1)

if __name__ == "__main__":
    main()
