<script lang="ts">
    export let data: unknown;

    const actions = [
        "Review high-risk customers",
        "Reassign overloaded technicians",
        "Inspect repeated failure assets",
        "Validate SLA breaches"
    ];
</script>

<div class="bg-slate-900 p-4 rounded-lg text-white">
    <h2 class="text-lg font-semibold mb-3">Next Best Actions (Manual)</h2>

    <div class="space-y-2">
        {#each actions as a}
            <button class="w-full text-left p-2 bg-slate-800 rounded hover:bg-slate-700">
                {a}
            </button>
        {/each}
    </div>
</div>