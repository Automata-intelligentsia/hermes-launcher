# Quick Launch for Hermes Agent

A sleek, dark-themed GUI launcher for managing your Hermes Agent ecosystem services.

## Features

- **Auto-Discovery**: Automatically discovers Hermes services from your `~/.local/bin` directory
- **Health Monitoring**: Real-time status monitoring with auto-restart on failure
- **One-Click Launch**: Start all enabled services with a single button
- **Log Management**: Copy errors, save logs, and view service logs in real-time
- **GPU-Aware**: Works with Ollama for local GPU-accelerated embeddings
- **Dark Theme**: Inspired by Nous Research aesthetic

## Default Services

### Core Services
| Service | Port | Status |
|---------|------|--------|
| Hermes Gateway | 8653 | Enabled |
| Hermes Dashboard | 9119 | Enabled |
| Hermes Workspace | 3000 | Enabled |
| Honcho Memory | 8000 | Enabled |

### AI Agents (Pre-loaded, disabled by default)
| Agent | Role |
|-------|------|
| CEO | Chief Executive Officer |
| CTO | Chief Technology Officer |
| CFO | Chief Financial Officer |
| COO | Chief Operating Officer |
| CIO | Chief Information Officer |
| CMO | Chief Marketing Officer |
| Head of AI Innovation | AI Strategy |
| Head of BizDev | Business Development |
| Lead Developer | Development Lead |
| Frontend Developer | UI/UX Development |
| Data Engineer | Data Infrastructure |
| QA Engineer | Quality Assurance |
| UX Designer | User Experience |
| Graphic Designer | Visual Design |
| Content Strategist | Content Strategy |
| Social Media Manager | Social Media |
| Cold Outreach | Sales Outreach |
| Customer Service | Support |
| Project Manager | Project Coordination |
| Personal Assistant | Executive Support |
| Presentation Designer | Deck Creation |
| SwarmClaw | Agent Orchestration |
| ZeroClaw | Autonomous Agent |

## Installation

### Windows

1. Download the latest release from [GitHub Releases](https://github.com/Automata-intelligentsia/quick-launch-hermes/releases)
2. Extract the ZIP file
3. Double-click `Quick-Launch.bat`

### Linux/WSL

```bash
# Clone the repository
git clone https://github.com/Automata-intelligentsia/quick-launch-hermes.git
cd quick-launch-hermes

# Run the launcher
python3 quick_launch.pyw
```

## Auto-Discovery

The launcher can automatically discover services from your Hermes installation:

1. Click the **"Auto-Discover"** button
2. The launcher scans `~/.local/bin` for `hermes-*` scripts
3. Discovered services appear in the "Custom Services" section
4. Enable them with the checkboxes

## Configuration

Configuration is stored in `~/.hermes/launcher-config.json`.

## Building from Source

### Requirements

- Python 3.8+
- tkinter (usually included with Python)

### Build Windows Executable

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "QuickLaunch" quick_launch.pyw
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
quick-launch-hermes/
├── quick_launch.pyw          # Main application
├── Quick-Launch.bat          # Windows launcher
├── README.md                 # This file
├── LICENSE                   # MIT License
└── packaging/                # Build scripts
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
- [Issue Tracker](https://github.com/Automata-intelligentsia/quick-launch-hermes/issues)

---

Built with ⚡ for the Hermes Agent ecosystem
