<script lang="ts">

    import { goto } from '$app/navigation';

    type EquipmentModuleCard = {
        title: string;
        description: string;
        icon: string;
        route?: string;
        action?: () => void;
    };

    /*
    =========================================
    TEMP MOCK EQUIPMENT
    ENTERPRISE HVAC READY
    =========================================
    */

    const recentEquipment = [

        {
            id: '550e8400-e29b-41d4-a716-446655440000',
            asset_tag: 'AC-001',
            customer: 'McDonalds',
            location: 'Bogotá Norte',
            type: 'Mini Split',
            brand: 'Mitsubishi',
            status: 'Active'
        },

        {
            id: '550e8400-e29b-41d4-a716-446655440001',
            asset_tag: 'RTU-014',
            customer: 'Hilton',
            location: 'Mechanical Room',
            type: 'Rooftop',
            brand: 'Carrier',
            status: 'Under Repair'
        },

        {
            id: '550e8400-e29b-41d4-a716-446655440002',
            asset_tag: 'BLR-003',
            customer: 'Hospital Central',
            location: 'Boiler Room',
            type: 'Boiler',
            brand: 'Bosch',
            status: 'Active'
        }
    ];

    /*
    =========================================
    MODULES
    =========================================
    */
   
    const modules: EquipmentModuleCard[] = [

        {
            title: 'Enterprise Equipment Registry',
            description:
                'Centralized HVAC equipment operations and lifecycle management.',
            icon: '🏢',
            route:
                '/app/infrastructure/equipment/list'
        },

        {
            title: 'Create Equipment',
            description:
                'Register new HVAC infrastructure assets.',
            icon: '➕',
            route:
                '/app/infrastructure/equipment/create'
        },

        {
            title: 'Maintenance Logs',
            description:
                'Cross-equipment maintenance history and technician operations.',
            icon: '🛠️',
            route:
                '/app/infrastructure/maintenance-logs'
        },

        {
            title: 'Component Registry',
            description:
                'Serialized HVAC component lifecycle and warranty tracking.',
            icon: '⚙️',
            route:
                '/app/infrastructure/components'
        },

        {
            title: 'Anomalies',
            description:
                'Predictive failure detection and infrastructure anomalies.',
            icon: '🚨',
            route:
                '/app/infrastructure/anomalies'
        },

        {
            title: 'QR Registry',
            description:
                'Equipment QR identity and technician scan operations.',
            icon: '🔳',
            route:
                '/app/infrastructure/qr'
        }
    ];

    /*
    =========================================
    HELPERS
    =========================================
    */

    function navigate(route: string) {

        goto(route);
    }

    function openEquipmentDetails(id: string) {

        goto(`/app/infrastructure/equipment/${id}`);
    }

</script>

<div class="p-6 space-y-8">

    <!-- HEADER -->
    <div>

        <h1 class="text-3xl font-bold text-white">
            Equipment Management
        </h1>

        <p class="text-sm text-gray-400 mt-1">
            Centralized HVAC infrastructure module for managing equipment,
            maintenance history, operational readings, asset lifecycle,
            technical documentation and enterprise service operations.
        </p>

    </div>

    <!-- QUICK ACCESS -->
    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">

        {#each modules as module}

            <button
                onclick={() => module.route && navigate(module.route)}
                class="text-left rounded-2xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-5 shadow-sm hover:shadow-lg transition-all hover:scale-[1.01]"
            >

                <div class="flex items-start justify-between">

                    <div class="space-y-2">

                        <div class="text-3xl">
                            {module.icon}
                        </div>

                        <h2 class="text-lg font-semibold text-gray-800 dark:text-white">
                            {module.title}
                        </h2>

                        <p class="text-sm text-gray-500 dark:text-gray-400 leading-relaxed">
                            {module.description}
                        </p>

                    </div>

                </div>

            </button>

        {/each}

    </div>

    <!-- RECENT EQUIPMENT -->
    <div
        class="rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 overflow-hidden"
    >

        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-800">

            <div class="flex items-center justify-between">

                <div>

                    <h2 class="text-xl font-semibold text-gray-800 dark:text-white">
                        Recent Equipment
                    </h2>

                    <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
                        Quick access to HVAC assets and infrastructure records.
                    </p>

                </div>

                <button
                    onclick={() => goto('/app/infrastructure/equipment/create')}
                    class="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-sm"
                >
                    Create Equipment
                </button>

            </div>

        </div>

        <!-- TABLE -->
        <div class="overflow-x-auto">

            <table class="min-w-full">

                <thead class="bg-gray-50 dark:bg-gray-800">

                    <tr class="text-left text-xs uppercase tracking-wider text-gray-500 dark:text-gray-400">

                        <th class="px-6 py-4">
                            Asset Tag
                        </th>

                        <th class="px-6 py-4">
                            Customer
                        </th>

                        <th class="px-6 py-4">
                            Location
                        </th>

                        <th class="px-6 py-4">
                            Type
                        </th>

                        <th class="px-6 py-4">
                            Brand
                        </th>

                        <th class="px-6 py-4">
                            Status
                        </th>

                    </tr>

                </thead>

                <tbody>

                    {#each recentEquipment as item}

                        <tr                            
                            class="border-t border-gray-200 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/60 cursor-pointer transition"
                        >

                            <td class="px-6 py-4 font-medium text-emerald-600 dark:text-emerald-400">
                                {item.asset_tag}
                            </td>

                            <td class="px-6 py-4 text-gray-700 dark:text-gray-300">
                                {item.customer}
                            </td>

                            <td class="px-6 py-4 text-gray-700 dark:text-gray-300">
                                {item.location}
                            </td>

                            <td class="px-6 py-4 text-gray-700 dark:text-gray-300">
                                {item.type}
                            </td>

                            <td class="px-6 py-4 text-gray-700 dark:text-gray-300">
                                {item.brand}
                            </td>

                            <td class="px-6 py-4">

                                <span
                                    class="px-2 py-1 rounded-full text-xs bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300"
                                >
                                    {item.status}
                                </span>

                                <button
                                    onclick={() => openEquipmentDetails(item.id)}
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