<script lang="ts">
    import { onMount } from 'svelte';
    import {
        getOptimizedRoutes
    } from '$lib/api/serviceOrders';

    let loading = $state(true);
    let routes = $state([]);

    async function loadRoutes() {
        loading = true;

        try {
            const res = await getOptimizedRoutes();
            routes = res.data;
        } catch (err) {
            console.error(err);
        } finally {
            loading = false;
        }
    }

    onMount(loadRoutes);
</script>

<h1 class="text-3xl font-bold mb-6">
    Route Optimization Engine
</h1>

{#if loading}

    <div class="text-gray-500">
        Loading routes...
    </div>

{:else}

    <div class="space-y-6">

        {#each routes as route}

            <div class="bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-800 overflow-hidden">

                <!-- HEADER -->
                <div class="p-5 border-b border-gray-200 dark:border-gray-800 flex items-center justify-between">

                    <div>
                        <div class="text-lg font-semibold">
                            {route.technician_name}
                        </div>

                        <div class="text-sm text-gray-500 mt-1">
                            {route.total_orders} stops
                            ·
                            {route.total_distance_km} km
                        </div>
                    </div>

                    <div class="bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300 px-3 py-1 rounded-xl text-sm">
                        Optimized
                    </div>

                </div>

                <!-- STOPS -->
                <div class="divide-y divide-gray-100 dark:divide-gray-800">

                    {#each route.orders as stop}

                        <div class="p-5 flex items-start gap-4">

                            <!-- SEQUENCE -->
                            <div class="w-10 h-10 rounded-full bg-verdant text-white flex items-center justify-center font-semibold shrink-0">
                                {stop.sequence}
                            </div>

                            <!-- CONTENT -->
                            <div class="flex-1">

                                <div class="flex items-center justify-between">

                                    <div>

                                        <div class="font-semibold text-gray-900 dark:text-white">
                                            {stop.title}
                                        </div>

                                        <div class="text-sm text-gray-500 mt-1">
                                            {stop.customer}
                                        </div>

                                    </div>

                                    <div class="text-right text-sm">

                                        <div class="text-gray-700 dark:text-gray-200">
                                            ETA:
                                            {stop.eta_minutes}m
                                        </div>

                                        <div class="text-gray-500">
                                            {stop.distance_from_previous_km} km
                                        </div>

                                    </div>

                                </div>

                                <div class="mt-3 grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">

                                    <div>
                                        <div class="text-gray-400">
                                            Equipment
                                        </div>

                                        <div class="text-gray-700 dark:text-gray-200">
                                            {stop.equipment ?? 'N/A'}
                                        </div>
                                    </div>

                                    <div>
                                        <div class="text-gray-400">
                                            Address
                                        </div>

                                        <div class="text-gray-700 dark:text-gray-200">
                                            {stop.address ?? 'N/A'}
                                        </div>
                                    </div>

                                    <div>
                                        <div class="text-gray-400">
                                            Scheduled
                                        </div>

                                        <div class="text-gray-700 dark:text-gray-200">
                                            {new Date(stop.scheduled_at).toLocaleString()}
                                        </div>
                                    </div>

                                </div>

                            </div>

                        </div>

                    {/each}

                </div>

            </div>

        {/each}

    </div>

{/if}