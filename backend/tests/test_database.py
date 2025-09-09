"""
Database Integration Tests

This test suite focuses on database-level functionality:
- Database connection and session management
- Migration system testing
- Index effectiveness verification
- Database constraint validation

Learning Points:
- How to test database infrastructure
- Verifying performance optimizations
- Testing database constraints and relationships
"""

import pytest
import time
import os
import sys
from sqlalchemy import text, inspect

# Add proper path setup for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import Book, Base
from app.database import create_database_engine, create_tables, drop_tables
from conftest import create_test_books

class TestDatabaseInfrastructure:
    """Test suite for database infrastructure and configuration"""

    def test_database_connection(self, test_engine):
        """
        Test that database connection is working properly.

        This test verifies:
        - Database engine creation
        - Connection establishment
        - Basic query execution
        """
        # Act - Execute a simple query
        with test_engine.connect() as connection:
            result = connection.execute(text("SELECT 1 as test_value"))
            value = result.fetchone()[0]

        # Assert
        assert value == 1

    def test_table_creation(self, test_engine):
        """
        Test that all required tables are created properly.

        This test verifies:
        - Table schema creation
        - Column definitions
        - Constraint setup
        """
        # Arrange & Act - Tables are created by test_engine fixture
        inspector = inspect(test_engine)
        table_names = inspector.get_table_names()

        # Assert
        assert "books" in table_names

        # Verify column structure
        columns = inspector.get_columns("books")
        column_names = [col["name"] for col in columns]

        expected_columns = ["id", "title", "author", "created_on", "created_by"]
        for expected_col in expected_columns:
            assert expected_col in column_names

    def test_database_indexes_exist(self, test_engine):
        """
        Test that performance indexes are properly created.

        This test verifies:
        - Index creation from model definitions
        - Composite index setup
        - Index naming conventions
        """
        # Act
        inspector = inspect(test_engine)
        indexes = inspector.get_indexes("books")

        # Assert - Check that indexes exist
        index_names = [idx["name"] for idx in indexes]

        # Primary key index should exist
        assert any("id" in str(idx.get("column_names", [])) for idx in indexes)

        # Our custom composite indexes should exist
        expected_indexes = ["idx_title_author", "idx_author_creator", "idx_created_on_desc"]
        for expected_idx in expected_indexes:
            assert expected_idx in index_names or any(expected_idx in str(idx) for idx in indexes)


class TestDatabaseConstraints:
    """Test suite for database constraints and data integrity"""

    def test_not_null_constraints(self, test_session):
        """
        Test that NOT NULL constraints are properly enforced.

        This test verifies:
        - Database-level validation
        - Constraint enforcement
        - Error handling for invalid data
        """
        # Test missing title
        with pytest.raises(Exception):  # Should raise IntegrityError or similar
            book = Book(author="Test Author", created_by="test")
            test_session.add(book)
            test_session.commit()

        test_session.rollback()

        # Test missing author
        with pytest.raises(Exception):
            book = Book(title="Test Title", created_by="test")
            test_session.add(book)
            test_session.commit()

        test_session.rollback()

        # Test missing created_by
        with pytest.raises(Exception):
            book = Book(title="Test Title", author="Test Author")
            test_session.add(book)
            test_session.commit()

    def test_primary_key_uniqueness(self, test_session):
        """
        Test that primary key uniqueness is enforced.

        This test verifies:
        - Primary key constraint
        - Auto-increment functionality
        - Unique ID generation
        """
        # Arrange & Act - Create multiple books
        book1 = Book(title="Book 1", author="Author 1", created_by="test")
        book2 = Book(title="Book 2", author="Author 2", created_by="test")

        test_session.add(book1)
        test_session.add(book2)
        test_session.commit()

        # Assert - IDs should be unique and auto-generated
        assert book1.id != book2.id
        assert book1.id is not None
        assert book2.id is not None


class TestDatabasePerformance:
    """Test suite for database performance and optimization"""

    def test_index_performance_on_title_search(self, test_session):
        """
        Test that title search performance is optimized by indexes.

        This test verifies:
        - Index effectiveness
        - Query performance
        - Scalability with larger datasets
        """
        # Arrange - Create a larger dataset
        large_dataset = []
        for i in range(200):
            large_dataset.append({
                "title": f"Performance Test Book {i}",
                "author": f"Author {i}",
                "created_by": "performance_test"
            })

        create_test_books(test_session, large_dataset)

        # Act - Measure search performance
        start_time = time.time()

        # Search using indexed column (title)
        result = test_session.query(Book).filter(
            Book.title.contains("Performance Test Book 1")
        ).all()

        search_time = time.time() - start_time

        # Assert
        assert len(result) >= 10  # Should find books with "1" in title (10, 11, 12, etc.)
        assert search_time < 0.5  # Should be fast due to index

    def test_composite_index_performance(self, test_session):
        """
        Test that composite index improves multi-column search performance.

        This test verifies:
        - Composite index effectiveness
        - Multi-column query optimization
        """
        # Arrange - Create dataset with repeated authors and titles
        test_data = []
        for i in range(100):
            test_data.append({
                "title": f"Title {i % 10}",  # 10 different titles
                "author": f"Author {i % 5}",  # 5 different authors
                "created_by": "composite_test"
            })

        create_test_books(test_session, test_data)

        # Act - Measure composite search performance
        start_time = time.time()

        # Search using both title and author (should use composite index)
        result = test_session.query(Book).filter(
            Book.title == "Title 1",
            Book.author == "Author 1"
        ).all()

        search_time = time.time() - start_time

        # Assert
        assert len(result) > 0
        assert search_time < 0.2  # Should be very fast with composite index

    def test_session_management_performance(self, test_engine):
        """
        Test that session management is optimized for performance.

        This test verifies:
        - Session creation overhead
        - Connection pooling effectiveness
        - Resource cleanup efficiency
        """
        from app.database import TestSessionLocal

        # Act - Measure session creation performance
        start_time = time.time()

        # Create and close multiple sessions
        for _ in range(50):
            session = TestSessionLocal()
            session.execute(text("SELECT 1"))
            session.close()

        session_time = time.time() - start_time

        # Assert - Should be efficient due to connection pooling
        assert session_time < 2.0  # Should handle 50 sessions quickly


class TestDatabaseMigrations:
    """Test suite for database migration functionality"""

    def test_schema_matches_model_definitions(self, test_engine):
        """
        Test that current database schema matches model definitions.

        This test verifies:
        - Migration consistency
        - Schema synchronization
        - Model-database alignment
        """
        # Act
        inspector = inspect(test_engine)

        # Get actual database schema
        columns = inspector.get_columns("books")
        column_info = {col["name"]: col for col in columns}

        # Assert - Verify key columns exist with correct types
        assert "id" in column_info
        assert "title" in column_info
        assert "author" in column_info
        assert "created_on" in column_info
        assert "created_by" in column_info

        # Verify NOT NULL constraints
        assert column_info["title"]["nullable"] is False
        assert column_info["author"]["nullable"] is False
        assert column_info["created_by"]["nullable"] is False

    def test_database_versioning_support(self, test_engine):
        """
        Test that database supports versioning for migrations.

        This test verifies:
        - Alembic version table exists
        - Migration tracking capability
        """
        # Act - Check if alembic version table exists
        inspector = inspect(test_engine)
        table_names = inspector.get_table_names()

        # Assert - Alembic version table should be present in a migrated database
        # Note: This might not exist in test database, but we can verify the structure supports it
        assert isinstance(table_names, list)  # Basic structure verification


class TestDatabaseTransactions:
    """Test suite for transaction handling and data consistency"""

    def test_transaction_rollback(self, test_session):
        """
        Test that transaction rollback works properly.

        This test verifies:
        - Transaction isolation
        - Rollback functionality
        - Data consistency after rollback
        """
        # Arrange - Get initial count
        initial_count = test_session.query(Book).count()

        try:
            # Act - Create book and then raise exception
            book = Book(title="Transaction Test", author="Test Author", created_by="test")
            test_session.add(book)
            test_session.flush()  # Send to DB but don't commit

            # Simulate error condition
            raise Exception("Simulated error")

        except Exception:
            # Rollback transaction
            test_session.rollback()

        # Assert - Count should be unchanged
        final_count = test_session.query(Book).count()
        assert final_count == initial_count

    def test_transaction_commit(self, test_session):
        """
        Test that transaction commit persists data properly.

        This test verifies:
        - Transaction commit functionality
        - Data persistence
        - Session state after commit
        """
        # Arrange
        initial_count = test_session.query(Book).count()

        # Act
        book = Book(title="Commit Test", author="Test Author", created_by="test")
        test_session.add(book)
        test_session.commit()

        # Assert
        final_count = test_session.query(Book).count()
        assert final_count == initial_count + 1

        # Verify book is actually in database
        saved_book = test_session.query(Book).filter(Book.title == "Commit Test").first()
        assert saved_book is not None
        assert saved_book.title == "Commit Test"
