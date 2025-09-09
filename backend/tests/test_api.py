"""
API Integration Tests for BookApp

This test suite demonstrates FastAPI testing patterns:
- TestClient for API testing
- Dependency override for isolated testing
- HTTP status code verification
- JSON response validation
"""

import pytest
import os
import sys
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Import from our app modules with proper path setup
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app, get_book_repository
from app.models import Base, Book
from app.repositories.sql_book_repository import SQLBookRepository

@pytest.fixture(scope="function")
def test_client():
    """
    Create a test client with isolated database for each test.

    This demonstrates:
    - Dependency override pattern
    - Test isolation
    - FastAPI TestClient usage
    """
    # Create shared in-memory database for this test
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

    Base.metadata.create_all(bind=test_engine)
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    def get_test_repository():
        """Override repository dependency for testing - uses same database throughout test"""
        db = TestSessionLocal()
        return SQLBookRepository(db)

    # Override the dependency
    app.dependency_overrides[get_book_repository] = get_test_repository

    # Create test client
    client = TestClient(app)

    yield client

    # Cleanup
    app.dependency_overrides.clear()

def test_root_endpoint(test_client):
    """Test the root welcome endpoint"""
    response = test_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Welcome to BookApp API" in data["message"]

def test_get_books_empty(test_client):
    """Test getting books when database is empty"""
    response = test_client.get("/books")
    assert response.status_code == 200
    assert response.json() == []

def test_create_book_success(test_client):
    """Test successful book creation"""
    book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "created_by": "test_user"
    }

    response = test_client.post("/books", json=book_data)
    assert response.status_code == 201

    data = response.json()
    assert data["title"] == book_data["title"]
    assert data["author"] == book_data["author"]
    assert data["created_by"] == book_data["created_by"]
    assert "id" in data
    assert "created_on" in data

def test_create_book_missing_fields(test_client):
    """Test book creation with missing required fields"""
    incomplete_data = {
        "title": "Test Book"
        # Missing author and created_by
    }

    response = test_client.post("/books", json=incomplete_data)
    assert response.status_code == 422  # Validation error

def test_get_book_by_id_success(test_client):
    """Test retrieving a book by ID"""
    # First create a book
    book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "created_by": "test_user"
    }

    create_response = test_client.post("/books", json=book_data)
    created_book = create_response.json()
    book_id = created_book["id"]

    # Then retrieve it
    response = test_client.get(f"/books/{book_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == book_id
    assert data["title"] == book_data["title"]

def test_get_book_by_id_not_found(test_client):
    """Test retrieving a non-existent book"""
    response = test_client.get("/books/99999")
    assert response.status_code == 404

def test_search_books_by_title(test_client):
    """Test searching books by title"""
    # Create multiple books
    books_data = [
        {"title": "Python Programming", "author": "Author 1", "created_by": "user1"},
        {"title": "Java Programming", "author": "Author 2", "created_by": "user2"},
        {"title": "Python Advanced", "author": "Author 3", "created_by": "user1"}
    ]

    for book_data in books_data:
        test_client.post("/books", json=book_data)

    # Search for Python books
    response = test_client.get("/books?title=Python")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2  # Should find 2 Python books
    for book in data:
        assert "Python" in book["title"]

def test_update_book_success(test_client):
    """Test updating an existing book"""
    # Create a book first
    book_data = {
        "title": "Original Title",
        "author": "Original Author",
        "created_by": "test_user"
    }

    create_response = test_client.post("/books", json=book_data)
    created_book = create_response.json()
    book_id = created_book["id"]

    # Update the book
    update_data = {
        "title": "Updated Title",
        "author": "Updated Author"
    }

    response = test_client.put(f"/books/{book_id}", json=update_data)
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["author"] == "Updated Author"
    assert data["created_by"] == "test_user"  # Should remain unchanged

def test_delete_book_success(test_client):
    """Test deleting an existing book"""
    # Create a book first
    book_data = {
        "title": "Book to Delete",
        "author": "Test Author",
        "created_by": "test_user"
    }

    create_response = test_client.post("/books", json=book_data)
    created_book = create_response.json()
    book_id = created_book["id"]

    # Delete the book
    response = test_client.delete(f"/books/{book_id}")
    assert response.status_code == 204

    # Verify it's deleted
    get_response = test_client.get(f"/books/{book_id}")
    assert get_response.status_code == 404

def test_pagination(test_client):
    """Test pagination functionality"""
    # Create multiple books
    for i in range(15):
        book_data = {
            "title": f"Book {i}",
            "author": f"Author {i}",
            "created_by": "test_user"
        }
        test_client.post("/books", json=book_data)

    # Test first page
    response = test_client.get("/books?skip=0&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5

    # Test second page
    response = test_client.get("/books?skip=5&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
