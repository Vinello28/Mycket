"""Services management panel."""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QLineEdit, QDoubleSpinBox, QTextEdit, QTableWidget, QTableWidgetItem,
    QGroupBox, QMessageBox, QHeaderView, QDialog, QDialogButtonBox
)
from PyQt6.QtCore import Qt

from database.models import Service


class ServicesPanelWidget(QWidget):
    """Widget for managing service types and rates."""
    
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.session = db_manager.get_session()
        
        self._setup_ui()
        self._load_services()
    
    def _setup_ui(self):
        """Setup UI layout."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Add service group
        add_group = QGroupBox("➕ Aggiungi Nuovo Servizio")
        add_layout = QVBoxLayout()
        
        # Name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Nome Servizio:"))
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("es. Consulenza Software")
        name_layout.addWidget(self.name_edit)
        add_layout.addLayout(name_layout)
        
        # Hourly rate
        rate_layout = QHBoxLayout()
        rate_layout.addWidget(QLabel("Tariffa Oraria (€):"))
        self.rate_spinbox = QDoubleSpinBox()
        self.rate_spinbox.setMinimum(0.0)
        self.rate_spinbox.setMaximum(999.99)
        self.rate_spinbox.setDecimals(2)
        self.rate_spinbox.setSuffix(" €/h")
        self.rate_spinbox.setValue(35.0)
        rate_layout.addWidget(self.rate_spinbox)
        rate_layout.addStretch()
        add_layout.addLayout(rate_layout)
        
        # Description
        desc_layout = QVBoxLayout()
        desc_layout.addWidget(QLabel("Descrizione:"))
        self.desc_edit = QTextEdit()
        self.desc_edit.setMaximumHeight(60)
        self.desc_edit.setPlaceholderText("Descrizione opzionale del servizio...")
        desc_layout.addWidget(self.desc_edit)
        add_layout.addLayout(desc_layout)
        
        # Add button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        add_button = QPushButton("➕ Aggiungi Servizio")
        add_button.clicked.connect(self._add_service)
        add_button.setMinimumHeight(35)
        button_layout.addWidget(add_button)
        add_layout.addLayout(button_layout)
        
        add_group.setLayout(add_layout)
        layout.addWidget(add_group)
        
        # Services table
        table_group = QGroupBox("📋 Servizi Configurati")
        table_layout = QVBoxLayout()
        
        self.services_table = QTableWidget()
        self.services_table.setColumnCount(4)
        self.services_table.setHorizontalHeaderLabels([
            "Nome Servizio", "Tariffa (€/h)", "Descrizione", "ID"
        ])
        self.services_table.setColumnHidden(3, True)  # Hide ID
        self.services_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.services_table.setAlternatingRowColors(True)
        self.services_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        self.services_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.services_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.services_table.setColumnWidth(0, 300)
        self.services_table.setColumnWidth(1, 120)
        self.services_table.doubleClicked.connect(self._edit_service)
        
        table_layout.addWidget(self.services_table)
        
        # Buttons
        button_row = QHBoxLayout()
        button_row.addStretch()
        
        edit_button = QPushButton("✏️ Modifica")
        edit_button.clicked.connect(self._edit_service)
        button_row.addWidget(edit_button)
        
        delete_button = QPushButton("🗑️ Elimina")
        delete_button.clicked.connect(self._delete_service)
        button_row.addWidget(delete_button)
        
        table_layout.addLayout(button_row)
        table_group.setLayout(table_layout)
        layout.addWidget(table_group, stretch=1)
    
    def _load_services(self):
        """Load services into table."""
        self.services_table.setRowCount(0)
        services = self.session.query(Service).order_by(Service.name).all()
        
        for service in services:
            row = self.services_table.rowCount()
            self.services_table.insertRow(row)
            
            self.services_table.setItem(row, 0, QTableWidgetItem(service.name))
            self.services_table.setItem(row, 1, QTableWidgetItem(f"{service.hourly_rate:.2f}"))
            self.services_table.setItem(row, 2, QTableWidgetItem(service.description or ""))
            self.services_table.setItem(row, 3, QTableWidgetItem(str(service.id)))
    
    def _add_service(self):
        """Add a new service."""
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Attenzione", "Inserisci il nome del servizio.")
            return
        
        # Check if service already exists
        existing = self.session.query(Service).filter(Service.name == name).first()
        if existing:
            QMessageBox.warning(self, "Attenzione", "Un servizio con questo nome esiste già.")
            return
        
        service = Service(
            name=name,
            hourly_rate=self.rate_spinbox.value(),
            description=self.desc_edit.toPlainText().strip() or None
        )
        
        self.session.add(service)
        self.session.commit()
        
        QMessageBox.information(self, "Successo", f"Servizio '{name}' aggiunto con successo!")
        
        # Clear form
        self.name_edit.clear()
        self.rate_spinbox.setValue(35.0)
        self.desc_edit.clear()
        
        self._load_services()
    
    def _edit_service(self):
        """Edit selected service."""
        selected_rows = set(item.row() for item in self.services_table.selectedItems())
        if not selected_rows:
            QMessageBox.warning(self, "Attenzione", "Seleziona un servizio da modificare.")
            return
        
        row = list(selected_rows)[0]
        service_id = int(self.services_table.item(row, 3).text())
        service = self.session.query(Service).get(service_id)
        
        if service:
            dialog = ServiceEditDialog(service, self)
            if dialog.exec():
                self.session.commit()
                self._load_services()
    
    def _delete_service(self):
        """Delete selected service."""
        selected_rows = set(item.row() for item in self.services_table.selectedItems())
        if not selected_rows:
            QMessageBox.warning(self, "Attenzione", "Seleziona un servizio da eliminare.")
            return
        
        row = list(selected_rows)[0]
        service_name = self.services_table.item(row, 0).text()
        service_id = int(self.services_table.item(row, 3).text())
        
        reply = QMessageBox.question(
            self,
            "Conferma Eliminazione",
            f"Eliminare il servizio '{service_name}'?\n\n"
            "Attenzione: verranno eliminate anche tutte le voci di tempo associate!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            service = self.session.query(Service).get(service_id)
            if service:
                self.session.delete(service)
                self.session.commit()
                self._load_services()


class ServiceEditDialog(QDialog):
    """Dialog for editing a service."""
    
    def __init__(self, service, parent=None):
        super().__init__(parent)
        self.service = service
        self.setWindowTitle(f"Modifica Servizio: {service.name}")
        self.setMinimumWidth(400)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup dialog UI."""
        layout = QVBoxLayout(self)
        
        # Name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Nome:"))
        self.name_edit = QLineEdit(self.service.name)
        name_layout.addWidget(self.name_edit)
        layout.addLayout(name_layout)
        
        # Rate
        rate_layout = QHBoxLayout()
        rate_layout.addWidget(QLabel("Tariffa:"))
        self.rate_spinbox = QDoubleSpinBox()
        self.rate_spinbox.setMinimum(0.0)
        self.rate_spinbox.setMaximum(999.99)
        self.rate_spinbox.setDecimals(2)
        self.rate_spinbox.setSuffix(" €/h")
        self.rate_spinbox.setValue(self.service.hourly_rate)
        rate_layout.addWidget(self.rate_spinbox)
        rate_layout.addStretch()
        layout.addLayout(rate_layout)
        
        # Description
        layout.addWidget(QLabel("Descrizione:"))
        self.desc_edit = QTextEdit()
        self.desc_edit.setPlainText(self.service.description or "")
        self.desc_edit.setMaximumHeight(80)
        layout.addWidget(self.desc_edit)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._save)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def _save(self):
        """Save changes."""
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Attenzione", "Il nome non può essere vuoto.")
            return
        
        self.service.name = name
        self.service.hourly_rate = self.rate_spinbox.value()
        self.service.description = self.desc_edit.toPlainText().strip() or None
        
        self.accept()
