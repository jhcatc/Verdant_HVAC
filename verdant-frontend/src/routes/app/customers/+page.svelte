<script lang="ts">

    import { onMount } from 'svelte';

    import { goto } from '$app/navigation';

    import api from '$lib/api/client';

    let loading =
        $state(true);

    let customers =
        $state([]);

    let search =
        $state('');

    async function load() {

        loading = true;

        try {

            const res =
                await api.get('/customers');

            customers =
                res.data || [];

        } catch (e) {

            console.error(e);

            customers = [];

        } finally {

            loading = false;
        }
    }

    onMount(load);

    const filteredCustomers = $derived(

        customers.filter((c) => {

            const q =
                search.trim().toLowerCase();

            if (!q) {
                return true;
            }

            return (

                c.name?.toLowerCase().includes(q) ||

                c.email?.toLowerCase().includes(q) ||

                c.phone?.toLowerCase().includes(q) ||

                c.city?.toLowerCase().includes(q)
            );
        })
    );

</script>

<div class="p-6 space-y-6">

    <!-- HEADER -->

    <div class="flex items-start justify-between">

        <div>

            <h1 class="text-3xl font-bold text-white">
                Customer Registry
            </h1>

            <p class="text-sm text-gray-400 mt-1">
                Enterprise customer operations, facilities,
                SLA visibility, equipment relationships
                and service history.
            </p>

        </div>

        <button
            onclick={() => goto('/app/customers/create')}
            class="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-sm"
        >
            Create Customer
        </button>

    </div>

    <!-- FILTERS -->

    <div
        class="rounded-2xl border border-gray-800 bg-gray-900 p-4"
    >

        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">

            <input
                bind:value={search}
                placeholder="Search customer, email, city..."
                class="px-4 py-2 rounded-xl bg-gray-950 border border-gray-700 text-white"
            />

        </div>

    </div>

    <!-- TABLE -->

    <div
        class="rounded-2xl border border-gray-800 bg-gray-900 overflow-hidden"
    >

        <div class="overflow-x-auto">

            <table class="min-w-full text-sm">

                <thead class="bg-gray-950">

                    <tr
                        class="text-left uppercase tracking-wider text-xs text-gray-400"
                    >

                        <th class="px-5 py-4">
                            Customer
                        </th>

                        <th class="px-5 py-4">
                            Email
                        </th>

                        <th class="px-5 py-4">
                            Phone
                        </th>

                        <th class="px-5 py-4">
                            City
                        </th>

                        <th class="px-5 py-4">
                            Equipment
                        </th>

                        <th class="px-5 py-4">
                            SLA
                        </th>

                        <th class="px-5 py-4">
                            Risk
                        </th>

                        <th class="px-5 py-4">
                            Actions
                        </th>

                    </tr>

                </thead>

                <tbody>

                    {#if loading}

                        <tr>

                            <td
                                colspan="8"
                                class="px-5 py-10 text-center text-gray-500"
                            >
                                Loading customers...
                            </td>

                        </tr>

                    {:else if filteredCustomers.length === 0}

                        <tr>

                            <td
                                colspan="8"
                                class="px-5 py-10 text-center text-gray-500"
                            >
                                No customers found.
                            </td>

                        </tr>

                    {:else}

                        {#each filteredCustomers as customer}

                            <tr
                                class="border-t border-gray-800 hover:bg-gray-800/40 transition"
                            >

                                <td class="px-5 py-4">

                                    <div
                                        class="font-medium text-white"
                                    >
                                        {customer.name}
                                    </div>

                                </td>

                                <td class="px-5 py-4 text-gray-300">
                                    {customer.email || '—'}
                                </td>

                                <td class="px-5 py-4 text-gray-300">
                                    {customer.phone || '—'}
                                </td>

                                <td class="px-5 py-4 text-gray-300">
                                    {customer.city || '—'}
                                </td>

                                <td class="px-5 py-4 text-gray-300">
                                    {customer.equipment_count || 0}
                                </td>

                                <td class="px-5 py-4">

                                    <span
                                        class="px-2 py-1 rounded-lg text-xs bg-emerald-500/20 text-emerald-400"
                                    >
                                        Active
                                    </span>

                                </td>

                                <td class="px-5 py-4">

                                    <span
                                        class="px-2 py-1 rounded-lg text-xs bg-yellow-500/20 text-yellow-400"
                                    >
                                        Medium
                                    </span>

                                </td>

                                <td class="px-5 py-4">

                                    <div class="flex gap-2">

                                        <button
                                            onclick={() => goto(`/app/customers/${customer.id}`)}
                                            class="px-3 py-1 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-xs"
                                        >
                                            Open
                                        </button>

                                        <button
                                            onclick={() => goto(`/app/customers/${customer.id}`)}
                                            class="px-3 py-1 rounded-lg bg-gray-700 hover:bg-gray-600 text-white text-xs"
                                        >
                                            Edit
                                        </button>

                                    </div>

                                </td>

                            </tr>

                        {/each}

                    {/if}

                </tbody>

            </table>

        </div>

    </div>

</div>