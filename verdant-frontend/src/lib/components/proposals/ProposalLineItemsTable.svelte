<script lang="ts">

    import {
        dndzone
    } from 'svelte-dnd-action';

    import ProposalLineItemRow
    from './ProposalLineItemRow.svelte';

    import {
        proposalLineItems
    } from '$lib/stores/proposal.store';

    import {
        reorderProposalLineItems
    } from '$lib/api/crm/proposals';

    let {
        proposalId
    } = $props();

    async function handleDnd(
        e: CustomEvent
    ) {

        proposalLineItems.set(
            e.detail.items
        );

        const reordered =
            e.detail.items.map(
                (item, index) => ({
                    id: item.id,
                    sort_order: index
                })
            );

        await reorderProposalLineItems(
            proposalId,
            reordered
        );
    }

</script>

<div
    class="
        rounded-2xl
        border
        border-gray-800
        overflow-hidden
        bg-gray-950
    "
>

    <div
        class="
            grid
            grid-cols-[40px_1fr_120px_160px_120px_120px_160px_80px]
            bg-black
            border-b
            border-gray-800
            text-sm
            font-semibold
        "
    >

        <div class="p-4"></div>

        <div class="p-4">
            Description
        </div>

        <div class="p-4">
            Qty
        </div>

        <div class="p-4">
            Unit Price
        </div>

        <div class="p-4">
            Tax %
        </div>

        <div class="p-4">
            Discount %
        </div>

        <div class="p-4 text-right">
            $proposalTotals.grand_total
        </div>

        <div class="p-4"></div>

    </div>

    <div

        use:dndzone={{

            items: $proposalLineItems,

            flipDurationMs: 150
        }}

        on:consider={handleDnd}

        on:finalize={handleDnd}

        class="
            divide-y
            divide-gray-900
        "
    >

        {#each $proposalLineItems as item (item.id)}

            <ProposalLineItemRow
                {item}
                proposalId={proposalId}
            />

        {/each}

    </div>

</div>