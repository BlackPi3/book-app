var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
define(["require", "exports", "sap/ui/model/json/JSONModel", "sap/ui/Device"], function (require, exports, JSONModel_1, Device_1) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    JSONModel_1 = __importDefault(JSONModel_1);
    Device_1 = __importDefault(Device_1);
    exports.default = {
        createDeviceModel: function () {
            const oModel = new JSONModel_1.default(Device_1.default);
            oModel.setDefaultBindingMode("OneWay");
            return oModel;
        }
    };
});
