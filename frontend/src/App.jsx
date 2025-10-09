// src/App.jsx
import React, { useState } from "react";
import UploadForm from "./components/UploadForm";
import AudioPlayer from "./components/AudioPlayer";
import ChatBox from "./components/ChatBox";

export default function App() {
  const [audioUrl, setAudioUrl] = useState(null);
  const [initialAnswer, setInitialAnswer] = useState(null);

  return (
    <div style={{
      maxWidth: 1000,
      margin: "40px auto",
      fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif",
      background: "#000000",
      padding: 24,
      borderRadius: 16,
      boxShadow: "0 8px 20px rgba(0,0,0,0.1)"
    }}>
      <h1 style={{ textAlign: "center", marginBottom: 32, color: "#ffffff" }}>
        📚 AI Audiobook Generator
      </h1>

      <div style={{ marginBottom: 32 }}>
        <UploadForm
          onAudio={(url) => setAudioUrl(url)}
          onAnswer={(ans) => setInitialAnswer(ans)}
        />
      </div>

      <div style={{ display: "flex", gap: 24, flexWrap: "wrap" }}>
        <div style={{ flex: 1, minWidth: 400, background: "#202020", padding: 16, borderRadius: 12, boxShadow: "0 4px 12px rgba(0,0,0,0.05)" }}>
          <h2 style={{ marginBottom: 16, color: "#ffffff" }}>🎧 Audiobook</h2>
          <AudioPlayer audioUrl={audioUrl} />
        </div>

        <div style={{ flex: 1, minWidth: 400, background: "#202020", padding: 16, borderRadius: 12, boxShadow: "0 4px 12px rgba(0,0,0,0.05)" }}>
          <h2 style={{ marginBottom: 16, color: "#ffffff" }}>💬 Chat (RAG)</h2>
          <ChatBox initialAnswer={initialAnswer} />
        </div>
      </div>
    </div>
  );
}
