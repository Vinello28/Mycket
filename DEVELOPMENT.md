# Guida per Sviluppatori

## Setup Ambiente di Sviluppo

### Prerequisiti
- Python 3.8 o superiore
- pip
- virtualenv

### Installazione

```bash
# Clone repository
git clone <repository-url>
cd Mycket

# Crea e attiva virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# oppure
venv\Scripts\activate     # Windows

# Installa dipendenze
pip install -r requirements.txt
```

### Avvio Applicazione

```bash
# Metodo 1: Script rapido (macOS/Linux)
./run.sh

# Metodo 2: Manuale
source venv/bin/activate
cd src
python main.py
```

## Struttura Progetto

```
src/
├── main.py              # Entry point applicazione
├── database/
│   ├── __init__.py     # DatabaseManager
│   └── models.py       # Modelli SQLAlchemy (Service, TimeEntry, Invoice)
└── ui/
    ├── __init__.py     # Export widgets
    ├── main_window.py  # Finestra principale con tabs
    ├── time_tracker.py # Widget per time tracking
    ├── services_panel.py # Gestione servizi
    └── reports_panel.py  # Report e fatturazione
```

## Database

### Schema
- **services**: id, name, hourly_rate, description, created_at, updated_at
- **time_entries**: id, service_id, start_time, end_time, notes, created_at, updated_at
- **invoices**: id, invoice_number, client_name, period_start, period_end, total_amount, notes, created_at

### Posizione
- Sviluppo: `~/.mycket/mycket.db`
- Produzione: Stessa posizione (home directory utente)

## Aggiungere Nuove Funzionalità

### 1. Nuova Tabella Database

Modifica `src/database/models.py`:

```python
class NuovoModello(Base):
    __tablename__ = 'nuovo_modello'
    id = Column(Integer, primary_key=True)
    # ... altri campi
```

### 2. Nuovo Widget UI

Crea `src/ui/nuovo_widget.py`:

```python
from PyQt6.QtWidgets import QWidget, QVBoxLayout

class NuovoWidget(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.session = db_manager.get_session()
        self._setup_ui()
```

Aggiungi alla `MainWindow` in `main_window.py`:

```python
self.nuovo_tab = NuovoWidget(self.db_manager)
self.tabs.addTab(self.nuovo_tab, "Nuovo Tab")
```

### 3. Modificare Stile

Modifica lo stylesheet in `src/ui/main_window.py`, metodo `_apply_stylesheet()`.

## Testing

### Test Manuale
1. Avvia applicazione: `./run.sh`
2. Testa ogni tab
3. Verifica database: `sqlite3 ~/.mycket/mycket.db`

### Test Funzionalità Chiave
- [ ] Avvio/stop timer
- [ ] Inserimento manuale voce
- [ ] Aggiunta/modifica/eliminazione servizio
- [ ] Generazione report
- [ ] Export CSV
- [ ] Creazione fattura

## Build & Packaging

### macOS
```bash
./build_macos.sh
# Output: dist/Mycket.app
```

### Windows
```bash
build_windows.bat
# Output: dist\Mycket.exe
```

### Note su PyInstaller
- Usa `--onefile` per singolo eseguibile
- `--windowed` nasconde console
- `--add-data` include risorse
- Hidden imports per PyQt6 e SQLAlchemy

## Troubleshooting

### Errori Comuni

**ImportError con PyQt6**
```bash
pip install --upgrade PyQt6
```

**Database locked**
- Chiudi tutte le istanze dell'app
- Elimina `~/.mycket/mycket.db-journal` se presente

**Errore build PyInstaller**
```bash
pip install --upgrade pyinstaller
pyinstaller --clean ...
```

## Convenzioni Codice

- **Lingua**: Codice in inglese, UI in italiano
- **Stile**: PEP 8
- **Docstrings**: Google style
- **Import**: Assoluti per moduli src/

## Roadmap

### v0.2.0 (Prossima Release)
- [ ] Export PDF fatture
- [ ] Multi-currency support
- [ ] Backup/restore automatico
- [ ] Statistiche avanzate

### v0.3.0
- [ ] Client management
- [ ] Fattura con logo personalizzato
- [ ] Sincronizzazione cloud (opzionale)
- [ ] Mobile companion app

## Contribuire

1. Fork repository
2. Crea feature branch (`git checkout -b feature/NuovaFeature`)
3. Commit modifiche (`git commit -am 'Aggiunta NuovaFeature'`)
4. Push branch (`git push origin feature/NuovaFeature`)
5. Apri Pull Request

## Licenza

Uso personale. Tutti i diritti riservati.
