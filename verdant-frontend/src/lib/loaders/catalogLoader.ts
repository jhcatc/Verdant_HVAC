import {
    loadEquipmentCatalogs
} from '$lib/api/catalogs';

import type {
    EquipmentCatalogs
} from '$lib/api/catalogs';

let cachedCatalogs:
EquipmentCatalogs | null = null;

export async function
getCatalogs():

Promise<EquipmentCatalogs> {

    if (cachedCatalogs) {

        return cachedCatalogs;
    }

    cachedCatalogs =
        await loadEquipmentCatalogs();

    return cachedCatalogs;
}