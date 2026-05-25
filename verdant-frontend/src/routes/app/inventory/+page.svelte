<script>
  import { onMount } from "svelte";
  import InventoryAutocomplete from "$lib/components/InventoryAutocomplete.svelte";
  import InventoryModal from "$lib/components/InventoryModal.svelte";
  import updateMaterial from "app/inventory/+page.svelte";

  let items = $state([]);
  let selectedItem = null;

  let showModal = false;
  let initialName = "";

  async function load() {
    try {
      const res = await fetch("http://127.0.0.1:8000/inventory/grid/");

      const data = await res.json();

      items = data.items ?? [];
    } catch (e) {
      console.error(e);
      items = [];
    }
  }
  onMount(load);

  function rowClass(item) {
    const stock = getTotalStock(item);

    if (stock <= 0) return "bg-red-500/20";
    if (stock < item.min_stock) return "bg-yellow-500/20";
    return "";
  }

  function getTotalStock(item) {
    return item.locations?.reduce((acc, l) => acc + l.quantity, 0) || 0;
  }

  function handleSelect(e) {
    selectedItem = e.detail;
  }

  function handleCreateFromSearch(name) {
    initialName = name;
    showModal = true;
  }

  function handleCreated() {
    showModal = false;
    load();
  }
</script>

<h1 class="text-xl font-bold mb-4">Inventory Grid</h1>

<!-- 🔍 AUTOCOMPLETE -->
<InventoryAutocomplete
    bind:selected={materials[i].name}
    on:select={(e) => updateMaterial(i, e.detail)}
/>

<!-- ➕ MODAL -->
<InventoryModal
  open={showModal}
  initialName={initialName}
  on:created={handleCreated}
  onclose={() => showModal = false}
/>

<!-- 📊 GRID -->
<table class="w-full text-left border-collapse mt-4">
  <thead>
    <tr class="border-b border-gray-600">
      <th class="p-2">Item</th>
      <th class="p-2">Stock</th>
      <th class="p-2">Min</th>
    </tr>
  </thead>

  <tbody>
    {#if items.length > 0}
      {#each items as item}
      <tr class={`border-b border-gray-700 ${rowClass(item)}`}>
        <td class="p-2">{item.name}</td>
        <td class="p-2">{getTotalStock(item)}</td>
        <td class="p-2">{item.min_stock}</td>
      </tr>
    {/each}
  {:else}
    <tr>
      <td class="p-2 text-gray-400" colspan="3">
        No data
      </td>
    </tr>
  {/if}
  </tbody>
</table>