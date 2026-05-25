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

    import {
        getContracts
    } from '$lib/api/crm/contracts';

    import type {
        Contract
    } from '$lib/types/crm/contracts';

    let contracts = $state<Contract[]>([]);

    let loading = $state(true);

    let error = $state('');

    let search = $state('');

    async function loadContracts() {

        loading = true;

        error = '';

        try {

            contracts = await getContracts();

        } catch (err) {

            console.error(err);

            error = 'Failed loading contracts';

        } finally {

            loading = false;
        }
    }

    onMount(async () => {

        await loadContracts();
    });

    const filtered = $derived(

        contracts.filter((contract) => {

            const q =
                search.toLowerCase();

            return (

                (contract.customer_name || '')
                    .toLowerCase()
                    .includes(q)

                ||

                (contract.status || '')
                    .toLowerCase()
                    .includes(q)

                ||

                (contract.sla_tier || '')
                    .toLowerCase()
                    .includes(q)
            );
        })
    );

    const kpis = $derived({

        active:

            contracts.filter(
                c => c.status === 'ACTIVE'
            ).length,

        revenue:

            contracts.reduce(

                (sum, c) =>
                    sum + Number(c.total_value || 0),

                0
            ),

        renewals:

            contracts.filter(
                c => !!c.renewal_date
            ).length,

        critical:

            contracts.filter(
                c => c.sla_tier === 'CRITICAL'
            ).length
    });

    function getSlaClass(
        tier: string
    ) {

        switch (tier) {

            case 'CRITICAL':

                return `
                    bg-red-500/20
                    text-red-400
                `;

            case 'HIGH':

                return `
                    bg-yellow-500/20
                    text-yellow-400
                `;

            default:

                return `
                    bg-emerald-500/20
                    text-emerald-400
                `;
        }
    }

    function formatDate(
        value?: string | null
    ) {

        if (!value) {
            return '—';
        }

        return new Date(value)
            .toLocaleDateString();
    }

    const columns:
        DataTableColumn<Contract>[] = [

        {
            key: 'customer_name',

            label: 'Customer',

            render: (row) =>
                row.customer_name || '—'
        },

        {
            key: 'status',

            label: 'Status',

            render: (row) =>
                row.status || '—'
        },

        {
            key: 'sla_tier',

            label: 'SLA Tier',

            snippet: (row) => ({

                render: () => `

                    <span
                        class="
                            px-2
                            py-1
                            rounded-lg
                            text-xs
                            ${getSlaClass(row.sla_tier)}
                        "
                    >
                        ${row.sla_tier || 'STANDARD'}
                    </span>
                `
            })
        },

        {
            key: 'total_value',

            label: 'Contract Value',

            render: (row) =>

                `$${Number(
                    row.total_value || 0
                ).toLocaleString()}`
        },

        {
            key: 'start_date',

            label: 'Start Date',

            render: (row) =>
                formatDate(
                    row.start_date
                )
        },

        {
            key: 'renewal_date',

            label: 'Renewal Date',

            render: (row) =>
                formatDate(
                    row.renewal_date
                )
        }
    ];

    const actions:
        DataTableAction<Contract>[] = [

        {
            label: 'Open',

            variant: 'success',

            onClick: (row) =>
                goto(
                    `/app/crm/contracts/${row.id}`
                )
        },

        {
            label: 'Renewal',

            variant: 'warning',

            onClick: (row) =>
                goto(
                    `/app/crm/renewals?contract=${row.id}`
                )
        }
    ];

</script>

<div class="p-6 space-y-6">

    <div
        class="flex items-start justify-between"
    >

        <div>

            <h1
                class="text-3xl font-bold text-white"
            >
                Service Contracts Registry
            </h1>

            <p
                class="text-sm text-gray-400 mt-2"
            >
                HVAC service contracts,
                SLA lifecycle management
                and renewal tracking.
            </p>

        </div>

        <button
            onclick={() =>
                goto('/app/crm/contracts/create')
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
            + New Contract
        </button>

    </div>

    <div
        class="grid grid-cols-1 md:grid-cols-4 gap-4"
    >

        <div
            class="rounded-2xl border border-gray-800 bg-gray-900 p-5"
        >

            <div class="text-sm text-gray-400">
                Active Contracts
            </div>

            <div
                class="mt-2 text-3xl font-bold text-white"
            >
                {kpis.active}
            </div>

        </div>

        <div
            class="rounded-2xl border border-gray-800 bg-gray-900 p-5"
        >

            <div class="text-sm text-gray-400">
                Total Revenue
            </div>

            <div
                class="mt-2 text-3xl font-bold text-emerald-400"
            >
                ${kpis.revenue.toLocaleString()}
            </div>

        </div>

        <div
            class="rounded-2xl border border-gray-800 bg-gray-900 p-5"
        >

            <div class="text-sm text-gray-400">
                Contracts With Renewal
            </div>

            <div
                class="mt-2 text-3xl font-bold text-yellow-400"
            >
                {kpis.renewals}
            </div>

        </div>

        <div
            class="rounded-2xl border border-gray-800 bg-gray-900 p-5"
        >

            <div class="text-sm text-gray-400">
                Critical SLA
            </div>

            <div
                class="mt-2 text-3xl font-bold text-red-400"
            >
                {kpis.critical}
            </div>

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

        <DataTableToolbar
            title="Contract Lifecycle"
            search={search}
            placeholder="Search contracts..."
            onSearch={(v) => search = v}
        />

        {#if error}

            <div
                class="
                    mt-4
                    rounded-xl
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

        <DataTable
            columns={columns}
            rows={filtered}
            loading={loading}
            rowActions={actions}
            emptyTitle="No contracts found"
            emptyDescription="
                Create your first HVAC contract.
            "
        />

    </div>

</div>