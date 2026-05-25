<script lang="ts">
    let { order } = $props();

    function drag(e: DragEvent) {
        e.dataTransfer?.setData('orderId', order.id);
    }
</script>

<div
    role="button"
    draggable="true"
    ondragstart={drag}
    class="card cursor-grab active:cursor-grabbing hover:shadow-md transition border border-gray-200 dark:border-gray-700"
>
    <div class="flex items-start justify-between">

        <div>

            <h3 class="font-medium text-sm text-gray-900 dark:text-white">
                {order.title}
            </h3>

            <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                {order.customer?.name ?? 'No customer'}
            </p>

        </div>

        <div
            class="text-[10px] px-2 py-1 rounded-full
            {order.priority === 'urgent'
                ? 'bg-red-100 text-red-700'
                : order.priority === 'high'
                ? 'bg-orange-100 text-orange-700'
                : 'bg-gray-100 text-gray-700'}"
        >
            {order.priority ?? 'medium'}
        </div>

    </div>

    <div class="grid grid-cols-2 gap-2 mt-4 text-[11px] text-gray-500">

        <div>
            ⏱ {order.duration_hours ?? 1}h
        </div>

        <div>
            📍 {order.city ?? 'N/A'}
        </div>

        <div>
            🧰 {order.equipment?.name ?? 'No equipment'}
        </div>

        <div>
            💰 ${order.actual_cost ?? 0}
        </div>

    </div>

</div>