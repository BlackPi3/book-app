# 📖 BookApp — Full-Stack Web Application

## 🎯 Goal
Build a complete web application to manage a list of books.

---

## 🔹 Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL (start with SQLite for simplicity, then switch later)
- **Features**:
    - Create, read, update, delete (CRUD) books
    - Search by title
    - Filter by creation date
    - Preloaded data in the database
    - REST API documented with Swagger (`/docs`)

---

## 🔹 Frontend
- **Framework**: SAPUI5 (TypeScript)
- **Features**:
    - Display books in a table (title, author, created on, created by)
    - Search and filter options
    - Forms to create and edit books
    - Delete books with confirmation

---

## 🔹 Infrastructure
- **Containerization**: Docker
    - Backend, frontend, and database run as separate containers
- **Startup**: Run everything with:
  ```bash
  docker compose up