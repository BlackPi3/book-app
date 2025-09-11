from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from .book_repository_interface import BookRepositoryInterface
from app.models import Book

class SQLBookRepository(BookRepositoryInterface):
    """
    Concrete implementation of BookRepositoryInterface using SQLAlchemy.

    This class implements the Repository Pattern - it encapsulates the logic
    needed to access data sources, centralizing common data access functionality
    and providing better maintainability and decoupling.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, book: Book) -> Book:
        """Create a new book in the database"""
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book

    def get_by_id(self, book_id: int) -> Optional[Book]:
        """Get a book by its ID"""
        return self.db.query(Book).filter(Book.id == book_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Book]:
        """Get all books with pagination"""
        return self.db.query(Book).offset(skip).limit(limit).all()

    def update(self, book_id: int, book_update: dict) -> Optional[Book]:
        """Update an existing book"""
        book = self.get_by_id(book_id)
        if not book:
            return None

        # Update only provided fields
        for field, value in book_update.items():
            if hasattr(book, field) and value is not None:
                setattr(book, field, value)

        self.db.commit()
        self.db.refresh(book)
        return book

    def delete(self, book_id: int) -> bool:
        """Delete a book by ID"""
        book = self.get_by_id(book_id)
        if not book:
            return False

        self.db.delete(book)
        self.db.commit()
        return True

    def search(self, title: Optional[str] = None, author: Optional[str] = None, created_by: Optional[str] = None) -> List[Book]:
        """Search books by title, author, or created_by with partial matching"""
        query = self.db.query(Book)

        # Build dynamic search conditions
        conditions = []

        if title:
            conditions.append(Book.title.contains(title))

        if author:
            conditions.append(Book.author.contains(author))

        if created_by:
            conditions.append(Book.created_by.contains(created_by))

        # Apply search conditions with OR logic
        if conditions:
            query = query.filter(or_(*conditions))

        return query.all()

    def search_by_title(self, title: str) -> List[Book]:
        """Search books by title"""
        return self.db.query(Book).filter(Book.title.contains(title)).all()

    def search_by_author(self, author: str) -> List[Book]:
        """Search books by author"""
        return self.db.query(Book).filter(Book.author.contains(author)).all()

    def get_by_created_by(self, created_by: str) -> List[Book]:
        """Get books by creator"""
        return self.db.query(Book).filter(Book.created_by == created_by).all()
