<script lang="ts">

    import { onMount } from 'svelte';

    import {
        getEquipmentCatalog
    } from '$lib/api/crm/equipment-catalog';

    import {
        createProposalLineItem
    } from '$lib/api/crm/proposals';

    let loading = $state(false);
    let search = $state('');
    let catalog = $state([]);
    let {
        proposalId,
        open = false,
        onCreated
    } = $props();

    async function loadCatalog() {

        loading = true;

        try {

            catalog =
                await getEquipmentCatalog(
                    search
                );

        } finally {

            loading = false;
        }
    }

    async function addEquipment(
        equipment
    ) {

        await createProposalLineItem(
            proposalId,
            {
                item_type: 'equipment',

                description:
                    equipment.name,

                qty: 1,

                unit_price:
                    equipment.equipment_price,

                unit_cost:
                    equipment.equipment_cost,

                tax_percent: 0,

                discount_percent: 0
            }
        );

        await onCreated?.();
    }

    onMount(loadCatalog);

</script>

{#if open}

<div
    class="
        fixed
        inset-0
        z-50
        bg-black/70
        backdrop-blur-sm
        flex
        items-center
        justify-center
    "
>

    <div
        class="
            w-[1100px]
            h-[700px]
            rounded-2xl
            border
            border-gray-800
            bg-gray-950
            overflow-hidden
            flex
            flex-col
        "
    >

        <!-- HEADER -->

        <div
            class="
                p-6
                border-b
                border-gray-800
            "
        >

            <div
                class="
                    text-2xl
                    font-bold
                "
            >
                Add Proposal Item
            </div>

            <div
                class="
                    text-sm
                    text-gray-500
                    mt-2
                "
            >
                Equipment Catalog · Bundles · PM Agreements
            </div>

        </div>

        <!-- SEARCH -->

        <div class="p-6">

            <input
                bind:value={search}

                oninput={loadCatalog}

                placeholder="
                    Search equipment...
                "

                class="
                    w-full
                    h-12
                    rounded-xl
                    border
                    border-gray-800
                    bg-black
                    px-4
                "
            />

        </div>

        <!-- TABLE -->

        <div
            class="
                flex-1
                overflow-auto
                px-6
                pb-6
            "
        >

            <div class="space-y-3">

                {#each catalog as item}

                    <button

                        onclick={() =>
                            addEquipment(item)
                        }

                        class="
                            w-full
                            rounded-xl
                            border
                            border-gray-800
                            bg-black
                            p-5
                            text-left
                            hover:border-cyan-500
                            transition
                        "
                    >

                        <div
                            class="
                                flex
                                justify-between
                            "
                        >

                            <div>

                                <div
                                    class="
                                        font-semibold
                                    "
                                >
                                    {item.name}
                                </div>

                                <div
                                    class="
                                        text-sm
                                        text-gray-500
                                        mt-1
                                    "
                                >
                                    {item.manufacturer}
                                    ·
                                    {item.model_number}
                                </div>

                            </div>

                            <div
                                class="
                                    text-right
                                "
                            >

                                <div
                                    class="
                                        text-cyan-400
                                        font-bold
                                    "
                                >
                                    $
                                    {
                                        item.equipment_price
                                            .toLocaleString()
                                    }
                                </div>

                            </div>

                        </div>

                    </button>

                {/each}

            </div>

        </div>

    </div>

</div>

{/if}