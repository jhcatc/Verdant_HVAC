<script lang="ts">
    import api from '$lib/api/client';
    import { onMount } from 'svelte';

    let locations = $state([]);

    let form = $state({
        name: '',
        code: '',
        type: 'van'
    });

    async function load() {
        const res = await api.get('/locations/');
        locations = res.data;
    }

    async function create() {
        await api.post('/locations/', form);
        form = { name: '', code: '', type: 'van' };
        await load();
    }

    onMount(load);
</script>

<h1 class="text-xl font-bold mb-4">Locations (Vans)</h1>

<div class="bg-gray-800 p-4 rounded mb-6 grid grid-cols-3 gap-3">

    <input bind:value={form.name}
        placeholder="Name"
        class="p-2 bg-gray-900 rounded" />

    <input bind:value={form.code}
        placeholder="Code (VAN-01)"
        class="p-2 bg-gray-900 rounded" />

    <select bind:value={form.type}
        class="p-2 bg-gray-900 rounded">
        <option value="warehouse">Warehouse</option>
        <option value="van">Van</option>
    </select>

    <button class="bg-green-600 px-3 py-2 rounded col-span-3"
        onclick={create}>
        Create Location
    </button>

</div>

<div class="space-y-2">
    {#each locations as l}
        <div class="bg-gray-800 p-3 rounded">
            {l.name} ({l.code}) - {l.type}
        </div>
    {/each}
</div>