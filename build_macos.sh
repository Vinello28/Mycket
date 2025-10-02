#!/bin/bash
# Build script for macOS

set -e

echo "🔨 Building Mycket for macOS..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Build with PyInstaller
echo "🚀 Building application..."
pyinstaller --noconfirm \
    --name "Mycket" \
    --windowed \
    --onefile \
    --icon="" \
    --add-data "src:src" \
    --hidden-import "PyQt6" \
    --hidden-import "sqlalchemy.ext.declarative" \
    src/main.py

echo "✅ Build complete! Application is in dist/Mycket"
