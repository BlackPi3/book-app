from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories import BookRepositoryInterface, SQLBookRepository
from app.services.book_service import BookService


def get_book_repository(db: Session = Depends(get_db)) -> BookRepositoryInterface:
    """Provide a book repository instance (DI dependency)."""
    return SQLBookRepository(db)


def get_book_service(
    repo: BookRepositoryInterface = Depends(get_book_repository),
) -> BookService:
    """Provide a BookService instance wrapping the repository."""
    return BookService(repo)
