"""Main application window."""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTabWidget, QStatusBar, QMenuBar, QMenu
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction

from .time_tracker import TimeTrackerWidget
from .services_panel import ServicesPanelWidget
from .reports_panel import ReportsPanelWidget


class MainWindow(QMainWindow):
    """Main application window with tabbed interface."""
    
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setWindowTitle("Mycket - Time Tracking & Billing")
        self.setMinimumSize(1000, 700)
        
        self._setup_ui()
        self._setup_menu()
        self._apply_stylesheet()
    
    def _setup_ui(self):
        """Setup main UI layout."""
        # Central widget with tabs
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        
        # Create tabs
        self.time_tracker = TimeTrackerWidget(self.db_manager)
        self.services_panel = ServicesPanelWidget(self.db_manager)
        self.reports_panel = ReportsPanelWidget(self.db_manager)
        
        self.tabs.addTab(self.time_tracker, "⏱️ Tracciamento Ore")
        self.tabs.addTab(self.services_panel, "🔧 Servizi")
        self.tabs.addTab(self.reports_panel, "📊 Report e Fatture")
        
        layout.addWidget(self.tabs)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Pronto")
    
    def _setup_menu(self):
        """Setup menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        export_action = QAction("&Esporta Dati...", self)
        export_action.setShortcut("Ctrl+E")
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        quit_action = QAction("&Esci", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Aiuto")
        
        about_action = QAction("&Info", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _show_about(self):
        """Show about dialog."""
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.about(
            self,
            "Info su Mycket",
            "<h2>Mycket</h2>"
            "<p>Applicazione per tracciamento ore e fatturazione</p>"
            "<p>Versione 0.1.0</p>"
        )
    
    def _apply_stylesheet(self):
        """Apply light green theme stylesheet."""
        stylesheet = """
        QMainWindow {
            background-color: #f5f5f5;
        }
        
        QTabWidget::pane {
            border: 1px solid #c0c0c0;
            background-color: white;
            border-radius: 4px;
        }
        
        QTabBar::tab {
            background-color: #e8e8e8;
            color: #333;
            padding: 10px 20px;
            margin-right: 2px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }
        
        QTabBar::tab:selected {
            background-color: #90EE90;
            color: #1a1a1a;
            font-weight: bold;
        }
        
        QTabBar::tab:hover {
            background-color: #b4f0b4;
        }
        
        QPushButton {
            background-color: #90EE90;
            color: #1a1a1a;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }
        
        QPushButton:hover {
            background-color: #7fd87f;
        }
        
        QPushButton:pressed {
            background-color: #6ec06e;
        }
        
        QPushButton:disabled {
            background-color: #d0d0d0;
            color: #888;
        }
        
        QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox {
            padding: 6px;
            border: 1px solid #c0c0c0;
            border-radius: 4px;
            background-color: white;
        }
        
        QLineEdit:focus, QTextEdit:focus {
            border: 2px solid #90EE90;
        }
        
        QTableWidget {
            border: 1px solid #c0c0c0;
            border-radius: 4px;
            background-color: white;
            gridline-color: #e0e0e0;
        }
        
        QTableWidget::item:selected {
            background-color: #90EE90;
            color: #1a1a1a;
        }
        
        QHeaderView::section {
            background-color: #e8e8e8;
            padding: 8px;
            border: none;
            border-right: 1px solid #c0c0c0;
            border-bottom: 1px solid #c0c0c0;
            font-weight: bold;
        }
        
        QStatusBar {
            background-color: #e8e8e8;
            border-top: 1px solid #c0c0c0;
        }
        
        QGroupBox {
            border: 2px solid #90EE90;
            border-radius: 6px;
            margin-top: 12px;
            padding-top: 10px;
            font-weight: bold;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
        }
        """
        self.setStyleSheet(stylesheet)
    
    def closeEvent(self, event):
        """Handle window close event."""
        # Close database connection
        self.db_manager.close()
        event.accept()
