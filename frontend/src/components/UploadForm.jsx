// src/components/UploadForm.jsx
import React, { useState } from "react";
import api, { API_BASE } from "../api";

export default function UploadForm({ onAudio, onAnswer }) {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [progress, setProgress] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    if (!file) return alert("Please upload a file.");

    setLoading(true);
    
    try {
      // Step 1: Upload and index file
      setProgress("Uploading file...");
      const fd = new FormData();
      fd.append("file", file);
      
      console.log("Uploading file:", file.name, "Size:", file.size);
      
      const uploadResp = await api.post("/upload", fd, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      console.log("Upload response:", uploadResp.data);
      const { file_path, message } = uploadResp.data;
      setUploadedFile(file_path);
      setProgress(message);
      
      // Step 2: Generate audiobook
      setProgress("Generating audiobook...");
      const audiobookResp = await api.post("/generate-audiobook", {
        file_path: file_path,
        voice_style: "storytelling",
        generate_audio: true,
        audio_length_limit: 25000
      });
      
      console.log("Audiobook response:", audiobookResp.data);
      
      const { audio_url } = audiobookResp.data;
      if (audio_url) {
        const audioFull = `${API_BASE}${audio_url}`;
        onAudio(audioFull);
      }
      
      // Step 3: Get initial answer if question provided
      if (question) {
        setProgress("Getting initial answer...");
        const queryResp = await api.post("/query", {
          question: question,
          top_k: 5
        });
        const { answer } = queryResp.data;
        onAnswer(answer);
      }
      
      setProgress("Complete!");
      
    } catch (err) {
      console.error("Error:", err);
      console.error("Error response:", err.response?.data);
      const errorMsg = err.response?.data?.detail || err.message || "Unknown error";
      alert(`Error: ${errorMsg}`);
      setProgress(`Error: ${errorMsg}`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      style={{
        padding: 24,
        borderRadius: 16,
        background: "#202020", // subtle light background
        color: "#ffffff",
        display: "flex",
        flexDirection: "column",
        gap: 20,
        maxWidth: 500,
        margin: "40px auto",
        boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
        fontFamily: "system-ui, Avenir, Helvetica, Arial, sans-serif",
      }}
    >
      <label style={{ display: "flex", flexDirection: "column", fontWeight: 500 }}>
        Upload document (.pdf, .docx, .txt)
        <input
          type="file"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
          accept=".pdf,.docx,.txt"
          style={{
            display: "block",
            marginTop: 8,
            padding: 8,
            borderRadius: 6,
            border: "1px solid #b2ebf2",
            background: "#fff",
            cursor: "pointer",
          }}
        />
      </label>

      <label style={{ display: "flex", flexDirection: "column", fontWeight: 500 }}>
        Initial question for RAG (optional)
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="e.g. What methods did Holmes use?"
          style={{
            width: "100%",
            padding: 10,
            marginTop: 8,
            borderRadius: 6,
            border: "1px solid #b2ebf2",
            fontSize: 14,
          }}
        />
      </label>
      
      {progress && (
        <div style={{ 
          padding: 8, 
          background: progress.includes("Error") ? "#f44336" : "#4caf50", 
          color: "white", 
          borderRadius: 4, 
          fontSize: 14 
        }}>
          {progress}
        </div>
      )}

      <button
        disabled={loading}
        type="submit"
        style={{
          padding: "12px 16px",
          borderRadius: 8,
          background: "#0288d1",
          color: "#fff",
          fontWeight: 600,
          border: "none",
          cursor: loading ? "not-allowed" : "pointer",
          transition: "background 0.3s",
        }}
        onMouseOver={(e) => {
          if (!loading) e.currentTarget.style.background = "#0277bd";
        }}
        onMouseOut={(e) => {
          e.currentTarget.style.background = "#0288d1";
        }}
      >
        {loading ? "Processing..." : "Upload & Generate Audiobook"}
      </button>
    </form>
  );
}