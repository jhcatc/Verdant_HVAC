<script lang="ts">

    import {
        onMount
    } from 'svelte';

    import {
        getComponentRegistrySnapshot
    } from '$lib/api/componentRegistry';

    import type {
        ComponentRegistrySnapshot,
        ComponentRegistryItem
    } from '$lib/types/component-registry';

    import type {
        DataTableColumn
    } from '$lib/types/data-table';

    let snapshot:
        ComponentRegistrySnapshot | null = null;

    let loading = true;

    const columns:
    DataTableColumn<ComponentRegistryItem>[] = [

        {
            key: 'equipment_asset_tag',
            label: 'Asset'
        },

        {
            key: 'component_name',
            label: 'Component'
        },

        {
            key: 'component_type',
            label: 'Type'
        },

        {
            key: 'status',
            label: 'Status'
        },

        {
            key: 'health_score',
            label: 'Health',
            sortable: true
        },

        {
            key: 'warranty_status',
            label: 'Warranty'
        },

        {
            key: 'mtbf_days',
            label: 'MTBF'
        }
    ];

    onMount(async () => {

        snapshot =
            await getComponentRegistrySnapshot();

        loading = false;
    });

</script>

<div class="space-y-6 p-6">

    <div>

        <h1
            class="text-3xl font-bold text-white"
        >
            Component Registry
        </h1>

        <p
            class="text-sm text-gray-400 mt-1"
        >
            Enterprise component lifecycle,
            MTBF analytics and predictive
            maintenance intelligence.
        </p>

    </div>

    {#if loading}

        <div
            class="rounded-2xl border border-gray-800 bg-gray-900 p-8"
        >
            Loading registry...
        </div>

    {:else if snapshot}

        <div
            class="grid grid-cols-1 md:grid-cols-5 gap-4"
        >

            <div
                class="rounded-2xl border border-gray-800 bg-gray-900 p-5"
            >
                <div class="text-sm text-gray-400">
                    Components
                </div>

                <div class="text-3xl font-bold text-white mt-2">
                    {snapshot.total_components}
                </div>
            </div>

            <div
                class="rounded-2xl border border-gray-800 bg-gray-900 p-5"
            >
                <div class="text-sm text-gray-400">
                    Critical
                </div>

                <div class="text-3xl font-bold text-red-500 mt-2">
                    {snapshot.critical_components}
                </div>
            </div>

            <div
                class="rounded-2xl border border-gray-800 bg-gray-900 p-5"
            >
                <div class="text-sm text-gray-400">
                    Failed
                </div>

                <div class="text-3xl font-bold text-orange-500 mt-2">
                    {snapshot.failed_components}
                </div>
            </div>

            <div
                class="rounded-2xl border border-gray-800 bg-gray-900 p-5"
            >
                <div class="text-sm text-gray-400">
                    Warranty Expired
                </div>

                <div class="text-3xl font-bold text-yellow-500 mt-2">
                    {snapshot.warranty_expiring}
                </div>
            </div>

            <div
                class="rounded-2xl border border-gray-800 bg-gray-900 p-5"
            >
                <div class="text-sm text-gray-400">
                    Avg Health
                </div>

                <div class="text-3xl font-bold text-emerald-500 mt-2">
                    {snapshot.average_health_score}%
                </div>
            </div>

        </div>

        <div
            class="rounded-2xl border border-gray-800 bg-gray-900 overflow-hidden"
        >

            <table class="w-full">

                <thead
                    class="bg-gray-950 border-b border-gray-800"
                >
                    <tr>

                        {#each columns as column}

                            <th
                                class="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase"
                            >
                                {column.label}
                            </th>

                        {/each}

                    </tr>
                </thead>

                <tbody>

                    {#each snapshot.items as row}

                        <tr
                            class="border-b border-gray-800 hover:bg-gray-800/50"
                        >

                            <td class="px-4 py-3 text-white">
                                {row.equipment_asset_tag}
                            </td>

                            <td class="px-4 py-3 text-white">
                                {row.component_name}
                            </td>

                            <td class="px-4 py-3 text-gray-300">
                                {row.component_type}
                            </td>

                            <td class="px-4 py-3">

                                <span
                                    class="px-2 py-1 rounded-lg text-xs bg-gray-800 text-gray-200"
                                >
                                    {row.status}
                                </span>

                            </td>

                            <td class="px-4 py-3">

                                <div
                                    class="w-full bg-gray-800 rounded-full h-2"
                                >
                                    <div
                                        class="bg-emerald-500 h-2 rounded-full"
                                        style={`width:${row.health_score}%`}
                                    />
                                </div>

                                <div
                                    class="text-xs text-gray-400 mt-1"
                                >
                                    {row.health_score}%
                                </div>

                            </td>

                            <td class="px-4 py-3 text-gray-300">
                                {row.warranty_status}
                            </td>

                            <td class="px-4 py-3 text-gray-300">
                                {row.mtbf_days ?? '-'}
                            </td>

                        </tr>

                    {/each}

                </tbody>

            </table>

        </div>

    {/if}

</div>