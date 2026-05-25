<script lang="ts">
  import api from '$lib/api/client';
  import { createEventDispatcher } from 'svelte';

  let { selected = $bindable(null) } = $props();

  let query = $state('');
  let results = $state([]);
  let show = $state(false);

  const dispatch = createEventDispatcher();

  let debounceTimer;

  async function search() {
    clearTimeout(debounceTimer);

    debounceTimer = setTimeout(async () => {
      if (!query) {
        results = [];
        return;
      }

      const res = await api.get(`/inventory/search?q=${query}`);
      results = res.data ?? [];
      show = true;
    }, 250); // 🔥 debounce real
  }

  function selectItem(item) {
    query = item.name;      // 🔥 ACTUALIZA INPUT
    selected = item;        // 🔥 guarda objeto completo
    dispatch('select', item);
    show = false;
  }
</script>

<div class="relative w-full">

  <input
    class="w-full border p-2 rounded"
    bind:value={query}
    oninput={search}
    onfocus={() => show = true}
  />

  {#if show && results.length > 0}
    <div class="absolute bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 w-full mt-1 rounded shadow z-10">

      {#each results as item}
      <div
          class="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer flex justify-between items-center text-gray-900 dark:text-white"
          onmousedown={(e) => {
              e.preventDefault(); // 🔥 evita perder foco
              selectItem(item);
          }}
      >
        <span>{item.name}</span>

        <span
          class={`text-xs px-2 py-1 rounded
            ${item.stock <= 0
              ? 'bg-red-500 text-white'
              : item.stock < 5
              ? 'bg-yellow-400 text-black'
              : 'bg-green-500 text-white'}
          `}
        >
          {item.stock ?? 0}
        </span>
      </div>
      {/each}

    </div>
  {/if}

</div>