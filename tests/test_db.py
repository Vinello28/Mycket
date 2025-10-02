"""
Quick test script to verify database operations
Run from project root: python tests/test_db.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from database import DatabaseManager
from database.models import Service, TimeEntry
from datetime import datetime, timedelta

def test_database():
    """Test basic database operations."""
    print("🧪 Testing Mycket Database Operations\n")
    
    # Initialize database
    db = DatabaseManager()
    session = db.get_session()
    
    # Test 1: List services
    print("1️⃣ Testing Services...")
    services = session.query(Service).all()
    print(f"   Found {len(services)} services:")
    for svc in services[:3]:
        print(f"   - {svc.name}: {svc.hourly_rate}€/h")
    
    # Test 2: Create time entry
    print("\n2️⃣ Creating test time entry...")
    if services:
        test_entry = TimeEntry(
            service_id=services[0].id,
            start_time=datetime.now() - timedelta(hours=2),
            end_time=datetime.now(),
            notes="Test entry from test script"
        )
        session.add(test_entry)
        session.commit()
        print(f"   ✓ Created entry: {test_entry.duration_hours:.2f} hours")
    
    # Test 3: Query time entries
    print("\n3️⃣ Testing Time Entries...")
    entries = session.query(TimeEntry).limit(5).all()
    print(f"   Found {len(entries)} entries:")
    for entry in entries:
        status = f"{entry.duration_hours:.2f}h" if entry.end_time else "Running"
        print(f"   - {entry.service.name}: {status}")
    
    # Test 4: Calculate totals
    print("\n4️⃣ Calculating totals...")
    all_entries = session.query(TimeEntry).filter(TimeEntry.end_time.isnot(None)).all()
    total_hours = sum(e.duration_hours or 0 for e in all_entries)
    total_amount = sum((e.duration_hours or 0) * e.service.hourly_rate for e in all_entries)
    print(f"   Total Hours: {total_hours:.2f}")
    print(f"   Total Amount: {total_amount:.2f}€")
    
    print("\n✅ All tests passed!")
    
    # Cleanup
    db.close()

if __name__ == "__main__":
    test_database()
