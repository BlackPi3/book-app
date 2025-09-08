#!/usr/bin/env python3
"""
Test script to verify MILESTONE 2.2: Repository Pattern Implementation
This script tests all CRUD operations and Repository Pattern principles.
"""

def test_repository_interface():
    """Test that the abstract interface is properly defined"""
    try:
        from backend.app.repositories import BookRepositoryInterface
        from abc import ABC

        # Verify it's an abstract base class
        assert issubclass(BookRepositoryInterface, ABC)

        # Verify all required methods are defined
        required_methods = [
            'create', 'get_by_id', 'get_all', 'update', 'delete',
            'search_by_title', 'search_by_author', 'get_by_created_by'
        ]

        for method in required_methods:
            assert hasattr(BookRepositoryInterface, method)

        print("✅ BookRepositoryInterface properly defined!")
        print(f"   Abstract methods: {required_methods}")
        return True

    except Exception as e:
        print(f"❌ Repository interface test failed: {e}")
        return False

def test_dependency_inversion_principle():
    """Test that the Repository Pattern follows Dependency Inversion Principle"""
    try:
        from backend.app.repositories import BookRepositoryInterface, SQLBookRepository

        # Verify SQLBookRepository implements the interface
        assert issubclass(SQLBookRepository, BookRepositoryInterface)

        # Test that we can treat SQLBookRepository as BookRepositoryInterface
        from backend.app.database import get_db
        db = next(get_db())

        # This demonstrates Dependency Inversion - we depend on abstraction
        repo: BookRepositoryInterface = SQLBookRepository(db)

        # We can call interface methods on the concrete implementation
        assert hasattr(repo, 'create')
        assert hasattr(repo, 'get_by_id')

        print("✅ Dependency Inversion Principle correctly implemented!")
        print("   ✓ High-level code can depend on BookRepositoryInterface")
        print("   ✓ SQLBookRepository implements the interface contract")

        db.close()
        return True

    except Exception as e:
        print(f"❌ Dependency Inversion test failed: {e}")
        return False

def test_crud_operations():
    """Test all CRUD operations through the repository"""
    try:
        from backend.app.repositories import SQLBookRepository
        from backend.app.models import Book
        from backend.app.database import get_db, create_tables

        # Create tables and get database session
        create_tables()
        db = next(get_db())
        repo = SQLBookRepository(db)

        # Test CREATE
        book_data = Book(
            title="Repository Pattern Test",
            author="Design Pattern Expert",
            created_by="Test System"
        )
        created_book = repo.create(book_data)
        assert created_book.id is not None
        print("✅ CREATE operation working!")

        # Test READ by ID
        found_book = repo.get_by_id(created_book.id)
        assert found_book is not None
        assert found_book.title == "Repository Pattern Test"
        print("✅ READ by ID operation working!")

        # Test UPDATE
        updated_book = repo.update(created_book.id, {
            "title": "Updated Repository Test",
            "author": "Updated Author"
        })
        assert updated_book.title == "Updated Repository Test"
        assert updated_book.author == "Updated Author"
        print("✅ UPDATE operation working!")

        # Test READ ALL
        all_books = repo.get_all()
        assert len(all_books) >= 1
        print(f"✅ READ ALL operation working! Found {len(all_books)} books")

        # Test DELETE
        delete_success = repo.delete(created_book.id)
        assert delete_success is True

        # Verify deletion
        deleted_book = repo.get_by_id(created_book.id)
        assert deleted_book is None
        print("✅ DELETE operation working!")

        db.close()
        return True

    except Exception as e:
        print(f"❌ CRUD operations test failed: {e}")
        return False

def test_search_functionality():
    """Test search operations"""
    try:
        from backend.app.repositories import SQLBookRepository
        from backend.app.models import Book
        from backend.app.database import get_db

        db = next(get_db())
        repo = SQLBookRepository(db)

        # Create test books for searching
        test_books = [
            Book(title="Python Programming", author="Guido van Rossum", created_by="Admin"),
            Book(title="Advanced Python", author="David Beazley", created_by="Admin"),
            Book(title="JavaScript Essentials", author="Douglas Crockford", created_by="User"),
        ]

        created_books = []
        for book in test_books:
            created_books.append(repo.create(book))

        # Test search by title
        python_books = repo.search_by_title("Python")
        assert len(python_books) >= 2
        print(f"✅ Search by title working! Found {len(python_books)} Python books")

        # Test search by author
        guido_books = repo.search_by_author("Guido")
        assert len(guido_books) >= 1
        print(f"✅ Search by author working! Found {len(guido_books)} books by Guido")

        # Test get by created_by
        admin_books = repo.get_by_created_by("Admin")
        assert len(admin_books) >= 2
        print(f"✅ Filter by created_by working! Found {len(admin_books)} admin books")

        # Clean up test data
        for book in created_books:
            repo.delete(book.id)

        db.close()
        return True

    except Exception as e:
        print(f"❌ Search functionality test failed: {e}")
        return False

def test_repository_benefits():
    """Test the benefits that Repository Pattern provides"""
    try:
        from backend.app.repositories import BookRepositoryInterface

        # Benefit 1: Easy to switch implementations
        # We could easily create MockBookRepository for testing
        class MockBookRepository(BookRepositoryInterface):
            def __init__(self):
                self.books = []
                self.next_id = 1

            def create(self, book):
                book.id = self.next_id
                self.next_id += 1
                self.books.append(book)
                return book

            def get_by_id(self, book_id):
                return next((b for b in self.books if b.id == book_id), None)

            def get_all(self, skip=0, limit=100):
                return self.books[skip:skip+limit]

            def update(self, book_id, book_update):
                book = self.get_by_id(book_id)
                if book:
                    for field, value in book_update.items():
                        setattr(book, field, value)
                return book

            def delete(self, book_id):
                book = self.get_by_id(book_id)
                if book:
                    self.books.remove(book)
                    return True
                return False

            def search_by_title(self, title):
                return [b for b in self.books if title.lower() in b.title.lower()]

            def search_by_author(self, author):
                return [b for b in self.books if author.lower() in b.author.lower()]

            def get_by_created_by(self, created_by):
                return [b for b in self.books if b.created_by == created_by]

        # Test that mock repository works the same way
        mock_repo: BookRepositoryInterface = MockBookRepository()

        from backend.app.models import Book
        test_book = Book(title="Mock Test", author="Test Author", created_by="Test")

        created = mock_repo.create(test_book)
        found = mock_repo.get_by_id(created.id)
        assert found.title == "Mock Test"

        print("✅ Repository Pattern benefits demonstrated!")
        print("   ✓ Easy to switch between SQL and Mock implementations")
        print("   ✓ Same interface works for different storage mechanisms")
        print("   ✓ Perfect for testing with mock data")

        return True

    except Exception as e:
        print(f"❌ Repository benefits test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing MILESTONE 2.2: Repository Pattern Implementation")
    print("=" * 75)

    # Run all tests
    interface_ok = test_repository_interface()
    print()
    dependency_ok = test_dependency_inversion_principle()
    print()
    crud_ok = test_crud_operations()
    print()
    search_ok = test_search_functionality()
    print()
    benefits_ok = test_repository_benefits()

    print("\n" + "=" * 75)
    if all([interface_ok, dependency_ok, crud_ok, search_ok, benefits_ok]):
        print("🎉 MILESTONE 2.2 SUCCESSFULLY COMPLETED!")
        print("✅ Abstract BookRepositoryInterface created")
        print("✅ Concrete SQLBookRepository implementation working")
        print("✅ All CRUD operations implemented (Create, Read, Update, Delete)")
        print("✅ Search by title functionality working")
        print("✅ Repository pattern properly abstracts data access")
        print("✅ Dependency Inversion Principle correctly applied")
        print("✅ Ready to proceed to MILESTONE 2.3: API Layer & FastAPI Setup")
    else:
        print("❌ MILESTONE 2.2 needs fixes before proceeding")
        print("Please review the failed tests above")
