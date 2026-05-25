<script lang="ts">

    let tickets = $state([]);

    async function run() {

        const res = await fetch('/api/anomalies/run', {
            method: 'POST'
        });

        const data = await res.json();

        tickets = data.tickets;
    }

</script>

<div  class="space-y-6 p-6">

    <h1 class="text-3xl font-bold text-white">
        HVAC Anomalies
    </h1>

    <button
        onclick={run}
        class="px-4 py-2 bg-emerald-600 text-white rounded-xl"
    >
        Run Detection
    </button>

    <div class="space-y-3">

        {#each tickets as t}

            <div class="p-4 rounded-xl border border-gray-700 bg-gray-900">

                <div class="flex justify-between">

                    <div class="font-bold text-white">
                        {t.title}
                    </div>

                    <span class="text-xs px-2 py-1 rounded bg-red-600 text-white">
                        {t.severity}
                    </span>

                </div>

                <div class="text-sm text-gray-400 mt-2">
                    {t.description}
                </div>

                <div class="text-xs text-gray-500 mt-2">
                    Equipment: {t.equipment_id}
                </div>

            </div>

        {/each}

    </div>

</div>