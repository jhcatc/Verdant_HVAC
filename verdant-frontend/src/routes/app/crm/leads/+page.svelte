<script lang="ts">

    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import DataTable
        from '$lib/components/data-table/DataTable.svelte';
    import DataTableToolbar
        from '$lib/components/data-table/DataTableToolbar.svelte';
    import {
        getLeads,
        deleteLead,
        getLeadMetrics
    } from '$lib/api/crm/leads';

    import type {
        Lead,
        LeadMetric
    } from '$lib/types/crm';

    let loading = $state(true);
    let error = $state('');
    let search = $state('');
    let leads = $state<Lead[]>([]);
    let summary = $state<LeadMetric[]>([]);
    async function loadPage() {

        loading = true;

        error = '';

        try {

            const [
                leadsResponse,
                metricsResponse
            ] = await Promise.all([

                getLeads({
                    search
                }),

                getLeadMetrics()
            ]);

            leads = Array.isArray(
                leadsResponse
            )
                ? leadsResponse
                : [];

            summary = Array.isArray(
                metricsResponse
            )
                ? metricsResponse
                : [];

        } catch (e: any) {

            console.error(
                'Load leads error:',
                e
            );

            error =
                e?.response?.data?.detail ||
                'Failed loading CRM leads';

        } finally {

            loading = false;
        }
    }

    async function removeLead(
        id: string
    ) {

        const confirmed = confirm(
            'Delete this lead?'
        );

        if (!confirmed) {
            return;
        }

        try {

            await deleteLead(id);

            await loadPage();

        } catch (e: any) {

            console.error(e);

            alert(
                e?.response?.data?.detail ||
                'Failed deleting lead'
            );
        }
    }

    function getStatusClass(
        status: string
    ) {

        switch (status) {

            case 'NEW':

                return `
                    bg-cyan-500/20
                    text-cyan-400
                `;

            case 'QUALIFIED':

                return `
                    bg-emerald-500/20
                    text-emerald-400
                `;

            case 'CONTACTED':

                return `
                    bg-yellow-500/20
                    text-yellow-400
                `;

            case 'PROPOSAL':

                return `
                    bg-purple-500/20
                    text-purple-400
                `;

            case 'NEGOTIATION':

                return `
                    bg-orange-500/20
                    text-orange-400
                `;

            case 'CONVERTED':

                return `
                    bg-emerald-500/20
                    text-emerald-400
                `;

            case 'LOST':

                return `
                    bg-red-500/20
                    text-red-400
                `;

            default:

                return `
                    bg-gray-500/20
                    text-gray-300
                `;
        }
    }

    const columns = [

        {
            key: 'company_name',
            label: 'Company',
            sortable: true,
            snippet: (row: Lead) => `
                <div>
                    <div class="font-medium text-white">
                        ${row.company_name || '—'}
                    </div>

                    <div class="text-xs text-gray-500 mt-1">
                        ${row.status || 'NEW'}
                    </div>
                </div>
            `
        },

        {
            key: 'source',
            label: 'Source',
            render: (row: Lead) =>
                row.source || '—'
        },

        {
            key: 'estimated_value',
            label: 'Estimated Value',
            render: (row: Lead) =>
                `$${Number(
                    row.estimated_value || 0
                ).toLocaleString()}`
        },

        {
            key: 'probability',
            label: 'Probability',
            render: (row: Lead) =>
                `${row.probability || 0}%`
        },

        {
            key: 'status',
            label: 'Status',
            snippet: (row: Lead) => `
                <span
                    class="
                        px-2
                        py-1
                        rounded-lg
                        text-xs
                        ${getStatusClass(row.status)}
                    "
                >
                    ${row.status || 'UNKNOWN'}
                </span>
            `
        },

        {
            key: 'email',
            label: 'Email',
            render: (row: Lead) =>
                row.email || '—'
        }
    ];

    const actions = [

        {
            label: 'Open',
            variant: 'success',
            onClick: (row: Lead) =>
                goto(
                    `/app/crm/leads/${row.id}`
                )
        },

        {
            label: 'Delete',
            variant: 'danger',
            onClick: (row: Lead) =>
                removeLead(
                    String(row.id)
                )
        }
    ];

    onMount(async () => {

        await loadPage();
    });

</script>

<div class="p-6 space-y-6">

    <div
        class="flex items-center justify-between"
    >

        <div>

            <h1
                class="text-3xl font-bold text-white"
            >
                CRM Leads Pipeline
            </h1>

            <p
                class="mt-2 text-sm text-gray-400"
            >
                Enterprise HVAC sales pipeline,
                qualification and opportunity tracking.
            </p>

        </div>

        <button
            onclick={() =>
                goto(
                    '/app/crm/leads/create'
                )
            }
            class="
                px-5
                py-3
                rounded-xl
                bg-emerald-600
                hover:bg-emerald-700
                text-white
                transition
            "
        >
            + Create Lead
        </button>

    </div>

    {#if error}

        <div
            class="
                rounded-2xl
                border
                border-red-500/30
                bg-red-500/10
                p-4
                text-red-400
            "
        >
            {error}
        </div>

    {/if}

    <div
        class="
            grid
            grid-cols-1
            md:grid-cols-2
            xl:grid-cols-4
            gap-4
        "
    >

        {#each summary as item}

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
                        text-sm
                        text-gray-400
                    "
                >
                    {item.title}
                </div>

                <div
                    class={`
                        mt-3
                        text-3xl
                        font-bold
                        ${item.color}
                    `}
                >
                    {item.value}
                </div>

            </div>

        {/each}

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

        <DataTableToolbar
            title="Lead Registry"
            search={search}
            placeholder="
                Search companies,
                sources or emails...
            "
            onSearch={async (
                value: string
            ) => {

                search = value;

                await loadPage();
            }}
        />

        <DataTable
            rows={leads}
            columns={columns}
            loading={loading}
            rowActions={actions}
            emptyTitle="No leads found"
            emptyDescription="
                Create your first HVAC sales
                lead to start the CRM pipeline.
            "
        />

    </div>

</div>