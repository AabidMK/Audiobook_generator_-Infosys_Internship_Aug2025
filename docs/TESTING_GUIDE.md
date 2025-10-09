# RAG Testing Guide - Step by Step

## 🎯 Objective
Test if the RAG (Retrieval-Augmented Generation) question-answering system works correctly in the frontend.

## ✅ Pre-Test Checklist

Before starting, verify:
- [x] `.env` file exists in root directory with GEMINI_API_KEY
- [x] `frontend/.env` file exists with VITE_API_URL
- [x] ChromaDB has data (chroma_db folder exists)
- [x] Collection name fixed in ChatBox.jsx

**All items checked!** ✅ Ready to test!

## 🚀 Test Procedure

### Step 1: Start the Servers

**Option A - Automated (Recommended):**
```powershell
.\start_servers.ps1
```
Wait for both windows to open and show "Running" status.

**Option B - Manual:**
```powershell
# Window 1 - Backend
python pipeline_orchestrator.py serve --port 8080

# Window 2 - Frontend
cd frontend
npm run dev
```

### Step 2: Verify Backend Health

1. Open browser
2. Navigate to: `http://localhost:8080/health`
3. **Expected**: Page shows "ok"
4. **If fails**: Backend not running, check terminal for errors

### Step 3: Open Frontend

1. Navigate to: `http://localhost:5173`
2. **Expected**: See "AI Audiobook Generator" interface
3. **If fails**: Frontend not running, check npm terminal

### Step 4: Test RAG with Existing Data

Since ChromaDB already has indexed documents, you can test immediately:

1. **Locate the Chat Box** (bottom right section, labeled "💬 Chat (RAG)")
2. **Type a question** in the input field:
   ```
   What is this document about?
   ```
3. **Click "Ask" button**
4. **Wait** 5-10 seconds
5. **Observe the response**

#### ✅ Success Indicators:
- Answer appears in chat box
- Answer is relevant and coherent
- Citations appear below answer
- No error messages

#### ❌ Failure Indicators:
- "Error fetching answer" message
- No response after 30+ seconds
- Browser console shows errors
- Network errors in DevTools

### Step 5: Test Follow-up Questions

If Step 4 worked, try follow-up questions:

```
Can you provide more details?
What are the key points?
Tell me about the main concepts.
```

Each should return relevant answers within 5-10 seconds.

### Step 6: Test with New Document Upload

1. **Click "Choose File"** in the upload form
2. **Select a document** (PDF, DOCX, or TXT)
3. **Enter initial question**:
   ```
   What is the main topic of this document?
   ```
4. **Click "Generate Audiobook & Answer"**
5. **Wait** (this takes 1-3 minutes for processing)
6. **Observe**:
   - Progress indicator shows
   - Audiobook generates
   - Initial answer appears in chat
   - Can ask follow-up questions

## 🐛 Debugging Guide

### Problem: "Connection refused" in console

**Diagnosis**: Backend server not running

**Solution**:
```powershell
python pipeline_orchestrator.py serve --port 8080
```

**Verify**: http://localhost:8080/health shows "ok"

---

### Problem: "Error fetching answer" in chat

**Diagnosis**: Backend error or API issue

**Debug Steps**:
1. Open browser DevTools (F12)
2. Go to Console tab
3. Look for red error messages
4. Go to Network tab
5. Find the failed `/rag-query/` request
6. Click it and check Response tab

**Common Causes**:
- Gemini API key invalid
- Collection not found
- Backend crashed

**Check Backend Terminal** for Python errors like:
```
ValueError: Gemini api key not found
```

**Solution**: Verify `.env` file has correct API key

---

### Problem: Answers are empty or irrelevant

**Diagnosis**: ChromaDB has no relevant data

**Solution**: Index documents first
```powershell
python pipeline_orchestrator.py index --files testing.pdf
```

**Verify**: Check ChromaDB size increased
```powershell
dir chroma_db
```

---

### Problem: Very slow responses (>30 seconds)

**Diagnosis**: Network issue or API rate limiting

**Check**:
1. Internet connection stable
2. Gemini API quota not exceeded
3. Backend terminal for timeout errors

---

### Problem: Frontend won't load

**Diagnosis**: Frontend server not running or port conflict

**Solution**:
```powershell
cd frontend
npm run dev
```

**Check for port conflicts**: Another app using port 5173?

---

## 📊 Expected vs Actual Results

### Test Case 1: Simple Question

**Input**: "What is this document about?"

**Expected Output**:
```
Answer: [Relevant summary of document content, 2-3 sentences]

Citations:
- File: testing.pdf, Chunk: 5, Distance: 0.234
- File: testing.pdf, Chunk: 12, Distance: 0.456
```

**Actual Output**: _(Test and record here)_

---

### Test Case 2: Specific Question

**Input**: "What are the key points discussed?"

**Expected Output**:
```
Answer: [Bullet points or paragraph listing main concepts]

Citations: [3-5 relevant chunks]
```

**Actual Output**: _(Test and record here)_

---

### Test Case 3: Follow-up Question

**Input**: "Can you elaborate on that?"

**Expected Output**:
```
Answer: [More detailed explanation based on context]

Citations: [Related chunks]
```

**Actual Output**: _(Test and record here)_

---

## 🔍 Verification Checklist

After testing, verify:

- [ ] Backend responds to health check
- [ ] Frontend loads without errors
- [ ] Chat box accepts input
- [ ] Questions return answers within 10 seconds
- [ ] Answers are relevant to documents
- [ ] Citations are displayed
- [ ] Follow-up questions work
- [ ] No console errors in browser
- [ ] No Python errors in backend terminal

## 📝 Test Results Template

```
Date: _____________
Tester: _____________

Backend Status: [ ] Running [ ] Not Running
Frontend Status: [ ] Running [ ] Not Running

Test 1 - Simple Question:
Status: [ ] Pass [ ] Fail
Notes: _________________________________

Test 2 - Follow-up Question:
Status: [ ] Pass [ ] Fail
Notes: _________________________________

Test 3 - New Document Upload:
Status: [ ] Pass [ ] Fail
Notes: _________________________________

Overall Status: [ ] All Tests Pass [ ] Some Failures

Issues Found:
_________________________________________
_________________________________________
```

## 🎓 Understanding the Flow

```
┌─────────────────────────────────────────────────────────┐
│ 1. USER TYPES QUESTION IN CHAT BOX                     │
│    "What is this document about?"                       │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ 2. FRONTEND (ChatBox.jsx)                              │
│    - Captures question                                  │
│    - Sends POST to /rag-query/                         │
│    - Payload: {question, collection: "documents"}      │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ 3. BACKEND (pipeline_orchestrator.py)                  │
│    - Receives request at /rag-query/ endpoint          │
│    - Extracts question from payload                     │
│    - Calls query_rag(question)                         │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ 4. RAG PIPELINE (rag.py)                               │
│    - Embeds question using SentenceTransformer         │
│    - Queries ChromaDB for similar chunks               │
│    - Retrieves top 5 relevant chunks                    │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ 5. CHROMADB                                             │
│    - Searches "documents" collection                    │
│    - Returns matching chunks with distances             │
│    - Includes metadata (file path, chunk index)        │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ 6. GEMINI API (via rag.py)                            │
│    - Receives context (top chunks) + question          │
│    - Generates coherent answer                          │
│    - Returns answer text                                │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ 7. BACKEND RESPONSE                                     │
│    - Formats: {answer, citations}                      │
│    - Sends JSON back to frontend                        │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ 8. FRONTEND DISPLAYS                                    │
│    - Shows answer in chat box                          │
│    - Shows citations below                              │
│    - Ready for next question                            │
└─────────────────────────────────────────────────────────┘
```

## 🎉 Success Criteria

The RAG system is working correctly if:

✅ Questions are answered within 10 seconds
✅ Answers are relevant to document content
✅ Citations are provided
✅ Follow-up questions work
✅ No errors in console or terminal
✅ System handles multiple questions in sequence

## 📞 If You Need Help

If tests fail:
1. Check `RAG_STATUS_REPORT.md` for detailed diagnostics
2. Run `python test_rag_endpoint.py` for automated checks
3. Review browser console (F12) and backend terminal logs
4. Verify all files in "Files Modified/Created" section exist

---

**Ready to test?** Start with Step 1! 🚀
