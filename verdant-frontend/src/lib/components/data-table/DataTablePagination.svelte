<script lang="ts">

    let {
        page = 1,
        totalPages = 1,
        onPrevious,
        onNext
    } = $props();

</script>

<div
    class="flex items-center justify-between pt-4"
>

    <p
        class="text-sm text-gray-500"
    >
        Page {page} of {totalPages}
    </p>

    <div class="flex items-center gap-2">

        <button
            onclick={onPrevious}
            disabled={page <= 1}
            class="px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-700 disabled:opacity-50"
        >
            Previous
        </button>

        <button
            onclick={onNext}
            disabled={page >= totalPages}
            class="px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-700 disabled:opacity-50"
        >
            Next
        </button>

    </div>

</div>