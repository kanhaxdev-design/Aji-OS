# Aji OS - Setup & Development Guide

## Prerequisites

### System Requirements
- **Python**: 3.13+
- **Node.js**: 18+
- **npm**: 9+
- **Rust**: 1.57+ (for Tauri desktop builds)

### For Desktop Builds (Tauri)

**Windows:**
- Windows 10+
- Visual Studio Build Tools or Visual Studio Community
- WebView2 Runtime

**macOS:**
- macOS 10.13+
- Xcode Command Line Tools: `xcode-select --install`

**Linux:**
- GTK 3.0 development files
- Ubuntu/Debian: `sudo apt-get install libgtk-3-dev libwebkit2gtk-4.0-dev libappindicator3-dev`
- Fedora: `sudo dnf install gtk3-devel webkit2gtk3-devel libappindicator-devel`

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/Aji-OS.git
cd Aji-OS
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

### 3. Frontend Setup (Web Version)

```bash
cd frontend

# Install dependencies
npm install
```

### 4. Desktop App Setup (Optional - Tauri)

```bash
# Install Rust (if not already installed)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install Tauri CLI
npm install -g @tauri-apps/cli

# Navigate to project root
cd Aji-OS

# Install desktop dependencies
cd src-tauri
cargo build
cd ..
```

## Running the Application

### Option 1: Web Version (Development)

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python main.py
# Server running on http://localhost:8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
# App running on http://localhost:5173
```

### Option 2: Desktop Version (Tauri)

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python main.py
```

**Terminal 2 - Desktop App:**
```bash
# From project root
cd src-tauri
cargo tauri dev
```

This will:
- Build the frontend
- Start the Tauri app
- Enable hot-reload during development

## Building for Production

### Web Version

```bash
cd frontend
npm run build

# Output in frontend/dist/
```

Deploy the contents of `frontend/dist/` to your web server.

### Desktop Application

**Windows (.msi, .nsis):**
```bash
cd src-tauri
cargo tauri build

# Output in src-tauri/target/release/bundle/msi/
```

**macOS (.dmg):**
```bash
cd src-tauri
cargo tauri build

# Output in src-tauri/target/release/bundle/dmg/
```

**Linux (.deb):**
```bash
cd src-tauri
cargo tauri build

# Output in src-tauri/target/release/bundle/deb/
```

## Configuration

### Backend Environment Variables (.env)

```env
# AI Providers
GROQ_API_KEY=your_key
GEMINI_API_KEY=your_key
OPENAI_API_KEY=your_key

# Server
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:5173

# Features
ENABLE_VOICE=true
ENABLE_PLUGINS=true
ENABLE_HISTORY=true
```

### Frontend Configuration

Edit `frontend/src/services/api.js`:
- Change `API_BASE_URL` to your backend URL
- Update CORS settings if needed

### Desktop App (Tauri)

Edit `src-tauri/tauri.conf.json`:
- Window size and properties
- Bundle settings
- Icon paths
- Permissions

## API Endpoints

### Chat
- `POST /api/chat` - Stream chat response
- `POST /api/chat-sync` - Get complete response
- `GET /api/conversations` - Get history
- `DELETE /api/conversation/{id}` - Delete conversation

### Commands
- `POST /api/command` - Execute command
- `GET /api/commands` - List commands

### Voice
- `POST /api/voice/recognize` - Speech to text
- `POST /api/voice/synthesize` - Text to speech

### System
- `GET /stats` - System statistics
- `GET /api/settings` - Get settings
- `POST /api/settings` - Update settings
- `GET /api/providers` - List AI providers
- `POST /api/provider` - Switch provider

## Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Change port in .env
BACKEND_PORT=8001
```

**Python version mismatch:**
```bash
python --version  # Must be 3.13+
```

**Missing dependencies:**
```bash
pip install -r requirements.txt --upgrade
```

### Frontend Issues

**Node modules not found:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Port 5173 already in use:**
```bash
# Edit frontend/vite.config.js and change port
```

### Desktop App Issues

**Rust/Cargo not found:**
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

**WebView2 not found (Windows):**
- Download from: https://developer.microsoft.com/en-us/microsoft-edge/webview2/

**Build fails on macOS:**
```bash
xcode-select --install
```

## Development Workflow

### Adding a New Plugin

1. Create file in `backend/plugins/myplugin.py`:
```python
class MyPlugin:
    NAME = "myplugin"
    DESCRIPTION = "My plugin description"
    TRIGGERS = ["command"]
    
    @staticmethod
    async def execute(command: str, args: dict):
        return {
            "status": "success",
            "message": "Done"
        }
```

2. Plugin auto-loads on backend restart

### Adding a New Component (React)

1. Create in `frontend/src/components/MyComponent.jsx`
2. Import and use in other components
3. HMR will auto-refresh

### Debugging

**Backend logs:**
```bash
tail -f logs/aji.log
```

**Frontend console:**
- Open DevTools: F12
- Check Network tab for API calls

**Desktop app devtools:**
- Right-click → Inspect Element
- Uses Chromium inspector

## Performance Optimization

1. **Frontend:**
   - Run `npm run build` for production bundle
   - Use Chrome DevTools to analyze

2. **Backend:**
   - Monitor logs for slow requests
   - Use `psutil` stats to check resources

3. **Desktop:**
   - Build with `--release` flag
   - Smaller bundle size

## Security Best Practices

1. **API Keys:**
   - Never commit `.env` files
   - Use environment variables
   - Rotate keys regularly

2. **CORS:**
   - Configure allowed origins
   - Restrict to your frontend domain

3. **Desktop App:**
   - Review Tauri allowlist settings
   - Only enable necessary permissions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## Support

- **Issues**: Open on GitHub
- **Discussions**: GitHub Discussions
- **Documentation**: Check README.md

## License

MIT License - See LICENSE file

## Changelog

### v1.0.0 (Initial Release)
- Multi-provider AI support (Groq, Gemini, OpenAI, Ollama)
- Voice input/output
- System automation plugins
- Desktop app with Tauri
- Conversation history
- Settings management
