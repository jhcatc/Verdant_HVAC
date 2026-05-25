<script lang="ts">

    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { page } from '$app/state';
    import {
        getCustomer360,
        type Customer360Response
    } from '$lib/api/crm/customers';

    const customerName =
        decodeURIComponent(page.params.id);

    let loading = $state(true);
    let data =
        $state<Customer360Response | null>(null);
    let error =
        $state<string | null>(null);

    async function loadCustomer() {

        loading = true;
        error = null;
        try {

            data = await getCustomer360(
                customerName
            );
        } catch (e) {
            console.error(e);
            error =
                'Failed loading customer profile';

        } finally {
            loading = false;
        }
    }

    onMount(async () => {

        await loadCustomer();
    });

</script>

{#if loading}

<div class="p-6 text-gray-400">
    Loading customer profile...
</div>

{:else if !customer}

<div class="p-6 text-red-400">
    Customer not found
</div>

{:else}

<div class="p-6 space-y-6">

    <!-- HEADER -->

    <div
        class="rounded-2xl border border-gray-800 bg-gray-900 p-6"
    >

        <div
            class="flex items-start justify-between"
        >

            <div>

                <h1
                    class="text-3xl font-bold text-white"
                >
                    {data?.customer.name}
                </h1>

                <p
                    class="text-sm text-gray-400 mt-2"
                >
                    Customer 360 HVAC Enterprise Profile
                </p>

            </div>

            <span
                class="px-3 py-2 rounded-xl bg-red-500/20 text-red-400 text-sm"
            >
                ENTERPRISE
            </span>

        </div>

    </div>

    <!-- KPI GRID -->

    <div
        class="grid grid-cols-1 md:grid-cols-4 gap-4"
    >

        <div
            class="rounded-2xl border border-gray-800 bg-gray-900 p-5"
        >

            <div
                class="text-xs uppercase text-gray-500"
            >
                Customer Health
            </div>

            <div
                class="mt-3 text-3xl font-bold text-emerald-400"
            >
                92
            </div>

        </div>

        <div
            class="rounded-2xl border border-gray-800 bg-gray-900 p-5"
        >

            <div
                class="text-xs uppercase text-gray-500"
            >
                Annual Revenue
            </div>

            <div
                class="mt-3 text-3xl font-bold text-cyan-400"
            >
                ${Number(
                    customer.revenue ?? 0
                ).toLocaleString()}
            </div>

        </div>

        <div
            class="rounded-2xl border border-gray-800 bg-gray-900 p-5"
        >

            <div
                class="text-xs uppercase text-gray-500"
            >
                Facilities
            </div>

            <div
                class="mt-3 text-3xl font-bold text-white"
            >
                {data?.facilities.length || 0}
            </div>

        </div>

        <div
            class="rounded-2xl border border-gray-800 bg-gray-900 p-5"
        >

            <div
                class="text-xs uppercase text-gray-500"
            >
                Active Contracts
            </div>

            <div
                class="mt-3 text-3xl font-bold text-orange-400"
            >
                {contracts.length}
            </div>

        </div>

    </div>

    <!-- GRID -->

    <div
        class="grid grid-cols-1 xl:grid-cols-2 gap-6"
    >

        <!-- CONTRACTS -->

        <div
            class="rounded-2xl border border-gray-800 bg-gray-900 p-6"
        >

            <h2
                class="text-lg font-semibold text-white mb-5"
            >
                Contracts & SLA
            </h2>

            <div class="space-y-4">

                {#each contracts as contract}

                    <div
                        class="rounded-xl border border-gray-800 bg-gray-950 p-4"
                    >

                        <div
                            class="flex items-center justify-between"
                        >

                            <div>

                                <div class="text-white">
                                    {contract.customer_name}
                                </div>

                                <div class="text-xs text-gray-500 mt-1">
                                    {contract.sla_tier}
                                </div>

                            </div>

                            <span
                                class="px-2 py-1 rounded-lg bg-cyan-500/20 text-cyan-400 text-xs"
                            >
                                {contract.status}
                            </span>

                        </div>

                    </div>

                {/each}

            </div>

        </div>

        <!-- OPPORTUNITIES -->

        <div
            class="rounded-2xl border border-gray-800 bg-gray-900 p-6"
        >

            <div
                class="flex items-center justify-between mb-6"
            >

                <h2
                    class="text-lg font-semibold text-white"
                >
                    Sales Opportunities
                </h2>

                <button
                    onclick={() =>
                        goto('/app/crm/opportunities')
                    }
                    class="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-sm"
                >
                    Open Pipeline
                </button>

            </div>

            <div class="space-y-4">

                {#each opportunities as opp}

                    <div
                        class="rounded-xl border border-gray-800 bg-gray-950 p-4"
                    >

                        <div
                            class="flex items-center justify-between"
                        >

                            <div>

                                <div class="text-white">
                                    {opp.title}
                                </div>

                                <div class="text-xs text-gray-500 mt-1">
                                    {opp.stage}
                                </div>

                            </div>

                            <div class="text-right">

                                <div class="text-emerald-400 font-semibold">
                                    ${Number(
                                        opp.estimated_value ?? 0
                                    ).toLocaleString()}
                                </div>

                                <div class="text-xs text-cyan-400 mt-1">
                                    {opp.probability}% probability
                                </div>

                            </div>

                        </div>

                    </div>

                {/each}

            </div>

        </div>

        <!-- RENEWALS -->

        <div
            class="rounded-2xl border border-gray-800 bg-gray-900 p-6"
        >

            <h2
                class="text-lg font-semibold text-white mb-6"
            >
                Renewals & Retention
            </h2>

            <div class="space-y-4">

                {#each renewals as renewal}

                    <div
                        class="rounded-xl border border-gray-800 bg-gray-950 p-4"
                    >

                        <div
                            class="flex items-center justify-between"
                        >

                            <div>

                                <div class="text-white">
                                    {renewal.customer_name}
                                </div>

                                <div class="text-xs text-gray-500 mt-1">
                                    Expires {renewal.renewal_date}
                                </div>

                            </div>

                            <span
                                class="px-2 py-1 rounded-lg bg-yellow-500/20 text-yellow-400 text-xs"
                            >
                                {renewal.sla_tier}
                            </span>

                        </div>

                    </div>

                {/each}

            </div>

        </div>

        <!-- FACILITIES -->

        <div
            class="rounded-2xl border border-gray-800 bg-gray-900 p-6"
        >

            <h2
                class="text-lg font-semibold text-white mb-6"
            >
                Facility Intelligence
            </h2>

            <div class="space-y-4">

                {#each facilities as facility}

                    <div
                        class="rounded-xl border border-gray-800 bg-gray-950 p-4"
                    >

                        <div class="text-white">
                            {facility.name}
                        </div>

                    </div>

                {/each}

            </div>

        </div>

    </div>

</div>

{/if}