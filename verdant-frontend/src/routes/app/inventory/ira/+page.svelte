<script lang="ts">
    import api from '$lib/api/client';
    import { onMount } from 'svelte';

    let data = $state([]);
    let loading = $state(false);
    let error = $state('');

    async function load() {
        loading = true;
        error = '';

        try {
            const res = await api.get('/inventory/ira');
            data = res.data;
        } catch (e) {
            console.error(e);
            error = 'Failed to load IRA data';
        }

        loading = false;
    }

    onMount(load);
</script>

<h1 class="text-xl font-bold mb-4">Inventory Turnover (IRA)</h1>

{#if loading}
    <p>Loading...</p>

{:else if error}
    <p class="text-red-500">{error}</p>

{:else if data.length === 0}
    <p>No data available</p>

{:else}
    <div class="overflow-auto">

        <table class="min-w-full text-sm">

            <thead class="bg-gray-800">
                <tr>
                    <th class="p-2 text-left">Location</th>
                    <th class="p-2 text-center">Type</th>
                    <th class="p-2 text-center">Stock</th>
                    <th class="p-2 text-center">30d Consumption</th>
                    <th class="p-2 text-center">IRA</th>
                </tr>
            </thead>

            <tbody>
                {#each data as row}
                    <tr class="border-b border-gray-700">

                        <td class="p-2">
                            {row.name} ({row.code})
                        </td>

                        <td class="p-2 text-center">
                            {row.type}
                        </td>

                        <td class="p-2 text-center">
                            {row.stock}
                        </td>

                        <td class="p-2 text-center">
                            {row.consumption_30d}
                        </td>

                        <td class={`p-2 text-center font-bold
                            ${row.ira > 1 ? 'text-green-400' :
                              row.ira > 0.5 ? 'text-yellow-400' :
                              'text-red-400'}`}
                        >
                            {row.ira}
                        </td>

                    </tr>
                {/each}
            </tbody>

        </table>

    </div>
{/if}