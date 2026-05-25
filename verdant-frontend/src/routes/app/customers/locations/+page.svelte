<script lang="ts">
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';

    import {
        getLocations
    } from '$lib/api/customerLocations';

    let locations = $state([]);
    let loading = $state(true);

    onMount(async () => {

        try {

            locations = await getLocations();

        } catch (e) {

            console.error(e);

        } finally {

            loading = false;
        }
    });
</script>

<div class="p-6">

    <div class="flex items-center justify-between mb-6">

        <div>

            <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
                Location List
            </h1>

            <p class="text-sm text-gray-500">
                Customer facilities and service locations.
            </p>

        </div>

        <button
            onclick={() => goto('/app/customers/locations/create')}
            class="bg-emerald-600 text-white px-4 py-2 rounded"
        >
            Create Location
        </button>

    </div>

    <div class="border rounded overflow-hidden">

        <table class="w-full text-sm">

            <thead class="bg-gray-100 dark:bg-gray-800">

                <tr>

                    <th class="text-left p-3">
                        Customer
                    </th>

                    <th class="text-left p-3">
                        Location
                    </th>

                    <th class="text-left p-3">
                        City
                    </th>

                    <th class="text-left p-3">
                        Contact
                    </th>

                    <th class="text-left p-3">
                        Actions
                    </th>

                </tr>

            </thead>

            <tbody>

                {#if loading}

                    <tr>
                        <td colspan="4" class="p-4">
                            Loading...
                        </td>
                    </tr>

                {:else if locations.length === 0}

                    <tr>
                        <td colspan="4" class="p-4">
                            No locations found
                        </td>
                    </tr>

                {:else}

                    {#each locations as location}

                        <tr class="border-t">

                            <td class="p-3">
                                {location.customer_name || '—'}
                            </td>

                            <td class="p-3">

                                <div class="font-medium">
                                    {location.name}
                                </div>

                                <div class="text-xs text-gray-500">
                                    {location.address || '—'}
                                </div>

                            </td>

                            <td class="p-3">
                                {location.city || '—'}
                            </td>

                            <td class="p-3">

                                <div>
                                    {location.contact_name || '—'}
                                </div>

                                <div class="text-xs text-gray-500">
                                    {location.contact_phone || ''}
                                </div>

                            </td>

                            <td class="p-3">

                                <button
                                    onclick={() =>
                                        goto(
                                            `/app/customers/locations/${location.id}`
                                        )
                                    }
                                    class="px-3 py-1 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-xs"
                                >
                                    Open
                                </button>

                            </td>

                        </tr>

                    {/each}

                {/if}

            </tbody>

        </table>

    </div>

</div>