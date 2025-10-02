"""Time tracker widget for logging work hours."""

from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QComboBox, QTextEdit, QTableWidget, QTableWidgetItem,
    QGroupBox, QMessageBox, QHeaderView, QDateTimeEdit
)
from PyQt6.QtCore import Qt, QTimer, QDateTime
from PyQt6.QtGui import QFont

from database.models import Service, TimeEntry


class TimeTrackerWidget(QWidget):
    """Widget for tracking time entries."""
    
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.session = db_manager.get_session()
        self.running_entry = None
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_timer_display)
        
        self._setup_ui()
        self._load_services()
        self._load_time_entries()
        self._check_running_timer()
    
    def _setup_ui(self):
        """Setup UI layout."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Timer control group
        timer_group = QGroupBox("⏱️ Timer")
        timer_layout = QVBoxLayout()
        
        # Service selection
        service_layout = QHBoxLayout()
        service_layout.addWidget(QLabel("Servizio:"))
        self.service_combo = QComboBox()
        self.service_combo.setMinimumWidth(300)
        service_layout.addWidget(self.service_combo)
        service_layout.addStretch()
        timer_layout.addLayout(service_layout)
        
        # Timer display
        self.timer_label = QLabel("00:00:00")
        timer_font = QFont()
        timer_font.setPointSize(32)
        timer_font.setBold(True)
        self.timer_label.setFont(timer_font)
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setStyleSheet("color: #2d5016; padding: 20px;")
        timer_layout.addWidget(self.timer_label)
        
        # Control buttons
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("▶ Avvia Timer")
        self.start_button.clicked.connect(self._start_timer)
        self.start_button.setMinimumHeight(40)
        
        self.stop_button = QPushButton("⏹ Ferma Timer")
        self.stop_button.clicked.connect(self._stop_timer)
        self.stop_button.setMinimumHeight(40)
        self.stop_button.setEnabled(False)
        
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        timer_layout.addLayout(button_layout)
        
        # Notes
        notes_layout = QVBoxLayout()
        notes_layout.addWidget(QLabel("Note:"))
        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(80)
        self.notes_edit.setPlaceholderText("Aggiungi note opzionali per questa sessione...")
        notes_layout.addWidget(self.notes_edit)
        timer_layout.addLayout(notes_layout)
        
        timer_group.setLayout(timer_layout)
        layout.addWidget(timer_group)
        
        # Manual entry group
        manual_group = QGroupBox("✏️ Inserimento Manuale")
        manual_layout = QVBoxLayout()
        
        manual_form = QHBoxLayout()
        
        # Start time
        manual_form.addWidget(QLabel("Inizio:"))
        self.start_time_edit = QDateTimeEdit()
        self.start_time_edit.setDateTime(QDateTime.currentDateTime())
        self.start_time_edit.setCalendarPopup(True)
        self.start_time_edit.setDisplayFormat("dd/MM/yyyy HH:mm")
        manual_form.addWidget(self.start_time_edit)
        
        # End time
        manual_form.addWidget(QLabel("Fine:"))
        self.end_time_edit = QDateTimeEdit()
        self.end_time_edit.setDateTime(QDateTime.currentDateTime())
        self.end_time_edit.setCalendarPopup(True)
        self.end_time_edit.setDisplayFormat("dd/MM/yyyy HH:mm")
        manual_form.addWidget(self.end_time_edit)
        
        # Add button
        add_manual_button = QPushButton("➕ Aggiungi")
        add_manual_button.clicked.connect(self._add_manual_entry)
        manual_form.addWidget(add_manual_button)
        
        manual_layout.addLayout(manual_form)
        manual_group.setLayout(manual_layout)
        layout.addWidget(manual_group)
        
        # Time entries table
        entries_group = QGroupBox("📋 Voci Registrate")
        entries_layout = QVBoxLayout()
        
        self.entries_table = QTableWidget()
        self.entries_table.setColumnCount(6)
        self.entries_table.setHorizontalHeaderLabels([
            "Servizio", "Inizio", "Fine", "Durata (h)", "Note", "ID"
        ])
        self.entries_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.entries_table.horizontalHeader().setStretchLastSection(False)
        self.entries_table.setColumnHidden(5, True)  # Hide ID column
        self.entries_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.entries_table.setAlternatingRowColors(True)
        
        # Set column widths
        self.entries_table.setColumnWidth(0, 250)
        self.entries_table.setColumnWidth(1, 150)
        self.entries_table.setColumnWidth(2, 150)
        self.entries_table.setColumnWidth(3, 100)
        self.entries_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        
        entries_layout.addWidget(self.entries_table)
        
        # Delete button
        delete_layout = QHBoxLayout()
        delete_layout.addStretch()
        delete_button = QPushButton("🗑️ Elimina Selezionati")
        delete_button.clicked.connect(self._delete_selected_entries)
        delete_layout.addWidget(delete_button)
        entries_layout.addLayout(delete_layout)
        
        entries_group.setLayout(entries_layout)
        layout.addWidget(entries_group, stretch=1)
    
    def _load_services(self):
        """Load services into combo box."""
        self.service_combo.clear()
        services = self.session.query(Service).order_by(Service.name).all()
        for service in services:
            self.service_combo.addItem(f"{service.name} ({service.hourly_rate}€/h)", service.id)
    
    def _load_time_entries(self):
        """Load time entries into table."""
        self.entries_table.setRowCount(0)
        entries = self.session.query(TimeEntry).order_by(TimeEntry.start_time.desc()).limit(100).all()
        
        for entry in entries:
            row = self.entries_table.rowCount()
            self.entries_table.insertRow(row)
            
            # Service name
            self.entries_table.setItem(row, 0, QTableWidgetItem(entry.service.name))
            
            # Start time
            start_str = entry.start_time.strftime("%d/%m/%Y %H:%M")
            self.entries_table.setItem(row, 1, QTableWidgetItem(start_str))
            
            # End time
            end_str = entry.end_time.strftime("%d/%m/%Y %H:%M") if entry.end_time else "In corso..."
            self.entries_table.setItem(row, 2, QTableWidgetItem(end_str))
            
            # Duration
            duration_str = f"{entry.duration_hours:.2f}" if entry.duration_hours else "-"
            self.entries_table.setItem(row, 3, QTableWidgetItem(duration_str))
            
            # Notes
            notes = entry.notes or ""
            self.entries_table.setItem(row, 4, QTableWidgetItem(notes))
            
            # ID (hidden)
            self.entries_table.setItem(row, 5, QTableWidgetItem(str(entry.id)))
    
    def _check_running_timer(self):
        """Check if there's a running timer and resume it."""
        running = self.session.query(TimeEntry).filter(TimeEntry.end_time.is_(None)).first()
        if running:
            self.running_entry = running
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.service_combo.setEnabled(False)
            self.timer.start(1000)  # Update every second
    
    def _start_timer(self):
        """Start a new timer."""
        service_id = self.service_combo.currentData()
        if service_id is None:
            QMessageBox.warning(self, "Attenzione", "Seleziona un servizio prima di avviare il timer.")
            return
        
        # Create new time entry
        entry = TimeEntry(
            service_id=service_id,
            start_time=datetime.now(),
            notes=self.notes_edit.toPlainText() or None
        )
        self.session.add(entry)
        self.session.commit()
        
        self.running_entry = entry
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.service_combo.setEnabled(False)
        self.timer.start(1000)
        
        self._load_time_entries()
    
    def _stop_timer(self):
        """Stop the running timer."""
        if self.running_entry:
            self.running_entry.end_time = datetime.now()
            self.running_entry.notes = self.notes_edit.toPlainText() or None
            self.session.commit()
            
            duration = self.running_entry.duration_hours
            service = self.running_entry.service
            
            QMessageBox.information(
                self,
                "Timer Fermato",
                f"Sessione completata!\n\n"
                f"Servizio: {service.name}\n"
                f"Durata: {duration:.2f} ore\n"
                f"Costo: {duration * service.hourly_rate:.2f}€"
            )
            
            self.running_entry = None
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.service_combo.setEnabled(True)
            self.timer.stop()
            self.timer_label.setText("00:00:00")
            self.notes_edit.clear()
            
            self._load_time_entries()
    
    def _update_timer_display(self):
        """Update timer display."""
        if self.running_entry:
            elapsed = datetime.now() - self.running_entry.start_time
            hours = int(elapsed.total_seconds() // 3600)
            minutes = int((elapsed.total_seconds() % 3600) // 60)
            seconds = int(elapsed.total_seconds() % 60)
            self.timer_label.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
    
    def _add_manual_entry(self):
        """Add a manual time entry."""
        service_id = self.service_combo.currentData()
        if service_id is None:
            QMessageBox.warning(self, "Attenzione", "Seleziona un servizio.")
            return
        
        start = self.start_time_edit.dateTime().toPyDateTime()
        end = self.end_time_edit.dateTime().toPyDateTime()
        
        if end <= start:
            QMessageBox.warning(self, "Errore", "L'orario di fine deve essere successivo all'inizio.")
            return
        
        entry = TimeEntry(
            service_id=service_id,
            start_time=start,
            end_time=end,
            notes=self.notes_edit.toPlainText() or None
        )
        self.session.add(entry)
        self.session.commit()
        
        QMessageBox.information(self, "Successo", "Voce aggiunta con successo!")
        self.notes_edit.clear()
        self._load_time_entries()
    
    def _delete_selected_entries(self):
        """Delete selected time entries."""
        selected_rows = set(item.row() for item in self.entries_table.selectedItems())
        if not selected_rows:
            QMessageBox.warning(self, "Attenzione", "Seleziona almeno una voce da eliminare.")
            return
        
        reply = QMessageBox.question(
            self,
            "Conferma Eliminazione",
            f"Eliminare {len(selected_rows)} voce/i selezionate?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            for row in selected_rows:
                entry_id = int(self.entries_table.item(row, 5).text())
                entry = self.session.query(TimeEntry).get(entry_id)
                if entry:
                    self.session.delete(entry)
            
            self.session.commit()
            self._load_time_entries()
