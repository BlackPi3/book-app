from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from contextlib import asynccontextmanager
from .database import get_db, create_tables
from app.api.books import router as books_router
from app.api.dependencies import get_book_repository  # re-export for tests expecting this symbol

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

# CORS configuration (explicit origins to satisfy browser security)
ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8080"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include modular routers
app.include_router(books_router)

@app.get("/", summary="Root endpoint")
async def read_root():
    """Welcome endpoint"""
    return {
        "message": "Welcome to BookApp API",
        "docs": "/docs",
        "version": "1.0.0"
    }
