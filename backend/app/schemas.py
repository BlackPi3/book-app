from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


# Base schema with common configuration
class BookBase(BaseModel):
    """Base schema for Book with common fields"""
    title: str = Field(..., min_length=1, max_length=200, description="Book title")
    author: str = Field(..., min_length=1, max_length=100, description="Book author")


class BookCreate(BookBase):
    """Schema for creating a new book (request body)"""
    created_by: str = Field(..., min_length=1, max_length=50, description="User who created the book")


class BookUpdate(BaseModel):
    """Schema for updating an existing book"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)


class BookResponse(BookBase):
    """Schema for book response (includes all fields from database)"""
    id: int
    created_on: datetime
    created_by: str

    # Pydantic v2 configuration
    model_config = ConfigDict(from_attributes=True)


class BookSearch(BaseModel):
    """Schema for book search parameters"""
    title: Optional[str] = Field(None, description="Search by title (partial match)")
    author: Optional[str] = Field(None, description="Search by author (partial match)")
    created_by: Optional[str] = Field(None, description="Filter by creator")


# Example of schema inheritance and composition
class BookList(BaseModel):
    """Schema for paginated book list responses"""
    books: list[BookResponse]
    total: int
    page: int = 1
    per_page: int = 10
