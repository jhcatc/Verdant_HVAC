<script lang="ts">
    import api from '$lib/api/client';

    const { orderId, technicians } = $props();

    let selected = $state('');

    async function assign() {
        await api.patch(`/service-orders/${orderId}/assign?technician_id=${selected}`);
        alert('Assigned!');
    }
</script>

<div class="flex gap-2">
    <select
        bind:value={selected}
        class="border p-2 rounded 
            bg-white text-gray-900 
            dark:bg-gray-800 dark:text-white 
            dark:border-gray-700
            focus:outline-none focus:ring-2 focus:ring-blue-500"
    >
        <option value="" class="bg-white dark:bg-gray-800">
            Select tech
        </option>

        {#each technicians as t}
            <option
                value={t.id}
                class="bg-white dark:bg-gray-800"
            >
                {t.name}
            </option>
        {/each}
    </select>

    <button
        class="bg-blue-600 text-white px-3 rounded"
        onclick={assign}
    >
        Assign
    </button>
</div>