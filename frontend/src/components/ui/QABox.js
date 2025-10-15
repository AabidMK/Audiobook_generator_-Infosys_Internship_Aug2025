import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Card, CardHeader, CardContent, CardTitle } from "./card";
import { Button } from "./button";
import { Loader2, Send, MessageCircleQuestion, Quote } from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "http://localhost:3001";

export default function QABox() {
  const [isOpen, setIsOpen] = useState(false);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [citations, setCitations] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!question.trim()) return alert("Please type a question.");

    setLoading(true);
    setAnswer("");
    setCitations([]);

    try {
      const res = await fetch(`${BACKEND_URL}/api/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      const data = await res.json();

      if (data.answer) {
        setAnswer(data.answer);
        setCitations(data.citations || []);
      } else {
        setAnswer("No answer found or backend error occurred.");
      }
    } catch (err) {
      console.error("Error fetching answer:", err);
      setAnswer("Error connecting to backend. Check if it's running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {/* Floating ? Button */}
      <motion.button
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.95 }}
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-6 right-6 bg-indigo-600 hover:bg-indigo-700 text-white rounded-full w-14 h-14 flex items-center justify-center shadow-xl transition z-50"
      >
        <MessageCircleQuestion className="w-6 h-6" />
      </motion.button>

      {/* Q&A Popup with Animation */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 40 }}
            transition={{ duration: 0.25, ease: "easeOut" }}
            className="fixed bottom-24 right-6 w-96 max-w-[90vw] z-50"
          >
            <Card className="border-0 shadow-2xl bg-white/90 backdrop-blur-md rounded-2xl">
              <CardHeader className="pb-2 border-b border-gray-200 flex justify-between items-center">
                <CardTitle className="text-lg font-semibold text-indigo-700 flex items-center gap-2">
                  <MessageCircleQuestion className="w-5 h-5" />
                  Ask a Question (AI Q&A)
                </CardTitle>
                <button
                  onClick={() => setIsOpen(false)}
                  className="text-gray-500 hover:text-gray-700 transition"
                >
                  ✕
                </button>
              </CardHeader>

              <CardContent className="p-4">
                <div className="flex items-center gap-2 mb-4">
                  <input
                    type="text"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Ask about your document..."
                    className="flex-1 p-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-400 outline-none text-sm"
                  />
                  <Button
                    onClick={handleAsk}
                    disabled={loading}
                    className="bg-indigo-600 hover:bg-indigo-700 text-white flex items-center gap-1 px-3 py-2 rounded-lg"
                  >
                    {loading ? (
                      <Loader2 className="animate-spin w-4 h-4" />
                    ) : (
                      <Send className="w-4 h-4" />
                    )}
                    Ask
                  </Button>
                </div>

                {loading && (
                  <p className="text-gray-500 italic text-center text-sm">
                    Thinking... analyzing your document...
                  </p>
                )}

                {answer && !loading && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 0.3 }}
                    className="mt-3 p-3 rounded-lg bg-gradient-to-br from-indigo-50 to-purple-50 border border-indigo-100 shadow-sm text-sm"
                  >
                    <div className="flex items-start gap-2 mb-1">
                      <Quote className="w-4 h-4 text-indigo-500 mt-1" />
                      <p className="text-gray-800 whitespace-pre-line leading-relaxed">{answer}</p>
                    </div>

                    {citations.length > 0 && (
                      <div className="mt-2 border-t border-indigo-100 pt-1">
                        <h3 className="text-xs font-semibold text-indigo-700 mb-1">Sources:</h3>
                        <ul className="text-xs text-gray-600 space-y-1">
                          {citations.map((c, i) => (
                            <li key={i}>
                              📄 <b>{c.source_file || "Unknown file"}</b> — Chunk {c.chunk_index} (
                              <span className="text-green-700 font-medium">
                                {c.relevance_score || "N/A"}
                              </span>
                              )
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </motion.div>
                )}
              </CardContent>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
