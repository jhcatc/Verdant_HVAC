<script lang="ts">

    import ModalShell
    from './ModalShell.svelte';

    import ModalHeader
    from './ModalHeader.svelte';

    import ModalFooter
    from './ModalFooter.svelte';

    let {

        open = false,

        title = 'Confirm Action',

        message = 'Are you sure?',

        confirmText = 'Confirm',

        cancelText = 'Cancel',

        onConfirm,

        onCancel
    } = $props();

</script>

<ModalShell
    {open}
    width="max-w-md"
>

    <ModalHeader
        {title}
    />

    <div
        class="px-6 py-5"
    >

        <p
            class="text-sm text-gray-600 dark:text-gray-300"
        >
            {message}
        </p>

    </div>

    <ModalFooter>

        <button
            onclick={onCancel}
            class="px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700"
        >
            {cancelText}
        </button>

        <button
            onclick={onConfirm}
            class="px-4 py-2 rounded-xl bg-red-600 hover:bg-red-700 text-white"
        >
            {confirmText}
        </button>

    </ModalFooter>

</ModalShell>