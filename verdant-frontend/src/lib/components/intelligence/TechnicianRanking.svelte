<script lang="ts">
    let { list = [] } = $props();
</script>

<div class="bg-slate-900 p-4 rounded-lg text-white">
    <h2 class="text-lg font-semibold mb-3">Technician Performance</h2>

    <div class="space-y-2">
        {#each list as tech}
            <div class="flex justify-between bg-slate-800 p-2 rounded">
                <span>{tech.name}</span>

                <div class="text-right text-sm text-gray-300">
                    <div>Orders: {tech.completed_orders}</div>
                    <div>{tech.avg_resolution_time_hours}h avg</div>
                </div>
            </div>
        {/each}
    </div>
</div>