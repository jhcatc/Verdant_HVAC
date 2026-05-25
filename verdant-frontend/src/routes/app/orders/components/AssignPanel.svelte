<script lang="ts">
    import api from '$lib/api/client';

    const { orderId, technicians } = $props();

    let selected = $state('');

    async function assign() {
        await api.patch(`/service-orders/${orderId}/dispatch`, {
            technician_id: selected
        });

        alert('Assigned!');
    }
</script>

<div class="flex gap-2">
    <select bind:value={selected} class="border p-2 rounded">
        <option value="">Select tech</option>
        {#each technicians as t}
            <option value={t.id}>{t.name}</option>
        {/each}
    </select>

    <button
        class="bg-blue-600 text-white px-3 rounded"
        onclick={assign}
    >
        Assign
    </button>
</div>