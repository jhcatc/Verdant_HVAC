<script lang="ts">

    import { goto } from '$app/navigation';

    /*
    =========================================
    MOCK ENTERPRISE REGISTRY
    =========================================
    */

    type EquipmentRegistryRow = {

        id: string;
        asset_tag: string;
        customer: string;
        facility: string;
        type: string;
        brand: string;
        status: string;
        health_score: number;
        anomaly_risk: 'LOW' | 'MEDIUM' | 'HIGH';
        last_maintenance: string;
    };

    let equipment =
        $state<EquipmentRegistryRow[]>([

            {
                id: '1',
                asset_tag: 'AC-001',
                customer: 'McDonalds',
                facility: 'Bogotá Norte',
                type: 'Mini Split',
                brand: 'Mitsubishi',
                status: 'ACTIVE',
                health_score: 91,
                anomaly_risk: 'LOW',
                last_maintenance: '2026-05-01'
            },

            {
                id: '2',
                asset_tag: 'RTU-014',
                customer: 'Hilton',
                facility: 'Mechanical Room',
                type: 'Rooftop',
                brand: 'Carrier',
                status: 'REPAIR',
                health_score: 58,
                anomaly_risk: 'HIGH',
                last_maintenance: '2026-04-12'
            },

            {
                id: '3',
                asset_tag: 'BLR-003',
                customer: 'Hospital Central',
                facility: 'Boiler Room',
                type: 'Boiler',
                brand: 'Bosch',
                status: 'ACTIVE',
                health_score: 73,
                anomaly_risk: 'MEDIUM',
                last_maintenance: '2026-05-10'
            }
        ]);

    /*
    =========================================
    FILTERS
    =========================================
    */

    let assetSearch = $state('');
    let selectedCustomer = $state('');
    let selectedLocation = $state('');
    let selectedStatus = $state('');
    let selectedType = $state('');

    /*
    =========================================
    AUTOCOMPLETE SOURCES
    =========================================
    */

    const customers = [

        'McDonalds',
        'Hilton',
        'Hospital Central',
        'Starbucks'
    ];

    const locations = [

        'Bogotá Norte',
        'Mechanical Room',
        'Boiler Room',
        'Roof'
    ];

    /*
    =========================================
    FILTERED DATA
    =========================================
    */

    const filteredEquipment = $derived(

        equipment.filter((row) => {

            const assetMatch =
                !assetSearch ||
                row.asset_tag
                    .toLowerCase()
                    .includes(
                        assetSearch.toLowerCase()
                    );

            const customerMatch =
                !selectedCustomer ||
                row.customer === selectedCustomer;

            const locationMatch =
                !selectedLocation ||
                row.facility === selectedLocation;

            const statusMatch =
                !selectedStatus ||
                row.status === selectedStatus;

            const typeMatch =
                !selectedType ||
                row.type === selectedType;

            return (
                assetMatch &&
                customerMatch &&
                locationMatch &&
                statusMatch &&
                typeMatch
            );
        })
    );

    /*
    =========================================
    ACTIONS
    =========================================
    */

    function openEquipment(id: string) {

        goto(
            `/app/infrastructure/equipment/${id}`
        );
    }

    function editEquipment(id: string) {

        goto(
            `/app/infrastructure/equipment/${id}?tab=edit`
        );
    }

    function openMaintenance(id: string) {

        goto(
            `/app/infrastructure/equipment/${id}?tab=maintenance`
        );
    }

    function openQr(id: string) {

        goto(
            `/app/infrastructure/equipment/${id}?tab=qr`
        );
    }

    function healthColor(score: number) {

        if (score >= 80) {
            return 'bg-emerald-500';
        }

        if (score >= 60) {
            return 'bg-yellow-500';
        }

        return 'bg-red-500';
    }

    function anomalyColor(
        risk: string
    ) {

        if (risk === 'LOW') {
            return 'bg-emerald-500/20 text-emerald-400';
        }

        if (risk === 'MEDIUM') {
            return 'bg-yellow-500/20 text-yellow-400';
        }

        return 'bg-red-500/20 text-red-400';
    }

</script>

<div class="p-6 space-y-6">

    <!-- HEADER -->

    <div class="flex items-center justify-between">

        <div>

            <h1
                class="text-3xl font-bold text-white"
            >
                Equipment Registry
            </h1>

            <p
                class="text-sm text-gray-400 mt-1"
            >
                Enterprise HVAC operational
                registry and infrastructure
                asset management.
            </p>

        </div>

        <button
            onclick={() =>
                goto(
                    '/app/infrastructure/equipment/create'
                )}
            class="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-sm"
        >
            Create Equipment
        </button>

    </div>

    <!-- FILTERS -->

    <div
        class="rounded-2xl border border-gray-800 bg-gray-900 p-5"
    >

        <div
            class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-5 gap-4"
        >

            <!-- ASSET SEARCH -->

            <div>

                <label
                    class="block text-xs text-gray-400 mb-2"
                >
                    Asset Search
                </label>

                <input
                    bind:value={assetSearch}
                    placeholder="AC-001"
                    class="w-full px-4 py-2 rounded-xl bg-gray-800 border border-gray-700 text-white"
                />

            </div>

            <!-- CUSTOMER -->

            <div>

                <label
                    class="block text-xs text-gray-400 mb-2"
                >
                    Customer
                </label>

                <input
                    bind:value={selectedCustomer}
                    list="customers"
                    placeholder="Select customer"
                    class="w-full px-4 py-2 rounded-xl bg-gray-800 border border-gray-700 text-white"
                />

                <datalist id="customers">

                    {#each customers as customer}

                        <option value={customer} />

                    {/each}

                </datalist>

            </div>

            <!-- LOCATION -->

            <div>

                <label
                    class="block text-xs text-gray-400 mb-2"
                >
                    Facility
                </label>

                <input
                    bind:value={selectedLocation}
                    list="locations"
                    placeholder="Select facility"
                    class="w-full px-4 py-2 rounded-xl bg-gray-800 border border-gray-700 text-white"
                />

                <datalist id="locations">

                    {#each locations as location}

                        <option value={location} />

                    {/each}

                </datalist>

            </div>

            <!-- STATUS -->

            <div>

                <label
                    class="block text-xs text-gray-400 mb-2"
                >
                    Status
                </label>

                <select
                    bind:value={selectedStatus}
                    class="w-full px-4 py-2 rounded-xl bg-gray-800 border border-gray-700 text-white"
                >

                    <option value="">
                        All
                    </option>

                    <option value="ACTIVE">
                        ACTIVE
                    </option>

                    <option value="REPAIR">
                        REPAIR
                    </option>

                </select>

            </div>

            <!-- TYPE -->

            <div>

                <label
                    class="block text-xs text-gray-400 mb-2"
                >
                    Type
                </label>

                <select
                    bind:value={selectedType}
                    class="w-full px-4 py-2 rounded-xl bg-gray-800 border border-gray-700 text-white"
                >

                    <option value="">
                        All
                    </option>

                    <option value="Mini Split">
                        Mini Split
                    </option>

                    <option value="Rooftop">
                        Rooftop
                    </option>

                    <option value="Boiler">
                        Boiler
                    </option>

                </select>

            </div>

        </div>

    </div>

    <!-- TABLE -->

    <div
        class="rounded-2xl border border-gray-800 bg-gray-900 overflow-hidden"
    >

        <div class="overflow-x-auto">

            <table class="min-w-full">

                <thead
                    class="bg-gray-950 border-b border-gray-800"
                >

                    <tr
                        class="text-left text-xs uppercase tracking-wider text-gray-400"
                    >

                        <th class="px-5 py-4">
                            Asset
                        </th>

                        <th class="px-5 py-4">
                            Customer
                        </th>

                        <th class="px-5 py-4">
                            Facility
                        </th>

                        <th class="px-5 py-4">
                            Type
                        </th>

                        <th class="px-5 py-4">
                            Brand
                        </th>

                        <th class="px-5 py-4">
                            Status
                        </th>

                        <th class="px-5 py-4">
                            Health
                        </th>

                        <th class="px-5 py-4">
                            Anomaly Risk
                        </th>

                        <th class="px-5 py-4">
                            Last Maintenance
                        </th>

                        <th class="px-5 py-4">
                            Actions
                        </th>

                    </tr>

                </thead>

                <tbody>

                    {#each filteredEquipment as row}

                        <tr
                            class="border-t border-gray-800 hover:bg-gray-800/40 transition"
                        >

                            <!-- ASSET -->

                            <td
                                class="px-5 py-4 font-semibold text-emerald-400"
                            >
                                {row.asset_tag}
                            </td>

                            <!-- CUSTOMER -->

                            <td
                                class="px-5 py-4 text-gray-300"
                            >
                                {row.customer}
                            </td>

                            <!-- FACILITY -->

                            <td
                                class="px-5 py-4 text-gray-300"
                            >
                                {row.facility}
                            </td>

                            <!-- TYPE -->

                            <td
                                class="px-5 py-4 text-gray-300"
                            >
                                {row.type}
                            </td>

                            <!-- BRAND -->

                            <td
                                class="px-5 py-4 text-gray-300"
                            >
                                {row.brand}
                            </td>

                            <!-- STATUS -->

                            <td class="px-5 py-4">

                                <span
                                    class="px-2 py-1 rounded-lg text-xs bg-emerald-500/20 text-emerald-400"
                                >
                                    {row.status}
                                </span>

                            </td>

                            <!-- HEALTH -->

                            <td class="px-5 py-4">

                                <div
                                    class="w-28 bg-gray-800 rounded-full h-2"
                                >

                                    <div
                                        class={`h-2 rounded-full ${healthColor(row.health_score)}`}
                                        style={`width:${row.health_score}%`}
                                    />

                                </div>

                                <div
                                    class="text-xs text-gray-400 mt-1"
                                >
                                    {row.health_score}%
                                </div>

                            </td>

                            <!-- ANOMALY -->

                            <td class="px-5 py-4">

                                <span
                                    class={`px-2 py-1 rounded-lg text-xs ${anomalyColor(row.anomaly_risk)}`}
                                >
                                    {row.anomaly_risk}
                                </span>

                            </td>

                            <!-- LAST MAINT -->

                            <td
                                class="px-5 py-4 text-gray-300"
                            >
                                {row.last_maintenance}
                            </td>

                            <!-- ACTIONS -->

                            <td class="px-5 py-4">

                                <div
                                    class="flex items-center gap-2"
                                >

                                    <button
                                        onclick={() =>
                                            openEquipment(
                                                row.id
                                            )}
                                        class="px-3 py-1 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-xs"
                                    >
                                        Open
                                    </button>

                                    <button
                                        onclick={() =>
                                            editEquipment(
                                                row.id
                                            )}
                                        class="px-3 py-1 rounded-lg border border-gray-700 hover:bg-gray-800 text-gray-300 text-xs"
                                    >
                                        Edit
                                    </button>

                                    <button
                                        onclick={() =>
                                            openQr(
                                                row.id
                                            )}
                                        class="px-3 py-1 rounded-lg border border-gray-700 hover:bg-gray-800 text-gray-300 text-xs"
                                    >
                                        QR
                                    </button>

                                    <button
                                        onclick={() =>
                                            openMaintenance(
                                                row.id
                                            )}
                                        class="px-3 py-1 rounded-lg border border-gray-700 hover:bg-gray-800 text-gray-300 text-xs"
                                    >
                                        Maintenance
                                    </button>

                                </div>

                            </td>

                        </tr>

                    {/each}

                </tbody>

            </table>

        </div>

    </div>

</div>