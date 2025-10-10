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

# Check if icon exists, if not skip icon parameter
if [ -f "icon.ico" ]; then
    ICON_PARAM="--icon=icon.ico"
else
    echo "⚠️  Warning: icon.ico not found, building without custom icon"
    ICON_PARAM=""
fi

pyinstaller --noconfirm \
    --name "Mycket" \
    --windowed \
    --onefile \
    --paths "src" \
    $ICON_PARAM \
    --hidden-import "database" \
    --hidden-import "database.models" \
    --hidden-import "ui" \
    --hidden-import "ui.main_window" \
    --hidden-import "ui.time_tracker" \
    --hidden-import "ui.services_panel" \
    --hidden-import "ui.reports_panel" \
    --hidden-import "PyQt6" \
    --hidden-import "PyQt6.QtCore" \
    --hidden-import "PyQt6.QtWidgets" \
    --hidden-import "PyQt6.QtGui" \
    --hidden-import "sqlalchemy.ext.declarative" \
    src/main.py

echo "✅ Build complete! Application is in dist/Mycket"
