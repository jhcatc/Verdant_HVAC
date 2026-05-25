<script lang="ts">

    import { onMount } from 'svelte';

    import {
        getCRMIntelligence
    } from '$lib/api/crm/intelligence';

    import type {
        CRMIntelligenceResponse
    } from '$lib/types/crm/intelligence';

    let loading = $state(true);

    let error = $state('');

    let intelligence =
        $state<CRMIntelligenceResponse>({

            open_pipeline_value: 0,

            active_contracts: 0,

            renewals_due: 0,

            avg_win_probability: 0,

            high_risk_opportunities: 0,

            total_customers: 0
        });

    onMount(async () => {

        try {

            loading = true;

            error = '';

            intelligence =
                await getCRMIntelligence();

        } catch (e) {

            console.error(e);

            error =
                'Failed loading CRM intelligence';

        } finally {

            loading = false;
        }
    });

</script>

<div class="p-6 space-y-6">

    <!-- HEADER -->

    <div>

        <h1 class="text-3xl font-bold text-white">
            CRM Intelligence Center
        </h1>

        <p class="text-sm text-gray-400 mt-2">
            Revenue forecasting, pipeline analytics,
            contract exposure and enterprise HVAC
            customer intelligence.
        </p>

    </div>

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
            Loading CRM intelligence...
        </div>

    {:else if error}

        <!-- ERROR -->

        <div
            class="
                rounded-2xl
                border
                border-red-900/50
                bg-red-950/30
                p-10
                text-center
            "
        >

            <div class="text-red-400 text-lg">
                {error}
            </div>

        </div>

    {:else}

        <!-- KPI GRID -->

        <div
            class="
                grid
                grid-cols-1
                md:grid-cols-2
                xl:grid-cols-3
                gap-4
            "
        >

            <!-- OPEN PIPELINE -->

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
                    Open Pipeline
                </div>

                <div
                    class="
                        mt-3
                        text-3xl
                        font-bold
                        text-emerald-400
                    "
                >
                    $
                    {intelligence
                        .open_pipeline_value
                        .toLocaleString()}
                </div>

                <div
                    class="
                        mt-2
                        text-xs
                        text-gray-500
                    "
                >
                    Active opportunity revenue
                    excluding WON/LOST stages.
                </div>

            </div>

            <!-- ACTIVE CONTRACTS -->

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
                    Active Contracts
                </div>

                <div
                    class="
                        mt-3
                        text-3xl
                        font-bold
                        text-cyan-400
                    "
                >
                    {intelligence.active_contracts}
                </div>

                <div
                    class="
                        mt-2
                        text-xs
                        text-gray-500
                    "
                >
                    Contracts currently under
                    active SLA lifecycle.
                </div>

            </div>

            <!-- RENEWALS -->

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
                    Renewals Due
                </div>

                <div
                    class="
                        mt-3
                        text-3xl
                        font-bold
                        text-yellow-400
                    "
                >
                    {intelligence.renewals_due}
                </div>

                <div
                    class="
                        mt-2
                        text-xs
                        text-gray-500
                    "
                >
                    Contracts expiring within
                    the next 90 days.
                </div>

            </div>

            <!-- WIN PROBABILITY -->

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
                    Avg Win Probability
                </div>

                <div
                    class="
                        mt-3
                        text-3xl
                        font-bold
                        text-purple-400
                    "
                >
                    {intelligence.avg_win_probability}%
                </div>

                <div
                    class="
                        mt-2
                        text-xs
                        text-gray-500
                    "
                >
                    Average probability across
                    active opportunities.
                </div>

            </div>

            <!-- HIGH RISK -->

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
                    High Risk Opportunities
                </div>

                <div
                    class="
                        mt-3
                        text-3xl
                        font-bold
                        text-red-400
                    "
                >
                    {intelligence
                        .high_risk_opportunities}
                </div>

                <div
                    class="
                        mt-2
                        text-xs
                        text-gray-500
                    "
                >
                    Opportunities below
                    30% probability.
                </div>

            </div>

            <!-- TOTAL CUSTOMERS -->

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
                    Total Customers
                </div>

                <div
                    class="
                        mt-3
                        text-3xl
                        font-bold
                        text-white
                    "
                >
                    {intelligence.total_customers}
                </div>

                <div
                    class="
                        mt-2
                        text-xs
                        text-gray-500
                    "
                >
                    Customers registered in
                    enterprise CRM.
                </div>

            </div>

        </div>

        <!-- EMPTY STATE -->

        {#if
            intelligence.open_pipeline_value === 0 &&
            intelligence.active_contracts === 0 &&
            intelligence.total_customers === 0
        }

            <div
                class="
                    rounded-2xl
                    border
                    border-gray-800
                    bg-gray-900
                    p-10
                    text-center
                "
            >

                <div
                    class="
                        text-lg
                        text-white
                    "
                >
                    No CRM intelligence data available
                </div>

                <div
                    class="
                        mt-2
                        text-sm
                        text-gray-500
                    "
                >
                    Create customers, opportunities
                    and contracts to populate
                    intelligence metrics.
                </div>

            </div>

        {/if}

    {/if}

</div>