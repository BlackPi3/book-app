import Controller from "sap/ui/core/mvc/Controller";
import JSONModel from "sap/ui/model/json/JSONModel";
import MessageToast from "sap/m/MessageToast";
import MessageBox from "sap/m/MessageBox";
import { BookService } from "../service/BookService";
import { IBookCreate, IBookUpdate } from "../model/types";

/**
 * @namespace bookapp.controller
 */
export default class Main extends Controller {
    private bookService!: BookService;

    public onInit(): void {
        // Initialize the book service
        this.bookService = new BookService();

        // Initialize the books model
        const oModel = new JSONModel({
            books: [],
            isLoading: false
        });
        this.getView()?.setModel(oModel);

        // Load initial data
        this.loadBooks();
    }

    public async onAddBook(): Promise<void> {
        // For now, create a sample book - will be replaced with dialog in next milestone
        const newBook: IBookCreate = {
            title: "Sample Book " + new Date().getTime(),
            author: "Sample Author",
            created_by: "Frontend User"
        };

        this.setLoading(true);
        const result = await this.bookService.createBook(newBook);
        this.setLoading(false);

        if (result.error) {
            MessageBox.error(result.error);
        } else {
            MessageToast.show("Book created successfully!");
            this.loadBooks(); // Refresh the list
        }
    }

    public async onEditBook(oEvent: any): Promise<void> {
        const oSource = oEvent.getSource();
        const oContext = oSource.getBindingContext();
        const oBook = oContext.getObject();

        // For now, just update the title - will be replaced with dialog in next milestone
        const updatedBook: IBookUpdate = {
            title: oBook.title + " (Updated)"
        };

        this.setLoading(true);
        const result = await this.bookService.updateBook(oBook.id, updatedBook);
        this.setLoading(false);

        if (result.error) {
            MessageBox.error(result.error);
        } else {
            MessageToast.show("Book updated successfully!");
            this.loadBooks(); // Refresh the list
        }
    }

    public async onDeleteBook(oEvent: any): Promise<void> {
        const oSource = oEvent.getSource();
        const oContext = oSource.getBindingContext();
        const oBook = oContext.getObject();

        const sConfirmMessage = `Are you sure you want to delete "${oBook.title}"?`;

        MessageBox.confirm(sConfirmMessage, {
            onClose: async (sAction: string) => {
                if (sAction === MessageBox.Action.OK) {
                    this.setLoading(true);
                    const result = await this.bookService.deleteBook(oBook.id);
                    this.setLoading(false);

                    if (result.error) {
                        MessageBox.error(result.error);
                    } else {
                        MessageToast.show("Book deleted successfully!");
                        this.loadBooks(); // Refresh the list
                    }
                }
            }
        });
    }

    public async onSearch(oEvent: any): Promise<void> {
        const sQuery = oEvent.getParameter("newValue") || oEvent.getParameter("query");

        if (sQuery && sQuery.trim()) {
            this.setLoading(true);
            const result = await this.bookService.searchBooks({ title: sQuery });
            this.setLoading(false);

            if (result.error) {
                MessageBox.error(result.error);
            } else {
                const oModel = this.getView()?.getModel() as JSONModel;
                oModel.setProperty("/books", result.data || []);
                MessageToast.show(`Found ${result.data?.length || 0} books matching "${sQuery}"`);
            }
        } else {
            // Empty search - reload all books
            this.loadBooks();
        }
    }

    private async loadBooks(): Promise<void> {
        this.setLoading(true);
        const result = await this.bookService.getAllBooks();
        this.setLoading(false);

        const oModel = this.getView()?.getModel() as JSONModel;

        if (result.error) {
            MessageBox.error(result.error);
            oModel.setProperty("/books", []);
        } else {
            oModel.setProperty("/books", result.data || []);
            MessageToast.show(`Loaded ${result.data?.length || 0} books from API`);
        }
    }

    private setLoading(bLoading: boolean): void {
        const oModel = this.getView()?.getModel() as JSONModel;
        oModel.setProperty("/isLoading", bLoading);
    }
}
