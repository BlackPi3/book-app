"""
Database Seeding Script for BookApp

This script demonstrates the Seeding Pattern - a way to populate the database
with initial or sample data. This is different from migrations which handle
schema changes.

Learning Points:
- Seeding vs Migration: Migrations change schema, seeds populate data
- Idempotent seeding: Can be run multiple times safely
- Separation of concerns: Seed data is separate from business logic
"""

import sys
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Add the parent directory to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import using relative imports from the current directory
from models import Book
from database import DATABASE_URL

def create_sample_books():
    """
    Create sample book data for development and testing.

    This demonstrates the Factory Pattern - creating objects
    with predefined configurations.
    """
    sample_books = [
        {
            "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
            "author": "Robert C. Martin",
            "created_by": "System"
        },
        {
            "title": "Design Patterns: Elements of Reusable Object-Oriented Software",
            "author": "Gang of Four",
            "created_by": "System"
        },
        {
            "title": "The Pragmatic Programmer",
            "author": "David Thomas, Andrew Hunt",
            "created_by": "System"
        },
        {
            "title": "Refactoring: Improving the Design of Existing Code",
            "author": "Martin Fowler",
            "created_by": "System"
        },
        {
            "title": "Domain-Driven Design: Tackling Complexity in the Heart of Software",
            "author": "Eric Evans",
            "created_by": "System"
        },
        {
            "title": "Patterns of Enterprise Application Architecture",
            "author": "Martin Fowler",
            "created_by": "System"
        },
        {
            "title": "Building Microservices: Designing Fine-Grained Systems",
            "author": "Sam Newman",
            "created_by": "System"
        },
        {
            "title": "You Don't Know JS: Scope & Closures",
            "author": "Kyle Simpson",
            "created_by": "System"
        }
    ]

    return [Book(**book_data) for book_data in sample_books]

def seed_database():
    """
    Main seeding function that populates the database with sample data.

    This function demonstrates:
    - Database session management
    - Idempotent operations (safe to run multiple times)
    - Bulk data insertion
    """

    # Create engine and session
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = SessionLocal()

    try:
        print("🌱 Starting database seeding...")

        # Check if we already have books to avoid duplicates
        existing_books_count = db.query(Book).count()

        if existing_books_count > 0:
            print(f"📚 Database already contains {existing_books_count} books.")
            print("🔄 Clearing existing data for fresh seeding...")
            # Clear existing books for fresh seeding
            db.query(Book).delete()
            db.commit()

        # Create and insert sample books
        sample_books = create_sample_books()

        print(f"📖 Adding {len(sample_books)} sample books...")
        for book in sample_books:
            db.add(book)
            print(f"   ✅ Added: '{book.title}' by {book.author}")

        # Commit all changes
        db.commit()

        print(f"🎉 Database seeding completed successfully!")
        print(f"📊 Total books in database: {db.query(Book).count()}")

    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        db.rollback()
        raise

    finally:
        db.close()

if __name__ == "__main__":
    # This allows the script to be run directly: python app/seed.py
    print("🚀 BookApp Database Seeding")
    print("=" * 40)
    seed_database()
