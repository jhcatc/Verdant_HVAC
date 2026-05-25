<script lang="ts">
    import { onMount } from 'svelte';
    import { page } from '$app/state';

    import {
        getFacilityDetail
    } from '$lib/api/intelligence';

    type FacilityDetail = {
        location_id: string;
        health_score: number;
        equipment: {
            asset_tag: string;
            failures: number;
        }[];
    };
    let facility =
        $state<FacilityDetail | null>(
            null
        );

    onMount(async () => {

        const id = page.params.id;

        facility = await getFacilityDetail(id);
    });
</script>

<div class="p-6 space-y-6 text-white">

    <h1 class="text-3xl font-bold">
        Facility Detail
    </h1>

    {#if facility}

        <!-- HEALTH -->

        <div class="bg-slate-800 rounded-xl p-5">

            <div class="flex justify-between">

                <div>
                    Facility #{facility.location_id}
                </div>

                <div>
                    Health Score: {facility.health_score}
                </div>

            </div>

        </div>

        <!-- EQUIPMENT -->

        <div class="bg-slate-800 rounded-xl p-5">

            <h2 class="text-xl font-semibold mb-4">
                Equipment
            </h2>

            <div class="space-y-2">

                {#each facility.equipment as item}

                    <div class="bg-slate-900 rounded p-3">

                        <div class="font-semibold">
                            {item.asset_tag}
                        </div>

                        <div class="text-sm text-gray-400">
                            Failures: {item.failures}
                        </div>

                    </div>

                {/each}

            </div>

        </div>

        <!-- ACTIONS -->

        <div class="bg-slate-800 rounded-xl p-5">

            <h2 class="text-xl font-semibold mb-4">
                Manual Actions
            </h2>

            <div class="flex gap-3">

                <button class="bg-emerald-600 px-4 py-2 rounded">
                    Create Internal Ticket
                </button>

                <button class="bg-slate-700 px-4 py-2 rounded">
                    Review SLA
                </button>

                <button class="bg-slate-700 px-4 py-2 rounded">
                    View Service Orders
                </button>

            </div>

        </div>

    {/if}

</div>