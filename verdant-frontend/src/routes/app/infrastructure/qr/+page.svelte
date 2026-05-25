<script lang="ts">

    import { onMount } from 'svelte';

    let equipment = $state([]);

    let loading = $state(true);

    async function load() {

        try {

            const res =
                await fetch(
                    '/api/hvac/equipment'
                );

            equipment =
                await res.json();

        } finally {

            loading = false;
        }
    }

    onMount(load);

</script>

<div class="space-y-6 p-6">

    <div>

        <h1 class="text-3xl font-bold text-white">
            QR Registry
        </h1>

        <p class="text-sm text-gray-400 mt-1">
            Equipment traceability and field technician access.
        </p>

    </div>

    {#if loading}

        <div class="rounded-2xl border border-gray-800 bg-gray-900 p-8">
            Loading QR registry...
        </div>

    {:else}

        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">

            {#each equipment as item}

                <div
                    class="rounded-2xl border border-gray-800 bg-gray-900 p-4"
                >

                    <div class="text-sm text-gray-400">
                        {item.asset_tag}
                    </div>

                    <img
                        src={`http://localhost:8000/api/equipment-qr/${item.id}`}
                        alt="QR"
                        class="w-full mt-4"
                    />

                </div>

            {/each}

        </div>

    {/if}

</div>