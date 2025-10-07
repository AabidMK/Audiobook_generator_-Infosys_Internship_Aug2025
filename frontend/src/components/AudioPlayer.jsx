// src/components/AudioPlayer.jsx
import React from "react";

export default function AudioPlayer({ audioUrl }) {
  if (!audioUrl) return <div style={{ color: "#555" }}>No audio yet. Upload your document and generate.</div>;

  return (
    <div style={{ borderRadius: 12, background: "#fffde7", padding: 16, boxShadow: "0 2px 8px rgba(0,0,0,0.05)" }}>
      <audio controls src={audioUrl} style={{ width: "100%" }} />
      <div style={{ marginTop: 10 }}>
        <a href={audioUrl} download style={{ color: "#f57f17", fontWeight: 500 }}>⬇️ Download audio</a>
      </div>
    </div>
  );
}