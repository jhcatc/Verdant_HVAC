<script lang="ts">
    import OrderCard from './OrderCard.svelte';

    let { title, status, orders, onDrop } = $props();

    function handleDrop(e: DragEvent) {
        e.preventDefault();

        const id = e.dataTransfer?.getData('orderId');
        if (!id) return;

        onDrop(id); // 🔥 SOLO ID
    }

    function handleDragOver(e: DragEvent) {
        e.preventDefault();
    }
</script>

<div
    class="bg-gray-100 dark:bg-gray-800 rounded-xl p-3 min-h-[400px]"
    ondragover={handleDragOver}
    ondrop={handleDrop}
>

    <h3 class="font-semibold mb-3 text-gray-900 dark:text-white">
        {title}
    </h3>

    <div class="space-y-2">
        {#each orders as o}
            <OrderCard order={o} />
        {/each}
    </div>

</div>