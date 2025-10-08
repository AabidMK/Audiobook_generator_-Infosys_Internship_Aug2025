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
    <form onSubmit={handleSubmit} style={{
      padding: 20,
      borderRadius: 12,
      background: "#202020",
      color: "#fff",
      display: "flex",
      flexDirection: "column",
      gap: 16
    }}>
      <label>
        Upload document (.pdf, .docx, .txt)
        <input
          type="file"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
          accept=".pdf,.docx,.txt"
          style={{ display: "block", marginTop: 8 }}
        />
      </label>

      <label>
        Initial question for RAG
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="e.g. What methods did Holmes use?"
          style={{ width: "100%", padding: 10, marginTop: 8, borderRadius: 6, border: "1px solid #b2ebf2" }}
        />
      </label>

      <button
        disabled={loading}
        type="submit"
        style={{
          padding: "10px 14px",
          borderRadius: 8,
          background: "#0288d1",
          color: "#fff",
          fontWeight: 600,
          border: "none",
          cursor: "pointer"
        }}
      >
        {loading ? "Processing..." : "Generate Audiobook & Answer"}
      </button>
    </form>
  );
}