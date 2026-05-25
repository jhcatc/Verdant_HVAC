<script lang="ts" generics="T">

    import type {
        DataTableColumn,
        DataTableAction,
        DataTableSort
    } from '$lib/types/data-table';

    import DataTableEmpty
    from './DataTableEmpty.svelte';

    import DataTableLoading
    from './DataTableLoading.svelte';

    import DataTableRowActions
    from './DataTableRowActions.svelte';

    let {

        columns,
        rows,
        loading = false,
        emptyTitle = 'No records found',
        emptyDescription = '',
        rowActions = [],
        sort,
        onSort

    } = $props<{

        columns: DataTableColumn<T>[];
        rows: T[];
        loading?: boolean;
        emptyTitle?: string;
        emptyDescription?: string;
        rowActions?: DataTableAction<T>[];
        sort?: DataTableSort<T> | null;
        onSort?: (
            column: DataTableColumn<T>
        ) => void;
    }>();

    function getAlignmentClass(
        align?: string
    ) {

        if (align === 'center') {
            return 'text-center';
        }

        if (align === 'right') {
            return 'text-right';
        }

        return 'text-left';
    }

    function isSorted(
        column: DataTableColumn<T>
    ) {

        return (
            sort &&
            sort.key === column.key
        );
    }

</script>

{#if loading}

<DataTableLoading />

{:else if rows.length === 0}

<DataTableEmpty
    title={emptyTitle}
    description={emptyDescription}
/>

{:else}

<div
    class="overflow-hidden rounded-2xl border border-gray-200 dark:border-gray-800"
>

    <div
        class="overflow-x-auto"
    >

        <table
            class="w-full text-sm"
        >

            <thead
                class="bg-gray-100 dark:bg-gray-800"
            >

                <tr>

                    {#each columns as column}

                        <th
                            class={`p-4 font-semibold whitespace-nowrap ${getAlignmentClass(column.align)}`}
                            style={`width:${column.width ?? 'auto'}`}
                        >

                            <button
                                type="button"
                                class={`inline-flex items-center gap-2 ${
                                    column.sortable
                                    ? 'hover:text-emerald-600 transition'
                                    : ''
                                }`}
                                onclick={() =>
                                    column.sortable &&
                                    onSort?.(column)
                                }
                            >

                                <span>
                                    {column.label}
                                </span>

                                {#if isSorted(column)}

                                    <span
                                        class="text-xs"
                                    >
                                        {sort?.direction === 'asc'
                                            ? '↑'
                                            : '↓'}
                                    </span>

                                {/if}

                            </button>

                        </th>

                    {/each}

                    {#if rowActions.length}

                        <th
                            class="p-4 text-right"
                        >
                            Actions
                        </th>

                    {/if}

                </tr>

            </thead>

            <tbody>

                {#each rows as row}

                    <tr
                        class="border-t border-gray-200 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-900/40 transition"
                    >

                        {#each columns as column}

                            <td
                                class={`p-4 whitespace-nowrap ${
                                    getAlignmentClass(column.align)
                                } ${
                                    column.className ?? ''
                                }`}
                            >

                                {#if column.snippet}

                                    {@render column.snippet(row)}

                                {:else if column.render}

                                    {column.render(row)}

                                {:else}

                                    {String(
                                        row[
                                            column.key as keyof T
                                        ] ?? ''
                                    )}

                                {/if}

                            </td>

                        {/each}

                        {#if rowActions.length}

                            <td
                                class="p-4 text-right"
                            >

                                <DataTableRowActions
                                    row={row}
                                    actions={rowActions}
                                />

                            </td>

                        {/if}

                    </tr>

                {/each}

            </tbody>

        </table>

    </div>

</div>

{/if}