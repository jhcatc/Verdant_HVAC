import api from '$lib/api/client';
export type CreateEquipmentDto = {
    customer_id: string;
    location_id: string;
    asset_tag: string;
    equipment_category: string;
    equipment_type: string;
    brand?: string;
    model?: string;
    serial_number?: string;
};
export async function createEquipment(
    data: CreateEquipmentDto
) 
export async function getEquipment(filters?: {
    customer_id?: string;
    location_id?: string;
}) {

    const params = new URLSearchParams();

    if (filters?.customer_id) {
        params.append(
            'customer_id',
            filters.customer_id
        );
    }

    if (filters?.location_id) {
        params.append(
            'location_id',
            filters.location_id
        );
    }

    const query = params.toString();
    const response = await api.get(
        `/equipment${query ? `?${query}` : ''}`
    );

    return response.data;
}

export async function getEquipmentById(id: string) {
    const { data } = await api.get(
        `/equipment/${id}`
    );

    return data;
}

export type EquipmentCreatePayload = {
    asset_tag: string;
    model?: string;
    serial_number?: string;
    manufacture_year?: number;
    installation_date?: string;
    warranty_expiration?: string;
    capacity?: string;
    seer_rating?: number;
    eer_rating?: number;
    customer_id?: string;
    location_id?: string;
    equipment_category_id?: number;
    equipment_type_id?: number;
    brand_id?: number;
    equipment_status_id?: number;
    refrigerant_type_id?: number;
    voltage_type_id?: number;
    installation_type_id?: number;
    power_source_id?: number;
};

export async function getEquipmentList(
    filters: {
        customer_id?: number;
        location_id?: number;
    }
) {

    const params =
        new URLSearchParams();
    if (filters.customer_id) {
        params.append(
            'customer_id',
            String(filters.customer_id)
        );
    }

    if (filters.location_id) {
        params.append(
            'location_id',
            String(filters.location_id)
        );
    }

    const res = await fetch(
        `/api/hvac/equipment?${params}`
    );

    if (!res.ok) {
        throw new Error(
            'Failed loading equipment'
        );
    }

    return await res.json();
}