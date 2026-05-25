<script lang="ts">
    import { onMount } from 'svelte';
    import api from '$lib/api/client';
    import { goto } from '$app/navigation';

    let orders = $state([]);
    let search = $state('');
    let statusFilter = $state('all');

    onMount(async () => {
        const res = await api.get('/service-orders/');
        orders = res.data;
    });

    let filtered = $derived(
        orders.filter(o => {
            const matchesSearch = o.title.toLowerCase().includes(search.toLowerCase());
            const matchesStatus = statusFilter === 'all' || o.status === statusFilter;
            return matchesSearch && matchesStatus;
        })
    );

    function goToNew() {
        goto('/app/orders/new');
    }

    function goToDetail(id: string) {
        goto(`/app/orders/${id}`);
    }
</script>

<div class="flex justify-between items-center mb-4">
    <h1 class="text-2xl font-bold heading">Orders</h1>

    <button
        class="bg-green-600 text-white px-4 py-2 rounded-lg"
        onclick={goToNew}
    >
        + New Order
    </button>
</div>

<div class="flex gap-4 mb-4">
    <input
        class="input"
        placeholder="Search..."
        bind:value={search}
    />

    <select bind:value={statusFilter} class="input w-48">
        <option value="all">All</option>
        <option value="pending">Pending</option>
        <option value="in_progress">In Progress</option>
        <option value="completed">Completed</option>
    </select>
</div>

<table class="table">
    <thead>
        <tr class="border-b text-left">
            <th class="p-2">Title</th>
            <th>Status</th>
            <th>City</th>
            <th>Cost</th>
        </tr>
    </thead>

    <tbody>
        {#each filtered as o}
        <tr
            class="border-b hover:bg-gray-50 cursor-pointer"
            onclick={() => goToDetail(o.id)}
        >
            <td class="p-2">{o.title}</td>
            <td>{o.status}</td>
            <td>{o.city}</td>
            <td>${o.actual_cost ?? 0}</td>
        </tr>
        {/each}
    </tbody>
</table>