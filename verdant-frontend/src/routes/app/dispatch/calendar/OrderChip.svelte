<script lang="ts">
  import dayjs from "dayjs";

  let { order } = $props();

  const START_HOUR = 8;
  const SLOT_HEIGHT = 48; // px por 15 min

  function handleDragStart(e: DragEvent) {
    e.dataTransfer?.setData("application/json", JSON.stringify(order));
  }

  const bg =
    order.status === "pending"
      ? "bg-gray-500"
      : order.status === "assigned"
      ? "bg-blue-500"
      : order.status === "in_progress"
      ? "bg-yellow-500"
      : "bg-green-600";

  function calculateTop() {
    if (!order.scheduled_at) {
      return 0;
    }

    const start = dayjs(order.scheduled_at);

    const minutes =
      (start.hour() - START_HOUR) * 60 +
      start.minute();

    return (minutes / 15) * SLOT_HEIGHT;
  }

  function calculateHeight() {
    const duration = Number(order.duration_hours || 1);

    return duration * 4 * SLOT_HEIGHT;
  }

  const top = calculateTop();
  const height = calculateHeight();
</script>

<div
  role="button"
  draggable="true"
  ondragstart={handleDragStart}
  class="absolute left-1 right-1 rounded-xl p-2 text-white shadow-lg cursor-grab active:cursor-grabbing overflow-hidden border border-white/10 {bg}"
  style="
    top: {top}px;
    height: {height}px;
    z-index: 20;
  "
>
  <div class="flex flex-col h-full">

    <!-- TITLE -->
    <div class="font-semibold text-sm truncate">
      {order.title}
    </div>

    <!-- CUSTOMER -->
    <div class="text-xs opacity-80 truncate mt-1">
      {order.customer?.name ?? 'No customer'}
    </div>

    <!-- TIME -->
    <div class="mt-auto text-[11px] opacity-80 pt-2">
      {dayjs(order.scheduled_at).format('HH:mm')}
      ·
      {order.duration_hours ?? 1}h
    </div>

  </div>
</div>