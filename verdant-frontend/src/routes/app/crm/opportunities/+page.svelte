<script lang="ts">
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import DataTable from '$lib/components/data-table/DataTable.svelte';
    import DataTableToolbar from '$lib/components/data-table/DataTableToolbar.svelte';

    import type {
        DataTableColumn,
        DataTableAction
    } from '$lib/types/data-table';

    import {
        getOpportunities,
        updateOpportunityStage
    } from '$lib/api/crm/opportunities';

    import type {
        Opportunity
    } from '$lib/types/crm';

    let opportunities = $state<Opportunity[]>([]);
    let loading = $state(false);
    let error = $state('');
    let search = $state('');

    const filtered = $derived(
        opportunities.filter((o) => {

            const q = search.toLowerCase();

            return (
                o.title?.toLowerCase().includes(q) ||
                o.customer_name?.toLowerCase().includes(q)
            );
        })
    );

    const kpis = $derived({

        total: opportunities.length,

        revenue: opportunities.reduce(
            (sum, o) =>
                sum + Number(o.estimated_value || 0),
            0
        ),

        won: opportunities.filter(
            (o) => o.stage === 'WON'
        ).length,

        weighted: opportunities.reduce(
            (sum, o) =>
                sum +
                (
                    Number(o.estimated_value || 0) *
                    Number(o.probability || 0)
                ) / 100,
            0
        )
    });

    async function reload() {

        loading = true;
        error = '';

        try {

            opportunities =
                await getOpportunities();

        } catch (err) {

            console.error(err);

            error =
                'Failed loading opportunities';

        } finally {

            loading = false;
        }
    }

    const columns:
        DataTableColumn<Opportunity>[] = [

        {
            key: 'title',
            label: 'Opportunity'
        },

        {
            key: 'customer_name',
            label: 'Customer'
        },

        {
            key: 'stage',
            label: 'Stage',

            snippet: (row) => {

                const color =
                    row.stage === 'WON'
                        ? 'bg-emerald-500/20 text-emerald-400'

                    : row.stage === 'LOST'
                        ? 'bg-red-500/20 text-red-400'

                    : row.stage === 'NEGOTIATION'
                        ? 'bg-yellow-500/20 text-yellow-300'

                    : 'bg-cyan-500/20 text-cyan-300';

                return `
                    <span class="
                        px-2
                        py-1
                        rounded-lg
                        text-xs
                        ${color}
                    ">
                        ${row.stage}
                    </span>
                `;
            }
        },

        {
            key: 'probability',
            label: 'Probability',

            render: (row) =>
                `${row.probability || 0}%`
        },

        {
            key: 'estimated_value',
            label: 'Forecast Revenue',

            render: (row) =>
                `$${Number(
                    row.estimated_value || 0
                ).toLocaleString()}`
        },

        {
            key: 'close_date',
            label: 'Close Date',

            render: (row) =>
                row.close_date
                    ? new Date(
                        row.close_date
                    ).toLocaleDateString()
                    : '—'
        }
    ];

    const rowActions:
        DataTableAction<Opportunity>[] = [

        {
            label: 'Open',

            variant: 'success',

            onClick: (row) =>
                goto(
                    `/app/crm/opportunities/${row.id}`
                )
        },

        {
            label: 'Move → PROPOSAL',

            onClick: async (row) => {

                await updateOpportunityStage(
                    row.id,
                    'PROPOSAL'
                );

                await reload();
            }
        },

        {
            label: 'Mark WON',

            variant: 'success',

            onClick: async (row) => {

                await updateOpportunityStage(
                    row.id,
                    'WON'
                );

                await reload();
            }
        }
    ];

    onMount(async () => {

        await reload();
    });
</script>

<div class="p-6 space-y-6">

    <div class="flex items-center justify-between">

        <div>

            <h1 class="text-3xl font-bold text-white">
                Opportunities Pipeline
            </h1>

            <p class="text-sm text-gray-400 mt-2">
                Enterprise HVAC revenue forecasting
                and sales pipeline management.
            </p>

        </div>

        <button
            onclick={() =>
                goto('/app/crm/opportunities/create')
            }
            class="
                px-5
                py-3
                rounded-xl
                bg-emerald-600
                hover:bg-emerald-700
                text-white
            "
        >
            + New Opportunity
        </button>

    </div>

    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">

        <div class="rounded-2xl border border-gray-800 bg-gray-900 p-5">

            <div class="text-sm text-gray-400">
                Open Opportunities
            </div>

            <div class="text-3xl font-bold text-white mt-2">
                {kpis.total}
            </div>

        </div>

        <div class="rounded-2xl border border-gray-800 bg-gray-900 p-5">

            <div class="text-sm text-gray-400">
                Forecast Revenue
            </div>

            <div class="text-3xl font-bold text-emerald-400 mt-2">
                ${kpis.revenue.toLocaleString()}
            </div>

        </div>

        <div class="rounded-2xl border border-gray-800 bg-gray-900 p-5">

            <div class="text-sm text-gray-400">
                Won Opportunities
            </div>

            <div class="text-3xl font-bold text-cyan-400 mt-2">
                {kpis.won}
            </div>

        </div>

        <div class="rounded-2xl border border-gray-800 bg-gray-900 p-5">

            <div class="text-sm text-gray-400">
                Weighted Pipeline
            </div>

            <div class="text-3xl font-bold text-yellow-400 mt-2">
                ${kpis.weighted.toLocaleString()}
            </div>

        </div>

    </div>

    <div class="rounded-2xl border border-gray-800 bg-gray-900 p-5">

        <DataTableToolbar
            title="Sales Pipeline"
            search={search}
            placeholder="Search opportunities..."
            onSearch={(v) => search = v}
        />

        {#if error}

            <div class="p-4 text-red-400">
                {error}
            </div>

        {/if}

        <DataTable
            {columns}
            rows={filtered}
            {loading}
            {rowActions}
            emptyTitle="No opportunities found"
            emptyDescription="
                Create opportunities to start
                the CRM sales pipeline.
            "
        />

    </div>

</div>