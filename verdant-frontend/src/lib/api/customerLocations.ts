import api from './client';

export async function getLocations() {

    const res = await api.get('/customer-locations');

    return res.data;
}

export async function getCustomerLocations(
    customerId: string
) {

    const res = await api.get(
        `/customer-locations/customer/${customerId}`
    );

    return res.data;
}

export type CreateLocationDto = {

    customer_id: string;
    name: string;
    code?: string;
    location_type?: string;
    address?: string;
    city?: string;
    state?: string;
    zip_code?: string;
    country?: string;
    contact_name?: string;
    contact_phone?: string;
    contact_email?: string;
    sla_tier?: string;
    access_notes?: string;
    refrigerant_notes?: string;
    technician_notes?: string;
    notes?: string;
};

export async function createLocation(
    data: CreateLocationDto
) {

    const res = await api.post(
        '/customer-locations',
        data
    );

    return res.data;
}