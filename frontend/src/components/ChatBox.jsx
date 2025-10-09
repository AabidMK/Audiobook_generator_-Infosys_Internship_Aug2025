// src/components/ChatBox.jsx
<<<<<<< HEAD
import React, { useState, useRef, useEffect } from "react";
=======
import React, { useState } from "react";
>>>>>>> 7508fd7f3204606fd8e9396d1b9d8870ceb8a5a4
import api from "../api";

export default function ChatBox({ initialAnswer }) {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState(() => initialAnswer ? [{role:"assistant", text: initialAnswer}] : []);
  const [loading, setLoading] = useState(false);
<<<<<<< HEAD
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  async function ask(e) {
    e?.preventDefault();
    if (!question.trim()) return;
    setLoading(true);
    const userQuestion = question;
    setQuestion("");
    setMessages((m) => [...m, {role: "user", text: userQuestion}]);
    
    try {
      const resp = await api.post("/rag-query/", new URLSearchParams({ question: userQuestion, collection: "documents" }), {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });
      const { answer, citations } = resp.data;
      setMessages((m) => [...m, {role: "assistant", text: answer}]);
    } catch (err) {
      console.error(err);
      setMessages((m) => [...m, { role: "assistant", text: "Error fetching answer. Please try again." }]);
=======

  async function ask() {
    if (!question) return;
    setLoading(true);
    setMessages((m) => [...m, {role: "user", text: question}]);
    try {
      const resp = await api.post("/rag-query/", new URLSearchParams({ question, collection: "audiobook_chunks" }));
      const { answer, citations } = resp.data;
      setMessages((m) => [...m, {role: "assistant", text: answer}, {role:"meta", text: citations.join("\n")}]);
      setQuestion("");
    } catch (err) {
      console.error(err);
      setMessages((m) => [...m, { role: "assistant", text: "Error fetching answer." }]);
>>>>>>> 7508fd7f3204606fd8e9396d1b9d8870ceb8a5a4
    } finally {
      setLoading(false);
    }
  }

  return (
<<<<<<< HEAD
    <div style={{ display: "flex", flexDirection: "column", height: "500px" }}>
      {/* Messages Area */}
      <div style={{
        flex: 1,
        overflowY: "auto",
        padding: "16px 0",
        display: "flex",
        flexDirection: "column",
        gap: 16,
      }}>
        {messages.length === 0 ? (
          <div style={{
            textAlign: "center",
            padding: 40,
            color: "#94a3b8",
          }}>
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" style={{ margin: "0 auto 16px" }}>
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
            </svg>
            <p style={{ margin: 0, fontSize: 14 }}>
              No questions yet. Start by asking something about your document!
            </p>
          </div>
        ) : (
          messages.map((m, i) => (
            <div key={i} style={{
              display: "flex",
              gap: 12,
              alignItems: "flex-start",
            }}>
              {/* Avatar */}
              <div style={{
                width: 32,
                height: 32,
                borderRadius: 8,
                background: m.role === "user" 
                  ? "linear-gradient(135deg, #667eea 0%, #764ba2 100%)" 
                  : "#f1f5f9",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                flexShrink: 0,
              }}>
                {m.role === "user" ? (
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                  </svg>
                ) : (
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#667eea" strokeWidth="2">
                    <polyline points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polyline>
                  </svg>
                )}
              </div>

              {/* Message Content */}
              <div style={{ flex: 1 }}>
                <div style={{
                  fontSize: 12,
                  fontWeight: 600,
                  color: "#64748b",
                  marginBottom: 6,
                  textTransform: "capitalize",
                }}>
                  {m.role === "user" ? "You" : "AI Assistant"}
                </div>
                <div style={{
                  background: m.role === "user" ? "#f8f9ff" : "#f8fafc",
                  padding: "12px 16px",
                  borderRadius: 12,
                  fontSize: 14,
                  lineHeight: 1.6,
                  color: "#1e293b",
                  whiteSpace: "pre-wrap",
                  border: m.role === "user" ? "1px solid #e0e7ff" : "1px solid #e2e8f0",
                }}>
                  {m.text}
                </div>
              </div>
            </div>
          ))
        )}
        {loading && (
          <div style={{
            display: "flex",
            gap: 12,
            alignItems: "flex-start",
          }}>
            <div style={{
              width: 32,
              height: 32,
              borderRadius: 8,
              background: "#f1f5f9",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#667eea" strokeWidth="2">
                <polyline points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polyline>
              </svg>
            </div>
            <div style={{
              background: "#f8fafc",
              padding: "12px 16px",
              borderRadius: 12,
              border: "1px solid #e2e8f0",
            }}>
              <div style={{ display: "flex", gap: 4 }}>
                <div style={{
                  width: 8,
                  height: 8,
                  borderRadius: "50%",
                  background: "#667eea",
                  animation: "bounce 1.4s infinite ease-in-out both",
                  animationDelay: "-0.32s",
                }}></div>
                <div style={{
                  width: 8,
                  height: 8,
                  borderRadius: "50%",
                  background: "#667eea",
                  animation: "bounce 1.4s infinite ease-in-out both",
                  animationDelay: "-0.16s",
                }}></div>
                <div style={{
                  width: 8,
                  height: 8,
                  borderRadius: "50%",
                  background: "#667eea",
                  animation: "bounce 1.4s infinite ease-in-out both",
                }}></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <form onSubmit={ask} style={{
        display: "flex",
        gap: 8,
        paddingTop: 16,
        borderTop: "1px solid #e2e8f0",
      }}>
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask anything about your document..."
          disabled={loading}
          style={{
            flex: 1,
            padding: "12px 16px",
            borderRadius: 12,
            border: "2px solid #e2e8f0",
            fontSize: 14,
            outline: "none",
            transition: "all 0.3s ease",
          }}
          onFocus={(e) => e.target.style.borderColor = "#667eea"}
          onBlur={(e) => e.target.style.borderColor = "#e2e8f0"}
        />
        <button
          type="submit"
          onClick={ask}
          disabled={loading || !question.trim()}
          style={{
            padding: "12px 20px",
            borderRadius: 12,
            background: (loading || !question.trim()) ? "#e2e8f0" : "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            color: "white",
            border: "none",
            cursor: (loading || !question.trim()) ? "not-allowed" : "pointer",
            fontWeight: 600,
            fontSize: 14,
            transition: "all 0.3s ease",
            display: "flex",
            alignItems: "center",
            gap: 6,
          }}
          onMouseOver={(e) => {
            if (!loading && question.trim()) {
              e.currentTarget.style.transform = "translateY(-1px)";
              e.currentTarget.style.boxShadow = "0 4px 12px rgba(102, 126, 234, 0.4)";
            }
          }}
          onMouseOut={(e) => {
            e.currentTarget.style.transform = "translateY(0)";
            e.currentTarget.style.boxShadow = "none";
          }}
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="22" y1="2" x2="11" y2="13"></line>
            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
          </svg>
          Send
        </button>
      </form>

      <style>{`
        @keyframes bounce {
          0%, 80%, 100% { transform: scale(0); }
          40% { transform: scale(1); }
        }
      `}</style>
=======
    <div style={{ borderRadius: 12, background: "#414141ff", padding: 16, display: "flex", flexDirection: "column", gap: 12 }}>
      <div style={{ minHeight: 200, maxHeight: 360, overflowY: "auto", display: "flex", flexDirection: "column", gap: 8 }}>
        {messages.map((m, i) => (
          <div key={i} style={{
            background: m.role === "user" ? "#646463ff" : (m.role==="assistant" ? "#bbdefb" : "#fff"),
            padding: 10,
            borderRadius: 8
          }}>
            <strong style={{ display:"block", fontSize:12, color:"#333" }}>{m.role}</strong>
            <div style={{ whiteSpace: "pre-wrap", marginTop: 4 }}>{m.text}</div>
          </div>
        ))}
      </div>

      <div style={{ display: "flex", gap: 8 }}>
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a follow-up question..."
          style={{ flex: 1, padding: 8, borderRadius: 6, border: "1px solid #0288d1" }}
        />
        <button onClick={ask} disabled={loading} style={{ padding: "6px 12px", borderRadius: 6, background: "#0288d1", color: "#ffffff", border: "none" }}>
          {loading ? "..." : "Ask"}
        </button>
      </div>
>>>>>>> 7508fd7f3204606fd8e9396d1b9d8870ceb8a5a4
    </div>
  );
}