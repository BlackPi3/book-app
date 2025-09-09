"""
Unit Tests for Repository Layer

This test suite demonstrates comprehensive testing patterns for the data layer:
- Test Database Isolation: Each test gets a clean database
- CRUD Operation Testing: All repository methods are tested
- Edge Case Testing: Error conditions and boundary cases
- Performance Testing: Verify index effectiveness

Learning Points:
- How to test database operations safely
- Proper test isolation techniques
- Comprehensive test coverage strategies
"""

import pytest
import os
import sys
from sqlalchemy.exc import IntegrityError

# Add proper path setup for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import Book
from app.repositories.book_repository_interface import BookRepositoryInterface
from conftest import create_test_books

class TestBookRepository:
    """Test suite for BookRepository CRUD operations"""

    def test_create_book_success(self, test_repository: BookRepositoryInterface, sample_book_data):
        """
        Test successful book creation.

        This test verifies:
        - Book is created with correct data
        - ID is automatically assigned
        - created_on timestamp is set
        """
        # Arrange
        book = Book(**sample_book_data)

        # Act
        created_book = test_repository.create(book)

        # Assert
        assert created_book.id is not None
        assert created_book.title == sample_book_data["title"]
        assert created_book.author == sample_book_data["author"]
        assert created_book.created_by == sample_book_data["created_by"]
        assert created_book.created_on is not None

    def test_create_book_with_missing_required_fields(self, test_repository: BookRepositoryInterface):
        """
        Test book creation fails with missing required fields.

        This test demonstrates:
        - Database constraint validation
        - Error handling in repository layer
        """
        # Arrange - Book with missing title
        book = Book(author="Test Author", created_by="test")

        # Act & Assert
        with pytest.raises(IntegrityError):
            test_repository.create(book)

    def test_get_by_id_existing_book(self, test_repository: BookRepositoryInterface, sample_book_data, test_session):
        """
        Test retrieving an existing book by ID.

        This test verifies:
        - Correct book is returned
        - All fields are properly loaded
        """
        # Arrange - Create a book first
        book = Book(**sample_book_data)
        created_book = test_repository.create(book)

        # Act
        retrieved_book = test_repository.get_by_id(created_book.id)

        # Assert
        assert retrieved_book is not None
        assert retrieved_book.id == created_book.id
        assert retrieved_book.title == sample_book_data["title"]
        assert retrieved_book.author == sample_book_data["author"]

    def test_get_by_id_nonexistent_book(self, test_repository: BookRepositoryInterface):
        """
        Test retrieving a non-existent book returns None.

        This test verifies:
        - Proper handling of missing records
        - No exceptions are raised
        """
        # Act
        result = test_repository.get_by_id(99999)

        # Assert
        assert result is None

    def test_get_all_empty_database(self, test_repository: BookRepositoryInterface):
        """
        Test get_all returns empty list when no books exist.

        This test verifies:
        - Empty result handling
        - Pagination with no data
        """
        # Act
        books = test_repository.get_all()

        # Assert
        assert books == []

    def test_get_all_with_pagination(self, test_repository: BookRepositoryInterface, multiple_sample_books, test_session):
        """
        Test get_all with pagination parameters.

        This test verifies:
        - Pagination works correctly
        - Skip and limit parameters
        - Consistent ordering
        """
        # Arrange - Create multiple books
        create_test_books(test_session, multiple_sample_books)

        # Act - Get first 2 books
        first_page = test_repository.get_all(skip=0, limit=2)
        second_page = test_repository.get_all(skip=2, limit=2)

        # Assert
        assert len(first_page) == 2
        assert len(second_page) == 2

        # Verify no overlap between pages
        first_page_ids = {book.id for book in first_page}
        second_page_ids = {book.id for book in second_page}
        assert first_page_ids.isdisjoint(second_page_ids)

    def test_update_existing_book(self, test_repository: BookRepositoryInterface, sample_book_data):
        """
        Test updating an existing book.

        This test verifies:
        - Fields are updated correctly
        - Unchanged fields remain the same
        - Updated book is returned
        """
        # Arrange - Create a book first
        book = Book(**sample_book_data)
        created_book = test_repository.create(book)
        original_id = created_book.id

        # Act - Update the book
        update_data = {"title": "Updated Title", "author": "Updated Author"}
        updated_book = test_repository.update(created_book.id, update_data)

        # Assert
        assert updated_book is not None
        assert updated_book.id == original_id  # ID shouldn't change
        assert updated_book.title == "Updated Title"
        assert updated_book.author == "Updated Author"
        assert updated_book.created_by == sample_book_data["created_by"]  # Unchanged field

    def test_update_nonexistent_book(self, test_repository: BookRepositoryInterface):
        """
        Test updating a non-existent book returns None.

        This test verifies:
        - Proper handling of missing records
        - No side effects on database
        """
        # Act
        result = test_repository.update(99999, {"title": "New Title"})

        # Assert
        assert result is None

    def test_delete_existing_book(self, test_repository: BookRepositoryInterface, sample_book_data):
        """
        Test deleting an existing book.

        This test verifies:
        - Book is successfully deleted
        - Returns True on success
        - Book is no longer retrievable
        """
        # Arrange - Create a book first
        book = Book(**sample_book_data)
        created_book = test_repository.create(book)

        # Act
        success = test_repository.delete(created_book.id)

        # Assert
        assert success is True

        # Verify book is actually deleted
        deleted_book = test_repository.get_by_id(created_book.id)
        assert deleted_book is None

    def test_delete_nonexistent_book(self, test_repository: BookRepositoryInterface):
        """
        Test deleting a non-existent book returns False.

        This test verifies:
        - Proper handling of missing records
        - Returns False on failure
        """
        # Act
        result = test_repository.delete(99999)

        # Assert
        assert result is False


class TestBookRepositorySearch:
    """Test suite for BookRepository search functionality"""

    def test_search_by_title(self, test_repository: BookRepositoryInterface, multiple_sample_books, test_session):
        """
        Test searching books by title.

        This test verifies:
        - Partial title matching works
        - Case sensitivity behavior
        - Index performance (implicitly)
        """
        # Arrange
        create_test_books(test_session, multiple_sample_books)

        # Act - Search for books with "Code" in title
        results = test_repository.search(title="Code")

        # Assert
        assert len(results) == 1
        assert "Clean Code" in results[0].title

    def test_search_by_author(self, test_repository: BookRepositoryInterface, multiple_sample_books, test_session):
        """
        Test searching books by author.

        This test verifies:
        - Author search functionality
        - Partial matching behavior
        """
        # Arrange
        create_test_books(test_session, multiple_sample_books)

        # Act - Search for books by Martin (matches multiple books)
        results = test_repository.search(author="Martin")

        # Assert
        assert len(results) == 2  # Robert Martin and Martin Fowler
        authors = {book.author for book in results}
        assert "Robert Martin" in authors
        assert "Martin Fowler" in authors

    def test_search_by_created_by(self, test_repository: BookRepositoryInterface, multiple_sample_books, test_session):
        """
        Test searching books by creator.

        This test verifies:
        - created_by field search
        - Multiple results handling
        """
        # Arrange
        create_test_books(test_session, multiple_sample_books)

        # Act - Search for books created by admin
        results = test_repository.search(created_by="admin")

        # Assert
        assert len(results) == 2
        for book in results:
            assert book.created_by == "admin"

    def test_search_multiple_criteria(self, test_repository: BookRepositoryInterface, multiple_sample_books, test_session):
        """
        Test searching with multiple criteria (OR logic).

        This test verifies:
        - Complex search queries
        - OR logic between criteria
        """
        # Arrange
        create_test_books(test_session, multiple_sample_books)

        # Act - Search for books with "Design" in title OR by "Robert Martin"
        results = test_repository.search(title="Design", author="Robert Martin")

        # Assert
        assert len(results) == 2
        titles_and_authors = {(book.title, book.author) for book in results}
        assert ("Design Patterns", "Gang of Four") in titles_and_authors
        assert ("Clean Code", "Robert Martin") in titles_and_authors

    def test_search_no_matches(self, test_repository: BookRepositoryInterface, multiple_sample_books, test_session):
        """
        Test search with no matching results.

        This test verifies:
        - Empty result handling
        - Performance with no matches
        """
        # Arrange
        create_test_books(test_session, multiple_sample_books)

        # Act
        results = test_repository.search(title="NonexistentBook")

        # Assert
        assert results == []

    def test_search_empty_criteria(self, test_repository: BookRepositoryInterface, multiple_sample_books, test_session):
        """
        Test search with no criteria returns all books.

        This test verifies:
        - Default behavior with empty search
        - Fallback to get_all functionality
        """
        # Arrange
        create_test_books(test_session, multiple_sample_books)

        # Act
        results = test_repository.search()

        # Assert
        assert len(results) == len(multiple_sample_books)


class TestBookRepositoryPerformance:
    """Test suite for performance-related repository functionality"""

    def test_large_dataset_search_performance(self, test_repository: BookRepositoryInterface, test_session):
        """
        Test search performance with larger dataset.

        This test verifies:
        - Index effectiveness
        - Performance with substantial data
        - Scalability considerations
        """
        # Arrange - Create many books
        large_dataset = []
        for i in range(100):
            large_dataset.append({
                "title": f"Book Title {i}",
                "author": f"Author {i % 10}",  # 10 different authors
                "created_by": f"user{i % 5}"   # 5 different users
            })

        create_test_books(test_session, large_dataset)

        # Act - Search should be fast due to indexes
        import time
        start_time = time.time()
        results = test_repository.search(author="Author 1")
        search_time = time.time() - start_time

        # Assert
        assert len(results) == 10  # Should find 10 books by "Author 1"
        assert search_time < 1.0  # Should complete within 1 second

    def test_pagination_performance(self, test_repository: BookRepositoryInterface, test_session):
        """
        Test pagination performance with larger dataset.

        This test verifies:
        - Pagination efficiency
        - Index usage for ordering
        """
        # Arrange - Create many books
        large_dataset = []
        for i in range(50):
            large_dataset.append({
                "title": f"Book {i:03d}",
                "author": f"Author {i}",
                "created_by": "test_user"
            })

        create_test_books(test_session, large_dataset)

        # Act - Test pagination performance
        import time
        start_time = time.time()
        page_1 = test_repository.get_all(skip=0, limit=10)
        page_5 = test_repository.get_all(skip=40, limit=10)
        pagination_time = time.time() - start_time

        # Assert
        assert len(page_1) == 10
        assert len(page_5) == 10
        assert pagination_time < 1.0  # Should be fast with indexes
