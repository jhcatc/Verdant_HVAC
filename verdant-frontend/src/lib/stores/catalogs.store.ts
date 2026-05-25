import { writable } from 'svelte/store';

import {
    loadEquipmentCatalogs
} from '$lib/api/catalogs';

import type {
    EquipmentCatalogs
} from '$lib/api/catalogs';

type CatalogsState = {

    catalogs:
        EquipmentCatalogs | null;

    loading: boolean;

    loaded: boolean;
};

function createCatalogsStore() {

    const {
        subscribe,
        update,
        set
    } = writable<CatalogsState>({
        catalogs: null,
        loading: false,
        loaded: false
    });

    async function load(
        fetcher: typeof fetch = fetch
    ) {

        let alreadyLoaded = false;

        update((state) => {

            alreadyLoaded =
                state.loaded ||
                state.loading;

            if (alreadyLoaded) {
                return state;
            }

            return {
                ...state,
                loading: true
            };
        });

        if (alreadyLoaded) {
            return;
        }

        try {

            const catalogs =
                await loadEquipmentCatalogs(
                    fetcher
                );

            set({
                catalogs,
                loading: false,
                loaded: true
            });

        } catch (error) {

            console.error(
                'Failed loading catalogs',
                error
            );

            set({
                catalogs: null,
                loading: false,
                loaded: false
            });
        }
    }

    return {

        subscribe,

        load,

        getEquipmentTypesByCategory(
            categoryId: number
        ) {

            let result = [];

            update((state) => {

                result =
                    state.catalogs
                        ?.equipment_types
                        ?.filter(
                            (type) =>
                                type.category_id === categoryId
                        ) ?? [];

                return state;
            });

            return result;
        }
    };
}

export const catalogsStore =
    createCatalogsStore();