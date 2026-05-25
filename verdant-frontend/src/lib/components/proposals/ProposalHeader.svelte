<script lang="ts">
    import ProposalAutosaveBadge
    from './ProposalAutosaveBadge.svelte';
    import {
        proposal
    } from '$lib/stores/proposal.store';
    
</script>

<div
    class="
        rounded-2xl
        border
        border-gray-800
        bg-gray-950
        p-6
    "
>

    <div
        class="
            flex
            items-start
            justify-between
            gap-6
        "
    >

        <div>

            <div
                class="
                    text-xs
                    uppercase
                    tracking-[0.2em]
                    text-gray-500
                    mb-2
                "
            >
                Proposal
            </div>

            <h1
                class="
                    text-3xl
                    font-bold
                "
            >
                {$proposal?.proposal_number}
            </h1>

            <div
                class="
                    mt-3
                    flex
                    items-center
                    gap-3
                    flex-wrap
                "
            >

                <div
                    class="
                        text-lg
                        text-gray-300
                    "
                >
                    {$proposal?.title}
                </div>

                <div
                    class="
                        px-3
                        py-1
                        rounded-full
                        bg-emerald-500/20
                        border
                        border-emerald-500/30
                        text-emerald-400
                        text-xs
                        uppercase
                    "
                >
                    {$proposal?.status}
                </div>

                <div
                    class="
                        text-sm
                        text-gray-500
                    "
                >
                    Valid Until
                    {$proposal?.valid_until}
                </div>

            </div>

        </div>

        <ProposalAutosaveBadge />

    </div>

</div>