<script lang="ts">

    let {

        title = '',

        subtitle = ''
    } = $props();

</script>

<div
    class="border-b border-gray-200 dark:border-gray-800 px-6 py-4"
>

    <h2
        class="text-xl font-semibold text-gray-900 dark:text-white"
    >
        {title}
    </h2>

    {#if subtitle}

    <p
        class="mt-1 text-sm text-gray-500"
    >
        {subtitle}
    </p>

    {/if}

</div>