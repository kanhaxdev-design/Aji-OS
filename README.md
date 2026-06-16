# Aji OS v1.0

**A Premium AI Desktop Assistant Built with Modern Tech Stack**

![Aji OS](https://img.shields.io/badge/Aji%20OS-v1.0-brightgreen)
![Python](https://img.shields.io/badge/Python-3.13-blue)
![React](https://img.shields.io/badge/React-18+-61DAFB?logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?logo=fastapi)

## Overview

Aji OS is a production-quality AI desktop assistant that seamlessly integrates with your workflow. Featuring multiple AI providers, voice capabilities, laptop automation, and a stunning modern UI inspired by ChatGPT Desktop, Cursor AI, Arc Browser, and Nothing OS.

## Tech Stack

### Frontend
- **React 18** - UI library
- **Vite** - Build tool (lightning fast)
- **Tailwind CSS** - Styling
- **Axios** - HTTP client
- **Zustand** - State management

### Backend
- **FastAPI** - High-performance API framework
- **Python 3.13** - Core language
- **Pydantic** - Data validation
- **SQLite** - Conversation storage

### AI & Automation
- **Groq API** - Primary AI provider
- **Google Gemini** - Secondary provider
- **OpenAI GPT** - Alternative provider
- **Ollama** - Offline AI support
- **PyAutoGUI** - Desktop automation
- **psutil** - System monitoring
- **pyttsx3** - Text-to-speech
- **SpeechRecognition** - Voice input

### Future
- **Tauri** - Desktop packaging

## Project Structure

```
Aji-OS/
├── frontend/                 # React + Vite application
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── store/           # Zustand state management
│   │   ├── services/        # API services
│   │   ├── hooks/           # Custom React hooks
│   │   ├── utils/           # Utility functions
│   │   ├── styles/          # Global styles
│   │   ├── App.jsx          # Root component
│   │   └── main.jsx         # Entry point
│   ├── public/              # Static assets
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── index.html
│
├── backend/                 # FastAPI application
│   ├── main.py              # FastAPI app entry point
│   ├── ai.py                # AI orchestration
│   ├── providers.py         # AI provider implementations
│   ├── commands.py          # Command processing
│   ├── voice.py             # Voice processing
│   ├── memory.py            # Conversation memory
│   ├── config.py            # Configuration management
│   ├── database.py          # Database operations
│   ├── plugins/             # Command plugins
│   │   ├── __init__.py
│   │   ├── chrome.py        # Chrome launcher
│   │   ├── vscode.py        # VS Code launcher
│   │   ├── spotify.py       # Spotify launcher
│   │   ├── system.py        # System controls
│   │   ├── media.py         # Volume & brightness
│   │   ├── screenshot.py    # Screenshot tool
│   │   ├── calculator.py    # Calculator plugin
│   │   ├── weather.py       # Weather plugin
│   │   └── browser.py       # Browser automation
│   ├── requirements.txt
│   ├── .env.example
│   └── logging_config.py
│
├── assets/                  # Images and icons
│   └── aji-logo.svg
│
├── data/                    # Data storage
│   ├── conversations.db     # SQLite database
│   └── .gitkeep
│
└── README.md
```

## Features

### 🤖 AI Capabilities
- **Multi-Provider Support**: Switch between Groq, Gemini, OpenAI, and Ollama
- **Streaming Responses**: Real-time text generation
- **Conversation Memory**: Persistent conversation history
- **System Prompts**: Customizable AI behavior
- **Context Awareness**: Maintains conversation state

### 🎤 Voice Features
- **Push-to-Talk**: Voice input on demand
- **Speech Recognition**: Convert voice to text
- **Text-to-Speech**: Hear AI responses
- **Wake Word Support**: Architecture ready for wake word detection

### 🖥️ Laptop Automation
- **App Launchers**: Chrome, VS Code, Spotify, folders
- **System Control**: Shutdown, restart, sleep, lock PC
- **Media Control**: Volume, brightness adjustment
- **Utilities**: Screenshot, battery info, CPU/RAM monitoring
- **Browser Automation**: Google search, tab management
- **Mouse & Keyboard**: Text typing, mouse movement

### 🎨 UI Features
- **Modern Chat Interface**: Responsive and intuitive
- **Glassmorphism Design**: Premium glass-effect styling
- **Dark Theme**: Comfortable for extended use
- **System Status Cards**: CPU, RAM, Battery monitoring
- **Animated Indicators**: Smooth typing animations
- **AI Avatar**: Visual feedback from assistant
- **Settings Panel**: AI provider selection, preferences
- **Conversation History**: Browse and manage past chats

### 🔌 Plugin System
- **Modular Architecture**: Each command is a plugin
- **Auto-Routing**: Intelligent command-to-plugin mapping
- **Easy Extension**: Add new plugins with minimal code
- **Consistent Interface**: All plugins follow same pattern

## Quick Start

### Prerequisites
- Python 3.13+
- Node.js 18+
- npm or yarn

### Installation

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your API keys
```

#### Frontend Setup
```bash
cd frontend
npm install
```

### Running the Application

#### Terminal 1: Start Backend
```bash
cd backend
source venv/bin/activate
python main.py
# Server runs on http://localhost:8000
```

#### Terminal 2: Start Frontend
```bash
cd frontend
npm run dev
# Frontend runs on http://localhost:5173
```

## API Endpoints

### Chat
- `POST /api/chat` - Send message and get AI response
- `GET /api/history` - Get conversation history
- `DELETE /api/history/{id}` - Delete conversation
- `POST /api/clear-history` - Clear all conversations

### Commands
- `POST /api/command` - Execute system command
- `GET /api/plugins` - List available plugins

### System
- `GET /api/stats` - Get system statistics (CPU, RAM, Battery)
- `GET /api/settings` - Get current settings
- `POST /api/settings` - Update settings

### Voice
- `POST /api/voice/recognize` - Convert speech to text
- `POST /api/voice/synthesize` - Convert text to speech

## Configuration

### Environment Variables (.env)
```env
# AI Providers
GROQ_API_KEY=your_groq_key
GEMINI_API_KEY=your_gemini_key
OPENAI_API_KEY=your_openai_key

# Default Provider
DEFAULT_PROVIDER=groq
DEFAULT_MODEL=mixtral-8x7b-32768

# Backend
BACKEND_HOST=localhost
BACKEND_PORT=8000

# Frontend
FRONTEND_URL=http://localhost:5173

# Logging
LOG_LEVEL=INFO
```

## Plugin Development

Create a new plugin in `backend/plugins/`:

```python
# backend/plugins/example.py
from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)

class ExamplePlugin:
    """Example plugin template"""
    
    NAME = "example"
    DESCRIPTION = "Example plugin description"
    TRIGGERS = ["trigger_word", "another_trigger"]
    
    @staticmethod
    async def execute(command: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the plugin command
        
        Args:
            command: The specific command to execute
            args: Additional arguments
            
        Returns:
            Result dictionary with status and data
        """
        try:
            # Implementation here
            return {
                "status": "success",
                "data": "Result here",
                "message": "Success message"
            }
        except Exception as e:
            logger.error(f"Plugin error: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
```

## Performance Optimization

- Async/await throughout backend
- Streaming responses for real-time feedback
- Lazy loading of plugins
- Efficient conversation memory management
- Optimized database queries

## Security

- Environment variables for sensitive data
- CORS configuration
- Input validation with Pydantic
- Rate limiting ready
- Secure API communication

## Future Enhancements

- [ ] Tauri desktop packaging
- [ ] Wake word detection (Hey Aji)
- [ ] Multi-language support
- [ ] Advanced conversation analysis
- [ ] Custom model fine-tuning
- [ ] Plugin marketplace
- [ ] Team collaboration features
- [ ] Advanced automation workflows
- [ ] Mobile companion app

## Troubleshooting

### Backend won't start
- Check Python version: `python --version` (need 3.13+)
- Verify API keys in `.env`
- Check if port 8000 is available
- Review logs: `logs/aji.log`

### Voice not working
- Install audio dependencies: `pip install pyaudio`
- Check microphone permissions
- Verify microphone is connected

### Frontend not connecting
- Ensure backend is running on port 8000
- Check CORS settings
- Clear browser cache and cookies

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

## License

MIT License - feel free to use for personal and commercial projects

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review plugin examples

## Author

**Kanhax Dev** - Senior Software Engineer

---

**Aji OS** - Your intelligent desktop companion 🤖✨
