import sys
import os
from pathlib import Path

# Add the parent directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine
from app.db.models import Base
from app.core.config import settings

def create_tables():
    """
    Create all database tables
    """
    # Create engine
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    
    # Create all tables
    Base.metadata.create_all(engine)
    
    print("Database tables created successfully")

if __name__ == "__main__":
    print("Creating database tables...")
    create_tables() 