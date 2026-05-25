import { writable } from 'svelte/store';

import {
    getIntelligenceSnapshot
} from '$lib/api/intelligence';

import {
    getComponentRegistrySnapshot
} from '$lib/api/componentRegistry';

type InfrastructureStore = {
    initialized: boolean;
    intelligence: any;
    components: any;
    loading: boolean;
};

const initialState:
InfrastructureStore = {
    initialized: false,
    intelligence: null,
    components: null,
    loading: false
};

function createInfrastructureStore() {

    const {
        subscribe,
        update,
        set
    } = writable(initialState);

    return {
        subscribe,
        async hydrate() {
            update(state => ({
                ...state,
                loading: true
            }));

            try {

                const [
                    intelligence,
                    components
                ] = await Promise.all([
                    getIntelligenceSnapshot(),
                    getComponentRegistrySnapshot()
                ]);

                set({

                    initialized: true,
                    intelligence,
                    components,
                    loading: false
                });

            } catch (error) {

                console.error(error);
                update(state => ({
                    ...state,
                    loading: false
                }));
            }
        }
    };
}

export const infrastructureStore =
    createInfrastructureStore();