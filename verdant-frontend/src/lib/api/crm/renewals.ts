import api from '$lib/api/client';

export interface Renewal {
    contract_id: string;
    customer_id: string;
    customer_name: string;
    renewal_date: string | null;
    sla_tier: string | null;
    total_value: number | null;
    status: string | null;
}

export async function getRenewals():

    Promise<Renewal[]> {

    const response =
        await api.get('/crm/renewals');

    return response.data;
}