<script lang="ts">

    import { goto } from '$app/navigation';

    const customers = [

        {
            id: 1,
            name: 'Northwind Manufacturing',
            sla: 'ACTIVE',
            payment_risk: 'LOW',
            equipment_risk: 'MEDIUM',
            violations: 1,
            open_orders: 6,
            critical_assets: 14,
            score: 'B'
        },

        {
            id: 2,
            name: 'Summit Medical Center',
            sla: 'AT RISK',
            payment_risk: 'HIGH',
            equipment_risk: 'HIGH',
            violations: 5,
            open_orders: 12,
            critical_assets: 31,
            score: 'D'
        },

        {
            id: 3,
            name: 'Evergreen Logistics',
            sla: 'ACTIVE',
            payment_risk: 'LOW',
            equipment_risk: 'LOW',
            violations: 0,
            open_orders: 2,
            critical_assets: 8,
            score: 'A'
        }
    ];

</script>

<div class="p-6 space-y-6">

    <!-- HEADER -->

    <div>

        <h1 class="text-3xl font-bold text-white">
            Customer Risk Profiles
        </h1>

        <p class="text-sm text-gray-400 mt-2">
            SLA violations, operational exposure, equipment criticality and customer risk intelligence.
        </p>

    </div>

    <!-- TABLE -->

    <div class="rounded-2xl border border-gray-800 bg-gray-900 overflow-hidden">

        <div class="overflow-x-auto">

            <table class="min-w-full text-sm">

                <thead class="bg-gray-950">

                    <tr class="text-left text-xs uppercase tracking-wider text-gray-500">

                        <th class="px-5 py-4">
                            Customer
                        </th>

                        <th class="px-5 py-4">
                            SLA
                        </th>

                        <th class="px-5 py-4">
                            Payment Risk
                        </th>

                        <th class="px-5 py-4">
                            Equipment Risk
                        </th>

                        <th class="px-5 py-4">
                            Violations
                        </th>

                        <th class="px-5 py-4">
                            Open Orders
                        </th>

                        <th class="px-5 py-4">
                            Critical Assets
                        </th>

                        <th class="px-5 py-4">
                            Score
                        </th>

                        <th class="px-5 py-4">
                            Actions
                        </th>

                    </tr>

                </thead>

                <tbody>

                    {#each customers as customer}

                        <tr class="border-t border-gray-800 hover:bg-gray-800/40">

                            <td class="px-5 py-4 text-white font-medium">
                                {customer.name}
                            </td>

                            <td class="px-5 py-4">

                                <span class={`px-2 py-1 rounded-lg text-xs ${
                                    customer.sla === 'ACTIVE'
                                        ? 'bg-emerald-500/20 text-emerald-400'
                                        : 'bg-red-500/20 text-red-400'
                                }`}>
                                    {customer.sla}
                                </span>

                            </td>

                            <td class="px-5 py-4 text-gray-300">
                                {customer.payment_risk}
                            </td>

                            <td class="px-5 py-4 text-gray-300">
                                {customer.equipment_risk}
                            </td>

                            <td class="px-5 py-4 text-gray-300">
                                {customer.violations}
                            </td>

                            <td class="px-5 py-4 text-gray-300">
                                {customer.open_orders}
                            </td>

                            <td class="px-5 py-4 text-gray-300">
                                {customer.critical_assets}
                            </td>

                            <td class="px-5 py-4">

                                <span class="font-bold text-yellow-400">
                                    {customer.score}
                                </span>

                            </td>

                            <td class="px-5 py-4">

                                <button
                                    onclick={() => goto(`/app/customers/${customer.id}`)}
                                    class="px-3 py-1 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-xs"
                                >
                                    Open
                                </button>

                            </td>

                        </tr>

                    {/each}

                </tbody>

            </table>

        </div>

    </div>

</div>