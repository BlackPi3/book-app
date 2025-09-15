// Initialize the SAPUI5 application using modern APIs
sap.ui.require(
    ["sap/ui/core/Core", "sap/ui/core/Component", "sap/ui/core/ComponentContainer"],
    (Core: any, Component: any, ComponentContainer: any) => {
        Core.ready().then(async () => {
            try {
                const oComponent = await Component.create({
                    name: "bookapp"
                });

                new ComponentContainer({
                    component: oComponent
                }).placeAt("content");
            } catch (error) {
                // eslint-disable-next-line no-console
                console.error("Error initializing the SAPUI5 application:", error);
            }
        });
    }
);
