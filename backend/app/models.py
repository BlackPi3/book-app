from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Book(Base):
    """
    Book entity representing a book in our library system.

    This follows the Domain-Driven Design (DDD) principles where
    the Book is our core domain entity with clear business rules.

    Performance Optimizations:
    - Indexes on title, author, and created_by for fast searching
    - Composite index for common search combinations
    """
    __tablename__ = "books"

    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Core book attributes with indexes for performance
    title = Column(String, nullable=False, index=True)  # Index for title searches
    author = Column(String, nullable=False, index=True)  # Index for author searches

    # Audit fields for tracking
    created_on = Column(DateTime, default=func.now(), nullable=False, index=True)  # Index for date filtering
    created_by = Column(String, nullable=False, index=True)  # Index for creator searches

    # Define composite indexes for common search patterns
    __table_args__ = (
        # Composite index for title + author searches (common pattern)
        Index('idx_title_author', 'title', 'author'),
        # Composite index for author + created_by (for finding books by specific authors from specific users)
        Index('idx_author_creator', 'author', 'created_by'),
        # Index for date range queries
        Index('idx_created_on_desc', 'created_on'),
    )

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', author='{self.author}')>"

    def __str__(self):
        return f"{self.title} by {self.author}"
