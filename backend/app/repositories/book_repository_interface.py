from abc import ABC, abstractmethod
from typing import List, Optional
from sqlalchemy.orm import Session
from ..models import Book

class BookRepositoryInterface(ABC):
    """
    Abstract interface for Book repository operations.

    This interface defines the contract that all book repositories must follow.
    This is the Dependency Inversion Principle in action - high-level modules
    (like services) depend on this abstraction, not concrete implementations.
    """

    @abstractmethod
    def create(self, book: Book) -> Book:
        """Create a new book in the repository"""
        pass

    @abstractmethod
    def get_by_id(self, book_id: int) -> Optional[Book]:
        """Get a book by its ID"""
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Book]:
        """Get all books with optional pagination"""
        pass

    @abstractmethod
    def update(self, book_id: int, book_update: dict) -> Optional[Book]:
        """Update an existing book"""
        pass

    @abstractmethod
    def delete(self, book_id: int) -> bool:
        """Delete a book by ID, returns True if successful"""
        pass

    @abstractmethod
    def search_by_title(self, title: str) -> List[Book]:
        """Search books by title (partial match)"""
        pass

    @abstractmethod
    def search_by_author(self, author: str) -> List[Book]:
        """Search books by author (partial match)"""
        pass

    @abstractmethod
    def get_by_created_by(self, created_by: str) -> List[Book]:
        """Get all books created by a specific user"""
        pass
