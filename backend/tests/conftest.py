"""
Test Configuration for BookApp

This module provides test fixtures and utilities for database testing.
It demonstrates the Test Database Isolation pattern - each test gets
a clean, isolated database state.

Key Patterns:
- Fixture-based test setup/teardown
- Test database isolation
- Factory pattern for test data creation
"""

import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Import our application components with proper path setup
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import Base, Book
from app.repositories.sql_book_repository import SQLBookRepository
from app.repositories.book_repository_interface import BookRepositoryInterface

@pytest.fixture(scope="function")
def test_engine():
    """
    Create a test database engine for each test function.

    This ensures complete isolation between tests by:
    - Using a unique in-memory database for each test
    - Creating fresh tables for each test
    - Automatic cleanup when test completes
    """
    # Use in-memory SQLite database for maximum isolation and speed
    test_db_url = "sqlite:///:memory:"

    # Create test engine with optimized settings
    engine = create_engine(
        test_db_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False  # Set to True for SQL debugging
    )

    # Create all tables
    Base.metadata.create_all(engine)

    yield engine

    # Cleanup happens automatically with in-memory database

@pytest.fixture(scope="function")
def test_session(test_engine):
    """
    Create a database session for testing.

    This fixture provides:
    - Fresh database session for each test
    - Automatic rollback after test completion
    - Proper session cleanup
    """
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine
    )

    session = SessionLocal()

    yield session

    # Cleanup: Close session
    session.close()

@pytest.fixture(scope="function")
def test_repository(test_session) -> BookRepositoryInterface:
    """
    Create a repository instance for testing.

    This demonstrates the Dependency Injection pattern in tests:
    - Repository depends on database session
    - Test provides controlled session
    - Easy to verify repository behavior
    """
    return SQLBookRepository(test_session)

@pytest.fixture
def sample_book_data():
    """
    Factory fixture for creating sample book data.

    This demonstrates the Test Data Factory pattern:
    - Centralized test data creation
    - Consistent test data across tests
    - Easy to modify test scenarios
    """
    return {
        "title": "Test Driven Development",
        "author": "Kent Beck",
        "created_by": "test_user"
    }

@pytest.fixture
def sample_book(sample_book_data):
    """Create a Book model instance from sample data"""
    return Book(**sample_book_data)

@pytest.fixture
def multiple_sample_books():
    """
    Factory for creating multiple test books.

    Useful for testing:
    - Search functionality
    - Pagination
    - Bulk operations
    """
    return [
        {
            "title": "Clean Code",
            "author": "Robert Martin",
            "created_by": "admin"
        },
        {
            "title": "The Pragmatic Programmer",
            "author": "David Thomas",
            "created_by": "admin"
        },
        {
            "title": "Design Patterns",
            "author": "Gang of Four",
            "created_by": "user1"
        },
        {
            "title": "Refactoring",
            "author": "Martin Fowler",
            "created_by": "user2"
        }
    ]

def create_test_books(session, book_data_list):
    """
    Utility function to create multiple books in the test database.

    This helper function:
    - Creates multiple books at once
    - Commits to database
    - Returns created book instances
    """
    books = []
    for book_data in book_data_list:
        book = Book(**book_data)
        session.add(book)
        books.append(book)

    session.commit()

    # Refresh to get IDs
    for book in books:
        session.refresh(book)

    return books
