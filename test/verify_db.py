"""Verify database connection and version"""
import sys
import os
from sqlalchemy import text

# Add parent directory to path so we can import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal

def verify_db():
    print("Checking database connection...")
    db = SessionLocal()
    try:
        # Check version (SQLite)
        result = db.execute(text("SELECT sqlite_version()"))
        version = result.scalar()
        print(f"Database connected successfully!")
        print(f"SQLite Version: {version}")
        
        # Dummy query
        db.execute(text("SELECT 1"))
        print("Dummy query executed successfully.")
        
    except Exception as e:
        print(f"Database connection failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    verify_db()
