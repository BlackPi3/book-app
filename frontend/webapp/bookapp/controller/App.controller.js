sap.ui.define([
    "sap/ui/core/mvc/Controller"
], function (Controller) {
    "use strict";

    return Controller.extend("bookapp.controller.App", {
        onInit: function () {
            var oApp = this.byId("app");
            if (oApp && oApp.getPages().length === 0) {
                // Create Main view and add as first page
                var oMainView = sap.ui.xmlview({ id: this.createId("Main"), viewName: "bookapp.view.Main" });
                oApp.addPage(oMainView);
                // eslint-disable-next-line no-console
                console.log("[BookApp] App.controller: Main view added. Table global ID:", oMainView.byId("booksTable").getId());
            }
        }
    });
});