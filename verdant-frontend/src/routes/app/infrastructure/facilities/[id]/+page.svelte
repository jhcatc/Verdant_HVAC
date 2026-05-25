<script lang="ts">

    import { onMount } from 'svelte';

    import { page } from '$app/state';

    import {
        getFacilityDetail
    } from '$lib/api/intelligence';

    let facility = $state(null);

    let loading = $state(true);

    async function load() {

        try {

            facility =
                await getFacilityDetail(
                    page.params.id
                );

        } finally {

            loading = false;
        }
    }

    onMount(load);

</script>

<div class="space-y-6 p-6">

    {#if loading}

        <div
            class="rounded-2xl border border-gray-800 bg-gray-900 p-8"
        >
            Loading facility...
        </div>

    {:else if facility}

        <div>

            <h1
                class="text-3xl font-bold text-white"
            >
                {facility.name}
            </h1>

            <p
                class="text-sm text-gray-400 mt-1"
            >
                Infrastructure facility intelligence
            </p>

        </div>

        <div
            class="grid grid-cols-1 md:grid-cols-4 gap-4"
        >

            <div
                class="rounded-2xl border border-gray-800 bg-gray-900 p-5"
            >
                <div class="text-sm text-gray-400">
                    Equipment
                </div>

                <div class="text-3xl font-bold text-white mt-2">
                    {facility.total_equipment}
                </div>
            </div>

            <div
                class="rounded-2xl border border-gray-800 bg-gray-900 p-5"
            >
                <div class="text-sm text-gray-400">
                    Critical Assets
                </div>

                <div class="text-3xl font-bold text-red-500 mt-2">
                    {facility.critical_assets}
                </div>
            </div>

            <div
                class="rounded-2xl border border-gray-800 bg-gray-900 p-5"
            >
                <div class="text-sm text-gray-400">
                    Health Score
                </div>

                <div class="text-3xl font-bold text-emerald-500 mt-2">
                    {facility.health_score}%
                </div>
            </div>

            <div
                class="rounded-2xl border border-gray-800 bg-gray-900 p-5"
            >
                <div class="text-sm text-gray-400">
                    Open Work Orders
                </div>

                <div class="text-3xl font-bold text-orange-500 mt-2">
                    {facility.open_work_orders}
                </div>
            </div>

        </div>

        <!-- EQUIPMENT -->

        <div
            class="rounded-2xl border border-gray-800 bg-gray-900 p-6"
        >

            <h2
                class="text-xl font-semibold text-white"
            >
                Equipment Inventory
            </h2>

            <div
                class="mt-6 space-y-3"
            >

                {#each facility.equipment as equipment}

                    <div
                        class="rounded-xl border border-gray-800 bg-gray-950 p-4 flex items-center justify-between"
                    >

                        <div>

                            <div
                                class="font-medium text-white"
                            >
                                {equipment.asset_tag}
                            </div>

                            <div
                                class="text-sm text-gray-400"
                            >
                                {equipment.model}
                            </div>

                        </div>

                        <div
                            class="text-sm text-emerald-400"
                        >
                            {equipment.status}
                        </div>

                    </div>

                {/each}

            </div>

        </div>

    {/if}

</div>