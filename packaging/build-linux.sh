#!/bin/bash
# Build script for Linux/WSL

set -e

echo "Building Hermes Quick Launch for Linux..."

# Create virtual environment
python3 -m venv build_env
source build_env/bin/activate

# Install dependencies
pip install pyinstaller

# Build executable
pyinstaller \
    --onefile \
    --windowed \
    --name "hermes-quick-launch" \
    --add-data "Hermes-Quick-Launch.bat:." \
    hermes_quick_launch.pyw

# Create distribution directory
mkdir -p dist/hermes-quick-launch-linux

# Copy files
cp dist/hermes-quick-launch dist/hermes-quick-launch-linux/
cp README.md dist/hermes-quick-launch-linux/
cp LICENSE dist/hermes-quick-launch-linux/

# Create tarball
cd dist
tar -czf hermes-quick-launch-linux.tar.gz hermes-quick-launch-linux/

echo "Build complete: dist/hermes-quick-launch-linux.tar.gz"
