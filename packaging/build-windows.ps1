# Build script for Windows
# Run in PowerShell

$ErrorActionPreference = "Stop"

Write-Host "Building Hermes Quick Launch for Windows..." -ForegroundColor Cyan

# Create virtual environment
python -m venv build_env
.\build_env\Scripts\Activate.ps1

# Install dependencies
pip install pyinstaller

# Build executable
pyinstaller `
    --onefile `
    --windowed `
    --name "HermesQuickLaunch" `
    --add-data "Hermes-Quick-Launch.bat;." `
    hermes_quick_launch.pyw

# Create distribution directory
New-Item -ItemType Directory -Force -Path "dist\HermesQuickLaunch-Windows" | Out-Null

# Copy files
Copy-Item "dist\HermesQuickLaunch.exe" "dist\HermesQuickLaunch-Windows\"
Copy-Item "Hermes-Quick-Launch.bat" "dist\HermesQuickLaunch-Windows\"
Copy-Item "README.md" "dist\HermesQuickLaunch-Windows\"
Copy-Item "LICENSE" "dist\HermesQuickLaunch-Windows\"

# Create ZIP
Compress-Archive -Path "dist\HermesQuickLaunch-Windows\*" -DestinationPath "dist\HermesQuickLaunch-Windows.zip" -Force

Write-Host "Build complete: dist\HermesQuickLaunch-Windows.zip" -ForegroundColor Green
