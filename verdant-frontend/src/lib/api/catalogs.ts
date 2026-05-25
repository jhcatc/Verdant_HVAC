import type {
    Brand,
    EquipmentCategory,
    EquipmentStatus,
    EquipmentType,
    InstallationType,
    MaintenanceType,
    PowerSource,
    RefrigerantType,
    VoltageType
} from '$lib/types/catalogs';

export type EquipmentCatalogs = {
    equipment_categories:
        EquipmentCategory[];
    equipment_types:
        EquipmentType[];
    brands:
        Brand[];
    refrigerants:
        RefrigerantType[];
    voltages:
        VoltageType[];
    statuses:
        EquipmentStatus[];
    installation_types:
        InstallationType[];
    power_sources:
        PowerSource[];
    maintenance_types:
        MaintenanceType[];
};

export async function loadEquipmentCatalogs(
    fetcher: typeof fetch
): Promise<EquipmentCatalogs> {
    const response = await fetcher(
        'http://localhost:8000/api/catalogs/'
    );
    if (!response.ok) {
        throw new Error(
            'Failed to load catalogs'
        );
    }

    return await response.json();
}