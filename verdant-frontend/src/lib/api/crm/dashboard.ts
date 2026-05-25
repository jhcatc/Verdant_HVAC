import api from '$lib/api/client';

export async function getDashboard() {

    const response = await api.get(
        '/crm/dashboard'
    );

    return response.data;
}