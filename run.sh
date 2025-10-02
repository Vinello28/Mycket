#!/bin/bash
# Quick start script for development

set -e

echo "🚀 Avvio Mycket..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment non trovato. Esegui prima l'installazione:"
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Activate and run
source venv/bin/activate
cd src
python main.py
