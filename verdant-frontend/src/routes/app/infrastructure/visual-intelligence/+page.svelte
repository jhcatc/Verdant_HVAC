<script lang="ts">
    import { onMount } from 'svelte';
    import { getVisualIntelligenceSnapshot } from '$lib/api/visual-intelligence';

    import type {
        IntelligenceSnapshot
    } from '$lib/types/intelligence';
    let loading = $state(true);

    onMount(async () => {
        data = await getVisualIntelligenceSnapshot();
        loading = false;
    });
</script>

<div class="p-6 space-y-6 text-white">

    <h1 class="text-2xl font-bold">
        Infrastructure Visual Intelligence
    </h1>

    {#if loading}
        <p class="text-gray-400">Loading...</p>
    {:else}

        <!-- HEALTH -->
        <div class="bg-slate-800 p-4 rounded">
            <h2 class="font-semibold mb-2">Facility Health</h2>

            {#each data.facility_health as item}
                <div class="flex justify-between border-b border-slate-700 py-1">
                    <span>{item.location_id}</span>
                    <span>{item.health_score} ({item.status})</span>
                </div>
            {/each}
        </div>

        <!-- CLUSTERS -->
        <div class="bg-slate-800 p-4 rounded">
            <h2 class="font-semibold mb-2">Failure Clusters</h2>

            {#each data.clusters as c}
                <div class="py-1">
                    {c.customer_id} → {c.cluster_type} ({c.cluster_strength})
                </div>
            {/each}
        </div>

    {/if}

</div>