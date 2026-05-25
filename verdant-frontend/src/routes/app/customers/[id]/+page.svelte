<script lang="ts">

    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import api from '$lib/api/client';
    let { params } = $props();
    let loading =
        $state(true);
    let customer =
        $state(null);
    let locations =
        $state([]);
    let equipment =
        $state([]);
    let orders =
        $state([]);
    async function load() {

        loading = true;

        try {

            const customerRes =
                await api.get(`/customers/${params.id}`);
            customer =
                customerRes.data;
            try {
                const locationsRes =
                    await api.get(
                        `/customer-locations/customer/${params.id}`
                    );
                locations =
                    locationsRes.data || [];
            } catch (e) {
                console.error('locations', e);
                locations = [];
            }
            try {
                const equipmentRes =
                    await api.get(
                        `/customers/${params.id}/equipment`
                    );
                equipment =
                    equipmentRes.data || [];

            } catch (e) {
                equipment = [];
            }
            try {
                const ordersRes =
                    await api.get(
                        `/customers/${params.id}/orders`
                    );
                orders =
                    ordersRes.data || [];
            } catch (e) {
                orders = [];
            }
        } catch (e) {
            console.error(e);
        } finally {
            loading = false;
        }
    }

    onMount(load);

</script>

{#if loading}

    <div class="p-6">

        <div
            class="rounded-2xl border border-gray-800 bg-gray-900 p-8 text-gray-400"
        >
            Loading customer profile...
        </div>

    </div>

{:else if customer}

    <div class="p-6 space-y-6">

        <!-- ===================================================== -->
        <!-- HEADER -->
        <!-- ===================================================== -->

        <div
            class="rounded-2xl border border-gray-800 bg-gray-900 p-6"
        >

            <div class="flex items-start justify-between">

                <div>

                    <h1 class="text-3xl font-bold text-white">
                        {customer.name}
                    </h1>

                    <div class="mt-2 flex flex-wrap gap-3">

                        <span
                            class="px-3 py-1 rounded-xl text-xs bg-emerald-500/20 text-emerald-400"
                        >
                            SLA ACTIVE
                        </span>

                        <span
                            class="px-3 py-1 rounded-xl text-xs bg-yellow-500/20 text-yellow-400"
                        >
                            MEDIUM RISK
                        </span>

                        <span
                            class="px-3 py-1 rounded-xl text-xs bg-blue-500/20 text-blue-400"
                        >
                            ENTERPRISE CUSTOMER
                        </span>

                    </div>

                    <div class="mt-5 grid grid-cols-1 md:grid-cols-4 gap-5">

                        <div>

                            <div class="text-xs text-gray-500 uppercase">
                                Email
                            </div>

                            <div class="text-sm text-white mt-1">
                                {customer.email || '—'}
                            </div>

                        </div>

                        <div>

                            <div class="text-xs text-gray-500 uppercase">
                                Phone
                            </div>

                            <div class="text-sm text-white mt-1">
                                {customer.phone || '—'}
                            </div>

                        </div>

                        <div>

                            <div class="text-xs text-gray-500 uppercase">
                                City
                            </div>

                            <div class="text-sm text-white mt-1">
                                {customer.city || '—'}
                            </div>

                        </div>

                        <div>

                            <div class="text-xs text-gray-500 uppercase">
                                Facilities
                            </div>

                            <div class="text-sm text-white mt-1">
                                {locations.length}
                            </div>

                        </div>

                    </div>

                </div>

                <div class="flex flex-wrap gap-2">

                    <button
                        onclick={() =>
                            goto(
                                `/app/customers/locations/create?customer=${customer.id}`
                            )
                        }
                        class="px-4 py-2 rounded-xl bg-gray-800 hover:bg-gray-700 text-white text-sm"
                    >
                        Add Facility
                    </button>

                    <button
                        onclick={() =>
                            goto(
                                `/app/infrastructure/equipment/create?customer=${customer.id}`
                            )
                        }
                        class="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-sm"
                    >
                        Add Equipment
                    </button>

                    <button
                        onclick={() =>
                            goto(
                                `/app/orders/new?customer=${customer.id}`
                            )
                        }
                        class="px-4 py-2 rounded-xl bg-yellow-600 hover:bg-yellow-700 text-white text-sm"
                    >
                        Create Service Order
                    </button>

                    <button
                        class="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-sm"
                    >
                        Edit Customer
                    </button>

                </div>

            </div>

        </div>

        <!-- ===================================================== -->
        <!-- METRICS -->
        <!-- ===================================================== -->

        <div class="grid grid-cols-1 md:grid-cols-4 gap-5">

            <div class="rounded-2xl border border-gray-800 bg-gray-900 p-5">

                <div class="text-xs text-gray-500 uppercase">
                    Equipment
                </div>

                <div class="mt-3 text-3xl font-bold text-white">
                    {equipment.length}
                </div>

            </div>

            <div class="rounded-2xl border border-gray-800 bg-gray-900 p-5">

                <div class="text-xs text-gray-500 uppercase">
                    Open Orders
                </div>

                <div class="mt-3 text-3xl font-bold text-white">
                    {orders.length}
                </div>

            </div>

            <div class="rounded-2xl border border-gray-800 bg-gray-900 p-5">

                <div class="text-xs text-gray-500 uppercase">
                    SLA Compliance
                </div>

                <div class="mt-3 text-3xl font-bold text-emerald-400">
                    98%
                </div>

            </div>

            <div class="rounded-2xl border border-gray-800 bg-gray-900 p-5">

                <div class="text-xs text-gray-500 uppercase">
                    Risk Score
                </div>

                <div class="mt-3 text-3xl font-bold text-yellow-400">
                    B
                </div>

            </div>

        </div>

        <!-- ===================================================== -->
        <!-- FACILITIES -->
        <!-- ===================================================== -->

        <div
            class="rounded-2xl border border-gray-800 bg-gray-900 overflow-hidden"
        >

            <div class="px-6 py-4 border-b border-gray-800">

                <div class="flex items-center justify-between">

                    <div>

                        <h2 class="text-xl font-semibold text-white">
                            Facilities
                        </h2>

                        <p class="text-sm text-gray-400 mt-1">
                            Customer operational locations and service facilities.
                        </p>

                    </div>

                </div>

            </div>

            <div class="overflow-x-auto">

                <table class="min-w-full text-sm">

                    <thead class="bg-gray-950">

                        <tr class="text-left text-xs uppercase tracking-wider text-gray-500">

                            <th class="px-5 py-4">
                                Facility
                            </th>

                            <th class="px-5 py-4">
                                Address
                            </th>

                            <th class="px-5 py-4">
                                City
                            </th>

                            <th class="px-5 py-4">
                                Contact
                            </th>

                            <th class="px-5 py-4">
                                Actions
                            </th>

                        </tr>

                    </thead>

                    <tbody>

                        {#if locations.length === 0}

                            <tr>

                                <td
                                    colspan="5"
                                    class="px-5 py-10 text-center text-gray-500"
                                >
                                    No facilities found.
                                </td>

                            </tr>

                        {:else}

                            {#each locations as location}

                                <tr
                                    class="border-t border-gray-800"
                                >

                                    <td class="px-5 py-4 text-white">
                                        {location.name}
                                    </td>

                                    <td class="px-5 py-4 text-gray-300">
                                        {location.address || '—'}
                                    </td>

                                    <td class="px-5 py-4 text-gray-300">
                                        {location.city || '—'}
                                    </td>

                                    <td class="px-5 py-4 text-gray-300">
                                        {location.contact_name || '—'}
                                    </td>

                                    <td class="px-5 py-4">

                                        <button
                                            onclick={() =>
                                                goto(
                                                    `/app/customers/locations/${location.id}`
                                                )
                                            }
                                            class="px-3 py-1 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-xs"
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

        <!-- ===================================================== -->
        <!-- EQUIPMENT -->
        <!-- ===================================================== -->

        <div
            class="rounded-2xl border border-gray-800 bg-gray-900 overflow-hidden"
        >

            <div class="px-6 py-4 border-b border-gray-800">

                <h2 class="text-xl font-semibold text-white">
                    Equipment Overview
                </h2>

            </div>

            <div class="overflow-x-auto">

                <table class="min-w-full text-sm">

                    <thead class="bg-gray-950">

                        <tr class="text-left text-xs uppercase tracking-wider text-gray-500">

                            <th class="px-5 py-4">
                                Asset Tag
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
                                Actions
                            </th>

                        </tr>

                    </thead>

                    <tbody>

                        {#if equipment.length === 0}

                            <tr>

                                <td
                                    colspan=""
                                    class="px-5 py-10 text-center text-gray-500"
                                >
                                    No equipment found.
                                </td>

                            </tr>

                        {:else}

                            {#each equipment as eq}

                                <tr class="border-t border-gray-800">

                                    <td class="px-5 py-4 text-emerald-400">
                                        {eq.asset_tag}
                                    </td>

                                    <td class="px-5 py-4 text-white">
                                        {eq.type}
                                    </td>

                                    <td class="px-5 py-4 text-gray-300">
                                        {eq.brand}
                                    </td>

                                    <td class="px-5 py-4 text-gray-300">
                                        {eq.status}
                                    </td>

                                    <td class="px-5 py-4">

                                        <div class="flex gap-2">

                                            <button
                                                onclick={() =>
                                                    goto(
                                                        `/app/infrastructure/equipment/${eq.id}`
                                                    )
                                                }
                                                class="px-3 py-1 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-xs"
                                            >
                                                Open
                                            </button>

                                            <button
                                                onclick={() =>
                                                    goto(
                                                        `/app/infrastructure/maintenance-logs?equipment=${eq.id}`
                                                    )
                                                }
                                                class="px-3 py-1 rounded-lg bg-gray-700 hover:bg-gray-600 text-white text-xs"
                                            >
                                                Maintenance
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

{/if}