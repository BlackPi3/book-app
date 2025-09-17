/**
 * BookService - Handles all API communication with the backend
 * 
 * This service class demonstrates:
 * - Separation of concerns (API logic separate from UI logic)
 * - Promise-based async operations
 * - Error handling patterns
 * - RESTful API integration
 */

export interface Book {
    id?: number;
    title: string;
    author: string;
    created_by: string;
    created_on?: string;
}

export interface BookSearchParams {
    search?: string;
    author?: string;
    limit?: number;
    offset?: number;
}

export default class BookService {
    private baseUrl: string;

    constructor(baseUrl: string = "http://localhost:8000") {
        this.baseUrl = baseUrl;
    }

    /**
     * Fetch all books with optional filtering
     */
    async getBooks(params?: BookSearchParams): Promise<Book[]> {
        let url = `${this.baseUrl}/books`;
        
        if (params) {
            const searchParams = new URLSearchParams();
            if (params.search) searchParams.append("search", params.search);
            if (params.author) searchParams.append("author", params.author);
            if (params.limit) searchParams.append("limit", params.limit.toString());
            if (params.offset) searchParams.append("offset", params.offset.toString());
            
            const queryString = searchParams.toString();
            if (queryString) {
                url += `?${queryString}`;
            }
        }

        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Failed to fetch books: ${response.status} ${response.statusText}`);
        }
        
        return response.json();
    }

    /**
     * Get a single book by ID
     */
    async getBook(id: number): Promise<Book> {
        const response = await fetch(`${this.baseUrl}/books/${id}`);
        if (!response.ok) {
            throw new Error(`Failed to fetch book: ${response.status} ${response.statusText}`);
        }
        
        return response.json();
    }

    /**
     * Create a new book
     */
    async createBook(book: Book): Promise<Book> {
        const response = await fetch(`${this.baseUrl}/books`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(book)
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(`Failed to create book: ${response.status} ${response.statusText}. ${errorData.detail || ""}`);
        }
        
        return response.json();
    }

    /**
     * Update an existing book
     */
    async updateBook(id: number, book: Book): Promise<Book> {
        const response = await fetch(`${this.baseUrl}/books/${id}`, {
            method: "PUT", 
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(book)
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(`Failed to update book: ${response.status} ${response.statusText}. ${errorData.detail || ""}`);
        }
        
        return response.json();
    }

    /**
     * Delete a book by ID
     */
    async deleteBook(id: number): Promise<void> {
        const response = await fetch(`${this.baseUrl}/books/${id}`, {
            method: "DELETE"
        });

        if (!response.ok) {
            throw new Error(`Failed to delete book: ${response.status} ${response.statusText}`);
        }
    }

    /**
     * Delete multiple books
     */
    async deleteBooks(ids: number[]): Promise<void> {
        const deletePromises = ids.map(id => this.deleteBook(id));
        await Promise.all(deletePromises);
    }

    /**
     * Check if the backend API is available
     */
    async healthCheck(): Promise<boolean> {
        try {
            const response = await fetch(`${this.baseUrl}/`);
            return response.ok;
        } catch (error) {
            return false;
        }
    }
}