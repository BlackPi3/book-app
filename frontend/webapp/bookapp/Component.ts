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

        // Routing disabled (no routing section in manifest) – removed getRouter().initialize()
        // console.log for debug
        // @ts-ignore
        window.__BOOKAPP_INIT__ = true;
        // eslint-disable-next-line no-console
        console.log("BookApp Component init completed (no router)");
    }
}
