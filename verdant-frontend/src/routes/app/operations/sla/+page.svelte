<script lang="ts">
    import { onMount } from 'svelte';

    import { getSLADashboard } from '$lib/api/sla';

    let dashboard = $state(null);

    let loading = $state(true);

    async function load() {

        loading = true;

        const res = await getSLADashboard();

        dashboard = res.data;

        loading = false;
    }

    onMount(load);

    function pct(v) {
        return `${v ?? 0}%`;
    }
</script>

{#if loading}

<div class="p-10 text-slate-400">
    Loading SLA engine...
</div>

{:else}

<div class="space-y-6">

    <!-- ================================================= -->
    <!-- HEADER -->
    <!-- ================================================= -->

    <div class="flex items-center justify-between">

        <div>

            <h1 class="text-3xl font-bold text-white">
                SLA & Compliance Engine
            </h1>

            <p class="text-slate-400 mt-1">
                Enterprise preventive maintenance governance,
                SLA orchestration and operational compliance.
            </p>

        </div>

    </div>

    <!-- ================================================= -->
    <!-- KPI GRID -->
    <!-- ================================================= -->

    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">

        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5">

            <div class="text-slate-400 text-sm">
                PM Compliance
            </div>

            <div class="text-4xl font-bold text-emerald-400 mt-2">
                {pct(dashboard.summary.pm_compliance_score)}
            </div>

        </div>

        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5">

            <div class="text-slate-400 text-sm">
                Overdue PM
            </div>

            <div class="text-4xl font-bold text-red-400 mt-2">
                {dashboard.summary.overdue_pm}
            </div>

        </div>

        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5">

            <div class="text-slate-400 text-sm">
                SLA Breaches
            </div>

            <div class="text-4xl font-bold text-orange-400 mt-2">
                {dashboard.summary.overdue_orders}
            </div>

        </div>

        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5">

            <div class="text-slate-400 text-sm">
                Emergency Escalations
            </div>

            <div class="text-4xl font-bold text-yellow-400 mt-2">
                {dashboard.summary.emergency_orders}
            </div>

        </div>

    </div>

    <!-- ================================================= -->
    <!-- OVERDUE PM -->
    <!-- ================================================= -->

    <div class="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden">

        <div class="p-4 border-b border-slate-800">

            <h2 class="text-lg font-semibold text-white">
                Overdue Maintenance Plans
            </h2>

        </div>

        <table class="w-full">

            <thead class="bg-slate-950 text-slate-400 text-sm">

                <tr>

                    <th class="p-4 text-left">Plan</th>
                    <th class="p-4 text-left">Next Run</th>
                    <th class="p-4 text-left">Frequency</th>

                </tr>

            </thead>

            <tbody>

                {#each dashboard.overdue_pm_plans as plan}

                    <tr class="border-t border-slate-800">

                        <td class="p-4 text-white">
                            {plan.name}
                        </td>

                        <td class="p-4 text-red-400">
                            {new Date(plan.next_run_at)
                                .toLocaleString()}
                        </td>

                        <td class="p-4 text-slate-300">
                            {plan.frequency_days} days
                        </td>

                    </tr>

                {/each}

            </tbody>

        </table>

    </div>

    <!-- ================================================= -->
    <!-- OVERDUE ORDERS -->
    <!-- ================================================= -->

    <div class="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden">

        <div class="p-4 border-b border-slate-800">

            <h2 class="text-lg font-semibold text-white">
                SLA Breaches
            </h2>

        </div>

        <table class="w-full">

            <thead class="bg-slate-950 text-slate-400 text-sm">

                <tr>

                    <th class="p-4 text-left">Order</th>
                    <th class="p-4 text-left">Customer</th>
                    <th class="p-4 text-left">Scheduled</th>
                    <th class="p-4 text-left">Priority</th>

                </tr>

            </thead>

            <tbody>

                {#each dashboard.overdue_orders as order}

                    <tr
                        class="border-t border-slate-800
                               hover:bg-slate-800/50
                               cursor-pointer"
                        onclick={() =>
                            location.href =
                            `/app/service-orders/${order.id}`
                        }
                    >

                        <td class="p-4 text-white">
                            {order.title}
                        </td>

                        <td class="p-4 text-slate-300">
                            {order.customer?.name ?? '-'}
                        </td>

                        <td class="p-4 text-red-400">
                            {new Date(order.scheduled_at)
                                .toLocaleString()}
                        </td>

                        <td class="p-4">

                            <div class="inline-flex px-3 py-1 rounded-full
                                        bg-red-500/20 text-red-400
                                        text-xs font-semibold">

                                {order.priority}

                            </div>

                        </td>

                    </tr>

                {/each}

            </tbody>

        </table>

    </div>

    <!-- ================================================= -->
    <!-- TECH UTILIZATION -->
    <!-- ================================================= -->

    <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5">

        <h2 class="text-lg font-semibold text-white mb-5">
            Technician Utilization
        </h2>

        <div class="space-y-3">

            {#each Object.entries(dashboard.technician_utilization) as [id, data]}

                <div class="bg-slate-800 rounded-xl p-4">

                    <div class="flex items-center justify-between">

                        <div class="text-white font-medium">
                            Technician {id.slice(0, 8)}
                        </div>

                        <div class="text-emerald-400 font-semibold">
                            {data.count} orders
                        </div>

                    </div>

                </div>

            {/each}

        </div>

    </div>

</div>

{/if}