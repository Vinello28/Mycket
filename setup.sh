#!/bin/bash
# Complete setup script for Mycket

set -e

echo "🚀 Mycket - Setup Completo"
echo "=============================="
echo ""

# Check Python version
echo "📋 Controllo prerequisiti..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 non trovato. Installa Python 3.8 o superiore."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Python $PYTHON_VERSION trovato"

# Create virtual environment
echo ""
echo "🔧 Creazione virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment già esistente. Vuoi ricrearlo? (y/N)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        rm -rf venv
        python3 -m venv venv
        echo "✓ Virtual environment ricreato"
    else
        echo "→ Utilizzo virtual environment esistente"
    fi
else
    python3 -m venv venv
    echo "✓ Virtual environment creato"
fi

# Activate virtual environment
echo ""
echo "📦 Installazione dipendenze..."
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip > /dev/null 2>&1

# Install dependencies
if pip install -r requirements.txt; then
    echo "✓ Dipendenze installate con successo"
else
    echo "❌ Errore nell'installazione delle dipendenze"
    exit 1
fi

# Test database
echo ""
echo "🧪 Test database..."
cd tests
if python test_db.py > /dev/null 2>&1; then
    echo "✓ Database funzionante"
else
    echo "⚠️  Test database fallito (potrebbe essere normale al primo avvio)"
fi
cd ..

# Create database directory
echo ""
echo "📁 Preparazione directory dati..."
MOLTO_DIR="$HOME/.mycket"
if [ ! -d "$MOLTO_DIR" ]; then
    mkdir -p "$MOLTO_DIR"
    echo "✓ Directory creata: $MOLTO_DIR"
else
    echo "→ Directory già esistente: $MOLTO_DIR"
fi

echo ""
echo "=============================="
echo "✅ Setup completato con successo!"
echo ""
echo "🎯 Prossimi passi:"
echo ""
echo "  1. Avvia l'applicazione:"
echo "     ./run.sh"
echo ""
echo "  2. Oppure manualmente:"
echo "     source venv/bin/activate"
echo "     cd src"
echo "     python main.py"
echo ""
echo "  3. Build eseguibile (opzionale):"
echo "     ./build_macos.sh"
echo ""
echo "📚 Documentazione:"
echo "  - README.md - Guida utente"
echo "  - DEVELOPMENT.md - Guida sviluppatore"
echo "  - IMPLEMENTATION_COMPLETE.md - Riepilogo implementazione"
echo ""
echo "Buon lavoro con Mycket! 🎉"
