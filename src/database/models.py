"""Database models for Mycket application."""

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class Service(Base):
    """Service type with hourly rate configuration."""
    
    __tablename__ = 'services'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, unique=True)
    hourly_rate = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    time_entries = relationship("TimeEntry", back_populates="service", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Service(name='{self.name}', rate={self.hourly_rate}€/h)>"


class TimeEntry(Base):
    """Individual time entry for a service."""
    
    __tablename__ = 'time_entries'
    
    id = Column(Integer, primary_key=True)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)  # Null if timer is running
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    service = relationship("Service", back_populates="time_entries")
    
    @property
    def duration_hours(self):
        """Calculate duration in hours."""
        if self.end_time is None:
            return None
        delta = self.end_time - self.start_time
        return delta.total_seconds() / 3600
    
    @property
    def is_running(self):
        """Check if timer is currently running."""
        return self.end_time is None
    
    def __repr__(self):
        status = "running" if self.is_running else f"{self.duration_hours:.2f}h"
        return f"<TimeEntry(service='{self.service.name if self.service else 'N/A'}', {status})>"


class Invoice(Base):
    """Invoice for a billing period."""
    
    __tablename__ = 'invoices'
    
    id = Column(Integer, primary_key=True)
    invoice_number = Column(String(50), unique=True, nullable=False)
    client_name = Column(String(200), nullable=True)
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    total_amount = Column(Float, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Invoice(number='{self.invoice_number}', amount={self.total_amount}€)>"


# Database initialization
def init_db(db_path='mycket.db'):
    """Initialize database and return session."""
    engine = create_engine(f'sqlite:///{db_path}', echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def seed_default_services(session):
    """Seed database with default service types."""
    default_services = [
        {"name": "Consulenza Software", "hourly_rate": 35.0, "description": "Consulenza generale su sviluppo software"},
        {"name": "Consulenza AI", "hourly_rate": 45.0, "description": "Consulenza su intelligenza artificiale e ML"},
        {"name": "Progettazione e Sviluppo SW", "hourly_rate": 40.0, "description": "Progettazione e sviluppo di soluzioni software"},
        {"name": "Progettazione e Sviluppo AI", "hourly_rate": 50.0, "description": "Progettazione e sviluppo di soluzioni AI"},
        {"name": "Analisi Dati", "hourly_rate": 38.0, "description": "Analisi e visualizzazione dati"},
        {"name": "Data Engineering", "hourly_rate": 42.0, "description": "Data engineering e preprocessing"},
    ]
    
    # Check if services already exist
    existing_count = session.query(Service).count()
    if existing_count == 0:
        for service_data in default_services:
            service = Service(**service_data)
            session.add(service)
        session.commit()
        print(f"✓ Aggiunti {len(default_services)} servizi predefiniti")
    else:
        print(f"✓ Database già contiene {existing_count} servizi")
