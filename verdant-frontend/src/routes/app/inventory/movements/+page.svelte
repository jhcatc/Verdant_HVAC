<script lang="ts">
    import api from '$lib/api/client';
    import { onMount } from 'svelte';

    let movements = $state([]);
    let items = $state([]);
    let locations = $state([]);

    let form = $state({
        item_id: '',
        from_location: '',
        to_location: '',
        quantity: 0
    });

    async function load() {
        const [m, i, l] = await Promise.all([
            api.get('/inventory/movements'),
            api.get('/inventory/'),
            api.get('/locations/')
        ]);

        movements = m.data;
        items = i.data;
        locations = l.data;
    }

    async function transfer() {
        await api.post('/inventory/transfer', form);
        await load();
    }

    onMount(load);
</script>

<h1 class="text-xl font-bold mb-4">Inventory Movements</h1>

<!-- 🔹 TRANSFER -->
<div class="bg-gray-800 p-4 rounded mb-6 grid grid-cols-4 gap-3">

    <select bind:value={form.item_id} class="p-2 bg-gray-900 rounded w-full">
        <option value="">Item</option>
        {#each items as i}
            <option value={i.id}>{i.name}</option>
        {/each}
    </select>

    <select bind:value={form.from_location} class="p-2 bg-gray-900 rounded w-full">
        <option value="">From</option>
        {#each locations as l}
            <option value={l.id}>{l.name}</option>
        {/each}
    </select>

    <select bind:value={form.to_location} class="p-2 bg-gray-900 rounded w-full">
        <option value="">To</option>
        {#each locations as l}
            <option value={l.id}>{l.name}</option>
        {/each}
    </select>

    <input type="number"
        bind:value={form.quantity}
        placeholder="Qty"
        class="p-2 bg-gray-900 rounded w-full" />

    <button class="bg-blue-600 px-3 py-2 rounded col-span-4"
        onclick={transfer}>
        Transfer
    </button>
</div>

<!-- 🔹 LIST -->
<div class="space-y-2">
    {#each movements as m}
        <div class="bg-gray-800 p-3 rounded">
            {m.item_name} | {m.from_name} → {m.to_name} | {m.quantity}
        </div>
    {/each}
</div>