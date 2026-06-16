# Aji OS - Desktop Application Guide

## Building the Desktop App

Aji OS can be packaged as a native desktop application using Tauri for Windows, macOS, and Linux.

### Prerequisites

1. **Rust & Cargo**
   ```bash
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   source $HOME/.cargo/env
   ```

2. **System Dependencies**
   
   **Ubuntu/Debian:**
   ```bash
   sudo apt-get install libgtk-3-dev libwebkit2gtk-4.0-dev libappindicator3-dev
   ```
   
   **Fedora:**
   ```bash
   sudo dnf install gtk3-devel webkit2gtk3-devel libappindicator-devel
   ```
   
   **macOS:**
   ```bash
   xcode-select --install
   ```
   
   **Windows:**
   - Install Visual Studio Build Tools
   - Install WebView2 Runtime

### Development Mode

```bash
# Terminal 1: Start backend
cd backend
source venv/bin/activate
python main.py

# Terminal 2: Run desktop app
cd src-tauri
cargo tauri dev
```

This launches the app with:
- Hot reload enabled
- DevTools available (Ctrl+Shift+I)
- Connected to backend on localhost:8000

### Production Build

```bash
cd src-tauri
cargo tauri build
```

Generated installers:
- **Windows**: `src-tauri/target/release/bundle/msi/` (MSI installer)
- **macOS**: `src-tauri/target/release/bundle/dmg/` (DMG installer)
- **Linux**: `src-tauri/target/release/bundle/deb/` (DEB package)

### Customization

**App Configuration** (`src-tauri/tauri.conf.json`):
```json
{
  "app": {
    "windows": [{
      "title": "Aji OS",
      "width": 1200,
      "height": 800,
      "minWidth": 900,
      "minHeight": 600
    }]
  },
  "bundle": {
    "icon": ["path/to/icon.png"]
  }
}
```

**Icons** (Required for bundling):
- `assets/icon.png` - 512x512
- `assets/icon.ico` - Windows icon

### Distribution

1. **Windows**: Distribute `.msi` or `.nsis` installer
2. **macOS**: Distribute `.dmg` or submit to App Store
3. **Linux**: Distribute `.deb` or via package managers

### Signing (macOS)

For distribution on macOS:
```bash
export APPLE_CERTIFICATE="path/to/cert.pfx"
export APPLE_CERTIFICATE_PASSWORD="password"
export APPLE_SIGNING_IDENTITY="Your Name"

cargo tauri build
```

## Desktop Features

✅ Native window management
✅ System tray integration (ready)
✅ Keyboard shortcuts
✅ File access via plugins
✅ Offline support with Ollama

## Troubleshooting

### Build fails on Linux
```bash
sudo apt-get install build-essential
```

### "Cannot find WebView2"
- Windows only issue
- Install: https://developer.microsoft.com/microsoft-edge/webview2/

### Large bundle size
- Release build is ~100-150MB
- Normal for embedded Chromium
- First run extracts and initializes WebView
