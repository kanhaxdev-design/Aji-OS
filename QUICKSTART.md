# Aji OS v1.0 - Quick Start

## 🚀 Quick Setup (5 minutes)

### Prerequisites
- Python 3.13+
- Node.js 18+
- Git

### Installation

```bash
# Clone repository
git clone https://github.com/kanhaxdev-design/Aji-OS.git
cd Aji-OS

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys

# Frontend setup
cd ../frontend
npm install
```

### Running

**Terminal 1 (Backend):**
```bash
cd backend
source venv/bin/activate
python main.py
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

Open `http://localhost:5173` in your browser!

## 📝 Configuration

### Add API Keys

Edit `backend/.env`:

```env
GROQ_API_KEY=your_groq_key
GEMINI_API_KEY=your_gemini_key  
OPENAI_API_KEY=your_openai_key
DEFAULT_PROVIDER=groq
```

Get free API keys:
- **Groq**: https://console.groq.com
- **Gemini**: https://ai.google.dev
- **OpenAI**: https://platform.openai.com

## 💻 Desktop Application

### Build Desktop App (with Tauri)

```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Development
cd src-tauri
cargo tauri dev

# Production build
cargo tauri build
```

Generated installers in `src-tauri/target/release/bundle/`

## 🎯 Key Features

✅ **Multi-AI Support**: Groq, Gemini, OpenAI, Ollama
✅ **Voice**: Speech-to-text & text-to-speech
✅ **Automation**: Launch apps, control system
✅ **Plugins**: Extensible command system
✅ **Desktop App**: Native packaging with Tauri
✅ **Offline**: Works with Ollama

## 📚 Documentation

- [Full Setup Guide](./SETUP.md)
- [Desktop App Guide](./DESKTOP.md)
- [Contributing Guide](./CONTRIBUTING.md)
- [Main README](./README.md)

## 🤖 Example Commands

```
"What's the weather?"
"Open Chrome and search for Python tutorial"
"Take a screenshot"
"What's 15 * 23?"
"Open VS Code in /home/user/projects"
"Set volume to 50%"
"Lock the PC"
```

## 🔧 Troubleshooting

**Backend won't start?**
```bash
python --version  # Must be 3.13+
pip install -r requirements.txt --upgrade
```

**Frontend not loading?**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**API key error?**
- Check `.env` file exists
- Verify key format
- Ensure key has proper permissions

## 📞 Support

- 🐛 Report issues: GitHub Issues
- 💬 Discuss: GitHub Discussions
- 📖 Learn: Check documentation

## 📄 License

MIT License - Free to use and modify

---

**Ready to build something amazing? Start contributing!** ✨
