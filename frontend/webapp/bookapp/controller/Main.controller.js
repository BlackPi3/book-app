sap.ui.define([
    "sap/ui/core/mvc/Controller",
    "sap/ui/model/json/JSONModel",
    "sap/m/MessageToast",
    "sap/m/MessageBox"
], function (Controller, JSONModel, MessageToast, MessageBox) {
    "use strict";

    return Controller.extend("bookapp.controller.Main", {
        onInit: function () {
            // Initialize the model with empty data
            var oModel = new JSONModel({
                books: [],
                totalBooks: 0,
                loading: false,
                searchQuery: "",
                selectedAuthor: "",
                authors: [
                    { key: "", text: "All Authors" }
                ]
            });
            
            this.getView().setModel(oModel);
            
            // Load initial data
            this.loadBooks();
        },

        loadBooks: function () {
            var oModel = this.getView().getModel();
            oModel.setProperty("/loading", true);

            // Check if backend is available
            fetch("http://localhost:8000/books")
                .then(function(response) {
                    if (!response.ok) {
                        throw new Error("Backend not available");
                    }
                    return response.json();
                })
                .then(function(books) {
                    oModel.setProperty("/books", books);
                    oModel.setProperty("/totalBooks", books.length);
                    oModel.setProperty("/loading", false);
                    
                    // Extract unique authors
                    var authors = [{ key: "", text: "All Authors" }];
                    var uniqueAuthors = [...new Set(books.map(function(book) { return book.author; }))];
                    uniqueAuthors.forEach(function(author) {
                        authors.push({ key: author, text: author });
                    });
                    oModel.setProperty("/authors", authors);
                    
                    MessageToast.show("Loaded " + books.length + " books successfully");
                })
                .catch(function(error) {
                    console.error("Error loading books:", error);
                    oModel.setProperty("/loading", false);
                    MessageBox.error("Failed to load books. Please ensure the backend server is running at http://localhost:8000");
                    
                    // Set some sample data for demo purposes
                    var sampleBooks = [
                        {
                            id: 1,
                            title: "Clean Code",
                            author: "Robert Martin", 
                            created_by: "demo_user",
                            created_on: new Date().toISOString()
                        },
                        {
                            id: 2,
                            title: "The Pragmatic Programmer",
                            author: "David Thomas",
                            created_by: "demo_user", 
                            created_on: new Date().toISOString()
                        }
                    ];
                    oModel.setProperty("/books", sampleBooks);
                    oModel.setProperty("/totalBooks", sampleBooks.length);
                });
        },

        onRefresh: function () {
            this.loadBooks();
        },

        onAddBook: function () {
            MessageBox.information("Add Book functionality will be implemented in the next iteration.");
        },

        onSearch: function () {
            var oModel = this.getView().getModel();
            var searchQuery = oModel.getProperty("/searchQuery");
            MessageToast.show("Search functionality: " + searchQuery);
        },

        onClearSearch: function () {
            var oModel = this.getView().getModel();
            oModel.setProperty("/searchQuery", "");
            this.loadBooks();
        },

        onAuthorFilter: function () {
            var oModel = this.getView().getModel();
            var selectedAuthor = oModel.getProperty("/selectedAuthor");
            MessageToast.show("Filter by author: " + selectedAuthor);
        },

        onEditBook: function (oEvent) {
            var oContext = oEvent.getSource().getBindingContext();
            var book = oContext.getObject();
            MessageBox.information("Edit functionality for: " + book.title);
        },

        onDeleteBook: function (oEvent) {
            var oContext = oEvent.getSource().getBindingContext();
            var book = oContext.getObject();
            
            MessageBox.confirm("Delete '" + book.title + "'?", {
                onClose: function(sAction) {
                    if (sAction === MessageBox.Action.OK) {
                        MessageToast.show("Book '" + book.title + "' would be deleted");
                    }
                }
            });
        },

        onBookPress: function (oEvent) {
            var oContext = oEvent.getSource().getBindingContext();
            var book = oContext.getObject();
            
            MessageBox.information(
                "Book Details:\n\n" +
                "Title: " + book.title + "\n" +
                "Author: " + book.author + "\n" +
                "Created By: " + book.created_by + "\n" +
                "Created On: " + (book.created_on || "N/A"),
                { title: "Book Information" }
            );
        }
    });
});