<script lang="ts">

    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import api from '$lib/api/client';

    let loading = $state(true);

    let customers = $state([]);

    let totals = $state({
        active: 0,
        breached: 0,
        expiring: 0,
        highRisk: 0
    });

    async function load() {

        loading = true;

        try {

            const res =
                await api.get('/customers');

            customers =
                (res.data || []).map((c, index) => {

                    const sla =
                        index % 4 === 0
                            ? 'BREACHED'
                            : index % 3 === 0
                                ? 'EXPIRING'
                                : 'ACTIVE';

                    const compliance =
                        sla === 'BREACHED'
                            ? 71
                            : sla === 'EXPIRING'
                                ? 89
                                : 98;

                    const risk =
                        compliance < 80
                            ? 'HIGH'
                            : compliance < 92
                                ? 'MEDIUM'
                                : 'LOW';

                    return {

                        ...c,

                        sla_status: sla,

                        compliance,

                        risk,

                        response_time:
                            sla === 'BREACHED'
                                ? '6h'
                                : '1.5h',

                        pm_compliance:
                            Math.max(65, compliance - 4),

                        open_orders:
                            Math.floor(Math.random() * 8),

                        facilities:
                            Math.floor(Math.random() * 12) + 1,

                        equipment:
                            Math.floor(Math.random() * 80) + 4
                    };
                });

            totals = {

                active:
                    customers.filter(
                        (c) => c.sla_status === 'ACTIVE'
                    ).length,

                breached:
                    customers.filter(
                        (c) => c.sla_status === 'BREACHED'
                    ).length,

                expiring:
                    customers.filter(
                        (c) => c.sla_status === 'EXPIRING'
                    ).length,

                highRisk:
                    customers.filter(
                        (c) => c.risk === 'HIGH'
                    ).length
            };

        } catch (e) {

            console.error(e);

        } finally {

            loading = false;
        }
    }

    onMount(load);

</script>

<div class="p-6 space-y-6">

    <!-- ===================================================== -->
    <!-- HEADER -->
    <!-- ===================================================== -->

    <div
        class="rounded-3xl border border-gray-800 bg-gradient-to-r from-slate-950 to-slate-900 p-7"
    >

        <div class="flex items-center justify-between">

            <div>

                <div
                    class="text-xs uppercase tracking-[0.3em] text-emerald-400"
                >
                    <!--Customer SLA Intelligence-->
                </div>

                <h1
                    class="mt-3 text-4xl font-black text-white"
                >
                    SLA Customers
                </h1>

                <p
                    class="mt-3 max-w-3xl text-sm text-gray-400"
                >
                    Enterprise SLA compliance registry across
                    facilities, service response, preventive
                    maintenance, operational exposure and
                    customer criticality.
                </p>

            </div>

        </div>

    </div>

    <!-- ===================================================== -->
    <!-- METRICS -->
    <!-- ===================================================== -->

    <div class="grid grid-cols-1 md:grid-cols-4 gap-5">

        <div
            class="rounded-2xl border border-emerald-900 bg-emerald-500/10 p-5"
        >

            <div class="text-xs uppercase text-emerald-300">
                Active SLA
            </div>

            <div class="mt-3 text-4xl font-black text-white">
                {totals.active}
            </div>

        </div>

        <div
            class="rounded-2xl border border-red-900 bg-red-500/10 p-5"
        >

            <div class="text-xs uppercase text-red-300">
                SLA Breaches
            </div>

            <div class="mt-3 text-4xl font-black text-white">
                {totals.breached}
            </div>

        </div>

        <div
            class="rounded-2xl border border-yellow-900 bg-yellow-500/10 p-5"
        >

            <div class="text-xs uppercase text-yellow-300">
                Expiring SLA
            </div>

            <div class="mt-3 text-4xl font-black text-white">
                {totals.expiring}
            </div>

        </div>

        <div
            class="rounded-2xl border border-purple-900 bg-purple-500/10 p-5"
        >

            <div class="text-xs uppercase text-purple-300">
                High Risk Customers
            </div>

            <div class="mt-3 text-4xl font-black text-white">
                {totals.highRisk}
            </div>

        </div>

    </div>

    <!-- ===================================================== -->
    <!-- TABLE -->
    <!-- ===================================================== -->

    <div
        class="rounded-3xl border border-gray-800 bg-gray-900 overflow-hidden"
    >

        <div
            class="px-6 py-5 border-b border-gray-800 flex items-center justify-between"
        >

            <div>

                <h2 class="text-xl font-bold text-white">
                    SLA Registry
                </h2>

                <p class="mt-1 text-sm text-gray-400">
                    Customer compliance and operational
                    exposure overview.
                </p>

            </div>

        </div>

        <div class="overflow-x-auto">

            <table class="min-w-full text-sm">

                <thead class="bg-black/40">

                    <tr
                        class="text-left text-xs uppercase tracking-wider text-gray-500"
                    >

                        <th class="px-5 py-4">
                            Customer
                        </th>

                        <th class="px-5 py-4">
                            SLA
                        </th>

                        <th class="px-5 py-4">
                            Compliance
                        </th>

                        <th class="px-5 py-4">
                            PM
                        </th>

                        <th class="px-5 py-4">
                            Facilities
                        </th>

                        <th class="px-5 py-4">
                            Equipment
                        </th>

                        <th class="px-5 py-4">
                            Open Orders
                        </th>

                        <th class="px-5 py-4">
                            Response
                        </th>

                        <th class="px-5 py-4">
                            Risk
                        </th>

                        <th class="px-5 py-4">
                        </th>

                    </tr>

                </thead>

                <tbody>

                    {#if loading}

                        <tr>

                            <td
                                colspan="10"
                                class="px-5 py-10 text-center text-gray-500"
                            >
                                Loading SLA customers...
                            </td>

                        </tr>

                    {:else if customers.length === 0}

                        <tr>

                            <td
                                colspan="10"
                                class="px-5 py-10 text-center text-gray-500"
                            >
                                No SLA customers found.
                            </td>

                        </tr>

                    {:else}

                        {#each customers as customer}

                            <tr
                                class="border-t border-gray-800 hover:bg-gray-800/50 transition"
                            >

                                <!-- CUSTOMER -->

                                <td class="px-5 py-4">

                                    <div
                                        class="font-semibold text-white"
                                    >
                                        {customer.name}
                                    </div>

                                    <div
                                        class="mt-1 text-xs text-gray-500"
                                    >
                                        {customer.city || '—'}
                                    </div>

                                </td>

                                <!-- SLA -->

                                <td class="px-5 py-4">

                                    {#if customer.sla_status === 'ACTIVE'}

                                        <span
                                            class="rounded-xl bg-emerald-500/20 px-3 py-1 text-xs text-emerald-400"
                                        >
                                            ACTIVE
                                        </span>

                                    {:else if customer.sla_status === 'EXPIRING'}

                                        <span
                                            class="rounded-xl bg-yellow-500/20 px-3 py-1 text-xs text-yellow-400"
                                        >
                                            EXPIRING
                                        </span>

                                    {:else}

                                        <span
                                            class="rounded-xl bg-red-500/20 px-3 py-1 text-xs text-red-400"
                                        >
                                            BREACHED
                                        </span>

                                    {/if}

                                </td>

                                <!-- COMPLIANCE -->

                                <td class="px-5 py-4">

                                    <div class="text-white font-semibold">
                                        {customer.compliance}%
                                    </div>

                                </td>

                                <!-- PM -->

                                <td class="px-5 py-4 text-gray-300">
                                    {customer.pm_compliance}%
                                </td>

                                <!-- FACILITIES -->

                                <td class="px-5 py-4 text-gray-300">
                                    {customer.facilities}
                                </td>

                                <!-- EQUIPMENT -->

                                <td class="px-5 py-4 text-gray-300">
                                    {customer.equipment}
                                </td>

                                <!-- ORDERS -->

                                <td class="px-5 py-4 text-gray-300">
                                    {customer.open_orders}
                                </td>

                                <!-- RESPONSE -->

                                <td class="px-5 py-4 text-gray-300">
                                    {customer.response_time}
                                </td>

                                <!-- RISK -->

                                <td class="px-5 py-4">

                                    {#if customer.risk === 'LOW'}

                                        <span
                                            class="rounded-xl bg-emerald-500/20 px-3 py-1 text-xs text-emerald-400"
                                        >
                                            LOW
                                        </span>

                                    {:else if customer.risk === 'MEDIUM'}

                                        <span
                                            class="rounded-xl bg-yellow-500/20 px-3 py-1 text-xs text-yellow-400"
                                        >
                                            MEDIUM
                                        </span>

                                    {:else}

                                        <span
                                            class="rounded-xl bg-red-500/20 px-3 py-1 text-xs text-red-400"
                                        >
                                            HIGH
                                        </span>

                                    {/if}

                                </td>

                                <!-- ACTION -->

                                <td class="px-5 py-4">

                                    <button
                                        onclick={() =>
                                            goto(
                                                `/app/customers/${customer.id}`
                                            )
                                        }
                                        class="rounded-xl bg-emerald-600 px-4 py-2 text-xs font-semibold text-white hover:bg-emerald-700"
                                    >
                                        Open
                                    </button>

                                </td>

                            </tr>

                        {/each}

                    {/if}

                </tbody>

            </table>

        </div>

    </div>

</div>