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
                selectedBooks: [], // added to prevent expression errors
                authors: [
                    { key: "", text: "All Authors" }
                ]
            });
            this.getView().setModel(oModel);
            // eslint-disable-next-line no-console
            console.log("[BookApp] Main.controller onInit: model initialized");
            // Load initial data
            this.loadBooks();
        },

        loadBooks: function () {
            var oModel = this.getView().getModel();
            oModel.setProperty("/loading", true);
            var that = this; // preserve context for logs
            // eslint-disable-next-line no-console
            console.log("[BookApp] loadBooks: starting fetch http://localhost:8000/books");
            // Check if backend is available
            fetch("http://localhost:8000/books")
                .then(function(response) {
                    // eslint-disable-next-line no-console
                    console.log("[BookApp] loadBooks: response status", response.status);
                    if (!response.ok) {
                        throw new Error("HTTP " + response.status);
                    }
                    return response.json();
                })
                .then(function(books) {
                    // eslint-disable-next-line no-console
                    console.log("[BookApp] loadBooks: parsed JSON count=", books.length, books.length ? books[0] : "<empty>");
                    books.forEach(function(b){
                        if (b.created_on && typeof b.created_on === 'string') {
                            b.created_on = b.created_on.trim();
                        }
                    });
                    oModel.setProperty("/books", books);
                    // Diagnostics after setting books
                    var oTable = that.byId("booksTable");
                    // eslint-disable-next-line no-console
                    console.log("[BookApp] diagnostics: table instance=", oTable);
                    // Delay to allow binding update
                    setTimeout(function(){
                        if (oTable) {
                            // eslint-disable-next-line no-console
                            console.log("[BookApp] diagnostics: items binding path=", oTable.getBinding("items")?.getPath(), "rendered items=", oTable.getItems().length);
                        }
                    },0);
                    oModel.setProperty("/totalBooks", books.length);
                    oModel.setProperty("/loading", false);
                    var authors = [{ key: "", text: "All Authors" }];
                    var uniqueAuthors = [...new Set(books.map(function(book) { return book.author; }))];
                    uniqueAuthors.forEach(function(author) { authors.push({ key: author, text: author }); });
                    oModel.setProperty("/authors", authors);
                    // eslint-disable-next-line no-console
                    console.log("[BookApp] loadBooks: model updated, authors=", authors.length);
                    MessageToast.show("Loaded " + books.length + " books successfully");
                })
                .catch(function(error) {
                    // eslint-disable-next-line no-console
                    console.error("[BookApp] loadBooks: error", error);
                    oModel.setProperty("/loading", false);
                    MessageBox.error("Failed to load books. Using sample data. Backend at http://localhost:8000?");
                    var sampleBooks = [
                        { id: 1, title: "Clean Code", author: "Robert Martin", created_by: "demo_user", created_on: new Date().toISOString() },
                        { id: 2, title: "The Pragmatic Programmer", author: "David Thomas", created_by: "demo_user", created_on: new Date().toISOString() }
                    ];
                    oModel.setProperty("/books", sampleBooks);
                    oModel.setProperty("/totalBooks", sampleBooks.length);
                    // eslint-disable-next-line no-console
                    console.log("[BookApp] loadBooks: fallback sample data applied", sampleBooks);
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

        onDeleteSelected: function () {
            var oTable = this.byId("booksTable");
            if (!oTable) { return; }
            var aSelected = oTable.getSelectedItems();
            if (!aSelected.length) {
                MessageToast.show("Select books first");
                return;
            }
            var that = this;
            MessageBox.confirm("Delete " + aSelected.length + " selected book(s)?", {
                onClose: function (sAction) {
                    if (sAction === MessageBox.Action.OK) {
                        var oModel = that.getView().getModel();
                        var aBooks = oModel.getProperty("/books") || [];
                        var idsToRemove = aSelected.map(function (it) { return it.getBindingContext().getObject().id; });
                        aBooks = aBooks.filter(function (b) { return idsToRemove.indexOf(b.id) === -1; });
                        oModel.setProperty("/books", aBooks);
                        oModel.setProperty("/totalBooks", aBooks.length);
                        oTable.removeSelections(true);
                        MessageToast.show("Deleted " + idsToRemove.length + " book(s) (frontend only)");
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
        },

        onSelectionChange: function(){
            var oTable = this.byId("booksTable");
            if(!oTable) return;
            var aContexts = oTable.getSelectedContexts();
            var aBooks = aContexts.map(function(c){ return c.getObject(); });
            var oModel = this.getView().getModel();
            oModel.setProperty("/selectedBooks", aBooks);
        },

        formatCreatedOn: function(v){
            if(!v) return "";
            // Accept ISO or date-only
            var d = (v instanceof Date) ? v : new Date(v);
            if (isNaN(d.getTime())) return ""; // avoid console error
            // Return locale date/time short
            try {
                return d.toLocaleDateString() + " " + d.toLocaleTimeString(undefined,{hour:'2-digit',minute:'2-digit'});
            } catch(e){
                return d.toISOString();
            }
        }
    });
});