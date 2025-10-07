import React, { useState } from 'react';
import { Upload, Play, Download } from 'lucide-react';

const AudiobookPage = () => {
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('idle');
  const [result, setResult] = useState(null);

  const handleFileSelect = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploadStatus('uploading');
    
    const formData = new FormData();
    formData.append('file', file);

    try {
      setUploadStatus('processing');
      const response = await fetch('http://localhost:8000/api/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Upload failed');
      }

      const data = await response.json();
      setResult({
        fileId: 'generated',
        text: data.text,
        text_length: data.text_length,
        audio_url: 'http://localhost:8000/api/download-audio'
      });
      setUploadStatus('completed');
    } catch (error) {
      console.error('Upload error:', error);
      setUploadStatus('idle');
      alert('Upload failed. Please try again.');
    }
  };

  const downloadAudio = () => {
    window.open('http://localhost:8000/api/download-audio', '_blank');
  };

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto' }}>
      <div className="text-center mb-6">
        <h1 className="text-4xl font-bold gradient-text mb-4">
          AI Audiobook Generator
        </h1>
        <p className="text-lg" style={{ color: '#6b7280' }}>
          Transform your documents into professional audiobooks with AI
        </p>
      </div>

      <div className="card">
        <div className="text-center">
          <div style={{ 
            width: '64px', 
            height: '64px', 
            background: 'linear-gradient(135deg, #3b82f6, #8b5cf6)',
            borderRadius: '50%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            margin: '0 auto 1rem'
          }}>
            <Upload size={32} color="white" />
          </div>
          <h2 className="text-2xl font-bold mb-2">Upload Document</h2>
          <p className="mb-6" style={{ color: '#6b7280' }}>
            Support for PDF, DOCX, PPTX, and image files
          </p>

          <div className="upload-zone">
            <input
              type="file"
              onChange={handleFileSelect}
              accept=".pdf,.docx,.pptx,.png,.jpg,.jpeg,.bmp,.tiff"
              style={{ display: 'none' }}
              id="file-upload"
            />
            <label htmlFor="file-upload" style={{ cursor: 'pointer', display: 'block' }}>
              <Upload size={48} style={{ color: '#9ca3af', margin: '0 auto 1rem' }} />
              <p style={{ color: '#6b7280' }}>
                {file ? file.name : 'Click to select a file or drag and drop'}
              </p>
            </label>
          </div>

          {file && (
            <button
              onClick={handleUpload}
              disabled={uploadStatus !== 'idle'}
              className="btn btn-primary mt-6"
              style={{ margin: '1.5rem auto 0', display: 'flex' }}
            >
              {uploadStatus === 'uploading' || uploadStatus === 'processing' ? (
                <>
                  <div className="spinner" style={{ marginRight: '0.5rem' }}></div>
                  <span>{uploadStatus === 'uploading' ? 'Uploading...' : 'Processing...'}</span>
                </>
              ) : (
                <>
                  <Upload size={20} style={{ marginRight: '0.5rem' }} />
                  <span>Generate Audiobook</span>
                </>
              )}
            </button>
          )}
        </div>
      </div>

      {result && (
        <div className="card">
          <h3 className="text-2xl font-bold mb-6" style={{ display: 'flex', alignItems: 'center' }}>
            <Play size={24} style={{ marginRight: '0.5rem', color: '#16a34a' }} />
            Audiobook Ready
          </h3>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
            <div>
              <h4 className="font-semibold mb-2">Generated Text Preview</h4>
              <div style={{ 
                background: '#f9fafb', 
                borderRadius: '0.5rem', 
                padding: '1rem', 
                maxHeight: '160px', 
                overflowY: 'auto',
                fontSize: '0.875rem'
              }}>
                {result.text}
              </div>
              <p style={{ fontSize: '0.875rem', color: '#6b7280', marginTop: '0.5rem' }}>
                Total length: {result.text_length} characters
              </p>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: '1rem' }}>
              <audio controls style={{ width: '100%' }}>
                <source src="http://localhost:8000/api/download-audio" type="audio/wav" />
                <source src="http://localhost:8000/api/download-audio" type="audio/mpeg" />
                Your browser does not support the audio element.
              </audio>
              <button
                onClick={downloadAudio}
                className="btn"
                style={{ 
                  background: 'linear-gradient(135deg, #16a34a, #3b82f6)',
                  color: 'white'
                }}
              >
                <Download size={20} style={{ marginRight: '0.5rem' }} />
                <span>Download Audio</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AudiobookPage;