<script lang="ts">
import api from '$lib/api/client';
import { onMount } from 'svelte';

let locations = $state([]);
let items = $state([]);

let form = $state({
    item_id: '',
    from_location: '',
    to_location: '',
    quantity: 0
});

async function load() {
    locations = (await api.get('/inventory/locations')).data;
    items = (await api.get('/inventory/')).data;
}

onMount(load);

async function transfer() {
    await api.post('/inventory/transfer', form);
    alert("Transfer completed");
}
</script>

<h1 class="text-xl font-bold mb-4">Inventory Transfer</h1>

<select bind:value={form.item_id}>
    <option value="">Select Item</option>
    {#each items as i}
        <option value={i.id}>{i.name}</option>
    {/each}
</select>

<select bind:value={form.from_location}>
    <option value="">From</option>
    {#each locations as l}
        <option value={l.id}>{l.name}</option>
    {/each}
</select>

<select bind:value={form.to_location}>
    <option value="">To</option>
    {#each locations as l}
        <option value={l.id}>{l.name}</option>
    {/each}
</select>

<input type="number" bind:value={form.quantity} />

<button onclick={transfer}
    class="bg-blue-600 px-3 py-2 mt-3">
    Transfer
</button>