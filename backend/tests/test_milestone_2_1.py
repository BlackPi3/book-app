#!/usr/bin/env python3
"""
Test script to verify MILESTONE 2.1 completion
This script tests the complete data layer implementation.
"""

def test_database_connection():
    """Test database connection and table creation"""
    from backend.app.database import create_tables, get_db

    # Create tables
    create_tables()
    print("✅ Database tables created successfully!")

    # Test database session factory
    db_gen = get_db()
    db = next(db_gen)
    print("✅ Database session factory working!")

    # Clean up
    db.close()
    assert True  # Test passed

def test_sqlalchemy_models():
    """Test SQLAlchemy Book model"""
    from backend.app.models import Book
    from backend.app.database import get_db

    # Get database session
    db = next(get_db())

    # Create a book using SQLAlchemy model
    book = Book(
        title="SQLAlchemy Test Book",
        author="Database Expert",
        created_by="Test System"
    )

    # Save to database
    db.add(book)
    db.commit()
    db.refresh(book)

    # Test that book was saved with ID
    assert book.id is not None
    assert book.title == "SQLAlchemy Test Book"
    assert book.created_on is not None

    print("✅ SQLAlchemy Book model working correctly!")
    print(f"   Created book: {book}")
    print(f"   Book ID: {book.id}")
    print(f"   Created on: {book.created_on}")

    db.close()

def test_pydantic_schemas():
    """Test Pydantic schemas for validation and serialization"""
    from backend.app.schemas import BookCreate, BookResponse, BookUpdate, BookSearch
    from datetime import datetime

    # Test BookCreate schema validation
    book_data = {
        "title": "Pydantic Test Book",
        "author": "Schema Expert",
        "created_by": "Validation System"
    }

    book_create = BookCreate(**book_data)
    assert book_create.title == "Pydantic Test Book"
    print("✅ BookCreate schema validation working!")

    # Test BookResponse schema serialization
    response_data = {
        "id": 1,
        "title": "Response Test",
        "author": "API Expert",
        "created_on": datetime.now(),
        "created_by": "Response System"
    }

    book_response = BookResponse(**response_data)
    assert book_response.id == 1
    print("✅ BookResponse schema serialization working!")

    # Test BookUpdate schema (optional fields)
    update_data = {"title": "Updated Title"}
    book_update = BookUpdate(**update_data)
    assert book_update.title == "Updated Title"
    assert book_update.author is None
    print("✅ BookUpdate schema with optional fields working!")

    # Test BookSearch schema
    search_data = {"title": "search term"}
    book_search = BookSearch(**search_data)
    assert book_search.title == "search term"
    print("✅ BookSearch schema working!")

def test_factory_pattern():
    """Test that the Factory Pattern is properly implemented"""
    from backend.app.database import SessionLocal, get_db

    # Test SessionLocal factory
    session1 = SessionLocal()
    session2 = SessionLocal()

    # Should be different instances
    assert session1 is not session2
    print("✅ SessionLocal factory creates different instances!")

    # Test get_db generator function
    db_gen1 = get_db()
    db_gen2 = get_db()

    db1 = next(db_gen1)
    db2 = next(db_gen2)

    # Should be different sessions
    assert db1 is not db2
    print("✅ get_db() factory function working correctly!")

    # Clean up
    session1.close()
    session2.close()
    db1.close()
    db2.close()

def test_milestone_2_1_integration():
    """Test the complete integration: SQLAlchemy + Pydantic + Database"""
    from backend.app.models import Book
    from backend.app.schemas import BookCreate, BookResponse
    from backend.app.database import get_db

    # Step 1: Create book using Pydantic schema
    book_data = BookCreate(
        title="Integration Test Book",
        author="Full Stack Developer",
        created_by="Integration Test"
    )

    # Step 2: Convert to SQLAlchemy model
    db = next(get_db())
    book = Book(**book_data.model_dump())

    # Step 3: Save to database
    db.add(book)
    db.commit()
    db.refresh(book)

    # Step 4: Convert back to Pydantic for response
    book_response = BookResponse.model_validate(book)

    # Verify the full cycle works
    assert book_response.title == "Integration Test Book"
    assert book_response.id is not None
    assert book_response.created_on is not None

    print("✅ Full SQLAlchemy ↔ Pydantic integration working!")
    print(f"   Book Response: {book_response.model_dump()}")

    db.close()

if __name__ == "__main__":
    print("🧪 Testing MILESTONE 2.1: Data Layer Implementation")
    print("=" * 70)

    # Run all tests with proper error handling
    try:
        test_database_connection()
        db_ok = True
    except Exception as e:
        print(f"❌ Database connection test failed: {e}")
        db_ok = False

    print()
    try:
        test_sqlalchemy_models()
        models_ok = True
    except Exception as e:
        print(f"❌ SQLAlchemy model test failed: {e}")
        models_ok = False

    print()
    try:
        test_pydantic_schemas()
        schemas_ok = True
    except Exception as e:
        print(f"❌ Pydantic schema test failed: {e}")
        schemas_ok = False

    print()
    try:
        test_factory_pattern()
        factory_ok = True
    except Exception as e:
        print(f"❌ Factory Pattern test failed: {e}")
        factory_ok = False

    print()
    try:
        test_milestone_2_1_integration()
        integration_ok = True
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        integration_ok = False

    print("\n" + "=" * 70)
    if all([db_ok, models_ok, schemas_ok, factory_ok, integration_ok]):
        print("🎉 MILESTONE 2.1 SUCCESSFULLY COMPLETED!")
        print("✅ Database connection and table creation working")
        print("✅ SQLAlchemy models properly implemented")
        print("✅ Pydantic schemas for validation/serialization")
        print("✅ Factory Pattern implemented correctly")
        print("✅ Full integration cycle working")
        print("✅ Ready to proceed to MILESTONE 2.2")
    else:
        print("❌ MILESTONE 2.1 needs fixes before proceeding")
        if not db_ok:
            print("   ❌ Database connection issues")
        if not models_ok:
            print("   ❌ SQLAlchemy model issues")
        if not schemas_ok:
            print("   ❌ Pydantic schema issues")
        if not factory_ok:
            print("   ❌ Factory Pattern issues")
        if not integration_ok:
            print("   ❌ Integration issues")
