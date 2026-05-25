<script lang="ts">
    import CustomerAutocomplete from '$lib/components/customer/CustomerAutocomplete.svelte';
    import api from '$lib/api/client';
    import { onMount } from 'svelte';

    let orders = $state([]);

    let customerId = $state(null);

    onMount(async () => {
        const res = await api.get('/service-orders/');
        orders = res.data;
    });
</script>

<h1 class="text-xl font-bold mb-4">Service Orders</h1>
<CustomerAutocomplete bind:value={customerId} />
<table class="w-full border">
    <thead>
        <tr>
            <th>Title</th>
            <th>Status</th>
            <th>City</th>
        </tr>
    </thead>
    <tbody>
        {#each orders as o}
        <tr class="cursor-pointer" onclick={() => location.href = `/app/service-orders/${o.id}`}>
            <td>{o.title}</td>
            <td>{o.status}</td>
            <td>{o.city}</td>
        </tr>
        {/each}
    </tbody>
</table>