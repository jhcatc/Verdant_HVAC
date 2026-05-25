<script lang="ts">

    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';

    import {
        getDashboard
    } from '$lib/api/crm/dashboard';

    type DashboardMetric = {
        title: string;
        value: number;
        color: string;
        description: string;
    };

    type DashboardOpportunity = {
        customer_name: string;
        opportunity_title: string;
        estimated_value: number;
        stage: string;
        probability: number;
    };

    type DashboardRenewal = {
        contract_id: string;
        customer_name: string;
        renewal_date: string | null;
        sla_tier: string | null;
        total_value: number;
        status: string;
    };

    type FieldKpis = {
        proposal_win_rate: number;
        average_contract_value: number;
        retention_score: number;
    };

    let loading = $state(true);

    let error = $state('');

    let metrics =
        $state<DashboardMetric[]>([]);

    let opportunities =
        $state<DashboardOpportunity[]>([]);

    let renewals =
        $state<DashboardRenewal[]>([]);

    let fieldKpis =
        $state<FieldKpis>({
            proposal_win_rate: 0,
            average_contract_value: 0,
            retention_score: 0
        });

    async function loadDashboard() {

        loading = true;

        error = '';

        try {

            const data =
                await getDashboard();

            metrics =
                data.metrics || [];

            opportunities =
                data.opportunities || [];

            renewals =
                data.renewals || [];

            fieldKpis = {

                proposal_win_rate:
                    Number(
                        data.field_kpis?.proposal_win_rate || 0
                    ),

                average_contract_value:
                    Number(
                        data.field_kpis?.average_contract_value || 0
                    ),

                retention_score:
                    Number(
                        data.field_kpis?.retention_score || 0
                    )
            };

        } catch (e) {

            console.error(
                'Dashboard load failed',
                e
            );

            error =
                'Failed loading CRM dashboard';

        } finally {

            loading = false;
        }
    }

    onMount(async () => {

        await loadDashboard();
    });

</script>

<div class="p-6 space-y-6">

    <!-- HEADER -->

    <div class="flex items-center justify-between">

        <div>

            <h1 class="text-3xl font-bold text-white">
                HVAC CRM Command Center
            </h1>

            <p class="mt-2 text-sm text-gray-400">
                Revenue forecasting,
                renewals,
                SLA exposure
                and HVAC pipeline intelligence.
            </p>

        </div>

        <div class="flex gap-3">
            <!--
            <button
                onclick={() => goto('/app/crm/leads')}
                class="
                    px-4
                    py-2
                    rounded-xl
                    bg-gray-800
                    hover:bg-gray-700
                    text-white
                "
            >
                Leads
            </button>

            <button
                onclick={() => goto('/app/crm/leads/create')}
                class="
                    px-4
                    py-2
                    rounded-xl
                    bg-emerald-600
                    hover:bg-emerald-700
                    text-white
                "
            >
                Create Lead
            </button>
            -->
        </div>

    </div>

    <!-- ERROR -->

    {#if error}

        <div
            class="
                rounded-2xl
                border
                border-red-900
                bg-red-950/40
                p-5
                text-red-400
            "
        >
            {error}
        </div>

    {/if}

    <!-- LOADING -->

    {#if loading}

        <div
            class="
                rounded-2xl
                border
                border-gray-800
                bg-gray-900
                p-10
                text-center
                text-gray-400
            "
        >
            Loading CRM dashboard...
        </div>

    {:else}

        <!-- METRICS -->

        <div
            class="
                grid
                grid-cols-1
                md:grid-cols-2
                xl:grid-cols-4
                gap-4
            "
        >

            {#each metrics as metric (metric.title)}

                <div
                    class="
                        rounded-2xl
                        border
                        border-gray-800
                        bg-gray-900
                        p-5
                    "
                >

                    <div class="text-sm text-gray-400">
                        {metric.title}
                    </div>

                    <div
                        class={`
                            mt-3
                            text-3xl
                            font-bold
                            ${metric.color}
                        `}
                    >

                        {#if metric.title === 'Open Pipeline'}

                            ${Number(
                                metric.value || 0
                            ).toLocaleString()}

                        {:else if metric.title === 'Conversion Rate'}

                            {metric.value}%

                        {:else}

                            {metric.value}

                        {/if}

                    </div>

                    <div class="mt-2 text-xs text-gray-500">
                        {metric.description}
                    </div>

                </div>

            {/each}

        </div>

        <!-- MAIN GRID -->

        <div
            class="
                grid
                grid-cols-1
                xl:grid-cols-3
                gap-6
            "
        >

            <!-- PIPELINE -->

            <div
                class="
                    xl:col-span-2
                    rounded-2xl
                    border
                    border-gray-800
                    bg-gray-900
                    overflow-hidden
                "
            >

                <div
                    class="
                        px-5
                        py-4
                        border-b
                        border-gray-800
                    "
                >

                    <h2
                        class="
                            text-lg
                            font-semibold
                            text-white
                        "
                    >
                        Revenue Pipeline
                    </h2>

                </div>

                <div class="overflow-x-auto">

                    <table class="min-w-full text-sm">

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
                                    Opportunity
                                </th>

                                <th class="px-5 py-4 text-left">
                                    Value
                                </th>

                                <th class="px-5 py-4 text-left">
                                    Stage
                                </th>

                                <th class="px-5 py-4 text-left">
                                    Probability
                                </th>

                            </tr>

                        </thead>

                        <tbody>

                            {#if opportunities.length === 0}

                                <tr>

                                    <td
                                        colspan="5"
                                        class="
                                            px-5
                                            py-10
                                            text-center
                                            text-gray-500
                                        "
                                    >
                                        No opportunities found
                                    </td>

                                </tr>

                            {:else}

                                {#each opportunities as row}

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
                                            "
                                        >
                                            {row.customer_name}
                                        </td>

                                        <td
                                            class="
                                                px-5
                                                py-4
                                                text-gray-300
                                            "
                                        >
                                            {row.opportunity_title}
                                        </td>

                                        <td
                                            class="
                                                px-5
                                                py-4
                                                text-emerald-400
                                                font-medium
                                            "
                                        >
                                            ${Number(
                                                row.estimated_value || 0
                                            ).toLocaleString()}
                                        </td>

                                        <td
                                            class="
                                                px-5
                                                py-4
                                                text-cyan-400
                                            "
                                        >
                                            {row.stage}
                                        </td>

                                        <td
                                            class="
                                                px-5
                                                py-4
                                                text-yellow-400
                                            "
                                        >
                                            {row.probability}%
                                        </td>

                                    </tr>

                                {/each}

                            {/if}

                        </tbody>

                    </table>

                </div>

            </div>

            <!-- SIDEBAR -->

            <div
                class="
                    rounded-2xl
                    border
                    border-gray-800
                    bg-gray-900
                    p-5
                    space-y-5
                "
            >

                <!-- RENEWALS -->

                <div>

                    <div
                        class="
                            text-xs
                            uppercase
                            tracking-widest
                            text-gray-500
                        "
                    >
                        SLA Renewals
                    </div>

                    <div class="mt-3 space-y-3">

                        {#if renewals.length === 0}

                            <div class="text-sm text-gray-500">
                                No renewals pending
                            </div>

                        {:else}

                            {#each renewals as renewal}

                                <div
                                    class="
                                        rounded-xl
                                        bg-gray-950
                                        p-4
                                        border
                                        border-gray-800
                                    "
                                >

                                    <div class="text-sm text-white">
                                        {renewal.customer_name}
                                    </div>

                                    <div
                                        class="
                                            text-xs
                                            text-gray-500
                                            mt-1
                                        "
                                    >
                                        SLA:
                                        {renewal.sla_tier || 'STANDARD'}
                                    </div>

                                    <div
                                        class="
                                            text-xs
                                            text-gray-500
                                            mt-1
                                        "
                                    >
                                        Renewal:
                                        {renewal.renewal_date || 'N/A'}
                                    </div>

                                </div>

                            {/each}

                        {/if}

                    </div>

                </div>

                <!-- KPI -->

                <div>

                    <div
                        class="
                            text-xs
                            uppercase
                            tracking-widest
                            text-gray-500
                        "
                    >
                        Field Sales KPI
                    </div>

                    <div class="mt-4 space-y-4">

                        <div class="flex justify-between text-sm">

                            <span class="text-gray-400">
                                Proposal Win Rate
                            </span>

                            <span class="text-emerald-400">
                                {fieldKpis.proposal_win_rate}%
                            </span>

                        </div>

                        <div class="flex justify-between text-sm">

                            <span class="text-gray-400">
                                Average Contract Value
                            </span>

                            <span class="text-cyan-400">

                                ${Number(
                                    fieldKpis.average_contract_value
                                ).toLocaleString()}

                            </span>

                        </div>

                        <div class="flex justify-between text-sm">

                            <span class="text-gray-400">
                                Retention Score
                            </span>

                            <span class="text-yellow-400">
                                {fieldKpis.retention_score}%
                            </span>

                        </div>

                    </div>

                </div>

            </div>

        </div>

    {/if}

</div>