import type {
    IntelligenceSnapshot,
    CorrelationSnapshot,
    VisualIntelligenceSnapshot
} from '$lib/types/intelligence';

const API = '/api/hvac';

export async function getIntelligenceSnapshot():
Promise<IntelligenceSnapshot> {

    const res = await fetch(
        `${API}/intelligence/snapshot`
    );

    if (!res.ok) {
        throw new Error(
            'Failed intelligence snapshot'
        );
    }

    return await res.json();
}

export async function getCorrelationSnapshot():
Promise<CorrelationSnapshot> {

    const res = await fetch(
        `${API}/intelligence/correlation`   
    );

    if (!res.ok) {
        throw new Error(
            'Failed correlation snapshot'
        );
    }

    return await res.json();
}

export async function getVisualSnapshot():
Promise<VisualIntelligenceSnapshot> {

    const res = await fetch(
        `${API}/visual-intelligence/snapshot`
    );

    if (!res.ok) {
        throw new Error(
            'Failed visual snapshot'
        );
    }

    return await res.json();
}

export async function getFacilityDetail(
    id: string
) {

    const res = await fetch(
        `${API}/facilities/${id}`
    );

    if (!res.ok) {
        throw new Error(
            'Failed facility detail'
        );
    }

    return await res.json();
}

export async function getClusterSnapshot() {

    const res = await fetch(
        '/api/hvac/intelligence/clusters'
    );

    if (!res.ok) {

        throw new Error(
            'Failed cluster snapshot'
        );
    }

    return await res.json();
}