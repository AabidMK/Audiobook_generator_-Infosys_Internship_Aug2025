import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navigation from './components/Navigation';
import AudiobookPage from './pages/AudiobookPage';
import ChatbotPage from './pages/ChatbotPage';

function App() {
  return (
    <Router>
      <div style={{ minHeight: '100vh' }}>
        <Navigation />
        <main className="container page-container">
          <Routes>
            <Route path="/" element={<AudiobookPage />} />
            <Route path="/chat" element={<ChatbotPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;