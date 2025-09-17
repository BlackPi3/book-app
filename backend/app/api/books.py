from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional

from app.api.dependencies import get_book_service
from app.schemas import BookCreate, BookResponse, BookUpdate
from app.models import Book
from app.services.book_service import BookService

# APIRouter for book-related endpoints. No prefix to preserve existing paths (/books, /books/{id}).
router = APIRouter()

@router.get("/books", response_model=List[BookResponse], summary="Get all books")
async def get_books(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    title: Optional[str] = Query(None, description="Filter by title (partial match)"),
    author: Optional[str] = Query(None, description="Filter by author (partial match)"),
    created_by: Optional[str] = Query(None, description="Filter by creator"),
    service: BookService = Depends(get_book_service)
):
    """Get all books with optional filtering and pagination."""
    books = service.search_books(title=title, author=author, created_by=created_by, skip=skip, limit=limit)
    return books

@router.get("/books/{book_id}", response_model=BookResponse, summary="Get book by ID")
async def get_book(book_id: int, service: BookService = Depends(get_book_service)):
    """Get a specific book by ID."""
    book = service.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/books", response_model=BookResponse, status_code=201, summary="Create a new book")
async def create_book(book_data: BookCreate, service: BookService = Depends(get_book_service)):
    """Create a new book."""
    book = Book(**book_data.model_dump())
    created_book = service.create_book(book)
    return created_book

@router.put("/books/{book_id}", response_model=BookResponse, summary="Update a book")
async def update_book(
    book_id: int,
    book_update: BookUpdate,
    service: BookService = Depends(get_book_service)
):
    """Update an existing book (only provided fields)."""
    update_data = book_update.model_dump(exclude_unset=True)
    updated_book = service.update_book(book_id, update_data)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book

@router.delete("/books/{book_id}", status_code=204, summary="Delete a book")
async def delete_book(book_id: int, service: BookService = Depends(get_book_service)):
    """Delete a book by ID (204 on success)."""
    success = service.delete_book(book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return None
