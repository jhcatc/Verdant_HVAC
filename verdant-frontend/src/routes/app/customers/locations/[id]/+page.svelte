<script lang="ts">

    import { goto } from '$app/navigation';

    let { params } = $props();

    const facility = {

        id: params.id,

        name: 'Northwind HQ',

        customer: 'Northwind Manufacturing',

        sla: 'Gold SLA',

        address: '742 Industrial Ave',

        city: 'Chicago',

        refrigerant_compliance: 'EPA COMPLIANT',

        site_risk: 'MEDIUM',

        technician_notes:
            'Roof access requires security authorization.',

        contacts: [
            {
                name: 'Michael Torres',
                phone: '(555) 221-8821'
            }
        ],

        equipment: [

            {
                asset_tag: 'RTU-1001',
                type: 'RTU',
                status: 'ONLINE',
                health: 'GOOD'
            },

            {
                asset_tag: 'CHLR-210',
                type: 'CHILLER',
                status: 'MAINTENANCE',
                health: 'WARNING'
            }
        ],

        work_orders: [

            {
                number: 'WO-4421',
                status: 'OPEN',
                priority: 'HIGH'
            }
        ],

        documents: [

            'Mechanical Drawings.pdf',
            'EPA Compliance Report.pdf'
        ],

        photos: [

            '/verdant.png',
            '/verdant.png'
        ]
    };

</script>

<div class="p-6 space-y-6">

    <!-- HEADER -->

    <div class="rounded-2xl border border-gray-800 bg-gray-900 p-6">

        <div class="flex items-start justify-between">

            <div>

                <h1 class="text-3xl font-bold text-white">
                    {facility.name}
                </h1>

                <div class="mt-2 text-gray-400">
                    {facility.customer}
                </div>

                <div class="mt-4 flex flex-wrap gap-3">

                    <span class="px-3 py-1 rounded-xl text-xs bg-emerald-500/20 text-emerald-400">
                        {facility.sla}
                    </span>

                    <span class="px-3 py-1 rounded-xl text-xs bg-yellow-500/20 text-yellow-400">
                        SITE RISK {facility.site_risk}
                    </span>

                    <span class="px-3 py-1 rounded-xl text-xs bg-blue-500/20 text-blue-400">
                        {facility.refrigerant_compliance}
                    </span>

                </div>

            </div>

            <div class="flex gap-2">

                <button
                    onclick={() => goto('/app/orders/create')}
                    class="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-sm"
                >
                    Create Work Order
                </button>

            </div>

        </div>

    </div>

    <!-- GRID -->

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">

        <!-- EQUIPMENT -->

        <div class="rounded-2xl border border-gray-800 bg-gray-900 overflow-hidden">

            <div class="px-5 py-4 border-b border-gray-800">

                <h2 class="text-lg font-semibold text-white">
                    Equipment Registry
                </h2>

            </div>

            <table class="min-w-full text-sm">

                <thead class="bg-gray-950">

                    <tr class="text-left text-xs uppercase tracking-wider text-gray-500">

                        <th class="px-5 py-3">
                            Asset
                        </th>

                        <th class="px-5 py-3">
                            Type
                        </th>

                        <th class="px-5 py-3">
                            Status
                        </th>

                        <th class="px-5 py-3">
                            Health
                        </th>

                    </tr>

                </thead>

                <tbody>

                    {#each facility.equipment as eq}

                        <tr class="border-t border-gray-800">

                            <td class="px-5 py-3 text-emerald-400">
                                {eq.asset_tag}
                            </td>

                            <td class="px-5 py-3 text-white">
                                {eq.type}
                            </td>

                            <td class="px-5 py-3 text-gray-300">
                                {eq.status}
                            </td>

                            <td class="px-5 py-3 text-gray-300">
                                {eq.health}
                            </td>

                        </tr>

                    {/each}

                </tbody>

            </table>

        </div>

        <!-- WORK ORDERS -->

        <div class="rounded-2xl border border-gray-800 bg-gray-900 overflow-hidden">

            <div class="px-5 py-4 border-b border-gray-800">

                <h2 class="text-lg font-semibold text-white">
                    Active Work Orders
                </h2>

            </div>

            <table class="min-w-full text-sm">

                <thead class="bg-gray-950">

                    <tr class="text-left text-xs uppercase tracking-wider text-gray-500">

                        <th class="px-5 py-3">
                            Order
                        </th>

                        <th class="px-5 py-3">
                            Status
                        </th>

                        <th class="px-5 py-3">
                            Priority
                        </th>

                    </tr>

                </thead>

                <tbody>

                    {#each facility.work_orders as wo}

                        <tr class="border-t border-gray-800">

                            <td class="px-5 py-3 text-white">
                                {wo.number}
                            </td>

                            <td class="px-5 py-3 text-gray-300">
                                {wo.status}
                            </td>

                            <td class="px-5 py-3 text-red-400">
                                {wo.priority}
                            </td>

                        </tr>

                    {/each}

                </tbody>

            </table>

        </div>

    </div>

    <!-- DOCUMENTS -->

    <div class="rounded-2xl border border-gray-800 bg-gray-900 p-6">

        <h2 class="text-xl font-semibold text-white mb-4">
            Documents
        </h2>

        <div class="space-y-3">

            {#each facility.documents as doc}

                <div class="flex items-center justify-between rounded-xl border border-gray-800 bg-gray-950 px-4 py-3">

                    <div class="text-sm text-gray-300">
                        {doc}
                    </div>

                    <button class="text-xs text-emerald-400">
                        Download
                    </button>

                </div>

            {/each}

        </div>

    </div>

    <!-- PHOTOS -->

    <div class="rounded-2xl border border-gray-800 bg-gray-900 p-6">

        <h2 class="text-xl font-semibold text-white mb-4">
            Site Photos
        </h2>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">

            {#each facility.photos as photo}

                <img
                    src={photo}
                    class="rounded-xl border border-gray-800"
                    alt="Facility photo"
                />

            {/each}

        </div>

    </div>

</div>