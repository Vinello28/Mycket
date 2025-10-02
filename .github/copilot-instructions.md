# Copilot Instructions - Mycket

## Project Overview
**Mycket** is a fully implemented time tracking and billing application for a junior software engineer offering consulting services. Built with Python and PyQt6, it tracks work hours across different service types and generates CSV invoices.

**Tech Stack (IMPLEMENTED):**
- **Language:** Python 3.8+
- **UI Framework:** PyQt6 (cross-platform desktop)
- **Database:** SQLite with SQLAlchemy ORM
- **Packaging:** PyInstaller for standalone executables
- **Currency:** Euro (€) only

## Architecture & Project Structure

### Directory Layout
```
src/
├── main.py                 # Application entry point
├── database/
│   ├── __init__.py        # DatabaseManager class
│   └── models.py          # SQLAlchemy models: Service, TimeEntry, Invoice
└── ui/
    ├── main_window.py     # QMainWindow with tabbed interface
    ├── time_tracker.py    # Timer widget + manual entry
    ├── services_panel.py  # Service CRUD operations
    └── reports_panel.py   # Reports & invoice generation
```

### Critical Import Pattern
**IMPORTANT:** Due to the way `main.py` runs from `src/`, all imports use **absolute imports** (not relative):
```python
# ✅ Correct
from database.models import Service, TimeEntry
from ui import MainWindow

# ❌ Wrong (causes ImportError)
from ..database.models import Service
```

## Database Schema (SQLAlchemy Models)

### Service Model (`database/models.py`)
```python
- id: Integer (PK)
- name: String(200), unique
- hourly_rate: Float
- description: Text (optional)
- time_entries: relationship → TimeEntry
```

### TimeEntry Model
```python
- id: Integer (PK)
- service_id: ForeignKey(services.id)
- start_time: DateTime
- end_time: DateTime (nullable for running timers)
- notes: Text (optional)
- service: relationship ← Service
- Properties: duration_hours, is_running
```

### Invoice Model
```python
- id: Integer (PK)
- invoice_number: String(50), unique
- period_start/end: DateTime
- total_amount: Float
- notes: Text (optional)
```

**Database Location:** `~/.mycket/mycket.db` (created automatically)

## Key UI Components

### 1. TimeTrackerWidget (`ui/time_tracker.py`)
- **Live Timer:** QTimer updates every second, shows HH:MM:SS
- **Running Entry Detection:** Checks for `TimeEntry.end_time IS NULL` on startup
- **Manual Entry:** QDateTimeEdit widgets for start/end times
- **Table View:** Shows last 100 entries, sortable, deletable

**Critical Pattern:** Only ONE running timer allowed at a time:
```python
# Check on startup
running = session.query(TimeEntry).filter(TimeEntry.end_time.is_(None)).first()
```

### 2. ServicesPanelWidget (`ui/services_panel.py`)
- **CRUD Operations:** Add, edit (double-click or button), delete services
- **Validation:** Prevents duplicate service names
- **Cascade Delete:** Deleting service also deletes all associated time entries
- **Edit Dialog:** Modal `ServiceEditDialog` for modifications

### 3. ReportsPanelWidget (`ui/reports_panel.py`)
- **Filters:** Date range (QDateEdit) + service combo box
- **CSV Export:** Uses Python's `csv` module, includes summary row
- **Invoice Generation:** 
  - Auto-generates invoice number: `INV-{year}-{count:04d}`
  - Saves record to `invoices` table
  - Exports formatted CSV with header

## Styling & Theme

**Light Green Theme:** Applied via QSS stylesheet in `MainWindow._apply_stylesheet()`:
- Primary: `#90EE90` (light green)
- Hover: `#b4f0b4`
- Active: `#6ec06e`
- Selected rows: Light green background
- Italian labels: All UI text in Italian

**Widget Styling Pattern:**
```python
QPushButton {
    background-color: #90EE90;
    border-radius: 4px;
    font-weight: bold;
}
```

## Development Workflows

### Running the App (Development)
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
cd src
python main.py
```

**Quick Start:** `./run.sh` (macOS/Linux)

### Building Executables
- **macOS:** `./build_macos.sh` → `dist/Mycket.app`
- **Windows:** `build_windows.bat` → `dist/Mycket.exe`

**PyInstaller Config:**
- `--windowed`: No console
- `--onefile`: Single executable
- `--add-data "src:src"`: Bundle source (adjust for platform)
- Hidden imports: `PyQt6`, `sqlalchemy.ext.declarative`

### Database Seeding
On first run, `database/models.py::seed_default_services()` populates 6 services:
- Consulenza Software (35€/h)
- Consulenza AI (45€/h)
- Progettazione e Sviluppo SW (40€/h)
- Progettazione e Sviluppo AI (50€/h)
- Analisi Dati (38€/h)
- Data Engineering (42€/h)

## Common Patterns & Best Practices

### 1. Session Management
Always use `self.session` from `db_manager.get_session()`:
```python
class MyWidget(QWidget):
    def __init__(self, db_manager):
        self.session = db_manager.get_session()
        # Use self.session for all queries
```

### 2. Refreshing UI After Changes
After DB modifications, reload tables:
```python
self.session.commit()
self._load_time_entries()  # Refresh table
```

### 3. Date Handling
- **Python:** `datetime.datetime` objects
- **PyQt6:** `QDateTime.currentDateTime()`, convert with `.toPyDateTime()`
- **Display Format:** Italian `dd/MM/yyyy HH:mm`

### 4. Validation Pattern
```python
if not name.strip():
    QMessageBox.warning(self, "Attenzione", "Campo obbligatorio")
    return
```

## Troubleshooting

### ImportError: "attempted relative import beyond top-level package"
- **Cause:** Using `from ..database` instead of `from database`
- **Fix:** Change to absolute imports (see Import Pattern above)

### Timer Not Updating
- **Cause:** `QTimer` not started or stopped
- **Check:** `self.timer.start(1000)` for 1-second interval

### Database Locked
- **Cause:** Multiple app instances or orphaned lock file
- **Fix:** Close all instances, delete `~/.mycket/mycket.db-journal`

## Adding Features

### Example: Add New Tab
1. Create widget in `src/ui/new_widget.py`
2. Import in `main_window.py`: `from ui.new_widget import NewWidget`
3. Add tab: `self.tabs.addTab(NewWidget(self.db_manager), "🆕 Nuovo")`

### Example: Add Model Field
1. Update model in `database/models.py`
2. **Migration:** Delete `~/.mycket/mycket.db` (dev only) or use Alembic for production
3. Update UI to display/edit new field

## Testing Guidelines
- **Manual Testing:** Test each tab's CRUD operations
- **Database Inspection:** `sqlite3 ~/.mycket/mycket.db` + `.schema`
- **Cross-Platform:** Test build scripts on both macOS and Windows

## Notes for AI Agents
- Code in **English**, UI text in **Italian**
- Follow PEP 8 style guidelines
- Use **absolute imports** from `src/` directory
- Prefer **direct DB queries** over complex ORM tricks (keep it simple)
- When modifying UI, maintain light green theme consistency
- Italian UX terms: "Servizio" (service), "Ore" (hours), "Fattura" (invoice)
