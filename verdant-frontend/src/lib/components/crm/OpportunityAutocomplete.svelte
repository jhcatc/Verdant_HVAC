<script lang="ts">
    import api from '$lib/api/client';
    type Opportunity = {
        id: string;
        title: string;
        customer_name?: string;
        company?: string;
        stage?: string;
    };

    let {
        onSelect
    } = $props<{
        onSelect: (
            opportunity: Opportunity
        ) => void;
    }>();
    let query = $state('');
    let opportunities =
        $state<Opportunity[]>([]);
    let loading =
        $state(false);
    let open =
        $state(false);
    async function search() {
        if (query.length < 2) {
            opportunities = [];
            return;
        }
        loading = true;
        try {
            const res = await api.get(
                `/crm/opportunities/search?q=${query}`
            );
            opportunities =
                res.data;

        } catch (e) {
            console.error(e);
        } finally {
            loading = false;
        }
    }

    function selectOpportunity(
        opportunity: Opportunity
    ) {
        query = `
            ${opportunity.title}            •
            ${opportunity.customer_name || ''}
        `;
        open = false;
        opportunities = [];
        onSelect(opportunity);
    }

</script>

<div class="relative">

    <input
        bind:value={query}
        oninput={search}
        onfocus={() => open = true}
        placeholder="
            Search opportunity...
        "
        class="
            w-full
            rounded-xl
            border
            border-gray-700
            bg-gray-950
            px-4
            py-3
            text-white
        "
    />

    {#if loading}

        <div
            class="
                absolute
                right-3
                top-3
                text-xs
                text-gray-500
            "
        >
            Searching...
        </div>

    {/if}

    {#if open && opportunities.length > 0}

        <div
            class="
                absolute
                z-50
                mt-1
                w-full
                overflow-y-auto
                rounded-xl
                border
                border-gray-700
                bg-gray-900
                shadow-xl
                max-h-64
            "
        >

            {#each opportunities as opportunity}

                <button
                    type="button"
                    class="
                        w-full
                        px-4
                        py-3
                        text-left
                        hover:bg-gray-800
                    "
                    onclick={() =>
                        selectOpportunity(
                            opportunity
                        )
                    }
                >

                    <div
                        class="
                            font-medium
                            text-white
                        "
                    >
                        {opportunity.title}
                    </div>

                    <div
                        class="
                            text-xs
                            text-gray-500
                            mt-1
                        "
                    >
                        {opportunity.customer_name}
                    </div>

                </button>

            {/each}

        </div>

    {/if}

</div>