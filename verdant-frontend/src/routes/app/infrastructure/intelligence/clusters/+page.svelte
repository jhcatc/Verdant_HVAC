<script lang="ts">

    import { onMount } from 'svelte';

    import {
        getClusterSnapshot
    } from '$lib/api/intelligence';

    import type {
        VisualIntelligenceSnapshot
    } from '$lib/types/intelligence';

    let loading = $state(true);

    let error = $state('');

    let data =
        $state<VisualIntelligenceSnapshot | null>(null);

    async function load() {

        try {

            loading = true;

            data =
                await getClusterSnapshot();

        } catch (e) {

            console.error(e);

            error =
                'Failed loading clusters';

        } finally {

            loading = false;
        }
    }

    onMount(load);

</script>

<div class="p-6 space-y-6 text-white">

    <div>

        <h1 class="text-3xl font-bold">
            Failure Clusters
        </h1>

        <p class="text-sm text-gray-400 mt-1">
            Infrastructure failure concentration
            and anomaly grouping intelligence.
        </p>

    </div>

    {#if loading}

        <div
            class="rounded-2xl border border-gray-800 bg-gray-900 p-8"
        >
            Loading clusters...
        </div>

    {:else if error}

        <div
            class="rounded-2xl border border-red-900 bg-red-950/40 p-6 text-red-400"
        >
            {error}
        </div>

    {:else if data?.clusters?.length}

        <div class="space-y-4">

            {#each data.clusters as cluster}

                <div
                    class="rounded-2xl border border-gray-800 bg-gray-900 p-6"
                >

                    <div
                        class="flex items-center justify-between"
                    >

                        <div>

                            <div
                                class="text-lg font-semibold"
                            >
                                Customer
                                {cluster.customer_id}
                            </div>

                            <div
                                class="text-sm text-gray-400 mt-1"
                            >
                                {cluster.cluster_type}
                            </div>

                        </div>

                        <div
                            class="rounded-xl bg-emerald-600/20 border border-emerald-700 px-4 py-2"
                        >

                            <div
                                class="text-xs text-emerald-400 uppercase"
                            >
                                Cluster Strength
                            </div>

                            <div
                                class="text-xl font-bold text-emerald-300 mt-1"
                            >
                                {cluster.cluster_strength}
                            </div>

                        </div>

                    </div>

                </div>

            {/each}

        </div>

    {:else}

        <div
            class="rounded-2xl border border-dashed border-gray-700 p-10 text-center text-gray-500"
        >
            No failure clusters detected.
        </div>

    {/if}

</div>