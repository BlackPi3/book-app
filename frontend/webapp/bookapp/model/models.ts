import JSONModel from "sap/ui/model/json/JSONModel";
import Device from "sap/ui/Device";

export default {
    /**
     * Provides runtime info for the device the UI5 app is running on as JSONModel
     */
    createDeviceModel(): JSONModel {
        const oModel = new JSONModel(Device);
        oModel.setDefaultBindingMode("OneWay");
        return oModel;
    },

    /**
     * Creates a JSON model for book data management
     */
    createBookModel(): JSONModel {
        const oModel = new JSONModel({
            books: [],
            selectedBook: null,
            loading: false,
            searchQuery: "",
            totalCount: 0
        });
        return oModel;
    }
};