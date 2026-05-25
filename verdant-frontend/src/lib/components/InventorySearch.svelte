<script>
  import { createEventDispatcher } from "svelte";

  let query = "";
  let results = [];
  let show = false;

  const dispatch = createEventDispatcher();

  async function search() {
    if (!query) {
      results = [];
      return;
    }

    const res = await fetch(`http://127.0.0.1:8000/inventory?q=${query}`);
    results = await res.json();

    show = true;
  }

  function select(item) {
    show = false;
    dispatch("select", item);
  }

  function createNew() {
    show = false;
    dispatch("create", { name: query });
  }
</script>

<div class="relative w-full">
  <input
    class="w-full p-2 border rounded bg-gray-900"
    placeholder="Search item..."
    bind:value={query}
    oninput={search}
    onfocus={() => (show = true)}
  />

  {#if show}
    <div class="absolute w-full bg-gray-800 border mt-1 rounded shadow-lg z-10">
      
      {#if results.length > 0}
        {#each results as item}
          <div
            class="p-2 hover:bg-gray-700 cursor-pointer"
            onclick={() => select(item)}
          >
            {item.name}
          </div>
        {/each}
      {:else}
        <div
          class="p-2 text-green-400 hover:bg-gray-700 cursor-pointer"
          onclick={createNew}
        >
          + Create "{query}"
        </div>
      {/if}

    </div>
  {/if}
</div>