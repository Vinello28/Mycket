# Mycket - Time Tracking & Billing

Applicazione desktop self-contained per il tracciamento delle ore di lavoro e la generazione di fatture. Progettata per consulenti che offrono diversi servizi con tariffe orarie differenti.

**Status:** ✅ Production Ready | **Version:** 0.1.0 | **Last Updated:** 2024-10-02

---

## 📚 Documentazione

- **[QUICKSTART.md](QUICKSTART.md)** - Guida rapida (3 passi)
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Guida per sviluppatori
- **[IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md)** - Riepilogo implementazione
- **[PROJECT_STATS.md](PROJECT_STATS.md)** - Statistiche progetto
- **[CHANGELOG.md](CHANGELOG.md)** - Storico versioni

---

## 🌟 Funzionalità

- **⏱️ Time Tracking**: Timer interattivo per tracciare le ore in tempo reale
- **✏️ Inserimento Manuale**: Aggiungi voci di tempo manualmente
- **🔧 Gestione Servizi**: Configura servizi con tariffe orarie personalizzate
- **📊 Report**: Visualizza report per periodo e tipo di servizio
- **🧾 Fatturazione**: Genera fatture in formato CSV
- **💾 Database Locale**: Tutti i dati salvati localmente con SQLite

## 📋 Requisiti

- Python 3.8 o superiore
- macOS o Windows

## 🚀 Installazione e Avvio

### Metodo 1: Esecuzione Diretta (Sviluppo)

```bash
# Clona il repository
git clone <repository-url>
cd Mycket

# Crea ambiente virtuale
python3 -m venv venv

# Attiva l'ambiente virtuale
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Installa le dipendenze
pip install -r requirements.txt

# Avvia l'applicazione
cd src
python main.py
```

### Metodo 2: Build dell'Eseguibile

**macOS:**
```bash
./build_macos.sh
# L'eseguibile sarà in: dist/Mycket.app
```

**Windows:**
```cmd
build_windows.bat
# L'eseguibile sarà in: dist\Mycket.exe
```

## 📁 Struttura Progetto

```
Mycket/
├── src/
│   ├── database/       # Modelli SQLAlchemy e gestione database
│   ├── ui/            # Interfaccia PyQt6
│   │   ├── main_window.py      # Finestra principale
│   │   ├── time_tracker.py     # Widget time tracking
│   │   ├── services_panel.py   # Gestione servizi
│   │   └── reports_panel.py    # Report e fatture
│   └── main.py        # Entry point applicazione
├── requirements.txt   # Dipendenze Python
├── build_macos.sh    # Script build macOS
└── build_windows.bat # Script build Windows
```

## 💼 Servizi Predefiniti

L'applicazione viene inizializzata con questi servizi (modificabili dall'interfaccia):

- **Consulenza Software** - 35€/h
- **Consulenza AI** - 45€/h
- **Progettazione e Sviluppo SW** - 40€/h
- **Progettazione e Sviluppo AI** - 50€/h
- **Analisi Dati** - 38€/h
- **Data Engineering** - 42€/h

## 🎨 Interfaccia

L'applicazione presenta un'interfaccia a tab con tema verde chiaro:

1. **Tracciamento Ore**: Avvia/ferma timer, inserisci voci manuali
2. **Servizi**: Aggiungi, modifica ed elimina servizi e tariffe
3. **Report e Fatture**: Genera report filtrabili ed esporta fatture CSV

## 💾 Database

I dati vengono salvati in `~/.mycket/mycket.db` (directory home dell'utente).

### Schema Database:
- **services**: Tipi di servizio con tariffe orarie
- **time_entries**: Voci di tempo registrate
- **invoices**: Fatture generate

## 🛠️ Sviluppo

### Tecnologie Utilizzate:
- **PyQt6**: Framework UI cross-platform
- **SQLAlchemy**: ORM per gestione database
- **SQLite**: Database embedded
- **PyInstaller**: Packaging applicazioni

### Aggiungere Nuove Funzionalità:

1. Modelli database: `src/database/models.py`
2. UI components: `src/ui/`
3. Business logic: Integrare nei widget esistenti

## 📝 License

Uso personale. Tutti i diritti riservati.

## 🐛 Problemi Noti

- Su macOS, l'app potrebbe richiedere permessi di sicurezza al primo avvio
- Su Windows, antivirus potrebbero richiedere conferma per l'eseguibile

## 📧 Contatti

Per supporto o domande, apri una issue su GitHub.