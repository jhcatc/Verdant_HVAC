<script lang="ts">
    import { onMount } from 'svelte';
    import { page } from '$app/state';
    import api from '$lib/api/client';

    import KanbanColumn from './components/KanbanColumn.svelte';
    import AssignModal from './components/AssignModal.svelte';

    import { connectWS } from '$lib/stores/ws';

    let orders = $state([]);
    let loading = $state(true);
    let selectedOrder = $state(null);

    const currentPath = $derived(page.url.pathname);

    const STATUS = {
        PENDING: 'pending',
        ASSIGNED: 'assigned',
        IN_PROGRESS: 'in_progress',
        COMPLETED: 'completed'
    } as const;    

    const columns = [
        { key: STATUS.PENDING, title: 'Pending' },
        { key: STATUS.ASSIGNED, title: 'Assigned' },
        { key: STATUS.IN_PROGRESS, title: 'In Progress' },
        { key: STATUS.COMPLETED, title: 'Completed' }
    ];

    async function loadOrders() {
        loading = true;

        try {
            const res = await api.get('/service-orders/');
            orders = res.data;
        } catch (err) {
            console.error('Error loading orders', err);
            orders = [];
        } finally {
            loading = false;
        }
    }

    function normalizeStatus(status: string) {
        return status?.toLowerCase().replace('-', '_');
    }

    function getOrdersByStatus(status) {
        return orders.filter(o => normalizeStatus(o.status) === status);
    }

    async function dispatchOrder({
        orderId,
        technicianId,
        scheduledAt,
        durationHours = 1
    }) {
        try {
            await api.patch(`/service-orders/${orderId}/dispatch`, {
                technician_id: technicianId,
                scheduled_at: scheduledAt,
                duration_hours: durationHours
            });

            // 🔥 REFRESH LOCAL
            await loadOrders();

        } catch (err) {
            console.error('Dispatch failed', err);
        }
    }

    function handleDrop(orderId: string) {
        selectedOrder = orders.find(o => o.id === orderId);
    }

    onMount(() => {
        loadOrders();

        // 🔥 REALTIME
        connectWS((data) => {
            if (data.type === 'order_status_changed') {
                orders = orders.map(o =>
                    o.id === data.order_id
                        ? { ...o, status: data.status }
                        : o
                );
            }
        });
    });
</script>

<h1 class="text-2xl font-bold mb-6">
    Dispatch Board
</h1>

{#if loading}
    <p>Loading...</p>

{:else if orders.length === 0}
    <div>No orders yet</div>

{:else}
    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
        {#each columns as col}
            <KanbanColumn
                title={col.title}
                status={col.key}
                orders={getOrdersByStatus(col.key)}
                onDrop={handleDrop}
            />
        {/each}
    </div>
{/if}

{#if selectedOrder}
    <AssignModal
        {selectedOrder}
        onConfirm={async ({ technicianId, scheduledAt, durationHours }) => {
            await dispatchOrder({
                orderId: selectedOrder.id,
                technicianId,
                scheduledAt,
                durationHours
            });

            selectedOrder = null;
        }}
        onClose={() => selectedOrder = null}
    />
{/if}