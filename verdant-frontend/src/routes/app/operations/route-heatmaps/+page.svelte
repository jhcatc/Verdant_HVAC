<script lang="ts">

    let hotspots = [
        {
            zone: 'Downtown',
            density: 'Very High',
            activeRoutes: 18,
            slaRisk: 'Low'
        },
        {
            zone: 'North Industrial',
            density: 'High',
            activeRoutes: 12,
            slaRisk: 'Medium'
        },
        {
            zone: 'South Retail',
            density: 'Medium',
            activeRoutes: 7,
            slaRisk: 'Low'
        }
    ];

</script>

<div class="space-y-6">

    <div>
        <h1 class="text-3xl font-bold text-white">
            Route Heatmaps
        </h1>

        <p class="text-slate-400 mt-2">
            Geographic route compression and SLA-aware density visualization.
        </p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">

        {#each hotspots as spot}

            <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5">

                <div class="flex items-center justify-between">

                    <div class="text-lg font-semibold text-white">
                        {spot.zone}
                    </div>

                    <div class="text-xs px-2 py-1 rounded-full bg-emerald-500/20 text-emerald-400">
                        {spot.density}
                    </div>

                </div>

                <div class="mt-5 space-y-2">

                    <div class="flex justify-between text-sm">
                        <span class="text-slate-400">
                            Active Routes
                        </span>

                        <span class="text-white">
                            {spot.activeRoutes}
                        </span>
                    </div>

                    <div class="flex justify-between text-sm">
                        <span class="text-slate-400">
                            SLA Risk
                        </span>

                        <span class="text-cyan-400">
                            {spot.slaRisk}
                        </span>
                    </div>

                </div>

            </div>

        {/each}

    </div>

</div>