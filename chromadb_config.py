import os
import sys

os.environ["CHROMA_DISABLE_DEFAULT_EMBED"] = "1"

class MockOnnxRuntime:
    """Mock onnxruntime module to prevent initialization errors"""
    def __getattr__(self, name):
        return None

sys.modules['onnxruntime'] = MockOnnxRuntime()