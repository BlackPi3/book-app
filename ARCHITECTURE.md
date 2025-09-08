# 📐 BookApp Architecture Design Document
*MILESTONE 1.2 Deliverable*

## 🏗️ Layered Architecture Overview

Our BookApp follows a **3-Layer Architecture Pattern** that promotes separation of concerns and maintainability:

```
┌─────────────────────────────────────────────┐
│           PRESENTATION LAYER                │
│  ┌─────────────────┐ ┌─────────────────┐   │
│  │   FastAPI       │ │   SAPUI5        │   │
│  │   Endpoints     │ │   Frontend      │   │
│  │   /api/*        │ │   Components    │   │
│  └─────────────────┘ └─────────────────┘   │
├─────────────────────────────────────────────┤
│              BUSINESS LAYER                 │
│  ┌─────────────────┐ ┌─────────────────┐   │
│  │    Services     │ │  Business Logic │   │
│  │   Validation    │ │   Workflows     │   │
│  │   Orchestration │ │   Domain Rules  │   │
│  └─────────────────┘ └─────────────────┘   │
├─────────────────────────────────────────────┤
│               DATA LAYER                    │
│  ┌─────────────────┐ ┌─────────────────┐   │
│  │  Repositories   │ │    Models       │   │
│  │  Data Access    │ │   Database      │   │
│  │  Abstraction    │ │   Entities      │   │
│  └─────────────────┘ └─────────────────┘   │
└─────────────────────────────────────────────┘
```

## 🎯 Layer Responsibilities

### **Presentation Layer** (API + UI)
- **FastAPI Endpoints**: RESTful API controllers (`/api/`)
- **SAPUI5 Frontend**: User interface components and views
- **Responsibilities**:
  - Handle HTTP requests/responses
  - Input validation and serialization
  - User interface interactions
  - Route management

### **Business Layer** (Services)
- **Services Directory**: Business logic implementation
- **Responsibilities**:
  - Business rules enforcement
  - Workflow orchestration
  - Complex operations coordination
  - Cross-cutting concerns (logging, caching)

### **Data Layer** (Models + Repositories)
- **Models**: SQLAlchemy entities (Book)
- **Repositories**: Data access abstraction
- **Responsibilities**:
  - Database operations (CRUD)
  - Data persistence
  - Query optimization
  - Database schema management

## 📊 Book Entity Schema

```sql
-- Database Schema for books table
CREATE TABLE books (
    id          SERIAL PRIMARY KEY,
    title       VARCHAR NOT NULL,
    author      VARCHAR NOT NULL,
    created_on  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by  VARCHAR NOT NULL
);

-- Indexes for performance
CREATE INDEX idx_books_title ON books(title);
CREATE INDEX idx_books_created_on ON books(created_on);
```

## 🔄 Data Flow Architecture

```
User Request → API Endpoint → Service → Repository → Database
     ↓              ↓           ↓          ↓          ↓
Frontend UI ← JSON Response ← Business Logic ← Data Access ← SQLAlchemy
```

## 🏛️ Design Principles Applied

### **1. Separation of Concerns**
Each layer has a single, well-defined responsibility.

### **2. Dependency Inversion Principle**
- High-level modules (Services) don't depend on low-level modules (Repositories)
- Both depend on abstractions (Interfaces)
- Example: `BookService` depends on `BookRepositoryInterface`, not `SQLBookRepository`

### **3. Single Responsibility Principle**
- Models: Only data structure and basic validation
- Repositories: Only data access logic
- Services: Only business logic
- Controllers: Only request/response handling

### **4. Open/Closed Principle**
- Easy to add new features without modifying existing code
- Repository pattern allows switching databases without changing business logic

## 🔧 Architecture Benefits

1. **Testability**: Each layer can be tested independently
2. **Maintainability**: Changes in one layer don't affect others
3. **Scalability**: Can optimize each layer separately
4. **Flexibility**: Easy to swap implementations (e.g., different databases)
5. **Team Development**: Different teams can work on different layers

## 🚀 Next Steps

This architecture will support:
- **Repository Pattern** (MILESTONE 2.2)
- **Dependency Injection** (MILESTONE 2.3)
- **API Design** (MILESTONE 2.3)
- **Frontend Integration** (MILESTONE 4.2)
- **Testing Strategy** (MILESTONE 5.1)

---
*Generated for MILESTONE 1.2: Domain Design & Architecture Planning*
