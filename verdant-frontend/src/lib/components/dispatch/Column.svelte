<script lang="ts">
    import Card from './Card.svelte';
    
    interface ServiceOrder {
        id: string;
        title: string;
        description?: string;
        priority?: 'low' | 'medium' | 'high';
        status: string;
        assignee?: { id: string; name: string };
        created_at: string;
    }
    
    interface Column {
        id: string;
        title: string;
        color: string;
        cards: ServiceOrder[];
    }
    
    interface Props {
        column: Column;
    }
    
    let { column }: Props = $props();
</script>

<div class="flex-shrink-0 w-80 bg-gray-100 dark:bg-gray-800/50 rounded-lg p-3 flex flex-col max-h-[calc(100vh-220px)]">
    <div class="flex items-center justify-between mb-3">
        <div class="flex items-center gap-2">
            <div class="w-3 h-3 rounded-full {column.color}"></div>
            <h3 class="font-semibold text-gray-700 dark:text-gray-200">{column.title}</h3>
        </div>
        <span class="text-xs font-medium text-gray-500 dark:text-gray-400 bg-gray-200 dark:bg-gray-700 px-2 py-0.5 rounded-full">
            {column.cards.length}
        </span>
    </div>
    
    <div class="flex-1 overflow-y-auto space-y-3 pr-1">
        {#each column.cards as item (item.id)}
            <Card card={item} />
        {:else}
            <div class="text-center py-8 text-gray-400 dark:text-gray-500 text-sm">
                No items
            </div>
        {/each}
    </div>
</div>