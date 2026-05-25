<script lang="ts">
    interface ServiceOrder {
        id: string;
        title: string;
        description?: string;
        priority?: 'low' | 'medium' | 'high';
        status: string;
        assignee?: { id: string; name: string };
        created_at: string;
    }

    interface Props {
        card: ServiceOrder;
    }
    
    let { card }: Props = $props();
    
    const priorityConfig = {
        low: { label: 'Low', bg: 'bg-gray-100 dark:bg-gray-700', text: 'text-gray-600 dark:text-gray-300' },
        medium: { label: 'Medium', bg: 'bg-yellow-100 dark:bg-yellow-900', text: 'text-yellow-700 dark:text-yellow-300' },
        high: { label: 'High', bg: 'bg-red-100 dark:bg-red-900', text: 'text-red-700 dark:text-red-300' }
    };
    
    const borderColors = {
        low: 'border-green-500',
        medium: 'border-yellow-500',
        high: 'border-red-500',
        default: 'border-gray-300'
    };
    
    const prio = card.priority ?? 'default';
    const borderColor = borderColors[prio as keyof typeof borderColors] ?? borderColors.default;
    const config = priorityConfig[prio as keyof typeof priorityConfig];
</script>

<div class="bg-white dark:bg-gray-800 rounded-lg p-3 shadow-sm border-l-4 {borderColor} hover:shadow-md transition-shadow cursor-pointer">
    <h4 class="font-medium text-gray-800 dark:text-gray-100 text-sm mb-1">{card.title}</h4>
    
    {#if card.description}
        <p class="text-xs text-gray-500 dark:text-gray-400 mb-2 line-clamp-2">{card.description}</p>
    {/if}
    
    <div class="flex items-center justify-between mt-2 pt-2 border-t border-gray-100 dark:border-gray-700">
        {#if config}
            <span class="text-xs px-2 py-0.5 rounded-full {config.bg} {config.text}">
                {config.label}
            </span>
        {:else}
            <span></span>
        {/if}
        
        <div class="flex items-center gap-2">
            {#if card.assignee}
                <span class="text-xs text-gray-500 dark:text-gray-400">{card.assignee.name}</span>
            {/if}
            {#if card.created_at}
                <span class="text-xs text-gray-400 dark:text-gray-500">
                    {new Date(card.created_at).toLocaleDateString()}
                </span>
            {/if}
        </div>
    </div>
</div>