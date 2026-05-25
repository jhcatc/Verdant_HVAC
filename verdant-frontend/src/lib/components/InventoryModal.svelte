<script lang="ts">
  import { createEventDispatcher } from 'svelte';

  let { open, initialName } = $props();

  const dispatch = createEventDispatcher();

  let name = $state(initialName ?? '');
  let sku = $state(""); // 🔥 NUEVO
  let category = $state('material');
  let unit_cost = $state(0);
  let stock = $state(0);
  let loading = $state(false);

  async function createItem() {
    loading = true;

    const res = await fetch('http://127.0.0.1:8000/inventory/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name,
        sku, // 🔥 enviado
        category,
        unit_cost,
        stock
      })
    });

    const item = await res.json();

    dispatch('created', item);
    loading = false;
  }
</script>

{#if open}
<div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">

  <div class="bg-white dark:bg-gray-900 rounded-xl shadow-xl w-full max-w-md p-6">

    <h2 class="text-xl font-bold mb-4 text-gray-900 dark:text-white">
      Create New Item
    </h2>

    <!-- NAME -->
    <div class="mb-3">
      <label class="block text-sm mb-1">Item Name</label>
      <input class="w-full border rounded p-2" bind:value={name} />
    </div>

    <!-- SKU 🔥 -->
    <div class="mb-3">
      <label class="block text-sm mb-1">SKU</label>
      <input class="w-full border rounded p-2" bind:value={sku} />
    </div>

    <!-- CATEGORY -->
    <div class="mb-3">
      <select class="w-full border rounded p-2" bind:value={category}>
        <option value="material">Material</option>
        <option value="tool">Tool</option>
        <option value="equipment">Equipment</option>
        <option value="spare_part">Spare Part</option>
      </select>
    </div>

    <!-- COST -->
    <div class="mb-3">
      <input type="number" class="w-full border rounded p-2" bind:value={unit_cost} />
      Coast
    </div>

    <!-- STOCK -->
    <div class="mb-4">
      <input type="number" class="w-full border rounded p-2" bind:value={stock} />
      Stock
    </div>

    <div class="flex justify-end gap-2">
      <button onclick={() => dispatch('close')}>Cancel</button>

      <button onclick={createItem} disabled={loading}>
        {loading ? 'Creating...' : 'Create'}
      </button>
    </div>

  </div>
</div>
{/if}