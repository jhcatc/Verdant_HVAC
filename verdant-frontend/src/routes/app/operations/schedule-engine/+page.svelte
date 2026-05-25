<script lang="ts">

    let schedulingMetrics = [
        {
            title: 'Recurring PM Waves',
            value: 24
        },
        {
            title: 'Emergency Insertions',
            value: 8
        },
        {
            title: 'Technician PTO Blocks',
            value: 11
        },
        {
            title: 'AI Rebalances',
            value: 17
        }
    ];

    let upcomingWaves = [
        {
            name: 'Downtown PM Wave',
            technicians: 6,
            orders: 42,
            date: '2026-05-20'
        },
        {
            name: 'Industrial HVAC Cycle',
            technicians: 9,
            orders: 61,
            date: '2026-05-23'
        },
        {
            name: 'Retail Seasonal PM',
            technicians: 5,
            orders: 29,
            date: '2026-05-28'
        }
    ];

</script>

<div class="space-y-6">

    <div>
        <h1 class="text-3xl font-bold text-white">
            Scheduling Engine
        </h1>

        <p class="text-slate-400 mt-2">
            Enterprise scheduling orchestration with AI rebalance and PM wave planning.
        </p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">

        {#each schedulingMetrics as metric}

            <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5">

                <div class="text-sm text-slate-400">
                    {metric.title}
                </div>

                <div class="text-3xl font-bold text-emerald-400 mt-3">
                    {metric.value}
                </div>

            </div>

        {/each}

    </div>

    <div class="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden">

        <div class="p-5 border-b border-slate-800">

            <h2 class="text-xl font-semibold text-white">
                Upcoming PM Waves
            </h2>

        </div>

        <table class="w-full">

            <thead class="bg-slate-950 text-slate-400 text-sm">

                <tr>
                    <th class="text-left p-4">Wave</th>
                    <th class="text-left p-4">Technicians</th>
                    <th class="text-left p-4">Orders</th>
                    <th class="text-left p-4">Date</th>
                </tr>

            </thead>

            <tbody>

                {#each upcomingWaves as wave}

                    <tr class="border-t border-slate-800 hover:bg-slate-800/40 transition">

                        <td class="p-4 text-white font-medium">
                            {wave.name}
                        </td>

                        <td class="p-4 text-slate-300">
                            {wave.technicians}
                        </td>

                        <td class="p-4 text-slate-300">
                            {wave.orders}
                        </td>

                        <td class="p-4 text-cyan-400 font-medium">
                            {wave.date}
                        </td>

                    </tr>

                {/each}

            </tbody>

        </table>

    </div>

</div>