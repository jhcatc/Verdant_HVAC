<script lang="ts">
  import dayjs from "dayjs";
  import api from "$lib/api/client";

  let { technician, slotTime, reload } = $props();

  let hovering = $state(false);

  async function handleDrop(e: DragEvent) {
    e.preventDefault();

    hovering = false;

    const raw = e.dataTransfer?.getData("application/json");

    if (!raw) {
      return;
    }

    const order = JSON.parse(raw);

    try {

      await api.patch(`/service-orders/${order.id}/dispatch`, {
        technician_id: technician.id,
        scheduled_at: dayjs(slotTime).toISOString(),
        duration_hours: order.duration_hours || 1
      });

      await reload();

    } catch (err) {

      console.error(err);
      alert("Dispatch error");
    }
  }

  function handleDragOver(e: DragEvent) {
    e.preventDefault();
    hovering = true;
  }

  function handleLeave() {
    hovering = false;
  }
</script>

<div
  class="h-12 border-b border-l border-gray-200 dark:border-gray-700 transition-colors
  {hovering ? 'bg-emerald-100 dark:bg-emerald-900/30' : 'bg-transparent'}"
  ondrop={handleDrop}
  ondragover={handleDragOver}
  ondragleave={handleLeave}
/>