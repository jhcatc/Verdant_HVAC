<script lang="ts">
    import { onMount } from 'svelte';
    import { createEventDispatcher } from 'svelte';
    import api from '$lib/api/client';
    import { getTechnicians } from '$lib/api/users';

    let { order } = $props();

    const dispatch = createEventDispatcher();

    let technicians = $state([]);
    let technician = $state('');

    let note = $state('');

    // 🔥 cargar técnicos reales
    onMount(async () => {
        technicians = await getTechnicians();

        // set actual
        const current = order.assignments?.[0];
        if (current) {
            technician = current.user_id;
        }
    });

    async function assign() {
        await api.patch(`/service-orders/${order.id}/assign`, {
            technician_id: technician
        });

        const tech = technicians.find(t => t.id === technician);

        // 🔥 actualizar UI local
        order.assignments = [{
            user_id: technician,
            user: { full_name: tech?.name }
        }];
        order = { ...order };

        dispatch('updateLog', {
            action: 'assigned',
            description: `Assigned to ${tech?.name}`,
            created_at: new Date().toISOString()
        });
    }

    async function addNote() {
        if (!note) return;

        await api.post(`/service-orders/${order.id}/notes`, { note });

        dispatch('updateLog', {
            action: 'note',
            description: note,
            created_at: new Date().toISOString()
        });

        note = '';
    }
</script>

<div class="card space-y-4">

    <h2 class="font-semibold">Technician</h2>

    <select bind:value={technician} class="w-full border p-2 rounded">
        <option value="">Unassigned</option>

        {#each technicians as t}
            <option value={t.id}>{t.name}</option>
        {/each}
    </select>

    <button
        onclick={assign}
        class="w-full bg-blue-500 text-white p-2 rounded"
    >
        Assign
    </button>

    <hr />

    <h2 class="font-semibold">Add Note</h2>

    <textarea
        bind:value={note}
        class="w-full border p-2 rounded"
        rows="3"
    />

    <button
        onclick={addNote}
        class="w-full bg-green-500 text-white p-2 rounded"
    >
        Save Note
    </button>

</div>