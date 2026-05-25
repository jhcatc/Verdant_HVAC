<script lang="ts">
    import { onMount } from 'svelte';
    import { getRouteHeatmap } from '$lib/api/serviceOrders';

    let loading = $state(true);
    let points = $state([]);

    onMount(async () => {
        try {
            const res = await getRouteHeatmap();
            points = res.data;
        } catch (err) {
            console.error(err);
        } finally {
            loading = false;
        }
    });
</script>

<h1 class="text-3xl font-bold mb-6">
    Route Heatmap
</h1>

{#if loading}

    <div>Loading heatmap...</div>

{:else}

    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">

        {#each points as p}

            <div class="rounded-2xl border border-gray-200 dark:border-gray-800 p-4 bg-white dark:bg-gray-900">

                <div class="flex items-center justify-between">

                    <div class="font-semibold">
                        {p.status}
                    </div>

                    <div class="text-sm text-gray-500">
                        weight {p.weight}
                    </div>

                </div>

                <div class="mt-4 space-y-2 text-sm">

                    <div>
                        Lat:
                        {p.lat}
                    </div>

                    <div>
                        Lng:
                        {p.lng}
                    </div>

                </div>

            </div>

        {/each}

    </div>

{/if}