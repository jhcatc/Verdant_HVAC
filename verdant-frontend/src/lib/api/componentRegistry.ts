import type {
    ComponentRegistrySnapshot
} from '$lib/types/component-registry';

const API = '/api/hvac';

export async function
getComponentRegistrySnapshot():
Promise<ComponentRegistrySnapshot> {

    const response = await fetch(
        `${API}/component-registry/snapshot`
    );

    if (!response.ok) {

        throw new Error(
            'Failed component registry snapshot'
        );
    }

    return await response.json();
}