<script lang="ts">

    import { onMount } from 'svelte';

    import { page } from '$app/state';

    import ProposalHeader
    from '$lib/components/proposals/ProposalHeader.svelte';

    import ProposalLineItemsTable
    from '$lib/components/proposals/ProposalLineItemsTable.svelte';

    import ProposalSummarySidebar
    from '$lib/components/proposals/ProposalSummarySidebar.svelte';

    import ProposalLineItemsToolbar
    from '$lib/components/proposals/ProposalLineItemsToolbar.svelte';

    import AddLineItemModal
    from '$lib/components/proposals/AddLineItemModal.svelte';

    import {
        proposal,
        proposalLineItems,
        proposalTotals
    } from '$lib/stores/proposal.store';

    import {
        getProposal,
        getProposalLineItems,
        getProposalTotals
    } from '$lib/api/crm/proposals';

    let loading = $state(true);

    let addModalOpen =
        $state(false);

    const proposalId =
        page.params.id;

    async function loadProposalWorkspace() {

        loading = true;

        try {

            const [
                proposalData,
                lineItems,
                totals
            ] = await Promise.all([

                getProposal(
                    proposalId
                ),

                getProposalLineItems(
                    proposalId
                ),

                getProposalTotals(
                    proposalId
                )
            ]);

            proposal.set(
                proposalData
            );

            proposalLineItems.set(
                lineItems
            );

            proposalTotals.set(
                totals
            );

        } catch (e) {

            console.error(e);

        } finally {

            loading = false;
        }
    }

    async function handleItemCreated() {

        await loadProposalWorkspace();

        addModalOpen = false;
    }

    onMount(() => {

        loadProposalWorkspace();
    });

</script>

{#if loading}

<div
    class="
        min-h-screen
        bg-black
        text-white
        flex
        items-center
        justify-center
    "
>
    Loading proposal workspace...
</div>

{:else}

<div
    class="
        min-h-screen
        bg-black
        text-white
    "
>

    <div
        class="
            max-w-[1600px]
            mx-auto
            p-6
        "
    >

        <div
            class="
                grid
                grid-cols-[1fr_380px]
                gap-6
            "
        >

            <!-- LEFT -->

            <div class="space-y-6">

                <ProposalHeader />

                <ProposalLineItemsToolbar
                    onAdd={() =>
                        addModalOpen = true
                    }
                />

                <ProposalLineItemsTable
                    proposalId={proposalId}
                />

            </div>

            <!-- RIGHT -->

            <div>

                <ProposalSummarySidebar />

            </div>

        </div>

    </div>

</div>

<AddLineItemModal
    proposalId={proposalId}
    open={addModalOpen}
    onCreated={handleItemCreated}
/>

{/if}