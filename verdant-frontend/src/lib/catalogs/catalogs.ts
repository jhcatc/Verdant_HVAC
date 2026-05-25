import type {
    EquipmentCatalogs
} from '$lib/types/catalogs';

export async function
loadEquipmentCatalogs():
Promise<EquipmentCatalogs> {

    const response = await fetch(
        '/api/catalogs'
    );

    if (!response.ok) {

        throw new Error(
            'Failed to load catalogs'
        );
    }

    return response.json();
}