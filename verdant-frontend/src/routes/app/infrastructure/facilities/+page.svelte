<script lang="ts">

    import { onMount } from 'svelte';

    import { goto } from '$app/navigation';

    let facilities = $state([]);

    let loading = $state(true);

    async function load() {

        try {

            const res =
                await fetch(
                    '/api/hvac/facilities'
                );

            facilities =
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
            Facilities
        </h1>

        <p class="text-sm text-gray-400 mt-1">
            Infrastructure locations and operational health.
        </p>

    </div>

    {#if loading}

        <div class="rounded-2xl border border-gray-800 bg-gray-900 p-8">
            Loading facilities...
        </div>

    {:else}

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">

            {#each facilities as facility}

                <button
                    onclick={() =>
                        goto(`/app/infrastructure/facilities/${facility.id}`)
                    }
                    class="rounded-2xl border border-gray-800 bg-gray-900 p-5 text-left hover:border-emerald-500 transition"
                >

                    <div class="text-lg font-semibold text-white">
                        {facility.name}
                    </div>

                    <div class="text-sm text-gray-400 mt-2">
                        {facility.city}
                    </div>

                    <div class="mt-4 text-xs text-emerald-400">
                        {facility.total_equipment}
                        assets
                    </div>

                </button>

            {/each}

        </div>

    {/if}

</div>