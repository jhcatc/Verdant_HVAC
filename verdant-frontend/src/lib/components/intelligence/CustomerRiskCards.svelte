<script lang="ts">
    let { list = [] } = $props();
</script>

<div class="bg-slate-900 p-4 rounded-lg text-white">
    <h2 class="text-lg font-semibold mb-3">Customer Risk</h2>

    <div class="grid gap-2">

        {#each list as c}
            <div class="flex justify-between p-3 rounded bg-slate-800">

                <div>
                    <div class="font-medium">
                        Customer {c.customer_id}
                    </div>

                    <div class="text-xs text-gray-400">
                        Orders: {c.total_orders}
                    </div>
                </div>

                <div class="text-right">
                    <div class="text-sm font-bold"
                        class:text-red-400={c.satisfaction_score < 60}
                        class:text-yellow-400={c.satisfaction_score >= 60 && c.satisfaction_score < 80}
                        class:text-green-400={c.satisfaction_score >= 80}
                    >
                        {c.satisfaction_score}
                    </div>

                    <div class="text-xs text-gray-400">
                        Risk Score
                    </div>
                </div>

            </div>
        {/each}

    </div>
</div>