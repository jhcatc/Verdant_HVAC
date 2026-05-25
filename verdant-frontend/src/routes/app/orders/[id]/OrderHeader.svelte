<script lang="ts">
    import { createEventDispatcher } from 'svelte';
    import api from '$lib/api/client';

    let { order } = $props();

    const dispatch = createEventDispatcher();

    let editing = $state(false);
    let status = $state(order.status);

    async function save() {
        try {
            await api.patch(`/service-orders/${order.id}/status`, {
                status
            });

            order.status = status;

            dispatch('updateLog', {
                action: 'status_changed',
                description: `Status changed to ${status}`,
                created_at: new Date().toISOString()
            });

            editing = false;

        } catch (e) {
            console.error(e);
            alert('Error updating status');
        }
    }
</script>

<div class="card flex justify-between items-center">

    <div>
        <h1 class="text-2xl font-bold">{order.title}</h1>
    </div>

    <div>

        {#if editing}
            <select
                bind:value={status}
                class="border p-1 rounded 
                    bg-white text-gray-900 
                    dark:bg-gray-800 dark:text-white 
                    dark:border-gray-700
                    focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
                <option value="pending" class="bg-white dark:bg-gray-800">Pending</option>
                <option value="in_progress" class="bg-white dark:bg-gray-800">In Progress</option>
                <option value="completed" class="bg-white dark:bg-gray-800">Completed</option>
            </select>

            <button onclick={save} class="ml-2 text-blue-500">
                Save
            </button>

        {:else}
            <span
                class="cursor-pointer bg-gray-100 px-3 py-1 rounded"
                onclick={() => editing = true}
            >
                {order.status}
            </span>
        {/if}

    </div>

</div>