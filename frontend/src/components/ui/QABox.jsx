import { useState } from "react";

export default function QABox() {
  const [open, setOpen] = useState(false);

  return (
    <div className="fixed bottom-5 right-5 z-50">
      {open ? (
        <div className="w-96 h-[500px] bg-white shadow-xl rounded-lg overflow-hidden border flex flex-col">
          {/* Header */}
          <div className="flex justify-between items-center bg-indigo-600 text-white px-4 py-2">
            <span className="font-semibold">Q&A Assistant</span>
            <button
              onClick={() => setOpen(false)}
              className="hover:text-gray-200 text-lg"
            >
              ✕
            </button>
          </div>

          {/* Chatbot Embed */}
          <div className="flex-grow">
            <iframe
              src="https://your-chatbot-link.com" 
              title="AI Chatbot"
              className="w-full h-full border-0"
              allow="microphone; camera"
            />
          </div>
        </div>
      ) : (
        <button
          className="bg-indigo-600 text-white w-12 h-12 rounded-full shadow-lg text-xl flex items-center justify-center hover:bg-indigo-700 transition"
          onClick={() => setOpen(true)}
        >
          ?
        </button>
      )}
    </div>
  );
}
