# Aji OS v1.0 - Complete Project Structure

## 📁 Directory Structure

```
Aji-OS/
├── frontend/                      # React + Vite frontend app
│   ├── src/
│   │   ├── components/            # React components
│   │   │   ├── ChatInterface.jsx  # Main chat UI
│   │   │   ├── Sidebar.jsx        # Conversation sidebar
│   │   │   ├── SettingsPanel.jsx  # Settings UI
│   │   │   ├── MessageBubble.jsx  # Chat message
│   │   │   ├── TypingIndicator.jsx
│   │   │   └── SystemStats.jsx    # System stats display
│   │   ├── pages/                 # Page components
│   │   ├── store/
│   │   │   └── appStore.js        # Zustand state management
│   │   ├── services/
│   │   │   └── api.js             # API client
│   │   ├── styles/
│   │   │   └── index.css          # Global styles
│   │   ├── App.jsx                # Root component
│   │   └── main.jsx               # Entry point
│   ├── public/                    # Static assets
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── postcss.config.js
│
├── backend/                       # FastAPI backend server
│   ├── main.py                    # FastAPI app entry
│   ├── ai.py                      # AI orchestration
│   ├── providers.py               # AI provider implementations
│   ├── commands.py                # Command routing system
│   ├── voice.py                   # Voice processing
│   ├── memory.py                  # Conversation memory
│   ├── config.py                  # Configuration management
│   ├── database.py                # Database operations
│   ├── plugins/                   # Command plugins
│   │   ├── __init__.py
│   │   ├── system.py              # System control (shutdown, restart, etc.)
│   │   ├── chrome.py              # Chrome launcher
│   │   ├── vscode.py              # VS Code launcher
│   │   ├── spotify.py             # Spotify launcher
│   │   ├── media.py               # Volume & brightness control
│   │   ├── screenshot.py          # Screenshot capture
│   │   ├── calculator.py          # Calculator
│   │   ├── weather.py             # Weather information
│   │   └── browser.py             # Browser automation
│   ├── requirements.txt           # Python dependencies
│   ├── .env.example               # Environment template
│   └── logging_config.py          # Logging setup
│
├── src-tauri/                     # Tauri desktop app configuration
│   ├── tauri.conf.json           # Tauri app config
│   ├── Cargo.toml                # Rust dependencies
│   ├── Cargo.lock
│   ├── src/
│   │   ├── main.rs               # Rust entry point
│   │   ├── lib.rs
│   │   └── build.rs              # Build script
│   └── icons/                    # App icons
│
├── assets/                        # Project assets
│   ├── aji-logo.svg
│   ├── icon.png                  # App icon (512x512)
│   └── icon.ico                  # Windows icon
│
├── data/                          # Data storage
│   ├── conversations.db          # SQLite database
│   ├── screenshots/              # Captured screenshots
│   └── tts_output.mp3            # Text-to-speech files
│
├── logs/                          # Application logs
│   └── aji.log
│
├── README.md                      # Main documentation
├── SETUP.md                       # Setup guide
├── DESKTOP.md                     # Desktop app guide
├── QUICKSTART.md                  # Quick start guide
├── CONTRIBUTING.md                # Contributing guide
└── .gitignore                     # Git ignore rules
```

## 🏗️ Architecture

### Frontend (React)
- **UI Framework**: React 18 + Vite
- **Styling**: Tailwind CSS + custom glass morphism
- **State**: Zustand for global state
- **API**: Axios for HTTP requests
- **Real-time**: WebSocket support for streaming

### Backend (FastAPI)
- **Framework**: FastAPI with async support
- **Database**: SQLite with custom ORM
- **AI**: Multi-provider support (Groq, Gemini, OpenAI, Ollama)
- **Plugins**: Dynamic plugin system for commands
- **Voice**: Speech recognition & text-to-speech
- **Automation**: PyAutoGUI for system control

### Desktop (Tauri)
- **Framework**: Tauri for cross-platform packaging
- **Rust**: System-level integrations
- **Packaging**: Automated builds for Windows, macOS, Linux

## 🔌 Plugin System

Each plugin implements the standard interface:

```python
class PluginName:
    NAME = "plugin_name"
    DESCRIPTION = "Plugin description"
    TRIGGERS = ["trigger1", "trigger2"]
    
    @staticmethod
    async def execute(command: str, args: dict) -> dict:
        return {"status": "success", "data": ...}
```

Plugins automatically:
- Load on startup
- Register commands
- Route commands based on triggers
- Handle errors gracefully

## 🌐 API Structure

### Chat Endpoints
- `POST /api/chat` - Stream response
- `POST /api/chat-sync` - Complete response
- `GET /api/conversations` - History
- `WebSocket /ws/chat` - Real-time chat

### Command Endpoints
- `POST /api/command` - Execute command
- `GET /api/commands` - List commands
- `GET /api/plugin/{name}` - Plugin info

### Voice Endpoints
- `POST /api/voice/recognize` - Speech to text
- `POST /api/voice/synthesize` - Text to speech

### System Endpoints
- `GET /stats` - System statistics
- `GET /api/settings` - Get settings
- `POST /api/settings` - Update settings
- `GET /api/providers` - List AI providers
- `POST /api/provider` - Switch provider

## 🎯 Component Breakdown

### Frontend Components
- **ChatInterface**: Main chat area
- **Sidebar**: Conversation history & new chat
- **MessageBubble**: Individual message display
- **TypingIndicator**: AI thinking animation
- **SystemStats**: CPU, Memory, Battery display
- **SettingsPanel**: Configuration UI

### Backend Modules
- **main.py**: FastAPI server setup
- **ai.py**: AI orchestration & provider management
- **providers.py**: AI provider implementations
- **commands.py**: Command routing system
- **voice.py**: Speech recognition & synthesis
- **memory.py**: Conversation context management
- **database.py**: SQLite operations
- **config.py**: Environment & settings management

### Plugins
- **system.py**: OS-level control
- **chrome.py**: Browser launcher
- **vscode.py**: Code editor launcher
- **spotify.py**: Music player launcher
- **media.py**: Volume & brightness
- **screenshot.py**: Screen capture
- **calculator.py**: Math operations
- **weather.py**: Weather information
- **browser.py**: Web search & navigation

## 📊 Data Flow

```
User Input → Frontend → API → Backend AI/Plugins → Response → Frontend → Display
    ↓
    Store (Zustand)
    ↓
    Database (SQLite)
```

## 🔐 Security

- Environment variables for API keys
- CORS configuration
- Input validation with Pydantic
- Error handling & logging
- No sensitive data in logs

## 🚀 Deployment

### Development
- Run backend on `localhost:8000`
- Run frontend on `localhost:5173`
- Hot reload enabled

### Production
- Build frontend: `npm run build`
- Run backend with production settings
- Deploy as static site or Docker container

### Desktop
- Build with Tauri: `cargo tauri build`
- Distributable installers for all platforms

## 📈 Performance

- Async/await throughout backend
- Streaming responses for real-time feedback
- Lazy loading of components
- Optimized database queries
- Efficient memory management

## 🎨 UI/UX Features

- Modern glassmorphism design
- Smooth animations & transitions
- Responsive layout
- Dark theme optimized
- Accessible components
- Real-time typing indicators
- Conversation history
- Copy-to-clipboard functionality

## 🛠️ Development Tools

- **Backend**: Python, FastAPI, Pydantic
- **Frontend**: React, Vite, Tailwind CSS
- **Desktop**: Tauri, Rust
- **Database**: SQLite
- **Version Control**: Git
- **Testing**: pytest, Jest (ready)
- **Linting**: ESLint, flake8
- **Formatting**: Black, Prettier

## 📚 Technologies

### Languages
- Python 3.13
- JavaScript/React 18
- Rust (Tauri)
- HTML/CSS

### Frameworks
- FastAPI
- React
- Tauri
- Tailwind CSS

### Libraries
- Groq SDK
- Google Generative AI
- OpenAI SDK
- PyAutoGUI
- pyttsx3
- SpeechRecognition
- Axios
- Zustand

## 🎓 Learning Path

1. Start with **QUICKSTART.md**
2. Read **SETUP.md** for detailed setup
3. Explore **components** folder
4. Review **plugins** folder
5. Check **API documentation** in main README
6. Contribute following **CONTRIBUTING.md**

---

**Aji OS - Making AI accessible to everyone** 🤖✨
