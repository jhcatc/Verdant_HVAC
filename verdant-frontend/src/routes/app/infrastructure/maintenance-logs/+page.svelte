<script lang="ts">

    import { onMount } from 'svelte';

    import type {
        MaintenanceLog
    } from '$lib/types/maintenance';

    let logs =
        $state<MaintenanceLog[]>([]);

    let loading =
        $state(true);

    async function load() {

        try {

            const res =
                await fetch(
                    '/api/hvac/maintenance/logs'
                );

            logs =
                await res.json();

        } finally {

            loading = false;
        }
    }

    onMount(load);

</script>

<div class="space-y-6 p-6">

    <div>

        <h1
            class="text-3xl font-bold text-white"
        >
            Maintenance Logs
        </h1>

        <p
            class="text-sm text-gray-400 mt-1"
        >
            Cross-equipment maintenance history,
            diagnostics and technician activity.
        </p>

    </div>

    {#if loading}

        <div
            class="rounded-2xl border border-gray-800 bg-gray-900 p-8"
        >
            Loading maintenance logs...
        </div>

    {:else}

        <div class="space-y-4">

            {#each logs as log}

                <div
                    class="rounded-2xl border border-gray-800 bg-gray-900 p-5"
                >

                    <div
                        class="flex items-center justify-between"
                    >

                        <div>

                            <div
                                class="text-lg font-semibold text-white"
                            >
                                {log.maintenance_type}
                            </div>

                            <div
                                class="text-sm text-gray-400"
                            >
                                {log.created_at}
                            </div>

                        </div>

                        <div
                            class="text-xs px-3 py-1 rounded-xl bg-emerald-500/20 text-emerald-400"
                        >
                            {log.equipment_condition}
                        </div>

                    </div>

                    <div
                        class="mt-4 text-sm text-gray-300"
                    >
                        {log.notes}
                    </div>

                </div>

            {/each}

        </div>

    {/if}

</div>