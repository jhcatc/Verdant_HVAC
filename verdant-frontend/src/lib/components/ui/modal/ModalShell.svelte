<script lang="ts">

    import {
        onMount
    } from 'svelte';

    let {

        open = false,

        width = 'max-w-2xl',

        closeOnBackdrop = true,

        onClose = () => {}
    } = $props();

    function handleBackdropClick() {

        if (!closeOnBackdrop) {
            return;
        }

        onClose();
    }

    function handleKeydown(
        event: KeyboardEvent
    ) {

        if (
            event.key === 'Escape'
        ) {

            onClose();
        }
    }

    onMount(() => {

        window.addEventListener(
            'keydown',
            handleKeydown
        );

        return () => {

            window.removeEventListener(
                'keydown',
                handleKeydown
            );
        };
    });

</script>

{#if open}

<div
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4"
    onclick={handleBackdropClick}
>

    <div
        onclick={(e) => e.stopPropagation()}
        class={`w-full ${width} rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 shadow-2xl overflow-hidden`}
    >

        <slot />

    </div>

</div>

{/if}