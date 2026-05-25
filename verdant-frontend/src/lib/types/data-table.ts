import type { Snippet } from 'svelte';

export type DataTableAlign =
    | 'left'
    | 'center'
    | 'right';

export type DataTableColumn<T> = {

    key: keyof T | string;
    label: string;
    width?: string;
    align?: DataTableAlign;
    sortable?: boolean;
    searchable?: boolean;
    className?: string;

    render?: (
        row: T
    ) =>
        | string
        | number
        | boolean
        | null
        | undefined;

    snippet?: Snippet<[T]>;
};

export type PaginationState = {

    page: number;
    page_size: number;
    total: number;
};

export type DataTableFilter = {

    key: string;
    label: string;
    value: string;
};

export type DataTableSort<T> = {

    key: keyof T | string;

    direction:
        | 'asc'
        | 'desc';
};

export type DataTableAction<T> = {

    label: string;

    icon?: string;

    variant?:
        | 'default'
        | 'danger'
        | 'success'
        | 'warning';

    disabled?: (
        row: T
    ) => boolean;

    hidden?: (
        row: T
    ) => boolean;

    loading?: boolean;

    onClick: (
        row: T
    ) => void | Promise<void>;
};