<script lang="ts">

    import { goto } from '$app/navigation';

    import { onMount } from 'svelte';

    import {
        getRenewals,
        type Renewal
    } from '$lib/api/crm/renewals';

    let renewals = $state<Renewal[]>([]);

    let loading = $state(true);

    let error = $state<string | null>(null);

    const metrics = $derived.by(() => {

        const pipeline =
            renewals.reduce(

                (acc, renewal) =>

                    acc + Number(
                        renewal.total_value || 0
                    ),

                0
            );

        const active =
            renewals.filter(

                (renewal) =>

                    renewal.status === 'ACTIVE'
            ).length;

        const premium =
            renewals.filter(

                (renewal) =>

                    renewal.sla_tier === 'PREMIUM'
            ).length;

        const enterprise =
            renewals.filter(

                (renewal) =>

                    Number(
                        renewal.total_value || 0
                    ) >= 100000
            ).length;

        return {

            pipeline,

            active,

            premium,

            enterprise
        };
    });

    function formatCurrency(
        value: number | null
    ) {

        return Number(
            value || 0
        ).toLocaleString(
            'en-US',
            {
                style: 'currency',
                currency: 'USD',
                maximumFractionDigits: 0
            }
        );
    }

    function formatDate(
        value: string | null
    ) {

        if (!value) {
            return '—';
        }

        return new Date(value)
            .toLocaleDateString();
    }

    async function loadRenewals() {

        loading = true;

        error = null;

        try {

            renewals =
                await getRenewals();

        } catch (e) {

            console.error(e);

            error =
                'Failed loading renewals';

        } finally {

            loading = false;
        }
    }

    onMount(async () => {

        await loadRenewals();
    });

</script>

<div class="p-6 space-y-6">

    <!-- HEADER -->

    <div
        class="flex items-center justify-between"
    >

        <div>

            <h1
                class="text-3xl font-bold text-white"
            >
                Renewals Pipeline
            </h1>

            <p
                class="text-sm text-gray-400 mt-2"
            >
                Contract renewal forecasting,
                SLA retention and enterprise
                HVAC customer lifecycle tracking.
            </p>

        </div>

    </div>

    <!-- KPI GRID -->

    <div
        class="
            grid
            grid-cols-1
            md:grid-cols-2
            xl:grid-cols-4
            gap-4
        "
    >

        <div
            class="
                rounded-2xl
                border
                border-gray-800
                bg-gray-900
                p-5
            "
        >

            <div
                class="
                    text-xs
                    uppercase
                    tracking-wider
                    text-gray-500
                "
            >
                Renewal Pipeline
            </div>

            <div
                class="
                    mt-3
                    text-3xl
                    font-bold
                    text-emerald-400
                "
            >
                {formatCurrency(
                    metrics.pipeline
                )}
            </div>

        </div>

        <div
            class="
                rounded-2xl
                border
                border-gray-800
                bg-gray-900
                p-5
            "
        >

            <div
                class="
                    text-xs
                    uppercase
                    tracking-wider
                    text-gray-500
                "
            >
                Active Renewals
            </div>

            <div
                class="
                    mt-3
                    text-3xl
                    font-bold
                    text-cyan-400
                "
            >
                {metrics.active}
            </div>

        </div>

        <div
            class="
                rounded-2xl
                border
                border-gray-800
                bg-gray-900
                p-5
            "
        >

            <div
                class="
                    text-xs
                    uppercase
                    tracking-wider
                    text-gray-500
                "
            >
                Premium SLA
            </div>

            <div
                class="
                    mt-3
                    text-3xl
                    font-bold
                    text-yellow-400
                "
            >
                {metrics.premium}
            </div>

        </div>

        <div
            class="
                rounded-2xl
                border
                border-gray-800
                bg-gray-900
                p-5
            "
        >

            <div
                class="
                    text-xs
                    uppercase
                    tracking-wider
                    text-gray-500
                "
            >
                Enterprise Contracts
            </div>

            <div
                class="
                    mt-3
                    text-3xl
                    font-bold
                    text-purple-400
                "
            >
                {metrics.enterprise}
            </div>

        </div>

    </div>

    <!-- ERROR -->

    {#if error}

        <div
            class="
                rounded-2xl
                border
                border-red-500/20
                bg-red-500/10
                p-4
                text-red-400
            "
        >
            {error}
        </div>

    {/if}

    <!-- TABLE -->

    <div
        class="
            rounded-2xl
            border
            border-gray-800
            bg-gray-900
            overflow-hidden
        "
    >

        {#if loading}

            <div
                class="
                    p-10
                    text-center
                    text-gray-400
                "
            >
                Loading renewals...
            </div>

        {:else if renewals.length === 0}

            <div
                class="
                    p-10
                    text-center
                    text-gray-500
                "
            >
                No active renewals found.
            </div>

        {:else}

            <div
                class="overflow-x-auto"
            >

                <table
                    class="min-w-full text-sm"
                >

                    <thead
                        class="
                            bg-gray-950
                            text-gray-500
                            uppercase
                            text-xs
                            tracking-wider
                        "
                    >

                        <tr>

                            <th class="px-5 py-4 text-left">
                                Customer
                            </th>

                            <th class="px-5 py-4 text-left">
                                SLA Tier
                            </th>

                            <th class="px-5 py-4 text-left">
                                Renewal Date
                            </th>

                            <th class="px-5 py-4 text-left">
                                Contract Value
                            </th>

                            <th class="px-5 py-4 text-left">
                                Status
                            </th>

                            <th class="px-5 py-4 text-left">
                                Actions
                            </th>

                        </tr>

                    </thead>

                    <tbody>

                        {#each renewals as renewal}

                            <tr
                                class="
                                    border-t
                                    border-gray-800
                                    hover:bg-gray-800/40
                                "
                            >

                                <td
                                    class="
                                        px-5
                                        py-4
                                        text-white
                                        font-medium
                                    "
                                >
                                    {renewal.customer_name}
                                </td>

                                <td
                                    class="
                                        px-5
                                        py-4
                                        text-cyan-400
                                    "
                                >
                                    {renewal.sla_tier || '—'}
                                </td>

                                <td
                                    class="
                                        px-5
                                        py-4
                                        text-gray-300
                                    "
                                >
                                    {formatDate(
                                        renewal.renewal_date
                                    )}
                                </td>

                                <td
                                    class="
                                        px-5
                                        py-4
                                        text-emerald-400
                                        font-semibold
                                    "
                                >
                                    {formatCurrency(
                                        renewal.total_value
                                    )}
                                </td>

                                <td
                                    class="
                                        px-5
                                        py-4
                                    "
                                >

                                    <span
                                        class="
                                            px-2
                                            py-1
                                            rounded-lg
                                            text-xs
                                            bg-emerald-500/20
                                            text-emerald-400
                                        "
                                    >
                                        {renewal.status}
                                    </span>

                                </td>

                                <td
                                    class="
                                        px-5
                                        py-4
                                    "
                                >

                                    <div
                                        class="flex gap-2"
                                    >

                                        <button
                                            onclick={() =>

                                                goto(
                                                    `/app/crm/customers/${renewal.customer_id}`
                                                )
                                            }

                                            class="
                                                px-3
                                                py-1
                                                rounded-lg
                                                bg-gray-800
                                                hover:bg-gray-700
                                                text-white
                                                text-xs
                                            "
                                        >
                                            Customer 360
                                        </button>

                                    </div>

                                </td>

                            </tr>

                        {/each}

                    </tbody>

                </table>

            </div>

        {/if}

    </div>

</div>