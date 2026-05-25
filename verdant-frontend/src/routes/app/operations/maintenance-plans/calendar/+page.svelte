<script lang="ts">
    import { onMount } from 'svelte';

    import api from '$lib/api/client';

    let orders = $state([]);

    let loading = $state(true);

    async function load() {

        loading = true;

        const res = await api.get('/service-orders/');

        orders = res.data.filter(
            o => o.source === 'preventive_maintenance'
        );

        loading = false;
    }

    async function runGenerator() {

        await api.post('/pm-generator/run');

        await load();
    }

    onMount(load);
</script>

<div class="space-y-6">

    <!-- HEADER -->

    <div class="flex items-center justify-between">

        <div>

            <h1 class="text-3xl font-bold text-white">
                PM Calendar Engine
            </h1>

            <p class="text-slate-400 mt-1">
                Preventive maintenance orchestration,
                generation and scheduling engine.
            </p>

        </div>

        <button
            onclick={runGenerator}
            class="bg-emerald-500 hover:bg-emerald-400
                   text-white px-5 py-3 rounded-xl
                   font-semibold shadow-lg"
        >
            Run PM Generator
        </button>

    </div>

    <!-- TABLE -->

    <div class="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden">

        <table class="w-full">

            <thead class="bg-slate-950">

                <tr class="text-left text-sm text-slate-400">

                    <th class="p-4">Work Order</th>
                    <th class="p-4">Customer</th>
                    <th class="p-4">Equipment</th>
                    <th class="p-4">Plan</th>
                    <th class="p-4">Scheduled</th>
                    <th class="p-4">Status</th>

                </tr>

            </thead>

            <tbody>

                {#if loading}

                    <tr>
                        <td colspan="6" class="p-10 text-center text-slate-500">
                            Loading PM orders...
                        </td>
                    </tr>

                {:else}

                    {#each orders as order}

                        <tr
                            class="border-t border-slate-800
                                   hover:bg-slate-800/50
                                   cursor-pointer"
                            onclick={() =>
                                location.href =
                                `/app/service-orders/${order.id}`
                            }
                        >

                            <td class="p-4 text-white font-medium">
                                {order.title}
                            </td>

                            <td class="p-4 text-slate-300">
                                {order.customer?.name ?? '-'}
                            </td>

                            <td class="p-4 text-slate-300">
                                {order.equipment?.name ?? '-'}
                            </td>

                            <td class="p-4 text-slate-300">
                                {order.maintenance_plan?.name ?? '-'}
                            </td>

                            <td class="p-4 text-slate-300">
                                {order.scheduled_at
                                    ? new Date(order.scheduled_at)
                                        .toLocaleString()
                                    : '-'}
                            </td>

                            <td class="p-4">

                                <div class="inline-flex px-3 py-1 rounded-full
                                            text-xs font-semibold
                                            bg-emerald-500/20
                                            text-emerald-400">

                                    {order.status}

                                </div>

                            </td>

                        </tr>

                    {/each}

                {/if}

            </tbody>

        </table>

    </div>

</div>