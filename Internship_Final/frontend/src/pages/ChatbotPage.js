import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

const ChatbotPage = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'assistant',
      content: "Hello! I'm your AI assistant. I can help you with questions about your documents and provide expert insights. How can I assist you today?",
      timestamp: new Date().toISOString()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString()
    };
    setMessages(prev => [...prev, userMessage]);
    const currentMessage = inputMessage;
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: currentMessage }),
      });

      if (!response.ok) throw new Error('Chat request failed');

      const data = await response.json();

      const assistantMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: data.response,
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, assistantMessage]);

    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto' }}>
      <div className="text-center mb-6">
        <h1 className="text-4xl font-bold gradient-text mb-2">AI Assistant</h1>
        <p style={{ color: '#6b7280' }}>
          Expert-level RAG chatbot for document analysis and insights
        </p>
      </div>

      <div className="card chat-container">
        <div className="chat-messages">
          {messages.map((message) => (
            <div key={message.id} className={`message ${message.type}`}>
              <div className={`message-avatar ${message.type}`}>
                {message.type === 'user' ? <User size={16} /> : <Bot size={16} />}
              </div>

              <div className={`message-bubble ${message.type}`}>
                {/* Markdown rendering with newline support */}
                <ReactMarkdown
                  components={{
                    p: ({ children }) => (
                      <p style={{ fontSize: '0.875rem', lineHeight: '1.5', whiteSpace: 'pre-line' }}>
                        {children}
                      </p>
                    )
                  }}
                >
                  {message.content}
                </ReactMarkdown>

                <p style={{
                  fontSize: '0.75rem',
                  marginTop: '0.5rem',
                  opacity: 0.7,
                  textAlign: 'right'
                }}>
                  {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </p>
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="message assistant">
              <div className="message-avatar assistant">
                <Bot size={16} />
              </div>
              <div className="message-bubble assistant">
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <div className="spinner"></div>
                  <span style={{ fontSize: '0.875rem', color: '#6b7280' }}>
                    Assistant is thinking...
                  </span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        <div className="chat-input-area">
          <div className="chat-input-container">
            <textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me anything about your documents..."
              className="chat-input"
              rows="1"
            />
            <button
              onClick={sendMessage}
              disabled={!inputMessage.trim() || isLoading}
              className="btn"
              style={{ background: 'linear-gradient(135deg, #8b5cf6, #3b82f6)', color: 'white', padding: '0.75rem' }}
            >
              <Send size={20} />
            </button>
          </div>
          <p style={{ fontSize: '0.75rem', color: '#6b7280', marginTop: '0.5rem', textAlign: 'center' }}>
            Press Enter to send • Shift + Enter for new line
          </p>
        </div>
      </div>
    </div>
  );
};

export default ChatbotPage;
