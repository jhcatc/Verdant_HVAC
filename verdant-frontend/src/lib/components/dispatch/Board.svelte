<script lang="ts">
    import { onMount } from 'svelte';
    import api from '$lib/api/client';
    import Column from './Column.svelte';
    
    interface ServiceOrder {
        id: string;
        title: string;
        description?: string;
        priority?: 'low' | 'medium' | 'high';
        status: 'pending' | 'assigned' | 'in_progress' | 'completed';
        assignee?: { id: string; name: string };
        created_at: string;
    }
    
    interface ColumnData {
        id: string;
        title: string;
        color: string;
        cards: ServiceOrder[];
    }
    
    let columns = $state<ColumnData[]>([
        { id: 'pending', title: 'Pending', color: 'bg-gray-400', cards: [] },
        { id: 'assigned', title: 'Assigned', color: 'bg-blue-500', cards: [] },
        { id: 'in_progress', title: 'In Progress', color: 'bg-yellow-500', cards: [] },
        { id: 'completed', title: 'Completed', color: 'bg-green-500', cards: [] }
    ]);
    
    let loading = $state(true);
    let error = $state<string | null>(null);
    
    async function loadOrders() {
        loading = true;
        error = null;

        try {
            const res = await api.get('/service-orders/');
            const data = res.data;

            columns.forEach(col => {
                col.cards = data.filter(o => o.status === col.id);
            });

        } catch (err) {
            console.error('Error loading orders', err);
            error = 'Failed to load orders';
        } finally {
            loading = false;
        }
    }
    
    onMount(() => {
        loadOrders();
    });
</script>

<div class="flex overflow-x-auto gap-4 pb-4 min-h-[calc(100vh-200px)]">
    {#if loading}
        <div class="flex items-center justify-center w-full">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-verdant-600"></div>
        </div>
    {:else if error}
        <div class="flex items-center justify-center w-full">
            <p class="text-red-500">{error}</p>
        </div>
    {:else}
        {#each columns as col}
            <Column column={col} />
        {/each}
    {/if}
</div>