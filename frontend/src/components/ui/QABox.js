import React, { useState } from "react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

function QABox() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [citations, setCitations] = useState([]);

  const askQuestion = async () => {
    if (!question.trim()) return;
    try {
      const response = await fetch(`${BACKEND_URL}/api/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      if (response.ok) {
        const data = await response.json();
        setAnswer(data.answer);
        setCitations(data.citations || []);
      } else {
        setAnswer("Error fetching answer");
      }
    } catch (err) {
      console.error(err);
      setAnswer("Error connecting to backend");
    }
  };

  return (
    <div className="fixed bottom-4 right-4 w-96 bg-white shadow-lg rounded-lg p-4">
      <h3 className="text-lg font-semibold">Q&A Assistant</h3>
      <input
        type="text"
        placeholder="Ask about your document..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        className="w-full border rounded px-3 py-2 mb-2"
      />
      <button onClick={askQuestion} className="bg-indigo-600 text-white px-4 py-2 rounded">
        Ask
      </button>
      {answer && (
        <div className="mt-3">
          <p><strong>Answer:</strong> {answer}</p>
          {citations.length > 0 && (
            <ul className="mt-2 text-sm text-gray-600 list-disc pl-5">
              {citations.map((c, i) => (
                <li key={i}>
                  {c.source_file} — chunk {c.chunk_index}  
                  <br />
                  <em>"{c.text_preview}"</em>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}

export default QABox;
