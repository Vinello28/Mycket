"""Database manager for Mycket application."""

import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from .models import Base, seed_default_services


class DatabaseManager:
    """Manages database connection and session lifecycle."""
    
    def __init__(self, db_path=None):
        """
        Initialize database manager.
        
        Args:
            db_path: Path to SQLite database file. If None, uses default location.
        """
        if db_path is None:
            # Store database in user's home directory
            app_dir = Path.home() / '.mycket'
            app_dir.mkdir(exist_ok=True)
            db_path = app_dir / 'mycket.db'
        
        self.db_path = str(db_path)
        self.engine = create_engine(f'sqlite:///{self.db_path}', echo=False)
        self.session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.session_factory)
        
        # Initialize database
        self._init_db()
    
    def _init_db(self):
        """Initialize database schema."""
        Base.metadata.create_all(self.engine)
        
        # Seed default services if database is new
        session = self.Session()
        try:
            seed_default_services(session)
        finally:
            session.close()
    
    def get_session(self):
        """Get a new database session."""
        return self.Session()
    
    def close(self):
        """Close database connection."""
        self.Session.remove()
        self.engine.dispose()
