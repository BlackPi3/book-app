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
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

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
def test_db(test_engine):
    """
    Create a test database fixture for database isolation testing.

    This fixture provides access to the test database engine
    and ensures proper cleanup after each test.
    """
    yield test_engine


@pytest.fixture(scope="function")
def book_repository(test_session) -> BookRepositoryInterface:
    """
    Create a book repository instance for testing.

    This demonstrates the Repository pattern in testing:
    - Uses test database session for isolation
    - Returns interface type for flexibility
    - Automatic cleanup via session fixture
    """
    return SQLBookRepository(test_session)


@pytest.fixture(scope="function")
def test_repository(test_session) -> BookRepositoryInterface:
    """
    Create a test repository fixture for repository testing.

    This is an alias for book_repository to maintain compatibility
    with existing repository tests.
    """
    return SQLBookRepository(test_session)


@pytest.fixture
def sample_book_data():
    """
    Provide sample book data for testing.

    This demonstrates the Factory pattern for test data:
    - Consistent test data across tests
    - Easy to modify for different test scenarios
    - Reusable across multiple test files
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


@pytest.fixture
def create_test_books(test_session):
    """
    Pytest fixture for creating multiple books in the test database.

    This fixture provides a function that:
    - Creates multiple books at once
    - Commits to database
    - Returns created book instances

    Usage:
        def test_something(create_test_books):
            books = create_test_books([
                {"title": "Book 1", "author": "Author 1", "created_by": "user1"},
                {"title": "Book 2", "author": "Author 2", "created_by": "user2"}
            ])
            assert len(books) == 2

    Args:
        book_data_list: List of dictionaries containing book data

    Returns:
        Function that takes book_data_list and returns List of created Book instances
    """
    def _create_books(book_data_list):
        books = []
        for book_data in book_data_list:
            book = Book(**book_data)
            test_session.add(book)
            books.append(book)

        test_session.commit()

        # Refresh to get IDs
        for book in books:
            test_session.refresh(book)

        return books

    return _create_books
