<script lang="ts">

    let {
        onAdd
    } = $props();

</script>

<div
    class="
        flex
        items-center
        gap-3
        flex-wrap
    "
>

    <button
        onclick={onAdd}
        class="
            h-11
            px-5
            rounded-xl
            bg-cyan-600
            hover:bg-cyan-700
        "
    >
        + Add Item
    </button>

    <button
        class="
            h-11
            px-5
            rounded-xl
            border
            border-gray-700
        "
    >
        Bundle
    </button>

    <button
        class="
            h-11
            px-5
            rounded-xl
            border
            border-gray-700
        "
    >
        PM Agreement
    </button>

</div>