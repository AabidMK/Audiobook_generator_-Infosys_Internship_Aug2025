// src/components/AudioPlayer.jsx
import React from "react";

export default function AudioPlayer({ audioUrl }) {
  if (!audioUrl) return <div style={{ color: "#ccc", textAlign: "center", padding: 20 }}>No audio yet. Upload your document and generate.</div>;

  return (
    <div style={{ borderRadius: 12, background: "#414141ff", padding: 16, boxShadow: "0 2px 8px rgba(0,0,0,0.05)" }}>
      <audio controls src={audioUrl} style={{ width: "100%", marginBottom: 10 }} />
      <div style={{ textAlign: "center" }}>
        <a href={audioUrl} download style={{ color: "#0288d1", fontWeight: 500, textDecoration: "none" }}>⬇️ Download Audio</a>
      </div>
    </div>
  );
}