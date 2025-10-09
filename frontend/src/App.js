import React, { useState, useCallback } from 'react';
import './App.css'; 

const API_BASE_URL = 'http://localhost:8000'; 

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileId, setFileId] = useState(null);
  const [query, setQuery] = useState('');
  const [answer, setAnswer] = useState(''); // Text answer
  const [citations, setCitations] = useState([]);
  const [audioBase64, setAudioBase64] = useState(null); // New state for audio
  const [status, setStatus] = useState('Ready to upload a PDF.');
  const [loading, setLoading] = useState(false);
  const [audioLoading, setAudioLoading] = useState(false); // New state for audio button

  // --- File Upload and Indexing (Unchanged) ---
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file && file.name.endsWith('.pdf')) {
      setSelectedFile(file);
      setStatus(`File selected: ${file.name}`);
      setFileId(null);
      setAnswer('');
      setAudioBase64(null); // Reset audio
    } else {
      setSelectedFile(null);
      setStatus('Please select a valid PDF file.');
    }
  };

  const handleUploadAndIndex = useCallback(async () => {
    if (!selectedFile) {
      alert('Please select a PDF file first.');
      return;
    }
    setLoading(true);
    setStatus(`Uploading and indexing ${selectedFile.name}... This may take a moment.`);
    setFileId(null);
    setAnswer('');
    setCitations([]);
    setAudioBase64(null);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch(`${API_BASE_URL}/upload_and_index/`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to index file.');
      }

      const data = await response.json();
      setFileId(data.file_id);
      setStatus(`Indexing successful! Ready to query file ID: ${data.file_id}`);
    } catch (error) {
      setStatus(`Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  }, [selectedFile]);
  
  // --- RAG Query (Updated to reset audio) ---
  const handleQuerySubmit = useCallback(async () => {
    if (!fileId) {
      alert('Please upload and index a file first.');
      return;
    }
    if (!query.trim()) {
        alert('Please enter a question.');
        return;
    }

    setLoading(true);
    setStatus(`Searching and generating answer for: "${query}"...`);
    setAnswer('');
    setCitations([]);
    setAudioBase64(null); // Reset audio on new query

    const formData = new FormData();
    formData.append('query', query);
    formData.append('file_id', fileId);

    try {
      const response = await fetch(`${API_BASE_URL}/rag_query/`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to get RAG answer.');
      }

      const data = await response.json();
      setAnswer(data.answer);
      setCitations(data.citations);
      setStatus('Query complete. Text answer ready.');

    } catch (error) {
      setStatus(`Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  }, [fileId, query]);

  // --- NEW: Audio Generation Handler ---
  const handleGenerateAudio = useCallback(async () => {
    if (!answer) {
      alert('Please run a query and get a text answer first.');
      return;
    }

    setAudioLoading(true);
    setAudioBase64(null);
    setStatus('Generating audio...');

    const formData = new FormData();
    formData.append('text_answer', answer);

    try {
      const response = await fetch(`${API_BASE_URL}/generate_audio/`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to generate audio.');
      }

      const data = await response.json();
      setAudioBase64(data.audio_base64);
      setStatus('Audio generation complete. Ready to play!');
    } catch (error) {
      setStatus(`Audio Error: ${error.message}`);
      setAudioBase64(null);
    } finally {
      setAudioLoading(false);
    }
  }, [answer]);


  return (
    <div className="App">
      <h1>PDF RAG Chatbot with Audio Answer (React + FastAPI)</h1>
      <p>Status: **{loading || audioLoading ? 'Processing...' : status}**</p>

      {/* --- File Upload and Indexing --- */}
      <div className="section">
        <h2>1. Upload PDF and Index</h2>
        <input 
          type="file" 
          accept=".pdf" 
          onChange={handleFileChange} 
          disabled={loading || audioLoading}
        />
        <button 
          onClick={handleUploadAndIndex} 
          disabled={!selectedFile || loading || audioLoading || fileId}
        >
          {fileId ? `Indexed (ID: ${fileId})` : 'Upload & Index'}
        </button>
        {fileId && <p style={{color: 'green'}}>Indexed Document ID: {fileId}</p>}
      </div>

      {/* --- RAG Query --- */}
      <div className="section">
        <h2>2. Ask a Question</h2>
        <textarea
          placeholder="Enter your question here..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          disabled={!fileId || loading || audioLoading}
          rows="3"
        />
        <button 
          onClick={handleQuerySubmit} 
          disabled={!fileId || loading || audioLoading || !query.trim()}
        >
          Get Text Answer
        </button>
      </div>

      {/* --- Results --- */}
      <div className="section results">
        <h2>3. RAG Answer</h2>
        <div className="answer-box">
          {answer ? <p>{answer}</p> : <p>Answer will appear here after a query.</p>}
        </div>

        {/* --- Audio Button and Player --- */}
        <div style={{ marginTop: '15px' }}>
          <button
            onClick={handleGenerateAudio}
            disabled={!answer || audioLoading || loading}
          >
            {audioLoading ? 'Generating Audio...' : 'Generate Audio Answer'}
          </button>
          
          {audioBase64 && (
            <div style={{ marginTop: '10px' }}>
              <p>Audio Ready:</p>
              {/* Data URL format for playing base64 audio */}
              <audio controls src={`data:audio/mp3;base64,${audioBase64}`} />
            </div>
          )}
        </div>

        {citations.length > 0 && (
          <>
            <h3>Citations</h3>
            <ul>
              {citations.map((cite, index) => (
                <li key={index}>
                  **{cite.source_id}** | File: {cite.file_path} | Chunk Index: {cite.chunk_index} | Relevance: {cite.distance}
                </li>
              ))}
            </ul>
          </>
        )}
      </div>
    </div>
  );
}

export default App;