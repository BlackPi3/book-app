var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
define(["require", "exports", "sap/ui/core/mvc/Controller", "sap/ui/model/json/JSONModel", "sap/m/MessageToast", "sap/m/MessageBox", "../service/BookService"], function (require, exports, Controller_1, JSONModel_1, MessageToast_1, MessageBox_1, BookService_1) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    Controller_1 = __importDefault(Controller_1);
    JSONModel_1 = __importDefault(JSONModel_1);
    MessageToast_1 = __importDefault(MessageToast_1);
    MessageBox_1 = __importDefault(MessageBox_1);
    /**
     * @namespace bookapp.controller
     */
    class Main extends Controller_1.default {
        onInit() {
            var _a;
            // Initialize the book service
            this.bookService = new BookService_1.BookService();
            // Initialize the books model
            const oModel = new JSONModel_1.default({
                books: [],
                isLoading: false
            });
            (_a = this.getView()) === null || _a === void 0 ? void 0 : _a.setModel(oModel);
            // Load initial data
            this.loadBooks();
        }
        onAddBook() {
            return __awaiter(this, void 0, void 0, function* () {
                // For now, create a sample book - will be replaced with dialog in next milestone
                const newBook = {
                    title: "Sample Book " + new Date().getTime(),
                    author: "Sample Author",
                    created_by: "Frontend User"
                };
                this.setLoading(true);
                const result = yield this.bookService.createBook(newBook);
                this.setLoading(false);
                if (result.error) {
                    MessageBox_1.default.error(result.error);
                }
                else {
                    MessageToast_1.default.show("Book created successfully!");
                    this.loadBooks(); // Refresh the list
                }
            });
        }
        onEditBook(oEvent) {
            return __awaiter(this, void 0, void 0, function* () {
                const oSource = oEvent.getSource();
                const oContext = oSource.getBindingContext();
                const oBook = oContext.getObject();
                // For now, just update the title - will be replaced with dialog in next milestone
                const updatedBook = {
                    title: oBook.title + " (Updated)"
                };
                this.setLoading(true);
                const result = yield this.bookService.updateBook(oBook.id, updatedBook);
                this.setLoading(false);
                if (result.error) {
                    MessageBox_1.default.error(result.error);
                }
                else {
                    MessageToast_1.default.show("Book updated successfully!");
                    this.loadBooks(); // Refresh the list
                }
            });
        }
        onDeleteBook(oEvent) {
            return __awaiter(this, void 0, void 0, function* () {
                const oSource = oEvent.getSource();
                const oContext = oSource.getBindingContext();
                const oBook = oContext.getObject();
                const sConfirmMessage = `Are you sure you want to delete "${oBook.title}"?`;
                MessageBox_1.default.confirm(sConfirmMessage, {
                    onClose: (sAction) => __awaiter(this, void 0, void 0, function* () {
                        if (sAction === MessageBox_1.default.Action.OK) {
                            this.setLoading(true);
                            const result = yield this.bookService.deleteBook(oBook.id);
                            this.setLoading(false);
                            if (result.error) {
                                MessageBox_1.default.error(result.error);
                            }
                            else {
                                MessageToast_1.default.show("Book deleted successfully!");
                                this.loadBooks(); // Refresh the list
                            }
                        }
                    })
                });
            });
        }
        onSearch(oEvent) {
            return __awaiter(this, void 0, void 0, function* () {
                var _a, _b;
                const sQuery = oEvent.getParameter("newValue") || oEvent.getParameter("query");
                if (sQuery && sQuery.trim()) {
                    this.setLoading(true);
                    const result = yield this.bookService.searchBooks({ title: sQuery });
                    this.setLoading(false);
                    if (result.error) {
                        MessageBox_1.default.error(result.error);
                    }
                    else {
                        const oModel = (_a = this.getView()) === null || _a === void 0 ? void 0 : _a.getModel();
                        oModel.setProperty("/books", result.data || []);
                        MessageToast_1.default.show(`Found ${((_b = result.data) === null || _b === void 0 ? void 0 : _b.length) || 0} books matching "${sQuery}"`);
                    }
                }
                else {
                    // Empty search - reload all books
                    this.loadBooks();
                }
            });
        }
        loadBooks() {
            return __awaiter(this, void 0, void 0, function* () {
                var _a, _b;
                this.setLoading(true);
                const result = yield this.bookService.getAllBooks();
                this.setLoading(false);
                const oModel = (_a = this.getView()) === null || _a === void 0 ? void 0 : _a.getModel();
                if (result.error) {
                    MessageBox_1.default.error(result.error);
                    oModel.setProperty("/books", []);
                }
                else {
                    oModel.setProperty("/books", result.data || []);
                    MessageToast_1.default.show(`Loaded ${((_b = result.data) === null || _b === void 0 ? void 0 : _b.length) || 0} books from API`);
                }
            });
        }
        setLoading(bLoading) {
            var _a;
            const oModel = (_a = this.getView()) === null || _a === void 0 ? void 0 : _a.getModel();
            oModel.setProperty("/isLoading", bLoading);
        }
    }
    exports.default = Main;
});
