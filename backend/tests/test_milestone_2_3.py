#!/usr/bin/env python3
"""
Test script to verify MILESTONE 2.3: API Layer & FastAPI Setup
This script tests all REST endpoints and FastAPI functionality using TestClient.
"""

import pytest
import os
import sys
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Add proper path setup for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.main import app, get_book_repository
from backend.app.models import Base
from backend.app.repositories.sql_book_repository import SQLBookRepository


@pytest.fixture(scope="function")
def test_client():
    """Create a test client for milestone testing"""
    # Create shared in-memory database for this test
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

    Base.metadata.create_all(bind=test_engine)
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    def get_test_repository():
        """Create a test repository with shared database"""
        db = TestSessionLocal()
        return SQLBookRepository(db)

    # Override the dependency with shared database
    app.dependency_overrides[get_book_repository] = get_test_repository

    client = TestClient(app)
    yield client

    # Cleanup
    app.dependency_overrides.clear()


def test_api_server(test_client):
    """Test that the API server is running"""
    response = test_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "BookApp API" in data["message"]
    print("✅ API server is running and responding!")


def test_swagger_docs():
    """Test that Swagger documentation is accessible"""
    # Note: TestClient doesn't render HTML, so we just check the OpenAPI schema
    client = TestClient(app)
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "openapi" in schema
    assert "info" in schema
    assert schema["info"]["title"] == "BookApp API"
    print("✅ OpenAPI schema is accessible!")


def test_create_book_endpoint(test_client):
    """Test POST /books endpoint"""
    book_data = {
        "title": "Test Book for Milestone 2.3",
        "author": "Milestone Test Author",
        "created_by": "milestone_test"
    }

    response = test_client.post("/books", json=book_data)
    assert response.status_code == 201

    data = response.json()
    assert data["title"] == book_data["title"]
    assert data["author"] == book_data["author"]
    assert "id" in data
    print("✅ POST /books endpoint working!")


def test_get_books_endpoint(test_client):
    """Test GET /books endpoint"""
    # First create a book
    book_data = {
        "title": "Get Test Book",
        "author": "Get Test Author",
        "created_by": "get_test"
    }
    test_client.post("/books", json=book_data)

    # Then get all books
    response = test_client.get("/books")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    print("✅ GET /books endpoint working!")


def test_get_book_by_id_endpoint(test_client):
    """Test GET /books/{id} endpoint"""
    # Create a book first
    book_data = {
        "title": "ID Test Book",
        "author": "ID Test Author",
        "created_by": "id_test"
    }
    create_response = test_client.post("/books", json=book_data)
    book_id = create_response.json()["id"]

    # Get the book by ID
    response = test_client.get(f"/books/{book_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == book_id
    assert data["title"] == book_data["title"]
    print("✅ GET /books/{id} endpoint working!")


def test_update_book_endpoint(test_client):
    """Test PUT /books/{id} endpoint"""
    # Create a book first
    book_data = {
        "title": "Update Test Book",
        "author": "Update Test Author",
        "created_by": "update_test"
    }
    create_response = test_client.post("/books", json=book_data)
    book_id = create_response.json()["id"]

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
    print("✅ PUT /books/{id} endpoint working!")


def test_delete_book_endpoint(test_client):
    """Test DELETE /books/{id} endpoint"""
    # Create a book first
    book_data = {
        "title": "Delete Test Book",
        "author": "Delete Test Author",
        "created_by": "delete_test"
    }
    create_response = test_client.post("/books", json=book_data)
    book_id = create_response.json()["id"]

    # Delete the book
    response = test_client.delete(f"/books/{book_id}")
    assert response.status_code == 204

    # Verify it's deleted
    get_response = test_client.get(f"/books/{book_id}")
    assert get_response.status_code == 404
    print("✅ DELETE /books/{id} endpoint working!")


def test_search_functionality(test_client):
    """Test search query parameters"""
    # Create test books
    books_data = [
        {"title": "Python Guide", "author": "Python Author", "created_by": "search_test"},
        {"title": "Java Guide", "author": "Java Author", "created_by": "search_test"},
        {"title": "Python Advanced", "author": "Advanced Author", "created_by": "search_test"}
    ]

    for book_data in books_data:
        test_client.post("/books", json=book_data)

    # Test title search
    response = test_client.get("/books?title=Python")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2  # Should find at least 2 Python books
    print("✅ Search functionality working!")


def test_pagination(test_client):
    """Test pagination parameters"""
    # Create multiple books
    for i in range(10):
        book_data = {
            "title": f"Pagination Book {i}",
            "author": f"Author {i}",
            "created_by": "pagination_test"
        }
        test_client.post("/books", json=book_data)

    # Test pagination
    response = test_client.get("/books?skip=0&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    print("✅ Pagination working!")


def test_validation_errors(test_client):
    """Test input validation"""
    # Test missing required fields
    invalid_data = {"title": "Missing Author"}
    response = test_client.post("/books", json=invalid_data)
    assert response.status_code == 422  # Validation error
    print("✅ Input validation working!")


def run_milestone_2_3_tests():
    """Run all milestone 2.3 tests"""
    print("🎯 MILESTONE 2.3 TEST SUITE")
    print("=" * 50)
    print("API Layer & FastAPI Setup")
    print()

    # Create test client with shared in-memory database
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

    Base.metadata.create_all(bind=test_engine)
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    def get_test_repository():
        db = TestSessionLocal()
        return SQLBookRepository(db)

    app.dependency_overrides[get_book_repository] = get_test_repository
    client = TestClient(app)

    try:
        test_api_server(client)
        test_swagger_docs()
        test_create_book_endpoint(client)
        test_get_books_endpoint(client)
        test_get_book_by_id_endpoint(client)
        test_update_book_endpoint(client)
        test_delete_book_endpoint(client)
        test_search_functionality(client)
        test_pagination(client)
        test_validation_errors(client)

        print()
        print("🎉 MILESTONE 2.3 COMPLETED SUCCESSFULLY!")
        print("✅ All API endpoints working correctly")
        print("✅ FastAPI setup complete")
        print("✅ REST principles implemented")
        print("✅ Dependency injection working")
        print("✅ Input validation active")
        print("✅ Search and pagination functional")

    except Exception as e:
        print(f"❌ MILESTONE 2.3 INCOMPLETE: {e}")
    finally:
        app.dependency_overrides.clear()


if __name__ == "__main__":
    run_milestone_2_3_tests()
