from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from typing import Generator
import os

# Database URL - using SQLite for development, easily switchable to PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./books.db")
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///./test_books.db")

# Optimized database engine configuration
def create_database_engine(database_url: str):
    """
    Create an optimized database engine with proper connection pooling.

    This demonstrates database optimization patterns:
    - Connection pooling for performance
    - Proper SQLite configuration for threading
    - Echo for development debugging
    """
    connect_args = {}

    if "sqlite" in database_url:
        # SQLite-specific optimizations
        connect_args = {
            "check_same_thread": False,  # Allow multiple threads
            "timeout": 20,               # Connection timeout
        }

        # Use StaticPool for SQLite to maintain connections
        return create_engine(
            database_url,
            connect_args=connect_args,
            poolclass=StaticPool,
            pool_recycle=3600,  # Recycle connections every hour
            echo=False          # Set to True for SQL debugging
        )
    else:
        # PostgreSQL-specific optimizations (for future use)
        return create_engine(
            database_url,
            pool_size=20,       # Connection pool size
            max_overflow=0,     # No overflow connections
            pool_recycle=3600,  # Recycle connections
            echo=False
        )

# Create optimized engines
engine = create_database_engine(DATABASE_URL)
test_engine = create_database_engine(TEST_DATABASE_URL)

# Create SessionLocal classes with optimized settings
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False  # Keep objects accessible after commit
)

TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
    expire_on_commit=False
)

# Import Base from models - using try/except to handle both relative and absolute imports
try:
    # Try relative import first (when used as module)
    from .models import Base
except ImportError:
    # Fall back to absolute import (when script is run directly)
    from models import Base

def create_tables(engine_to_use=None):
    """Create all database tables"""
    target_engine = engine_to_use or engine
    Base.metadata.create_all(bind=target_engine)

def drop_tables(engine_to_use=None):
    """Drop all database tables (useful for testing)"""
    target_engine = engine_to_use or engine
    Base.metadata.drop_all(bind=target_engine)

def get_db() -> Generator:
    """
    Optimized database session dependency for FastAPI.

    This implements several optimization patterns:
    - Proper session lifecycle management
    - Exception handling for rollbacks
    - Resource cleanup in finally block
    """
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def get_test_db() -> Generator:
    """Test database session factory for isolated testing"""
    db = TestSessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
