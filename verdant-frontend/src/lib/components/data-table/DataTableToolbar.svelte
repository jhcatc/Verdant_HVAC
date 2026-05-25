<script lang="ts">

    let {
        title = '',
        search = '',
        placeholder = 'Search...',
        onSearch
    } = $props();

</script>

<div
    class="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-5"
>

    <div>

        <h2
            class="text-lg font-semibold text-gray-900 dark:text-white"
        >
            {title}
        </h2>

    </div>

    <div class="w-full md:w-80">

        <input
            value={search}
            oninput={(e) =>
                onSearch?.(
                    (e.target as HTMLInputElement).value
                )
            }
            placeholder={placeholder}
            class="w-full px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900"
        />

    </div>

</div>