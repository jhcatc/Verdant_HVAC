import api from '$lib/api/client';

import type {
    Opportunity
} from '$lib/types/crm';

export async function getOpportunities() {

    const res = await api.get(
        '/crm/opportunities'
    );

    return res.data;
}

export async function getOpportunity(
    id: string
) {

    const res = await api.get(
        `/crm/opportunities/${id}`
    );

    return res.data;
}

export async function createOpportunity(
    data: Partial<Opportunity>
) {

    const res = await api.post(
        '/crm/opportunities',
        data
    );

    return res.data;
}

export async function updateOpportunityStage(
    id: string,
    stage: string
) {

    const res = await api.patch(
        `/crm/opportunities/${id}/stage`,
        { stage }
    );

    return res.data;
}

export async function deleteOpportunity(
    id: string
) {

    const res = await api.delete(
        `/crm/opportunities/${id}`
    );

    return res.data;
}