from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from contextlib import asynccontextmanager
from .database import get_db, create_tables
from .repositories import BookRepositoryInterface, SQLBookRepository
from .schemas import BookCreate, BookResponse, BookUpdate
from .models import Book

# Lifespan event handler to replace deprecated on_event
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_tables()
    yield
    # Shutdown (if needed in future)

# Create FastAPI application
app = FastAPI(
    title="BookApp API",
    description="A REST API for managing books with Repository Pattern and Dependency Injection",
    version="1.0.0",
    lifespan=lifespan
)

# Dependency Injection: Repository Factory
def get_book_repository(db: Session = Depends(get_db)) -> BookRepositoryInterface:
    """
    Dependency factory that returns a BookRepository instance.
    This demonstrates Dependency Injection - FastAPI will automatically
    provide the database session and create the repository.
    """
    return SQLBookRepository(db)

# RESTful API Endpoints

@app.get("/", summary="Root endpoint")
async def read_root():
    """Welcome endpoint"""
    return {
        "message": "Welcome to BookApp API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/books", response_model=List[BookResponse], summary="Get all books")
async def get_books(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    title: Optional[str] = Query(None, description="Filter by title (partial match)"),
    author: Optional[str] = Query(None, description="Filter by author (partial match)"),
    created_by: Optional[str] = Query(None, description="Filter by creator"),
    repo: BookRepositoryInterface = Depends(get_book_repository)
):
    """
    Get all books with optional filtering and pagination.

    This endpoint demonstrates:
    - RESTful design (GET /books)
    - Query parameters for filtering
    - Dependency injection for repository
    - Pydantic response models
    """
    if title or author or created_by:
        # Use advanced search if filters provided
        books = repo.search(title=title, author=author, created_by=created_by)
        # Apply pagination to search results
        books = books[skip:skip + limit]
    else:
        # Get all books with pagination
        books = repo.get_all(skip=skip, limit=limit)

    return books

@app.get("/books/{book_id}", response_model=BookResponse, summary="Get book by ID")
async def get_book(
    book_id: int,
    repo: BookRepositoryInterface = Depends(get_book_repository)
):
    """
    Get a specific book by ID.

    RESTful endpoint: GET /books/{id}
    """
    book = repo.get_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.post("/books", response_model=BookResponse, status_code=201, summary="Create a new book")
async def create_book(
    book_data: BookCreate,
    repo: BookRepositoryInterface = Depends(get_book_repository)
):
    """
    Create a new book.

    This endpoint demonstrates:
    - RESTful design (POST /books)
    - Pydantic request validation
    - Repository pattern usage
    - HTTP status codes (201 Created)
    """
    # Convert Pydantic model to SQLAlchemy model
    book = Book(**book_data.model_dump())

    # Create book using repository
    created_book = repo.create(book)

    return created_book

@app.put("/books/{book_id}", response_model=BookResponse, summary="Update a book")
async def update_book(
    book_id: int,
    book_update: BookUpdate,
    repo: BookRepositoryInterface = Depends(get_book_repository)
):
    """
    Update an existing book.

    RESTful endpoint: PUT /books/{id}
    Only provided fields will be updated.
    """
    # Convert Pydantic model to dict, excluding None values
    update_data = book_update.model_dump(exclude_unset=True)

    updated_book = repo.update(book_id, update_data)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")

    return updated_book

@app.delete("/books/{book_id}", status_code=204, summary="Delete a book")
async def delete_book(
    book_id: int,
    repo: BookRepositoryInterface = Depends(get_book_repository)
):
    """
    Delete a book by ID.

    RESTful endpoint: DELETE /books/{id}
    Returns 204 No Content on success.
    """
    success = repo.delete(book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")

    return None  # 204 No Content
