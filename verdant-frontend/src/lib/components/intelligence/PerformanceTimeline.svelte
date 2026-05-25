<script lang="ts">
    let { list = [] } = $props();
</script>

<div class="bg-slate-900 p-4 rounded-lg text-white">
    <h2 class="text-lg font-semibold mb-3">Repair Time Trends</h2>

    <div class="space-y-2">

        {#each list as item}
            <div class="flex justify-between bg-slate-800 p-2 rounded">

                <span>{item.status}</span>

                <span class="text-gray-300">
                    {item.avg_repair_time_hours}h
                </span>

            </div>
        {/each}

    </div>
</div>