export type CatalogBase = {

    id: number;
    name: string;
};

export type EquipmentCategory =
    CatalogBase & {

        code?: string;
    };

export type EquipmentType =
    CatalogBase & {

        category_id?: number;
    };
export type Brand =
    CatalogBase;
export type RefrigerantType =
    CatalogBase;
export type VoltageType =
    CatalogBase;
export type EquipmentStatus =
    CatalogBase;
export type InstallationType =
    CatalogBase;
export type PowerSource =
    CatalogBase;
export type MaintenanceType =
    CatalogBase;