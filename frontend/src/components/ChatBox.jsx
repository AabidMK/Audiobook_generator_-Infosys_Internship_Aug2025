// src/components/ChatBox.jsx
import React, { useState } from "react";
import api from "../api";

export default function ChatBox({ initialAnswer }) {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState(() => initialAnswer ? [{role:"assistant", text: initialAnswer}] : []);
  const [loading, setLoading] = useState(false);

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
    } finally {
      setLoading(false);
    }
  }

  return (
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
    </div>
  );
}