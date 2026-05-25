<script lang="ts">

    let {
        title = '',
        value = ''
    }: {
        title?: string;
        value?: string | number;
    } = $props();

</script>

<div class="card">

    <p class="text-sm text-gray-500 dark:text-gray-400">
        {title}
    </p>

    <h3 class="text-2xl font-bold mt-2">
        {value}
    </h3>

</div>