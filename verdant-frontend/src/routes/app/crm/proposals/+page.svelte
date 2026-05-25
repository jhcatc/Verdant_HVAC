<script lang="ts">

    import { onMount } from 'svelte';

    import { goto } from '$app/navigation';

    import DataTable
        from '$lib/components/data-table/DataTable.svelte';

    import DataTableToolbar
        from '$lib/components/data-table/DataTableToolbar.svelte';

    import type {
        DataTableColumn,
        DataTableAction
    } from '$lib/types/data-table';

    import type {
        Proposal
    } from '$lib/types/crm';

    import {
        getProposals,
        deleteProposal
    } from '$lib/api/crm/proposals';

    let loading = $state(true);

    let error = $state('');

    let search = $state('');

    let proposals =
        $state<Proposal[]>([]);

    async function loadProposals() {

        loading = true;

        error = '';

        try {

            proposals =
                await getProposals();

        } catch (e) {

            console.error(e);

            error =
                'Failed loading proposals';

        } finally {

            loading = false;
        }
    }

    async function removeProposal(
        id: string
    ) {

        const confirmed = confirm(
            'Delete proposal?'
        );

        if (!confirmed) {
            return;
        }

        try {

            await deleteProposal(id);

            await loadProposals();

        } catch (e) {

            console.error(e);

            alert(
                'Failed deleting proposal'
            );
        }
    }

    const filtered = $derived(

        proposals.filter((proposal) => {

            const q =
                search.toLowerCase();

            return (

                proposal.proposal_number
                    ?.toLowerCase()
                    .includes(q)

                ||

                proposal.title
                    ?.toLowerCase()
                    .includes(q)

                ||

                proposal.status
                    ?.toLowerCase()
                    .includes(q)
            );
        })
    );

    function getStatusClass(
        status: string
    ) {

        switch (status) {

            case 'APPROVED':

                return `
                    bg-emerald-500/20
                    text-emerald-400
                `;

            case 'SENT':

                return `
                    bg-cyan-500/20
                    text-cyan-400
                `;

            case 'REJECTED':

                return `
                    bg-red-500/20
                    text-red-400
                `;

            default:

                return `
                    bg-yellow-500/20
                    text-yellow-400
                `;
        }
    }

    function getSource(
        proposal: Proposal
    ) {

        return proposal.opportunity_id
            ? 'PIPELINE'
            : 'DIRECT';
    }

    const columns:
        DataTableColumn<Proposal>[] = [

        {
            key: 'proposal_number',
            label: 'Proposal #'
        },

        {
            key: 'title',
            label: 'Title'
        },

        {
            key: 'amount',
            label: 'Amount',

            render: (row) =>

                `$${Number(
                    row.amount || 0
                ).toLocaleString()}`
        },

        {
            key: 'source',
            label: 'Source',

            render: (row) =>
                getSource(row)
        },

        {
            key: 'status',
            label: 'Status',

            snippet: (row) => ({

                render: () => `

                    <span
                        class="
                            px-2
                            py-1
                            rounded-lg
                            text-xs
                            ${getStatusClass(row.status)}
                        "
                    >
                        ${row.status}
                    </span>
                `
            })
        },

        {
            key: 'created_at',
            label: 'Created',

            render: (row) =>

                row.created_at

                    ? new Date(
                        row.created_at
                    ).toLocaleDateString()

                    : '—'
        }
    ];

    const actions:
        DataTableAction<Proposal>[] = [

        {
            label: 'Open',

            variant: 'success',

            onClick: (row) =>
                goto(
                    `/app/crm/proposals/${row.id}`
                )
        },

        {
            label: 'Delete',

            variant: 'danger',

            onClick: (row) =>
                removeProposal(row.id)
        }
    ];

    const metrics = $derived({

        total:
            proposals.length,

        revenue:

            proposals.reduce(

                (sum, p) =>

                    sum + Number(
                        p.amount || 0
                    ),

                0
            ),

        pipeline:

            proposals.filter(
                (p) => p.opportunity_id
            ).length,

        direct:

            proposals.filter(
                (p) => !p.opportunity_id
            ).length
    });

    onMount(async () => {

        await loadProposals();
    });

</script>

<div class="p-6 space-y-6">

    <!-- HEADER -->

    <div
        class="flex flex-col gap-5 lg:flex-row lg:items-start lg:justify-between"
    >

        <div>

            <h1
                class="text-3xl font-bold text-white"
            >
                Proposal Management
            </h1>

            <p
                class="text-sm text-gray-400 mt-2 max-w-3xl"
            >
                Unified HVAC proposal workflow supporting
                pipeline-driven opportunities and direct
                recurring customer quotations.
            </p>

        </div>

        <div
            class="flex flex-col sm:flex-row gap-3"
        >

            <button
                onclick={() =>
                    goto('/app/crm/proposals/create?mode=pipeline')
                }
                class="
                    px-5
                    py-3
                    rounded-xl
                    bg-cyan-600
                    hover:bg-cyan-700
                    text-white
                    font-medium
                    transition
                "
            >
                + Proposal From Pipeline
            </button>

            <button
                onclick={() =>
                    goto('/app/crm/proposals/create?mode=direct')
                }
                class="
                    px-5
                    py-3
                    rounded-xl
                    bg-emerald-600
                    hover:bg-emerald-700
                    text-white
                    font-medium
                    transition
                "
            >
                + Direct Customer Proposal
            </button>

        </div>

    </div>

    <!-- METRICS -->

    <div
        class="grid grid-cols-1 md:grid-cols-4 gap-4"
    >

        <div
            class="rounded-2xl border border-gray-800 bg-gray-900 p-5"
        >

            <div class="text-sm text-gray-400">
                Total Proposals
            </div>

            <div
                class="mt-2 text-3xl font-bold text-white"
            >
                {metrics.total}
            </div>

        </div>

        <div
            class="rounded-2xl border border-gray-800 bg-gray-900 p-5"
        >

            <div class="text-sm text-gray-400">
                Revenue Forecast
            </div>

            <div
                class="mt-2 text-3xl font-bold text-emerald-400"
            >
                ${metrics.revenue.toLocaleString()}
            </div>

        </div>

        <div
            class="rounded-2xl border border-gray-800 bg-gray-900 p-5"
        >

            <div class="text-sm text-gray-400">
                Pipeline Proposals
            </div>

            <div
                class="mt-2 text-3xl font-bold text-cyan-400"
            >
                {metrics.pipeline}
            </div>

        </div>

        <div
            class="rounded-2xl border border-gray-800 bg-gray-900 p-5"
        >

            <div class="text-sm text-gray-400">
                Direct Customer
            </div>

            <div
                class="mt-2 text-3xl font-bold text-yellow-400"
            >
                {metrics.direct}
            </div>

        </div>

    </div>

    <!-- TABLE -->

    <div
        class="
            rounded-2xl
            border
            border-gray-800
            bg-gray-900
            p-5
        "
    >

        <DataTableToolbar
            title="Proposal Registry"
            search={search}
            placeholder="Search proposals..."
            onSearch={(v) => search = v}
        />

        {#if error}

            <div
                class="
                    rounded-xl
                    border
                    border-red-500/30
                    bg-red-500/10
                    p-4
                    text-red-400
                    mt-4
                "
            >
                {error}
            </div>

        {/if}

        <DataTable
            columns={columns}
            rows={filtered}
            loading={loading}
            rowActions={actions}
            emptyTitle="No proposals found"
            emptyDescription="
                Create your first proposal.
            "
        />

    </div>

</div>