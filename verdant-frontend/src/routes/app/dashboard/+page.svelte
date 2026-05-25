<script lang="ts">
    import { onMount } from 'svelte';
    import api from '$lib/api/client';

    import StatsCard from './components/StatsCard.svelte';
    import OrdersTable from './components/OrdersTable.svelte';
    import Charts from './components/Charts.svelte';

    let orders = $state([]);
    let loading = $state(true);

    let stats = $state({
        total: 0,
        in_progress: 0,
        completed: 0,
        revenue: 0
    });

    onMount(async () => {
        try {
            const res = await api.get('/service-orders/');
            orders = res.data;

            stats = {
                total: orders.length,
                in_progress: orders.filter(o => o.status === 'in_progress').length,
                completed: orders.filter(o => o.status === 'completed').length,
                revenue: orders.reduce((acc, o) => acc + (o.actual_cost || 0), 0)
            };

        } catch (err) {
            console.error('Error loading dashboard:', err);
        } finally {
            loading = false;
        }
    });
</script>

<h1 class="text-2xl font-bold mb-6">Dashboard</h1>

{#if loading}
    <p class="text-gray-500">Loading dashboard...</p>

{:else if orders.length === 0}
    <div class="bg-white p-6 rounded-xl shadow text-center text-gray-500">
        No orders yet
    </div>

{:else}
    <div class="grid grid-cols-4 gap-4 mb-6">
        <StatsCard title="Total Orders" value={stats.total} />
        <StatsCard title="In Progress" value={stats.in_progress} />
        <StatsCard title="Completed" value={stats.completed} />
        <StatsCard title="Revenue" value={`$${stats.revenue}`} />
    </div>

    <Charts {orders} />

    <OrdersTable {orders} />
{/if}