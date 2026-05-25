<script lang="ts">

    let {
        rows = 5
    } = $props();

</script>

<div class="space-y-3">

    {#each Array(rows) as _}

        <div
            class="h-14 rounded-xl bg-gray-100 dark:bg-gray-800 animate-pulse"
        ></div>

    {/each}

</div>