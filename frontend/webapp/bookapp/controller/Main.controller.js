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
                _allBooks: [], // keep unfiltered source
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
                    oModel.setProperty("/_allBooks", books);
                    that._rebuildAuthors(books);
                    that.applyFilters(); // will set /books + /totalBooks
                    oModel.setProperty("/loading", false);
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
                    oModel.setProperty("/_allBooks", sampleBooks);
                    that._rebuildAuthors(sampleBooks);
                    that.applyFilters();
                });
        },

        _rebuildAuthors: function(books){
            var oModel = this.getView().getModel();
            var authors = [{ key: "", text: "All Authors" }];
            var uniqueAuthors = [...new Set(books.map(function(b){ return b.author; }))];
            uniqueAuthors.forEach(function(a){ authors.push({ key:a, text:a }); });
            oModel.setProperty("/authors", authors);
        },

        applyFilters: function(){
            var oModel = this.getView().getModel();
            var all = oModel.getProperty("/_allBooks") || [];
            var q = (oModel.getProperty("/searchQuery") || "").toLowerCase().trim();
            var author = oModel.getProperty("/selectedAuthor") || "";
            var filtered = all.filter(function(b){
                var okAuthor = !author || b.author === author;
                var okText = !q || (b.title && b.title.toLowerCase().includes(q)) || (b.author && b.author.toLowerCase().includes(q));
                return okAuthor && okText;
            });
            oModel.setProperty("/books", filtered);
            oModel.setProperty("/totalBooks", filtered.length);
        },

        onRefresh: function () {
            this.loadBooks();
        },

        onAddBook: function () {
            MessageBox.information("Add Book functionality will be implemented in the next iteration.");
        },

        onSearch: function(oEvent){
            var oModel = this.getView().getModel();
            // search event provides 'query'; liveChange provides 'newValue'
            var val = oEvent.getParameter("query");
            if (val === undefined) { val = oEvent.getParameter("newValue"); }
            if (val !== undefined) { oModel.setProperty("/searchQuery", val); }
            this.applyFilters();
        },

        onClearSearch: function () {
            var oModel = this.getView().getModel();
            oModel.setProperty("/searchQuery", "");
            this.applyFilters();
        },

        onAuthorFilter: function () {
            this.applyFilters();
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
                        var all = oModel.getProperty("/_allBooks") || [];
                        var idsToRemove = aSelected.map(it => it.getBindingContext().getObject().id);
                        all = all.filter(b => idsToRemove.indexOf(b.id) === -1);
                        oModel.setProperty("/_allBooks", all);
                        that.applyFilters();
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

