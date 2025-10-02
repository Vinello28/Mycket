"""Reports and invoicing panel."""

from datetime import datetime, timedelta
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QDateEdit, QComboBox, QTableWidget, QTableWidgetItem,
    QGroupBox, QMessageBox, QHeaderView, QFileDialog, QTextEdit
)
from PyQt6.QtCore import Qt, QDate
import csv

from database.models import Service, TimeEntry, Invoice


class ReportsPanelWidget(QWidget):
    """Widget for generating reports and invoices."""
    
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.session = db_manager.get_session()
        
        self._setup_ui()
        self._load_services()
        self._generate_report()
    
    def _setup_ui(self):
        """Setup UI layout."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Filters group
        filters_group = QGroupBox("🔍 Filtri Report")
        filters_layout = QVBoxLayout()
        
        # Date range
        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("Periodo:"))
        
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addMonths(-1))
        self.start_date.setCalendarPopup(True)
        self.start_date.setDisplayFormat("dd/MM/yyyy")
        date_layout.addWidget(QLabel("Da:"))
        date_layout.addWidget(self.start_date)
        
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        self.end_date.setDisplayFormat("dd/MM/yyyy")
        date_layout.addWidget(QLabel("A:"))
        date_layout.addWidget(self.end_date)
        
        # Service filter
        date_layout.addWidget(QLabel("Servizio:"))
        self.service_filter = QComboBox()
        self.service_filter.setMinimumWidth(200)
        date_layout.addWidget(self.service_filter)
        
        # Generate button
        generate_button = QPushButton("📊 Genera Report")
        generate_button.clicked.connect(self._generate_report)
        generate_button.setMinimumHeight(35)
        date_layout.addWidget(generate_button)
        
        date_layout.addStretch()
        filters_layout.addLayout(date_layout)
        
        filters_group.setLayout(filters_layout)
        layout.addWidget(filters_group)
        
        # Summary group
        summary_group = QGroupBox("📈 Riepilogo")
        summary_layout = QHBoxLayout()
        
        self.total_hours_label = QLabel("Ore Totali: 0.00")
        self.total_hours_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #2d5016;")
        summary_layout.addWidget(self.total_hours_label)
        
        self.total_amount_label = QLabel("Importo Totale: 0.00€")
        self.total_amount_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #2d5016;")
        summary_layout.addWidget(self.total_amount_label)
        
        summary_layout.addStretch()
        summary_group.setLayout(summary_layout)
        layout.addWidget(summary_group)
        
        # Report table
        table_group = QGroupBox("📋 Dettaglio Voci")
        table_layout = QVBoxLayout()
        
        self.report_table = QTableWidget()
        self.report_table.setColumnCount(6)
        self.report_table.setHorizontalHeaderLabels([
            "Data", "Servizio", "Inizio", "Fine", "Ore", "Importo (€)"
        ])
        self.report_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.report_table.setAlternatingRowColors(True)
        self.report_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.report_table.setColumnWidth(0, 100)
        self.report_table.setColumnWidth(1, 250)
        self.report_table.setColumnWidth(2, 100)
        self.report_table.setColumnWidth(3, 100)
        self.report_table.setColumnWidth(4, 80)
        self.report_table.setColumnWidth(5, 100)
        
        table_layout.addWidget(self.report_table)
        table_group.setLayout(table_layout)
        layout.addWidget(table_group, stretch=1)
        
        # Export buttons
        export_layout = QHBoxLayout()
        export_layout.addStretch()
        
        export_csv_button = QPushButton("📄 Esporta CSV")
        export_csv_button.clicked.connect(self._export_csv)
        export_layout.addWidget(export_csv_button)
        
        create_invoice_button = QPushButton("🧾 Crea Fattura")
        create_invoice_button.clicked.connect(self._create_invoice)
        export_layout.addWidget(create_invoice_button)
        
        layout.addLayout(export_layout)
    
    def _load_services(self):
        """Load services into filter combo."""
        self.service_filter.clear()
        self.service_filter.addItem("Tutti i Servizi", None)
        
        services = self.session.query(Service).order_by(Service.name).all()
        for service in services:
            self.service_filter.addItem(service.name, service.id)
    
    def _generate_report(self):
        """Generate report based on filters."""
        start = self.start_date.date().toPyDate()
        end = self.end_date.date().toPyDate()
        end = datetime.combine(end, datetime.max.time())  # End of day
        service_id = self.service_filter.currentData()
        
        # Query time entries
        query = self.session.query(TimeEntry).filter(
            TimeEntry.start_time >= start,
            TimeEntry.start_time <= end,
            TimeEntry.end_time.isnot(None)  # Only completed entries
        )
        
        if service_id is not None:
            query = query.filter(TimeEntry.service_id == service_id)
        
        entries = query.order_by(TimeEntry.start_time).all()
        
        # Populate table
        self.report_table.setRowCount(0)
        total_hours = 0.0
        total_amount = 0.0
        
        for entry in entries:
            row = self.report_table.rowCount()
            self.report_table.insertRow(row)
            
            # Date
            date_str = entry.start_time.strftime("%d/%m/%Y")
            self.report_table.setItem(row, 0, QTableWidgetItem(date_str))
            
            # Service
            self.report_table.setItem(row, 1, QTableWidgetItem(entry.service.name))
            
            # Start time
            start_str = entry.start_time.strftime("%H:%M")
            self.report_table.setItem(row, 2, QTableWidgetItem(start_str))
            
            # End time
            end_str = entry.end_time.strftime("%H:%M") if entry.end_time else "-"
            self.report_table.setItem(row, 3, QTableWidgetItem(end_str))
            
            # Hours
            hours = entry.duration_hours or 0.0
            self.report_table.setItem(row, 4, QTableWidgetItem(f"{hours:.2f}"))
            
            # Amount
            amount = hours * entry.service.hourly_rate
            self.report_table.setItem(row, 5, QTableWidgetItem(f"{amount:.2f}"))
            
            total_hours += hours
            total_amount += amount
        
        # Update summary
        self.total_hours_label.setText(f"Ore Totali: {total_hours:.2f}")
        self.total_amount_label.setText(f"Importo Totale: {total_amount:.2f}€")
    
    def _export_csv(self):
        """Export report to CSV."""
        if self.report_table.rowCount() == 0:
            QMessageBox.warning(self, "Attenzione", "Nessun dato da esportare.")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Salva Report CSV",
            f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            "CSV Files (*.csv)"
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Write headers
                    headers = []
                    for col in range(self.report_table.columnCount()):
                        headers.append(self.report_table.horizontalHeaderItem(col).text())
                    writer.writerow(headers)
                    
                    # Write data
                    for row in range(self.report_table.rowCount()):
                        row_data = []
                        for col in range(self.report_table.columnCount()):
                            item = self.report_table.item(row, col)
                            row_data.append(item.text() if item else "")
                        writer.writerow(row_data)
                    
                    # Write summary
                    writer.writerow([])
                    writer.writerow(["Totale Ore", self.total_hours_label.text().split(": ")[1]])
                    writer.writerow(["Importo Totale", self.total_amount_label.text().split(": ")[1]])
                
                QMessageBox.information(self, "Successo", f"Report esportato in:\n{filename}")
            except Exception as e:
                QMessageBox.critical(self, "Errore", f"Errore durante l'esportazione:\n{str(e)}")
    
    def _create_invoice(self):
        """Create invoice from current report."""
        if self.report_table.rowCount() == 0:
            QMessageBox.warning(self, "Attenzione", "Nessun dato per creare la fattura.")
            return
        
        # Get total amount
        total_text = self.total_amount_label.text().split(": ")[1]
        total_amount = float(total_text.replace("€", "").strip())
        
        # Generate invoice number
        invoice_count = self.session.query(Invoice).count()
        invoice_number = f"INV-{datetime.now().year}-{invoice_count + 1:04d}"
        
        # Create invoice record
        invoice = Invoice(
            invoice_number=invoice_number,
            period_start=datetime.combine(self.start_date.date().toPyDate(), datetime.min.time()),
            period_end=datetime.combine(self.end_date.date().toPyDate(), datetime.max.time()),
            total_amount=total_amount
        )
        
        self.session.add(invoice)
        self.session.commit()
        
        # Export invoice
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Salva Fattura",
            f"fattura_{invoice_number}.csv",
            "CSV Files (*.csv)"
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Invoice header
                    writer.writerow(["FATTURA"])
                    writer.writerow(["Numero Fattura", invoice_number])
                    writer.writerow(["Data", datetime.now().strftime("%d/%m/%Y")])
                    writer.writerow(["Periodo", f"{self.start_date.date().toString('dd/MM/yyyy')} - {self.end_date.date().toString('dd/MM/yyyy')}"])
                    writer.writerow([])
                    
                    # Write headers
                    headers = []
                    for col in range(self.report_table.columnCount()):
                        headers.append(self.report_table.horizontalHeaderItem(col).text())
                    writer.writerow(headers)
                    
                    # Write data
                    for row in range(self.report_table.rowCount()):
                        row_data = []
                        for col in range(self.report_table.columnCount()):
                            item = self.report_table.item(row, col)
                            row_data.append(item.text() if item else "")
                        writer.writerow(row_data)
                    
                    # Totals
                    writer.writerow([])
                    writer.writerow(["", "", "", "", "TOTALE ORE:", self.total_hours_label.text().split(": ")[1]])
                    writer.writerow(["", "", "", "", "TOTALE €:", f"{total_amount:.2f}"])
                
                QMessageBox.information(
                    self,
                    "Successo",
                    f"Fattura {invoice_number} creata e salvata in:\n{filename}"
                )
            except Exception as e:
                QMessageBox.critical(self, "Errore", f"Errore durante la creazione della fattura:\n{str(e)}")
