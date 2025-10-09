# Project Reorganization Plan

## Current Structure Issues
- All Python files in root directory (cluttered)
- Multiple documentation files scattered
- Temporary MP3 files in root
- Test files mixed with production code
- No clear separation of concerns

## Proposed Professional Structure

```
audiobook-generator/
├── backend/                    # All Python backend code
│   ├── __init__.py
│   ├── core/                   # Core modules
│   │   ├── __init__.py
│   │   ├── audiobook_generator.py
│   │   ├── text_extractor.py
│   │   └── enhanced_extraction.py
│   ├── rag/                    # RAG-related modules
│   │   ├── __init__.py
│   │   ├── rag_pipeline.py (renamed from rag.py)
│   │   ├── text_chunking.py
│   │   ├── vector_embedding.py
│   │   └── chroma_storing.py
│   ├── pipeline/               # Pipeline orchestration
│   │   ├── __init__.py
│   │   ├── orchestrator.py (renamed from pipeline_orchestrator.py)
│   │   └── indexing.py (renamed from pipeline_rag.py)
│   └── server.py               # Main entry point
│
├── frontend/                   # React frontend (existing)
│   └── ... (unchanged)
│
├── tests/                      # All test files
│   ├── __init__.py
│   ├── test_rag_pipeline.py
│   ├── test_rag_endpoint.py
│   └── test_upload.py
│
├── docs/                       # All documentation
│   ├── SETUP_GUIDE.md
│   ├── TESTING_GUIDE.md
│   ├── API_DOCUMENTATION.md
│   ├── TROUBLESHOOTING.md
│   └── RAG_FIX_HISTORY.md
│
├── outputs/                    # Generated files
│   ├── audiobooks/            # Generated audiobook files
│   └── transcripts/           # Text transcripts
│
├── data/                       # Data storage
│   ├── chroma_db/             # Vector database
│   └── llm_cache/             # LLM cache
│
├── scripts/                    # Utility scripts
│   ├── start_servers.ps1
│   ├── start_servers.bat
│   └── check_status.bat
│
├── .env                        # Environment variables
├── .env.template              # Template for .env
├── .gitignore                 # Git ignore rules
├── requirements.txt           # Python dependencies
├── README.md                  # Main README
├── LICENSE                    # License file
└── PROJECT_STRUCTURE.md       # This file

```

## Files to Move

### To backend/core/
- audiobook_generator.py
- text_extractor.py
- enhanced_extraction.py

### To backend/rag/
- rag.py → rag_pipeline.py
- text_chunking.py
- vector_embedding.py
- chroma_storing.py

### To backend/pipeline/
- pipeline_orchestrator.py → orchestrator.py
- pipeline_rag.py → indexing.py

### To tests/
- test_rag.py → test_rag_pipeline.py
- test_rag_endpoint.py
- test_upload.py

### To docs/
- SETUP_INSTRUCTIONS.md → SETUP_GUIDE.md
- TESTING_GUIDE.md
- FIX_400_ERROR.md → TROUBLESHOOTING.md (merge)
- FIX_RAG_CHECKLIST.md → TROUBLESHOOTING.md (merge)
- RAG_ISSUES_AND_FIXES.md → RAG_FIX_HISTORY.md
- RAG_STATUS_REPORT.md → RAG_FIX_HISTORY.md (merge)
- READY_TO_TEST.md → SETUP_GUIDE.md (merge)
- SUMMARY.md → RAG_FIX_HISTORY.md (merge)

### To scripts/
- start_servers.ps1
- start_servers.bat
- check_status.bat

### To outputs/audiobooks/
- All *_COMPLETE_audiobook_AUDIO_*.mp3 files

### To data/
- chroma_db/ (move entire folder)
- complete_llm_cache/ → llm_cache/

## Files to Delete
- env_example.txt (replaced by .env.template)
- package-lock.json (root - not needed, frontend has its own)
- test_document.txt (sample file - can be in tests/)
- test_document_COMPLETE_audiobook_AUDIO_storytelling.mp3 (sample output)
- All tmp*.mp3 files (temporary files)
- __pycache__/ (will be regenerated)
- complete_audiobooks/ folder (move contents to outputs/audiobooks/)
- UI/ folder (empty)
- .venv/ (empty, users create their own)

## Import Path Changes Required

### Example Changes:
```python
# OLD
from rag import rag_pipeline
from audiobook_generator import StateOfTheArtAudiobookGenerator

# NEW
from backend.rag.rag_pipeline import rag_pipeline
from backend.core.audiobook_generator import StateOfTheArtAudiobookGenerator
```

## Critical Files That Need Path Updates
1. backend/pipeline/orchestrator.py (imports all modules)
2. backend/pipeline/indexing.py (imports extraction, chunking, embedding)
3. backend/server.py (new main entry point)
4. All test files
5. start_servers scripts

## Execution Order
1. Create new directory structure
2. Copy files to new locations (don't move yet, to be safe)
3. Update all import statements
4. Update startup scripts
5. Test that everything works
6. Delete old files
7. Clean up temporary files
