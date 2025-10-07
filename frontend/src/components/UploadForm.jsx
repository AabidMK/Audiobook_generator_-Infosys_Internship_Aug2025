// src/components/UploadForm.jsx
import React, { useState } from "react";
import api, { API_BASE } from "../api";

export default function UploadForm({ onAudio, onAnswer }) {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!file || !question) return alert("Please upload a file and type a question.");

    setLoading(true);
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
        Initial question for RAG
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
        {loading ? "Processing..." : "Generate Audiobook & Answer"}
      </button>
    </form>
  );
}