<script lang="ts">
    import { onMount } from 'svelte';

    let loading = $state(true);

    let routes = $state([
        {
            technician: 'Mike Johnson',
            zone: 'North District',
            orders: 12,
            driveTime: '4h 10m',
            utilization: 91,
            etaAccuracy: 96
        },
        {
            technician: 'Sarah Connor',
            zone: 'Downtown',
            orders: 9,
            driveTime: '2h 50m',
            utilization: 87,
            etaAccuracy: 94
        },
        {
            technician: 'David Miller',
            zone: 'Industrial West',
            orders: 15,
            driveTime: '5h 20m',
            utilization: 97,
            etaAccuracy: 92
        }
    ]);

    onMount(async () => {
        await new Promise((r) => setTimeout(r, 500));
        loading = false;
    });
</script>

<div class="space-y-6">

    <div>
        <h1 class="text-3xl font-bold text-white">
            Route Optimization
        </h1>

        <p class="text-slate-400 mt-2">
            Traffic-aware dispatch optimization and technician route orchestration.
        </p>
    </div>

    {#if loading}

        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-8">
            <div class="text-slate-400">
                Loading optimization engine...
            </div>
        </div>

    {:else}

        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">

            <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5">
                <div class="text-sm text-slate-400">
                    Active Routes
                </div>

                <div class="text-3xl font-bold text-white mt-2">
                    36
                </div>
            </div>

            <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5">
                <div class="text-sm text-slate-400">
                    Avg ETA Accuracy
                </div>

                <div class="text-3xl font-bold text-emerald-400 mt-2">
                    94%
                </div>
            </div>

            <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5">
                <div class="text-sm text-slate-400">
                    Travel Reduction
                </div>

                <div class="text-3xl font-bold text-cyan-400 mt-2">
                    -22%
                </div>
            </div>

            <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5">
                <div class="text-sm text-slate-400">
                    Same-Building Batches
                </div>

                <div class="text-3xl font-bold text-orange-400 mt-2">
                    18
                </div>
            </div>

        </div>

        <div class="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden">

            <div class="p-5 border-b border-slate-800">
                <h2 class="text-xl font-semibold text-white">
                    Technician Route Matrix
                </h2>
            </div>

            <table class="w-full">

                <thead class="bg-slate-950 text-slate-400 text-sm">
                    <tr>
                        <th class="text-left p-4">Technician</th>
                        <th class="text-left p-4">Zone</th>
                        <th class="text-left p-4">Orders</th>
                        <th class="text-left p-4">Drive Time</th>
                        <th class="text-left p-4">Utilization</th>
                        <th class="text-left p-4">ETA Accuracy</th>
                    </tr>
                </thead>

                <tbody>

                    {#each routes as route}

                        <tr class="border-t border-slate-800 hover:bg-slate-800/40 transition">

                            <td class="p-4 text-white font-medium">
                                {route.technician}
                            </td>

                            <td class="p-4 text-slate-300">
                                {route.zone}
                            </td>

                            <td class="p-4 text-slate-300">
                                {route.orders}
                            </td>

                            <td class="p-4 text-slate-300">
                                {route.driveTime}
                            </td>

                            <td class="p-4">
                                <span class="text-emerald-400 font-semibold">
                                    {route.utilization}%
                                </span>
                            </td>

                            <td class="p-4">
                                <span class="text-cyan-400 font-semibold">
                                    {route.etaAccuracy}%
                                </span>
                            </td>

                        </tr>

                    {/each}

                </tbody>

            </table>

        </div>

    {/if}

</div>