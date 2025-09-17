from typing import List, Optional
from app.repositories import BookRepositoryInterface
from app.models import Book

class BookService:
    """Service layer encapsulating book-related business logic.

    Currently a thin wrapper around the repository to illustrate layering and
    future-proof for additional business rules (validation, events, etc.).
    """

    def __init__(self, repository: BookRepositoryInterface):
        self.repository = repository

    # CRUD operations
    def list_books(self, skip: int = 0, limit: int = 100) -> List[Book]:
        return self.repository.get_all(skip=skip, limit=limit)

    def get_book(self, book_id: int) -> Optional[Book]:  # type: ignore[name-defined]
        return self.repository.get_by_id(book_id)

    def create_book(self, book: Book) -> Book:
        return self.repository.create(book)

    def update_book(self, book_id: int, update_data: dict) -> Optional[Book]:  # type: ignore[name-defined]
        return self.repository.update(book_id, update_data)

    def delete_book(self, book_id: int) -> bool:
        return self.repository.delete(book_id)

    # Search functionality
    def search_books(
        self,
        title: Optional[str] = None,
        author: Optional[str] = None,
        created_by: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Book]:
        if title or author or created_by:
            results = self.repository.search(title=title, author=author, created_by=created_by)
            return results[skip: skip + limit]
        return self.list_books(skip=skip, limit=limit)

