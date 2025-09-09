from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Book(Base):
    """
    Book entity representing a book in our library system.

    This follows the Domain-Driven Design (DDD) principles where
    the Book is our core domain entity with clear business rules.
    """
    __tablename__ = "books"

    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Core book attributes
    title = Column(String, nullable=False, index=True)
    author = Column(String, nullable=False)

    # Audit fields for tracking
    created_on = Column(DateTime, default=func.now(), nullable=False)
    created_by = Column(String, nullable=False)

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', author='{self.author}')>"

    def __str__(self):
        return f"{self.title} by {self.author}"
