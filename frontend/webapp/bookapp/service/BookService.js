var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
define(["require", "exports"], function (require, exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.BookService = void 0;
    class BookService {
        constructor(baseUrl = "http://localhost:8000") {
            this.baseUrl = baseUrl;
        }
        /**
         * Fetch all books from the API
         */
        getAllBooks() {
            return __awaiter(this, void 0, void 0, function* () {
                try {
                    const response = yield fetch(`${this.baseUrl}/books`);
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    const data = yield response.json();
                    return { data };
                }
                catch (error) {
                    console.error("Error fetching books:", error);
                    return { error: "Failed to fetch books" };
                }
            });
        }
        /**
         * Create a new book
         */
        createBook(book) {
            return __awaiter(this, void 0, void 0, function* () {
                try {
                    const response = yield fetch(`${this.baseUrl}/books`, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify(book),
                    });
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    const data = yield response.json();
                    return { data };
                }
                catch (error) {
                    console.error("Error creating book:", error);
                    return { error: "Failed to create book" };
                }
            });
        }
        /**
         * Update an existing book
         */
        updateBook(id, book) {
            return __awaiter(this, void 0, void 0, function* () {
                try {
                    const response = yield fetch(`${this.baseUrl}/books/${id}`, {
                        method: "PUT",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify(book),
                    });
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    const data = yield response.json();
                    return { data };
                }
                catch (error) {
                    console.error("Error updating book:", error);
                    return { error: "Failed to update book" };
                }
            });
        }
        /**
         * Delete a book
         */
        deleteBook(id) {
            return __awaiter(this, void 0, void 0, function* () {
                try {
                    const response = yield fetch(`${this.baseUrl}/books/${id}`, {
                        method: "DELETE",
                    });
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return { message: "Book deleted successfully" };
                }
                catch (error) {
                    console.error("Error deleting book:", error);
                    return { error: "Failed to delete book" };
                }
            });
        }
        /**
         * Search books by parameters
         */
        searchBooks(params) {
            return __awaiter(this, void 0, void 0, function* () {
                try {
                    const queryParams = new URLSearchParams();
                    if (params.title)
                        queryParams.append("title", params.title);
                    if (params.author)
                        queryParams.append("author", params.author);
                    if (params.created_by)
                        queryParams.append("created_by", params.created_by);
                    const response = yield fetch(`${this.baseUrl}/books?${queryParams.toString()}`);
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    const data = yield response.json();
                    return { data };
                }
                catch (error) {
                    console.error("Error searching books:", error);
                    return { error: "Failed to search books" };
                }
            });
        }
        /**
         * Get a single book by ID
         */
        getBookById(id) {
            return __awaiter(this, void 0, void 0, function* () {
                try {
                    const response = yield fetch(`${this.baseUrl}/books/${id}`);
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    const data = yield response.json();
                    return { data };
                }
                catch (error) {
                    console.error("Error fetching book:", error);
                    return { error: "Failed to fetch book" };
                }
            });
        }
    }
    exports.BookService = BookService;
});
