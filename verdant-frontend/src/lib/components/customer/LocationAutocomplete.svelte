<script lang="ts">

    type Location = {
        id: string;
        name: string;
        city?: string;
    };

    let {
        locations = [],
        onSelect
    } = $props();

    let query = $state('');

    let open = $state(false);

    $effect(() => {

        if (!query) {
            return;
        }
    });

    function filteredLocations() {

        return locations.filter((location: Location) =>
            location.name
                .toLowerCase()
                .includes(query.toLowerCase())
        );
    }

    function selectLocation(location: Location) {

        query = location.name;

        open = false;

        onSelect(location);
    }

</script>

<div class="relative">

    <input
        bind:value={query}
        onfocus={() => open = true}
        placeholder="Search location..."
        class="w-full border rounded p-2 bg-white dark:bg-gray-800"
    />

    {#if open}

        <div class="absolute z-50 mt-1 w-full rounded border bg-white dark:bg-gray-900 shadow-lg max-h-64 overflow-y-auto">

            {#each filteredLocations() as location}

                <button
                    type="button"
                    class="w-full text-left px-3 py-2 hover:bg-gray-100 dark:hover:bg-gray-800"
                    onclick={() => selectLocation(location)}
                >

                    <div class="font-medium">
                        {location.name}
                    </div>

                    <div class="text-xs text-gray-500">
                        {location.city || '—'}
                    </div>

                </button>

            {/each}

        </div>

    {/if}

</div>