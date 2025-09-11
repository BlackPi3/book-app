#!/usr/bin/env python3
"""
Test script to verify MILESTONE 2.2: Repository Pattern Implementation
This script tests all CRUD operations and Repository Pattern principles.
"""

def test_repository_interface():
    """Test that the abstract interface is properly defined"""
    from app.repositories import BookRepositoryInterface
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

def test_dependency_inversion_principle():
    """Test that the Repository Pattern follows Dependency Inversion Principle"""
    from app.repositories import BookRepositoryInterface, SQLBookRepository

    # Verify SQLBookRepository implements the interface
    assert issubclass(SQLBookRepository, BookRepositoryInterface)

    # Test that we can treat SQLBookRepository as BookRepositoryInterface
    from app.database import get_db
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

def test_crud_operations():
    """Test all CRUD operations through the repository"""
    from app.repositories import SQLBookRepository
    from app.models import Book
    from app.database import get_db, create_tables

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

def test_search_functionality():
    """Test search operations"""
    from app.repositories import SQLBookRepository
    from app.models import Book
    from app.database import get_db

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

def test_repository_benefits():
    """Test the benefits that Repository Pattern provides"""
    from app.repositories import BookRepositoryInterface

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

        def search(self, title=None, author=None, created_by=None):
            results = []
            for book in self.books:
                if (title and title.lower() in book.title.lower()) or \
                   (author and author.lower() in book.author.lower()) or \
                   (created_by and created_by in book.created_by):
                    results.append(book)
            return results

        def search_by_title(self, title):
            return [b for b in self.books if title.lower() in b.title.lower()]

        def search_by_author(self, author):
            return [b for b in self.books if author.lower() in b.author.lower()]

        def get_by_created_by(self, created_by):
            return [b for b in self.books if b.created_by == created_by]

    # Test mock repository
    from app.models import Book
    mock_repo = MockBookRepository()

    # Same interface, different implementation
    test_book = Book(title="Mock Test", author="Test Author", created_by="Test")
    created = mock_repo.create(test_book)
    assert created.id == 1

    found = mock_repo.get_by_id(1)
    assert found.title == "Mock Test"

    print("✅ Repository Pattern benefits demonstrated!")
    print("   ✓ Easy to create different implementations")
    print("   ✓ Same interface for different storage backends")
    print("   ✓ Easier unit testing with mock implementations")

if __name__ == "__main__":
    print("🧪 Testing MILESTONE 2.2: Repository Pattern Implementation")
    print("=" * 70)

    # Run all tests with proper error handling
    try:
        test_repository_interface()
        interface_ok = True
    except Exception as e:
        print(f"❌ Repository interface test failed: {e}")
        interface_ok = False

    print()
    try:
        test_dependency_inversion_principle()
        dip_ok = True
    except Exception as e:
        print(f"❌ Dependency Inversion test failed: {e}")
        dip_ok = False

    print()
    try:
        test_crud_operations()
        crud_ok = True
    except Exception as e:
        print(f"❌ CRUD operations test failed: {e}")
        crud_ok = False

    print()
    try:
        test_search_functionality()
        search_ok = True
    except Exception as e:
        print(f"❌ Search functionality test failed: {e}")
        search_ok = False

    print()
    try:
        test_repository_benefits()
        benefits_ok = True
    except Exception as e:
        print(f"❌ Repository benefits test failed: {e}")
        benefits_ok = False

    print("\n" + "=" * 70)
    if all([interface_ok, dip_ok, crud_ok, search_ok, benefits_ok]):
        print("🎉 MILESTONE 2.2 SUCCESSFULLY COMPLETED!")
        print("✅ Repository Interface properly abstracted")
        print("✅ Dependency Inversion Principle implemented")
        print("✅ All CRUD operations working through repository")
        print("✅ Search functionality implemented")
        print("✅ Repository Pattern benefits demonstrated")
        print("✅ Ready to proceed to MILESTONE 2.3")
    else:
        print("❌ MILESTONE 2.2 needs fixes before proceeding")
        if not interface_ok:
            print("   ❌ Repository interface issues")
        if not dip_ok:
            print("   ❌ Dependency Inversion issues")
        if not crud_ok:
            print("   ❌ CRUD operations issues")
        if not search_ok:
            print("   ❌ Search functionality issues")
        if not benefits_ok:
            print("   ❌ Repository benefits issues")
