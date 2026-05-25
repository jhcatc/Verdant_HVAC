import api from '$lib/api/client';

export async function getEquipmentCatalog(
    search = ''
) {

    const response = await api.get(
        '/crm/equipment-catalog',
        {
            params: { search }
        }
    );

    return response.data;
}