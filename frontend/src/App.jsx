// src/App.jsx
import React, { useState } from "react";
import UploadForm from "./components/UploadForm";
import AudioPlayer from "./components/AudioPlayer";
import ChatBox from "./components/ChatBox";

export default function App() {
  const [audioUrl, setAudioUrl] = useState(null);
  const [initialAnswer, setInitialAnswer] = useState(null);
  const [processing, setProcessing] = useState(false);

  return (
    <div style={{
      minHeight: "100vh",
      background: "linear-gradient(135deg, #f5f7fa 0%, #e8eef5 100%)",
      fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
      padding: "40px 20px",
    }}>
      {/* Header */}
      <div style={{
        maxWidth: 1200,
        margin: "0 auto 40px",
        textAlign: "center",
      }}>
        <div style={{
          display: "inline-flex",
          alignItems: "center",
          gap: 16,
          marginBottom: 16,
        }}>
          <div style={{
            width: 64,
            height: 64,
            background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            borderRadius: 16,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            boxShadow: "0 8px 24px rgba(102, 126, 234, 0.4)",
          }}>
            <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
              <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
              <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
            </svg>
          </div>
          <h1 style={{
            fontSize: 42,
            fontWeight: 700,
            background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent",
            margin: 0,
          }}>
            AudioBook Generator
          </h1>
          <span style={{ fontSize: 24 }}>✨</span>
        </div>
        <p style={{
          fontSize: 16,
          color: "#64748b",
          maxWidth: 600,
          margin: "0 auto 12px",
          lineHeight: 1.6,
        }}>
          Transform your documents into captivating audiobooks with AI-powered text enhancement and natural text-to-speech technology
        </p>
        <div style={{
          display: "inline-flex",
          alignItems: "center",
          gap: 8,
          padding: "8px 16px",
          background: "white",
          borderRadius: 20,
          fontSize: 13,
          color: "#667eea",
          fontWeight: 500,
          boxShadow: "0 2px 8px rgba(0,0,0,0.06)",
        }}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polyline>
          </svg>
          Powered by Advanced AI
        </div>
      </div>

      {/* Main Content */}
      <div style={{ maxWidth: 1200, margin: "0 auto" }}>
        {/* Upload Form */}
        <UploadForm
          onAudio={(url) => setAudioUrl(url)}
          onAnswer={(ans) => setInitialAnswer(ans)}
          onProcessing={(state) => setProcessing(state)}
        />

        {/* Audio Player and Chat - Only show when audio is generated */}
        {audioUrl && (
          <div style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(500px, 1fr))",
            gap: 24,
            marginTop: 32,
          }}>
            {/* Audio Player Section */}
            <div style={{
              background: "white",
              borderRadius: 20,
              padding: 32,
              boxShadow: "0 4px 24px rgba(0,0,0,0.08)",
            }}>
              <div style={{
                display: "flex",
                alignItems: "center",
                gap: 12,
                marginBottom: 24,
              }}>
                <div style={{
                  width: 40,
                  height: 40,
                  background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                  borderRadius: 10,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}>
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
                    <path d="M9 18V5l12-2v13"></path>
                    <circle cx="6" cy="18" r="3"></circle>
                    <circle cx="18" cy="16" r="3"></circle>
                  </svg>
                </div>
                <h2 style={{
                  fontSize: 20,
                  fontWeight: 600,
                  color: "#1e293b",
                  margin: 0,
                }}>
                  Your Audiobook
                </h2>
              </div>
              <AudioPlayer audioUrl={audioUrl} />
            </div>

            {/* Chat Section */}
            <div style={{
              background: "white",
              borderRadius: 20,
              padding: 32,
              boxShadow: "0 4px 24px rgba(0,0,0,0.08)",
            }}>
              <div style={{
                display: "flex",
                alignItems: "center",
                gap: 12,
                marginBottom: 24,
              }}>
                <div style={{
                  width: 40,
                  height: 40,
                  background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                  borderRadius: 10,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}>
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                  </svg>
                </div>
                <div>
                  <h2 style={{
                    fontSize: 20,
                    fontWeight: 600,
                    color: "#1e293b",
                    margin: 0,
                  }}>
                    Ask Questions About Your Document
                  </h2>
                  <p style={{
                    fontSize: 13,
                    color: "#94a3b8",
                    margin: "4px 0 0 0",
                  }}>
                    Get instant answers powered by AI
                  </p>
                </div>
              </div>
              <ChatBox initialAnswer={initialAnswer} />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
