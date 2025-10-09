// src/components/UploadForm.jsx
import React, { useState } from "react";
import api, { API_BASE } from "../api";

export default function UploadForm({ onAudio, onAnswer, onProcessing }) {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [dragActive, setDragActive] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!file || !question) return alert("Please upload a file and type a question.");

    setLoading(true);
    if (onProcessing) onProcessing(true);
    const fd = new FormData();
    fd.append("file", file);
    fd.append("question", question);

    try {
      const resp = await api.post("/generate-audiobook/", fd);
      const { audio_url, answer } = resp.data;
      const audioFull = new URL(audio_url, API_BASE).toString();
      onAudio(audioFull);
      onAnswer(answer);
    } catch (err) {
      console.error("generate error", err);
      alert("Error generating audiobook. Check backend logs.");
    } finally {
      setLoading(false);
      if (onProcessing) onProcessing(false);
    }
  }

  function handleDrag(e) {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }

  function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  }

  return (
    <div style={{
      background: "white",
      borderRadius: 20,
      padding: 40,
      boxShadow: "0 4px 24px rgba(0,0,0,0.08)",
      maxWidth: 700,
      margin: "0 auto",
    }}>
      <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: 24 }}>
        {/* Upload Area */}
        <div>
          <label style={{
            display: "block",
            fontSize: 14,
            fontWeight: 600,
            color: "#1e293b",
            marginBottom: 12,
          }}>
            Upload Your Document
          </label>
          <div
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            style={{
              border: dragActive ? "2px dashed #667eea" : "2px dashed #e2e8f0",
              borderRadius: 16,
              padding: 40,
              textAlign: "center",
              background: dragActive ? "#f8f9ff" : "#f8fafc",
              transition: "all 0.3s ease",
              cursor: "pointer",
              position: "relative",
            }}
            onClick={() => document.getElementById("fileInput").click()}
          >
            <input
              id="fileInput"
              type="file"
              onChange={(e) => setFile(e.dataTransfer?.files?.[0] || e.target.files?.[0] || null)}
              accept=".pdf,.docx,.txt"
              style={{ display: "none" }}
            />
            <div style={{
              width: 64,
              height: 64,
              background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
              borderRadius: 16,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              margin: "0 auto 16px",
              boxShadow: "0 4px 16px rgba(102, 126, 234, 0.3)",
            }}>
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="17 8 12 3 7 8"></polyline>
                <line x1="12" y1="3" x2="12" y2="15"></line>
              </svg>
            </div>
            <h3 style={{
              fontSize: 18,
              fontWeight: 600,
              color: "#667eea",
              margin: "0 0 8px 0",
            }}>
              {file ? file.name : "Upload Your Document"}
            </h3>
            <p style={{
              fontSize: 14,
              color: "#64748b",
              margin: 0,
            }}>
              Drag and drop or click to browse
            </p>
            <div style={{
              display: "flex",
              gap: 8,
              justifyContent: "center",
              marginTop: 16,
            }}>
              <span style={{
                padding: "4px 12px",
                background: "#fee2e2",
                color: "#dc2626",
                borderRadius: 6,
                fontSize: 12,
                fontWeight: 600,
              }}>PDF</span>
              <span style={{
                padding: "4px 12px",
                background: "#d1fae5",
                color: "#059669",
                borderRadius: 6,
                fontSize: 12,
                fontWeight: 600,
              }}>DOCX</span>
              <span style={{
                padding: "4px 12px",
                background: "#fef3c7",
                color: "#d97706",
                borderRadius: 6,
                fontSize: 12,
                fontWeight: 600,
              }}>TXT</span>
            </div>
          </div>
        </div>

        {/* Question Input */}
        <div>
          <label style={{
            display: "block",
            fontSize: 14,
            fontWeight: 600,
            color: "#1e293b",
            marginBottom: 12,
          }}>
            Initial Question for RAG
          </label>
          <input
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="e.g., What are the main topics discussed in this document?"
            style={{
              width: "100%",
              padding: "14px 16px",
              borderRadius: 12,
              border: "2px solid #e2e8f0",
              fontSize: 15,
              outline: "none",
              transition: "all 0.3s ease",
              boxSizing: "border-box",
            }}
            onFocus={(e) => e.target.style.borderColor = "#667eea"}
            onBlur={(e) => e.target.style.borderColor = "#e2e8f0"}
          />
        </div>

        {/* Submit Button */}
        <button
          disabled={loading}
          type="submit"
          style={{
            padding: "16px 24px",
            borderRadius: 12,
            background: loading ? "#94a3b8" : "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            color: "white",
            fontSize: 16,
            fontWeight: 600,
            border: "none",
            cursor: loading ? "not-allowed" : "pointer",
            transition: "all 0.3s ease",
            boxShadow: loading ? "none" : "0 4px 16px rgba(102, 126, 234, 0.4)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: 8,
          }}
          onMouseOver={(e) => {
            if (!loading) {
              e.currentTarget.style.transform = "translateY(-2px)";
              e.currentTarget.style.boxShadow = "0 6px 20px rgba(102, 126, 234, 0.5)";
            }
          }}
          onMouseOut={(e) => {
            e.currentTarget.style.transform = "translateY(0)";
            e.currentTarget.style.boxShadow = "0 4px 16px rgba(102, 126, 234, 0.4)";
          }}
        >
          {loading ? (
            <>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ animation: "spin 1s linear infinite" }}>
                <path d="M21 12a9 9 0 1 1-6.219-8.56"></path>
              </svg>
              Processing...
            </>
          ) : (
            <>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <polyline points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polyline>
              </svg>
              Generate Audiobook & Answer
            </>
          )}
        </button>
      </form>

      <style>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}