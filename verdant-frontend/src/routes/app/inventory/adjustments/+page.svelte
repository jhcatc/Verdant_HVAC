<script lang="ts">
    import api from '$lib/api/client';
    import { onMount } from 'svelte';

    let requests = $state([]);
    let items = $state([]);
    let locations = $state([]);

    let form = $state({
        item_id: '',
        location_id: '',
        quantity: 0,
        reason: ''
    });

    async function load() {
        const [r1, r2, r3] = await Promise.all([
            api.get('/inventory/adjustments'),
            api.get('/inventory/'),
            api.get('/locations/')
        ]);

        requests = r1.data;
        items = r2.data;
        locations = r3.data;
    }

    async function requestAdjustment() {
        await api.post('/inventory/adjustments/request', form);
        await load();
    }

    async function approve(id) {
        await api.post(`/inventory/adjustments/${id}/approve`);
        await load();
    }

    onMount(load);
</script>

<h1 class="text-xl font-bold mb-4">Adjustment Requests</h1>

<!-- 🔹 CREATE REQUEST -->
<div class="bg-gray-800 p-4 rounded mb-6 grid grid-cols-4 gap-3">

    <select bind:value={form.item_id} class="p-2 bg-gray-900 rounded">
        <option value="">Select Item</option>
        {#each items as i}
            <option value={i.id}>{i.name}</option>
        {/each}
    </select>

    <select bind:value={form.location_id} class="p-2 bg-gray-900 rounded">
        <option value="">Select Location</option>
        {#each locations as l}
            <option value={l.id}>{l.name}</option>
        {/each}
    </select>

    <input type="number" bind:value={form.quantity}
        placeholder="Quantity (+/-)"
        class="p-2 bg-gray-900 rounded" />

    <input bind:value={form.reason}
        placeholder="Reason"
        class="p-2 bg-gray-900 rounded" />

    <button class="bg-yellow-600 px-3 py-2 rounded col-span-4"
        onclick={requestAdjustment}>
        Request Adjustment
    </button>

</div>

<!-- 🔹 LIST -->
<div class="space-y-2">
    {#each requests as r}
        <div class="bg-gray-800 p-3 rounded flex justify-between items-center">

            <div>
                <div>{r.item_name} | {r.location_name}</div>
                <div class="text-sm text-gray-400">
                    {r.quantity} | {r.reason}
                </div>
            </div>

            <div class="flex gap-2">
                <span>{r.status}</span>

                {#if r.status === 'pending'}
                    <button class="bg-green-600 px-2 py-1 rounded"
                        onclick={() => approve(r.id)}>
                        Approve
                    </button>
                {/if}
            </div>

        </div>
    {/each}
</div>