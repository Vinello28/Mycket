#!/usr/bin/env python3
"""
Mycket - Time Tracking and Billing Application
Main application entry point
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QStyleFactory
from PyQt6.QtGui import QIcon, QPalette, QColor
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
    
    # Force light mode
    app.setStyle(QStyleFactory.create("Fusion"))
    
    # Set light palette
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(245, 245, 245))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 220))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(144, 238, 144))  # Light green
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))
    app.setPalette(palette)
    
    # Initialize database
    db_manager = DatabaseManager()
    
    # Create and show main window
    window = MainWindow(db_manager)
    window.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
