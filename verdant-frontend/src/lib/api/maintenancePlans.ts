import api from '$lib/api/client';

export async function getMaintenancePlans() {

    const { data } = await api.get(
        '/maintenance-plans'
    );

    return data;
}

export async function createMaintenancePlan(
    payload: any
) {

    const { data } = await api.post(
        '/maintenance-plans',
        payload
    );

    return data;
}