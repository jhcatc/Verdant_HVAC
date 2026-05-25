import api from '$lib/api/client';

import type {
    CRMIntelligenceResponse
} from '$lib/types/crm/intelligence';

export async function getCRMIntelligence():
Promise<CRMIntelligenceResponse> {

    const res = await api.get(
        '/crm/intelligence'
    );

    return res.data;
}