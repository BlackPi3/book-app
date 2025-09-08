from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator
import os

# Database URL - using SQLite for development, easily switchable to PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./books.db")

# Create database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Create SessionLocal class - this is the Factory Pattern!
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models - imported from models.py
from .models import Base

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

def get_db() -> Generator:
    """
    Database session dependency for FastAPI.
    This is the Factory Pattern in action - creates database sessions on demand.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
