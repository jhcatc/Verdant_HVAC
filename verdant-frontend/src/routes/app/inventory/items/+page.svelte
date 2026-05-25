<script lang="ts">
  import { onMount } from 'svelte';
  import api from '$lib/api/client';
  import InventoryModal from '$lib/components/InventoryModal.svelte';

  let items = $state([]);
  let total = $state(0);

  let query = $state('');
  let loading = $state(false);

  let showModal = $state(false);
  let initialName = $state("");

  // 🔥 PAGINATION STATE
  let page = $state(1);
  let limit = 20;

    // 🔥 PAGINATION LOGIC
  let totalPages = $derived(Math.ceil(total / limit));

  // 🔥 LOAD DATA
  async function load() {
    loading = true;

    try {
      const offset = (page - 1) * limit;

      const res = await api.get('/inventory/', {
        params: {
          q: query || undefined,
          limit,
          offset
        }
      });

      items = res.data.items ?? [];
      total = res.data.total ?? 0;

    } finally {
      loading = false;
    }
  }

  onMount(load);

  // 🔥 SEARCH
  function search() {
    page = 1; // reset page
    load();
  }

  // 🔥 CREATE
  function openCreate() {
    initialName = query || "";
    showModal = true;
  }

  function handleCreated() {
    showModal = false;
    load();
  }

  // 🔥 HELPERS
  function rowClass(item) {
    if (item.stock <= 0) return "bg-red-500/20";
    if (item.stock < item.min_stock) return "bg-yellow-500/20";
    return "";
  }


 

  function nextPage() {
    if (page < totalPages) {
      page++;
      load();
    }
  }

  function prevPage() {
    if (page > 1) {
      page--;
      load();
    }
  }
</script>

<h1 class="text-xl font-bold mb-4">Inventory Items</h1>

<!-- 🔍 SEARCH + BUTTON -->
<div class="flex gap-2 mb-4">

  <input
    class="flex-1 border p-2 rounded"
    placeholder="Search item..."
    bind:value={query}
    oninput={search}
  />

  <button
    class="bg-blue-600 text-white px-4 rounded"
    onclick={openCreate}
  >
    + New Item
  </button>

</div>

<!-- ➕ MODAL -->
<InventoryModal
  open={showModal}
  initialName={initialName}
  on:created={handleCreated}
  on:close={() => showModal = false}
/>

<!-- 📊 GRID -->
{#if loading}
  <p>Loading...</p>

{:else}

  <table class="w-full text-sm border-collapse">

    <thead class="bg-gray-800 text-white">
      <tr>
        <th class="p-2 text-left">Name</th>
        <th class="p-2 text-left">SKU</th>
        <th class="p-2 text-left">Category</th>
        <th class="p-2 text-right">Stock</th>
        <th class="p-2 text-right">Cost</th>
      </tr>
    </thead>

    <tbody>

      {#if items.length > 0}

        {#each items as item}
          <tr class={`border-b ${rowClass(item)}`}>
            <td class="p-2">{item.name}</td>
            <td class="p-2">{item.sku || "-"}</td>
            <td class="p-2">{item.category}</td>
            <td class="p-2 text-right">{item.stock}</td>
            <td class="p-2 text-right">{item.unit_cost}</td>
          </tr>
        {/each}

      {:else}

        <tr>
          <td colspan="5" class="p-4 text-center text-gray-500">
            No results
          </td>
        </tr>

      {/if}

    </tbody>

  </table>

  <!-- 🔥 PAGINATION UI -->
  <div class="flex justify-between items-center mt-4">

    <button
      class="px-3 py-1 bg-gray-300 rounded"
      onclick={prevPage}
      disabled={page === 1}
    >
      Prev
    </button>

    <span>
      Page {page} / {totalPages}
    </span>

    <button
      class="px-3 py-1 bg-gray-300 rounded"
      onclick={nextPage}
      disabled={page === totalPages}
    >
      Next
    </button>

  </div>

{/if}