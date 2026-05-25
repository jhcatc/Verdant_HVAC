<script lang="ts">
    import api from '$lib/api/client';

    let { tech, hour, occupied } = $props();

    function handleDragOver(e: DragEvent) {
        e.preventDefault();
    }

    function drop(e: DragEvent) {
        e.preventDefault();

        const orderId = e.dataTransfer?.getData('orderId');
        if (!orderId) return;

        if (occupied) {
            alert('Slot ocupado');
            return;
        }

        const date = new Date();
        date.setHours(hour, 0, 0);

        assign(orderId, tech.id, date);
    }

    async function assign(orderId: string, techId: string, date: Date) {
        await api.patch(`/service-orders/${orderId}/dispatch`, {
            technician_id: techId,
            scheduled_at: date.toISOString(),
            duration_hours: 2
        });
    }
</script>

<div
    class={`h-16 border flex items-center justify-center text-xs
    ${occupied ? 'bg-red-200 dark:bg-red-800' : 'bg-gray-50 dark:bg-gray-700'}`}
    ondragover={handleDragOver}
    ondrop={drop}
>
    {#if occupied}
        Busy
    {/if}
</div>