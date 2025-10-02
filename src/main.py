#!/usr/bin/env python3
"""
Mycket - Time Tracking and Billing Application
Main application entry point
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

from database import DatabaseManager
from ui import MainWindow


def main():
    """Main application entry point."""
    # Enable high DPI support
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Mycket")
    app.setApplicationVersion("0.1.0")
    app.setOrganizationName("Mycket")
    
    # Initialize database
    db_manager = DatabaseManager()
    
    # Create and show main window
    window = MainWindow(db_manager)
    window.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
