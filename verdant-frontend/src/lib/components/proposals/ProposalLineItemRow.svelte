<script lang="ts">

    import { debounce }
    from 'perfect-debounce';

    import {
        proposalSaving,
        proposalLineItems,
        proposalTotals
    } from '$lib/stores/proposal.store';

    import {
        updateProposalLineItem,
        getProposalTotals
    } from '$lib/api/crm/proposals';

    let {
        item,
        proposalId
    } = $props();

    async function persist() {

        proposalSaving.set(true);

        try {

            await updateProposalLineItem(

                proposalId,

                item.id,

                {
                    description:
                        item.description,

                    qty: item.qty,

                    unit_price:
                        item.unit_price
                }
            );

            const totals =
                await getProposalTotals(
                    proposalId
                );

            proposalTotals.set(
                totals
            );

        } catch (e) {

            console.error(e);

        } finally {

            proposalSaving.set(false);
        }
    }

    const autosave =
        debounce(
            persist,
            500
        );

</script>

<div
    class="
        grid
        grid-cols-[1fr_120px_160px]
        items-center
        hover:bg-gray-950/50
    "
>

    <div class="p-4">

        <input
            bind:value={item.description}
            oninput={autosave}
            class="
                w-full
                bg-transparent
                border
                border-gray-800
                rounded-lg
                px-3
                py-2
            "
        />

    </div>

    <div class="p-4">

        <input
            type="number"
            bind:value={item.qty}
            oninput={autosave}
            class="
                w-full
                bg-transparent
                border
                border-gray-800
                rounded-lg
                px-3
                py-2
            "
        />

    </div>

    <div class="p-4">

        <input
            type="number"
            bind:value={item.unit_price}
            oninput={autosave}
            class="
                w-full
                bg-transparent
                border
                border-gray-800
                rounded-lg
                px-3
                py-2
            "
        />

    </div>

</div>