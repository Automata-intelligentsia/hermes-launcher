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

## Auto-Discovery

The launcher can automatically discover services from your Hermes installation:

1. Click the **"Auto-Discover"** button
2. The launcher scans `~/.local/bin` for `hermes-*` scripts
3. Discovered services appear in the "Custom Services" section
4. Enable them with the checkboxes

## Configuration

Configuration is stored in `~/.hermes/launcher-config.json`.

## License

MIT License - see [LICENSE](LICENSE) file

---

Built with ⚡ for the Hermes Agent ecosystem
