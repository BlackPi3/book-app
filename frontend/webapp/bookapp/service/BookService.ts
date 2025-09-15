import { IBook, IBookCreate, IBookUpdate, IBookResponse, IApiResponse, IBookSearchParams } from "../model/types";

export class BookService {
    private baseUrl: string;

    constructor(baseUrl: string = "http://localhost:8000") {
        this.baseUrl = baseUrl;
    }

    /**
     * Fetch all books from the API
     */
    async getAllBooks(): Promise<IApiResponse<IBookResponse[]>> {
        try {
            const response = await fetch(`${this.baseUrl}/books`);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return { data };
        } catch (error) {
            console.error("Error fetching books:", error);
            return { error: "Failed to fetch books" };
        }
    }

    /**
     * Create a new book
     */
    async createBook(book: IBookCreate): Promise<IApiResponse<IBookResponse>> {
        try {
            const response = await fetch(`${this.baseUrl}/books`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(book),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return { data };
        } catch (error) {
            console.error("Error creating book:", error);
            return { error: "Failed to create book" };
        }
    }

    /**
     * Update an existing book
     */
    async updateBook(id: number, book: IBookUpdate): Promise<IApiResponse<IBookResponse>> {
        try {
            const response = await fetch(`${this.baseUrl}/books/${id}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(book),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return { data };
        } catch (error) {
            console.error("Error updating book:", error);
            return { error: "Failed to update book" };
        }
    }

    /**
     * Delete a book
     */
    async deleteBook(id: number): Promise<IApiResponse<void>> {
        try {
            const response = await fetch(`${this.baseUrl}/books/${id}`, {
                method: "DELETE",
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return { message: "Book deleted successfully" };
        } catch (error) {
            console.error("Error deleting book:", error);
            return { error: "Failed to delete book" };
        }
    }

    /**
     * Search books by parameters
     */
    async searchBooks(params: IBookSearchParams): Promise<IApiResponse<IBookResponse[]>> {
        try {
            const queryParams = new URLSearchParams();

            if (params.title) queryParams.append("title", params.title);
            if (params.author) queryParams.append("author", params.author);
            if (params.created_by) queryParams.append("created_by", params.created_by);

            const response = await fetch(`${this.baseUrl}/books?${queryParams.toString()}`);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return { data };
        } catch (error) {
            console.error("Error searching books:", error);
            return { error: "Failed to search books" };
        }
    }

    /**
     * Get a single book by ID
     */
    async getBookById(id: number): Promise<IApiResponse<IBookResponse>> {
        try {
            const response = await fetch(`${this.baseUrl}/books/${id}`);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return { data };
        } catch (error) {
            console.error("Error fetching book:", error);
            return { error: "Failed to fetch book" };
        }
    }
}
