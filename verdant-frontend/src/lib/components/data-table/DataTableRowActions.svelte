<script lang="ts" generics="T">

    import type {
        DataTableAction
    } from '$lib/types/data-table';

    let {
        row,
        actions = []
    } = $props<{

        row: T;

        actions: DataTableAction<T>[];
    }>();

    function getVariantClass(
        variant?: string
    ) {

        switch (variant) {

            case 'danger':
                return `
                    bg-red-100
                    text-red-700
                    hover:bg-red-200
                `;

            case 'success':
                return `
                    bg-emerald-100
                    text-emerald-700
                    hover:bg-emerald-200
                `;

            case 'warning':
                return `
                    bg-amber-100
                    text-amber-700
                    hover:bg-amber-200
                `;

            default:
                return `
                    bg-gray-100
                    dark:bg-gray-800
                    hover:bg-gray-200
                    dark:hover:bg-gray-700
                `;
        }
    }

</script>

<div
    class="flex items-center justify-end gap-2"
>

    {#each actions as action}

        {#if !action.hidden?.(row)}

            <button
                onclick={() =>
                    action.onClick(row)
                }
                disabled={
                    action.disabled?.(row)
                }
                class={`
                    px-3
                    py-1
                    rounded-lg
                    text-sm
                    transition
                    disabled:opacity-50
                    disabled:cursor-not-allowed
                    ${getVariantClass(
                        action.variant
                    )}
                `}
            >

                {action.label}

            </button>

        {/if}

    {/each}

</div>