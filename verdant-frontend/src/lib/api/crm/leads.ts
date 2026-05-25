import api from '$lib/api/client';

export async function getLeads(params?: {
    search?: string;
}) {

    const res = await api.get(
        '/crm/leads/',
        {
            params
        }
    );

    return res.data;
}

export async function createLead(
    payload: any
) {

    const res = await api.post(
        '/crm/leads/',
        payload
    );

    return res.data;
}

export async function deleteLead(
    id: string
) {

    const res = await api.delete(
        `/crm/leads/${id}`
    );

    return res.data;
}

export async function getLeadMetrics() {

    const res = await api.get(
        '/crm/leads/metrics'
    );

    return res.data;
}