
import React from 'react';
import { createRoot } from 'react-dom/client'; // Import createRoot from the client package
import './index.css'; // Standard place for global styles
import App from './App'; // Import your main App component
import reportWebVitals from './reportWebVitals'; // Keep this for performance monitoring

// Get the root DOM node where the React app will be mounted
const container = document.getElementById('root');

// Create a root instance for React 18+ concurrent mode
if (container) {
  const root = createRoot(container);

  // Initial render: The App component is rendered into the root.
  root.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );
} else {
  console.error("The root element with id 'root' was not found in the DOM.");
}


// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();