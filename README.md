# Hermes Quick Launch for Hermes Agent

A sleek, dark-themed GUI launcher for managing your Hermes Agent ecosystem services.

## Features

- **Auto-Discovery**: Automatically discovers Hermes services from your `~/.local/bin` directory
- **Health Monitoring**: Real-time status monitoring with auto-restart on failure
- **One-Click Launch**: Start all enabled services with a single button
- **Log Management**: Copy errors, save logs, and view service logs in real-time
- **GPU-Aware**: Works with Ollama for local GPU-accelerated embeddings
- **Dark Theme**: Inspired by Nous Research aesthetic

## Default Services

| Service | Port | Category |
|---------|------|----------|
| Hermes Gateway | 8653 | Core |
| Hermes Dashboard | 9119 | Core |
| Hermes Workspace | 3000 | Core |
| Hermes API Server | 8000 | Core |
| Honcho Memory | 8000 | Memory |

## Installation

### Windows

1. Download the latest release from [GitHub Releases](https://github.com/Automata-intelligentsia/hermes-launcher/releases)
2. Extract the ZIP file
3. Double-click `Hermes-Quick-Launch.bat`

### Linux/WSL

```bash
# Clone the repository
git clone https://github.com/Automata-intelligentsia/hermes-launcher.git
cd hermes-launcher

# Run the launcher
python3 hermes_quick_launch.pyw
```

### Via Hermes Agent

```bash
# Hermes can install the launcher for you
hermes tool install hermes-launcher
```

## Auto-Discovery

The launcher can automatically discover services from your Hermes installation:

1. Click the **"Auto-Discover"** button
2. The launcher scans `~/.local/bin` for `hermes-*` scripts
3. Discovered services appear in the "Custom Services" section
4. Enable them with the checkboxes

## Configuration

Configuration is stored in `~/.hermes/launcher-config.json`:

```json
{
  "gateway": {
    "name": "Hermes Gateway",
    "port": 8653,
    "health_url": "http://127.0.0.1:8653/health",
    "script": "~/.local/bin/hermes-gateway",
    "enabled": true,
    "category": "core"
  }
}
```

## Building from Source

### Requirements

- Python 3.8+
- tkinter (usually included with Python)

### Build Windows Executable

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "HermesQuickLaunch" hermes_quick_launch.pyw
```

### Build Linux Package

```bash
# See packaging/ directory for scripts
cd packaging
./build-linux.sh
```

## Development

### Project Structure

```
hermes-launcher/
├── hermes_quick_launch.pyw    # Main application
├── Hermes-Quick-Launch.bat    # Windows launcher
├── README.md                  # This file
├── LICENSE                    # MIT License
└── packaging/                 # Build scripts
    ├── build-windows.ps1
    └── build-linux.sh
```

## License

MIT License - see [LICENSE](LICENSE) file

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## Support

- [Hermes Agent Documentation](https://github.com/Automata-intelligentsia/hermes-agent)
- [Issue Tracker](https://github.com/Automata-intelligentsia/hermes-launcher/issues)

---

Built with ⚡ for the Hermes Agent ecosystem
