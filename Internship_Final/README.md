# AI Audiobook Generator UI

A production-grade frontend interface for AI audiobook generation and RAG chatbot functionality.

## Features

### 🎧 Audiobook Generator UI
- File upload interface with drag-and-drop
- Processing simulation with loading states
- Results display with text preview
- Download functionality (demo mode)

### 🤖 AI Assistant Chat Interface
- Premium chat UI with smooth animations
- Real-time message display
- Mock AI responses for demonstration
- Modern gradient design

## Tech Stack

- **React 18** - Modern UI framework
- **Custom CSS** - Optimized styling without external dependencies
- **Lucide React** - Beautiful icons
- **React Router** - Navigation

## Quick Start

1. **Install dependencies:**
```bash
cd frontend
npm install
```

2. **Start the development server:**
```bash
npm start
```

3. **Open your browser:**
Navigate to http://localhost:3000

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   └── Navigation.js      # Navigation bar
│   ├── pages/
│   │   ├── AudiobookPage.js   # File upload & processing UI
│   │   └── ChatbotPage.js     # Chat interface
│   ├── App.js                 # Main application
│   └── index.css              # Custom styles
└── package.json
```

## Features

### Audiobook Generator
- **File Upload**: Supports PDF, DOCX, PPTX, and image files
- **Processing Simulation**: Shows realistic upload and processing states
- **Results Display**: Preview of generated audiobook text
- **Download Ready**: Interface prepared for actual file downloads

### AI Chat Assistant
- **Interactive Chat**: Real-time message interface
- **Mock Responses**: Demonstrates chat functionality
- **Professional UI**: Premium design with gradients and animations
- **Responsive**: Works on all screen sizes

## Usage

1. **Audiobook Generation:**
   - Click "Audiobook Generator" in navigation
   - Upload a document file
   - Watch the processing simulation
   - View the generated text preview

2. **AI Assistant:**
   - Click "AI Assistant" in navigation
   - Type messages in the chat input
   - Receive mock AI responses
   - Experience the full chat interface

## Development Notes

- **No Backend Required**: Fully functional UI with mock data
- **Production Ready**: Clean, maintainable code structure
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern UI**: Premium gradients, animations, and interactions
- **Easy Integration**: Ready to connect with actual backend APIs

## Future Integration

The UI is structured to easily integrate with:
- Document processing APIs
- AI/LLM services for chat responses
- File storage and download systems
- Authentication and user management

Simply replace the mock functions with actual API calls when backend services are available.