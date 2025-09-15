var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
define(["require", "exports", "sap/ui/core/UIComponent", "./model/models"], function (require, exports, UIComponent_1, models_1) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    UIComponent_1 = __importDefault(UIComponent_1);
    models_1 = __importDefault(models_1);
    /**
     * @namespace bookapp
     */
    class Component extends UIComponent_1.default {
        /**
         * The component is initialized by UI5 automatically during the startup of the app and calls the init method once.
         * @public
         * @override
         */
        init() {
            // call the base component's init function
            super.init();
            // set the device model
            this.setModel(models_1.default.createDeviceModel(), "device");
            // create the views based on the url/hash
            this.getRouter().initialize();
        }
    }
    Component.metadata = {
        manifest: "json"
    };
    exports.default = Component;
});
