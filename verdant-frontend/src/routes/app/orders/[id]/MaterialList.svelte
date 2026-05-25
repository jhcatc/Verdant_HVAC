<script lang="ts">
    let { materials } = $props();

    const total = $derived(
        materials?.reduce(
            (sum, m) => sum + (m.quantity * m.unit_cost),
            0
        ) ?? 0
    );
</script>

<div class="card">

    <h2 class="font-semibold mb-4">Materials</h2>

    {#if !materials || materials.length === 0}
        <p class="text-gray-400 text-sm">No materials</p>
    {/if}

    <div class="space-y-2">

        {#each materials as m}
        <div class="flex justify-between text-sm">
            <span>{m.name}</span>
            <span>
                {m.quantity} × ${m.unit_cost}
            </span>
        </div>
        {/each}

    </div>

    <div class="border-t mt-4 pt-3 flex justify-between font-semibold">
        <span>Total</span>
        <span>${total.toFixed(2)}</span>
    </div>

</div>