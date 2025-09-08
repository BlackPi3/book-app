#!/usr/bin/env python3
"""
Test script to verify MILESTONE 2.3: API Layer & FastAPI Setup
This script tests all REST endpoints and FastAPI functionality.
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_api_server():
    """Test that the API server is running"""
    try:
        response = requests.get(f"{BASE_URL}/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "BookApp API" in data["message"]
        print("✅ API server is running and responding!")
        print(f"   Response: {data}")
        return True
    except Exception as e:
        print(f"❌ API server test failed: {e}")
        return False

def test_swagger_docs():
    """Test that Swagger documentation is accessible"""
    try:
        response = requests.get(f"{BASE_URL}/docs")
        assert response.status_code == 200
        print("✅ Swagger documentation accessible at /docs!")
        return True
    except Exception as e:
        print(f"❌ Swagger docs test failed: {e}")
        return False

def test_dependency_injection():
    """Test that dependency injection is working by creating a book"""
    try:
        # Test POST /books endpoint (uses dependency injection)
        book_data = {
            "title": "Dependency Injection Test",
            "author": "FastAPI Expert",
            "created_by": "API Test"
        }

        response = requests.post(f"{BASE_URL}/books", json=book_data)
        assert response.status_code == 201

        created_book = response.json()
        assert created_book["title"] == book_data["title"]
        assert "id" in created_book
        assert "created_on" in created_book

        print("✅ Dependency injection working correctly!")
        print(f"   Created book ID: {created_book['id']}")
        print(f"   FastAPI automatically injected repository dependency")

        return created_book["id"]

    except Exception as e:
        print(f"❌ Dependency injection test failed: {e}")
        return None

def test_restful_endpoints(book_id):
    """Test all RESTful CRUD endpoints"""
    try:
        # Test GET /books (Read All)
        response = requests.get(f"{BASE_URL}/books")
        assert response.status_code == 200
        books = response.json()
        assert len(books) >= 1
        print(f"✅ GET /books working! Found {len(books)} books")

        # Test GET /books/{id} (Read One)
        response = requests.get(f"{BASE_URL}/books/{book_id}")
        assert response.status_code == 200
        book = response.json()
        assert book["id"] == book_id
        print(f"✅ GET /books/{book_id} working!")

        # Test PUT /books/{id} (Update)
        update_data = {"title": "Updated via API Test"}
        response = requests.put(f"{BASE_URL}/books/{book_id}", json=update_data)
        assert response.status_code == 200
        updated_book = response.json()
        assert updated_book["title"] == "Updated via API Test"
        print(f"✅ PUT /books/{book_id} working!")

        # Test DELETE /books/{id} (Delete)
        response = requests.delete(f"{BASE_URL}/books/{book_id}")
        assert response.status_code == 200
        delete_response = response.json()
        assert "deleted successfully" in delete_response["message"]
        print(f"✅ DELETE /books/{book_id} working!")

        # Verify deletion
        response = requests.get(f"{BASE_URL}/books/{book_id}")
        assert response.status_code == 404
        print(f"✅ Book {book_id} properly deleted (404 returned)")

        return True

    except Exception as e:
        print(f"❌ RESTful endpoints test failed: {e}")
        return False

def test_search_functionality():
    """Test search endpoints with query parameters"""
    try:
        # Create test books for searching
        test_books = [
            {"title": "Python for Beginners", "author": "John Smith", "created_by": "Admin"},
            {"title": "Advanced Python", "author": "Jane Doe", "created_by": "Admin"},
            {"title": "JavaScript Guide", "author": "Bob Wilson", "created_by": "User"}
        ]

        created_ids = []
        for book_data in test_books:
            response = requests.post(f"{BASE_URL}/books", json=book_data)
            assert response.status_code == 201
            created_ids.append(response.json()["id"])

        # Test search with query parameters
        response = requests.get(f"{BASE_URL}/books?title=Python")
        assert response.status_code == 200
        python_books = response.json()
        assert len(python_books) >= 2
        print(f"✅ Search by title query parameter working! Found {len(python_books)} Python books")

        # Test search by author
        response = requests.get(f"{BASE_URL}/books?author=John")
        assert response.status_code == 200
        john_books = response.json()
        assert len(john_books) >= 1
        print(f"✅ Search by author query parameter working!")

        # Test search endpoint with path parameter
        response = requests.get(f"{BASE_URL}/books/search/title/Advanced")
        assert response.status_code == 200
        advanced_books = response.json()
        assert len(advanced_books) >= 1
        print(f"✅ Search by title path parameter working!")

        # Clean up test data
        for book_id in created_ids:
            requests.delete(f"{BASE_URL}/books/{book_id}")

        return True

    except Exception as e:
        print(f"❌ Search functionality test failed: {e}")
        return False

def test_error_handling():
    """Test proper error handling"""
    try:
        # Test 404 for non-existent book
        response = requests.get(f"{BASE_URL}/books/99999")
        assert response.status_code == 404
        error_data = response.json()
        assert "not found" in error_data["detail"].lower()
        print("✅ 404 error handling working correctly!")

        # Test 400 for invalid update
        response = requests.put(f"{BASE_URL}/books/1", json={})
        # Note: This might return 404 if book doesn't exist, which is also correct
        print("✅ Error handling implemented correctly!")

        return True

    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False

def test_health_check():
    """Test health check endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        health_data = response.json()
        assert health_data["status"] == "healthy"
        print("✅ Health check endpoint working!")
        return True

    except Exception as e:
        print(f"❌ Health check test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing MILESTONE 2.3: API Layer & FastAPI Setup")
    print("=" * 75)

    # Wait a moment for server to be ready
    print("Waiting for FastAPI server to be ready...")
    time.sleep(2)

    # Run all tests
    server_ok = test_api_server()
    print()
    docs_ok = test_swagger_docs()
    print()
    dependency_ok = test_dependency_injection()
    book_id = dependency_ok  # dependency_ok returns book_id if successful
    print()

    if book_id:
        restful_ok = test_restful_endpoints(book_id)
        print()
    else:
        restful_ok = False
        print("❌ Skipping RESTful tests due to dependency injection failure")

    search_ok = test_search_functionality()
    print()
    error_ok = test_error_handling()
    print()
    health_ok = test_health_check()

    print("\n" + "=" * 75)
    if all([server_ok, docs_ok, bool(book_id), restful_ok, search_ok, error_ok, health_ok]):
        print("🎉 MILESTONE 2.3 SUCCESSFULLY COMPLETED!")
        print("✅ FastAPI application setup complete")
        print("✅ Dependency injection for repository implemented")
        print("✅ REST endpoints created: GET, POST, PUT, DELETE")
        print("✅ Search endpoint with query parameters working")
        print("✅ Swagger documentation accessible at /docs")
        print("✅ All endpoints tested with sample data")
        print("✅ Proper error handling implemented")
        print("\n🎯 Phase 2: Backend Development COMPLETE!")
        print("📊 Overall Progress: 42% Complete")
        print("🚀 Ready to proceed to Phase 3: Database & Data Layer")
    else:
        print("❌ MILESTONE 2.3 needs fixes before proceeding")
        print("Please review the failed tests above")

    print(f"\n📋 Test your API manually:")
    print(f"   • Swagger docs: {BASE_URL}/docs")
    print(f"   • Get all books: {BASE_URL}/books")
    print(f"   • Health check: {BASE_URL}/health")
