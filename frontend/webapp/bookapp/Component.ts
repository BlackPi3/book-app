import UIComponent from "sap/ui/core/UIComponent";
import models from "./model/models";

/**
 * @namespace bookapp
 */
export default class Component extends UIComponent {

    public static metadata = {
        manifest: "json"
    };

    /**
     * The component is initialized by UI5 automatically during the startup of the app and calls the init method once.
     * @public
     * @override
     */
    public init(): void {
        // call the base component's init function
        super.init();

        // set the device model
        this.setModel(models.createDeviceModel(), "device");

        // create the views based on the url/hash
        this.getRouter().initialize();
    }
}
