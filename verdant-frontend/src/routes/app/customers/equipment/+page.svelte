<script lang="ts">

    import { goto } from '$app/navigation';

    let search = $state('');

    let manufacturerFilter = $state('ALL');
    let slaFilter = $state('ALL');
    let riskFilter = $state('ALL');

    const equipment = [

        {
            id: 1,
            asset_tag: 'RTU-1001',
            customer: 'Northwind Manufacturing',
            facility: 'Chicago HQ',
            type: 'RTU',
            manufacturer: 'Trane',
            refrigerant: 'R410A',
            sla_exposure: 'HIGH',
            lifecycle_risk: 'MEDIUM',
            anomaly_score: 82,
            failures: 4,
            cluster: 'Midwest RTU Cluster',
            status: 'ONLINE',
            age: 11,
            pm_compliance: 91
        },

        {
            id: 2,
            asset_tag: 'CHLR-210',
            customer: 'Summit Medical',
            facility: 'Tower B',
            type: 'Chiller',
            manufacturer: 'Carrier',
            refrigerant: 'R134A',
            sla_exposure: 'CRITICAL',
            lifecycle_risk: 'HIGH',
            anomaly_score: 94,
            failures: 9,
            cluster: 'Critical Cooling Cluster',
            status: 'WARNING',
            age: 18,
            pm_compliance: 72
        },

        {
            id: 3,
            asset_tag: 'AHU-778',
            customer: 'Evergreen Logistics',
            facility: 'Distribution Hub',
            type: 'AHU',
            manufacturer: 'Daikin',
            refrigerant: 'R32',
            sla_exposure: 'LOW',
            lifecycle_risk: 'LOW',
            anomaly_score: 21,
            failures: 1,
            cluster: 'Warehouse AHU Group',
            status: 'ONLINE',
            age: 4,
            pm_compliance: 99
        },

        {
            id: 4,
            asset_tag: 'VRF-440',
            customer: 'Apex Commercial',
            facility: 'Miami Offices',
            type: 'VRF',
            manufacturer: 'Mitsubishi',
            refrigerant: 'R32',
            sla_exposure: 'HIGH',
            lifecycle_risk: 'HIGH',
            anomaly_score: 87,
            failures: 5,
            cluster: 'South VRF Cluster',
            status: 'WARNING',
            age: 14,
            pm_compliance: 83
        }
    ];

    let filtered = $derived(

        equipment.filter((eq) => {

            const q =
                search.toLowerCase();

            const matchesSearch =

                eq.asset_tag.toLowerCase().includes(q) ||

                eq.customer.toLowerCase().includes(q) ||

                eq.facility.toLowerCase().includes(q) ||

                eq.manufacturer.toLowerCase().includes(q);

            const matchesManufacturer =
                manufacturerFilter === 'ALL'
                    ? true
                    : eq.manufacturer === manufacturerFilter;

            const matchesSla =
                slaFilter === 'ALL'
                    ? true
                    : eq.sla_exposure === slaFilter;

            const matchesRisk =
                riskFilter === 'ALL'
                    ? true
                    : eq.lifecycle_risk === riskFilter;

            return (

                matchesSearch &&
                matchesManufacturer &&
                matchesSla &&
                matchesRisk
            );
        })
    );

    const totalAssets =
        equipment.length;

    const criticalAssets =
        equipment.filter(
            (e) => e.sla_exposure === 'CRITICAL'
        ).length;

    const highRisk =
        equipment.filter(
            (e) => e.lifecycle_risk === 'HIGH'
        ).length;

    const avgAnomaly =
        Math.round(
            equipment.reduce(
                (acc, e) => acc + e.anomaly_score,
                0
            ) / equipment.length
        );

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
                    class="text-xs uppercase tracking-[0.3em] text-cyan-400"
                >
                    <!--Customer Infrastructure Intelligence-->
                </div>

                <h1
                    class="mt-3 text-4xl font-black text-white"
                >
                    Customer Equipment Intelligence
                </h1>

                <p
                    class="mt-3 max-w-4xl text-sm text-gray-400"
                >
                    Cross-customer HVAC infrastructure analytics including SLA exposure,
                    anomaly propagation, lifecycle risk, refrigerant compliance,
                    operational clustering and manufacturer failure intelligence.
                </p>

            </div>

        </div>

    </div>

    <!-- ===================================================== -->
    <!-- METRICS -->
    <!-- ===================================================== -->

    <div class="grid grid-cols-1 md:grid-cols-4 gap-5">

        <div
            class="rounded-2xl border border-gray-800 bg-gray-900 p-5"
        >

            <div class="text-xs uppercase text-gray-500">
                Total Assets
            </div>

            <div class="mt-3 text-4xl font-black text-white">
                {totalAssets}
            </div>

        </div>

        <div
            class="rounded-2xl border border-red-900 bg-red-500/10 p-5"
        >

            <div class="text-xs uppercase text-red-300">
                Critical SLA Exposure
            </div>

            <div class="mt-3 text-4xl font-black text-white">
                {criticalAssets}
            </div>

        </div>

        <div
            class="rounded-2xl border border-yellow-900 bg-yellow-500/10 p-5"
        >

            <div class="text-xs uppercase text-yellow-300">
                High Lifecycle Risk
            </div>

            <div class="mt-3 text-4xl font-black text-white">
                {highRisk}
            </div>

        </div>

        <div
            class="rounded-2xl border border-orange-900 bg-orange-500/10 p-5"
        >

            <div class="text-xs uppercase text-orange-300">
                Avg Anomaly Score
            </div>

            <div class="mt-3 text-4xl font-black text-white">
                {avgAnomaly}
            </div>

        </div>

    </div>

    <!-- ===================================================== -->
    <!-- FILTER BAR -->
    <!-- ===================================================== -->

    <div
        class="rounded-3xl border border-gray-800 bg-gray-900 p-5"
    >

        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">

            <input
                bind:value={search}
                placeholder="Search asset, customer, facility..."
                class="bg-gray-950 border border-gray-700 rounded-2xl px-4 py-3 text-sm text-white"
            />

            <select
                bind:value={manufacturerFilter}
                class="bg-gray-950 border border-gray-700 rounded-2xl px-4 py-3 text-sm text-white"
            >

                <option value="ALL">
                    All Manufacturers
                </option>

                <option value="Trane">
                    Trane
                </option>

                <option value="Carrier">
                    Carrier
                </option>

                <option value="Daikin">
                    Daikin
                </option>

                <option value="Mitsubishi">
                    Mitsubishi
                </option>

            </select>

            <select
                bind:value={slaFilter}
                class="bg-gray-950 border border-gray-700 rounded-2xl px-4 py-3 text-sm text-white"
            >

                <option value="ALL">
                    All SLA Exposure
                </option>

                <option value="LOW">
                    LOW
                </option>

                <option value="HIGH">
                    HIGH
                </option>

                <option value="CRITICAL">
                    CRITICAL
                </option>

            </select>

            <select
                bind:value={riskFilter}
                class="bg-gray-950 border border-gray-700 rounded-2xl px-4 py-3 text-sm text-white"
            >

                <option value="ALL">
                    All Lifecycle Risk
                </option>

                <option value="LOW">
                    LOW
                </option>

                <option value="MEDIUM">
                    MEDIUM
                </option>

                <option value="HIGH">
                    HIGH
                </option>

            </select>

        </div>

    </div>

    <!-- ===================================================== -->
    <!-- TABLE -->
    <!-- ===================================================== -->

    <div
        class="rounded-3xl border border-gray-800 bg-gray-900 overflow-hidden"
    >

        <div
            class="px-6 py-5 border-b border-gray-800"
        >

            <h2 class="text-xl font-bold text-white">
                Infrastructure Exposure Registry
            </h2>

            <p class="mt-1 text-sm text-gray-400">
                HVAC operational infrastructure across all enterprise customers.
            </p>

        </div>

        <div class="overflow-x-auto">

            <table class="min-w-full text-sm">

                <thead class="bg-black/40">

                    <tr
                        class="text-left text-xs uppercase tracking-wider text-gray-500"
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
                            Manufacturer
                        </th>

                        <th class="px-5 py-4">
                            Refrigerant
                        </th>

                        <th class="px-5 py-4">
                            Age
                        </th>

                        <th class="px-5 py-4">
                            PM
                        </th>

                        <th class="px-5 py-4">
                            SLA
                        </th>

                        <th class="px-5 py-4">
                            Risk
                        </th>

                        <th class="px-5 py-4">
                            Anomaly
                        </th>

                        <th class="px-5 py-4">
                            Cluster
                        </th>

                        <th class="px-5 py-4">
                        </th>

                    </tr>

                </thead>

                <tbody>

                    {#if filtered.length === 0}

                        <tr>

                            <td
                                colspan="12"
                                class="px-5 py-10 text-center text-gray-500"
                            >
                                No equipment found.
                            </td>

                        </tr>

                    {:else}

                        {#each filtered as eq}

                            <tr
                                class="border-t border-gray-800 hover:bg-gray-800/40 transition"
                            >

                                <td class="px-5 py-4">

                                    <div
                                        class="font-semibold text-emerald-400"
                                    >
                                        {eq.asset_tag}
                                    </div>

                                    <div
                                        class="mt-1 text-xs text-gray-500"
                                    >
                                        {eq.type}
                                    </div>

                                </td>

                                <td class="px-5 py-4 text-white">
                                    {eq.customer}
                                </td>

                                <td class="px-5 py-4 text-gray-300">
                                    {eq.facility}
                                </td>

                                <td class="px-5 py-4 text-gray-300">
                                    {eq.manufacturer}
                                </td>

                                <td class="px-5 py-4 text-cyan-400">
                                    {eq.refrigerant}
                                </td>

                                <td class="px-5 py-4 text-gray-300">
                                    {eq.age} yrs
                                </td>

                                <td class="px-5 py-4 text-gray-300">
                                    {eq.pm_compliance}%
                                </td>

                                <td class="px-5 py-4">

                                    <span class={`px-3 py-1 rounded-xl text-xs ${
                                        eq.sla_exposure === 'CRITICAL'
                                            ? 'bg-red-500/20 text-red-400'
                                            : eq.sla_exposure === 'HIGH'
                                                ? 'bg-yellow-500/20 text-yellow-400'
                                                : 'bg-emerald-500/20 text-emerald-400'
                                    }`}>
                                        {eq.sla_exposure}
                                    </span>

                                </td>

                                <td class="px-5 py-4">

                                    <span class={`px-3 py-1 rounded-xl text-xs ${
                                        eq.lifecycle_risk === 'HIGH'
                                            ? 'bg-red-500/20 text-red-400'
                                            : eq.lifecycle_risk === 'MEDIUM'
                                                ? 'bg-yellow-500/20 text-yellow-400'
                                                : 'bg-emerald-500/20 text-emerald-400'
                                    }`}>
                                        {eq.lifecycle_risk}
                                    </span>

                                </td>

                                <td class="px-5 py-4">

                                    <div class="text-orange-400 font-bold">
                                        {eq.anomaly_score}
                                    </div>

                                </td>

                                <td class="px-5 py-4 text-gray-300">
                                    {eq.cluster}
                                </td>

                                <td class="px-5 py-4">

                                    <div class="flex gap-2">

                                        <button
                                            onclick={() =>
                                                goto(
                                                    `/app/infrastructure/equipment/${eq.id}`
                                                )
                                            }
                                            class="px-3 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs"
                                        >
                                            Open
                                        </button>

                                        <button
                                            class="px-3 py-2 rounded-xl bg-gray-800 hover:bg-gray-700 text-white text-xs"
                                        >
                                            Analytics
                                        </button>

                                    </div>

                                </td>

                            </tr>

                        {/each}

                    {/if}

                </tbody>

            </table>

        </div>

    </div>

</div>