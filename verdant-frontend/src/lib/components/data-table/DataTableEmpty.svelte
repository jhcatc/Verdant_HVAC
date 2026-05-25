<script lang="ts">

    let {
        title = 'No data found',
        description = ''
    } = $props();

</script>

<div
    class="rounded-2xl border border-dashed border-gray-300 dark:border-gray-700 p-10 text-center"
>

    <h3
        class="text-lg font-semibold text-gray-800 dark:text-white"
    >
        {title}
    </h3>

    {#if description}

        <p
            class="mt-2 text-sm text-gray-500"
        >
            {description}
        </p>

    {/if}

</div>