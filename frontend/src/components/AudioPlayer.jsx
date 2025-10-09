// src/components/AudioPlayer.jsx
import React from "react";

export default function AudioPlayer({ audioUrl }) {
<<<<<<< HEAD
  if (!audioUrl) {
    return (
      <div style={{
        textAlign: "center",
        padding: 60,
        color: "#94a3b8",
        background: "#f8fafc",
        borderRadius: 16,
        border: "2px dashed #e2e8f0",
      }}>
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" style={{ margin: "0 auto 16px" }}>
          <path d="M9 18V5l12-2v13"></path>
          <circle cx="6" cy="18" r="3"></circle>
          <circle cx="18" cy="16" r="3"></circle>
        </svg>
        <p style={{ margin: 0, fontSize: 14 }}>
          No audio yet. Upload your document to generate an audiobook.
        </p>
      </div>
    );
  }

  return (
    <div style={{
      background: "linear-gradient(135deg, #2d3748 0%, #1a202c 100%)",
      borderRadius: 16,
      padding: 24,
      boxShadow: "0 8px 24px rgba(0,0,0,0.15)",
    }}>
      {/* Audio Title */}
      <div style={{
        display: "flex",
        alignItems: "center",
        gap: 12,
        marginBottom: 20,
      }}>
        <div style={{
          width: 48,
          height: 48,
          background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
          borderRadius: 12,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
            <path d="M9 18V5l12-2v13"></path>
            <circle cx="6" cy="18" r="3"></circle>
            <circle cx="18" cy="16" r="3"></circle>
          </svg>
        </div>
        <div>
          <h3 style={{
            margin: 0,
            fontSize: 16,
            fontWeight: 600,
            color: "white",
          }}>
            Your AI-Enhanced Audiobook
          </h3>
          <p style={{
            margin: "4px 0 0 0",
            fontSize: 13,
            color: "#94a3b8",
          }}>
            Ready to listen
          </p>
        </div>
      </div>

      {/* Audio Player */}
      <audio
        controls
        src={audioUrl}
        style={{
          width: "100%",
          height: 48,
          borderRadius: 8,
          marginBottom: 16,
        }}
      />

      {/* Download Button */}
      <a
        href={audioUrl}
        download
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          gap: 8,
          padding: "12px 20px",
          background: "linear-gradient(135deg, #10b981 0%, #059669 100%)",
          color: "white",
          borderRadius: 10,
          textDecoration: "none",
          fontWeight: 600,
          fontSize: 14,
          transition: "all 0.3s ease",
          boxShadow: "0 4px 12px rgba(16, 185, 129, 0.3)",
        }}
        onMouseOver={(e) => {
          e.currentTarget.style.transform = "translateY(-2px)";
          e.currentTarget.style.boxShadow = "0 6px 16px rgba(16, 185, 129, 0.4)";
        }}
        onMouseOut={(e) => {
          e.currentTarget.style.transform = "translateY(0)";
          e.currentTarget.style.boxShadow = "0 4px 12px rgba(16, 185, 129, 0.3)";
        }}
      >
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
          <polyline points="7 10 12 15 17 10"></polyline>
          <line x1="12" y1="15" x2="12" y2="3"></line>
        </svg>
        Download Audiobook
      </a>
=======
  if (!audioUrl) return <div style={{ color: "#555" }}>No audio yet. Upload your document and generate.</div>;

  return (
    <div style={{ borderRadius: 12, background: "#fffde7", padding: 16, boxShadow: "0 2px 8px rgba(0,0,0,0.05)" }}>
      <audio controls src={audioUrl} style={{ width: "100%" }} />
      <div style={{ marginTop: 10 }}>
        <a href={audioUrl} download style={{ color: "#f57f17", fontWeight: 500 }}>⬇️ Download audio</a>
      </div>
>>>>>>> 7508fd7f3204606fd8e9396d1b9d8870ceb8a5a4
    </div>
  );
}