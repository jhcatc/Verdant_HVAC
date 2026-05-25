<script lang="ts">

    import { goto } from '$app/navigation';

    import { page } from '$app/state';

    import {
        createProposal
    } from '$lib/api/crm/proposals';

    import CustomerAutocomplete
        from '$lib/components/customer/CustomerAutocomplete.svelte';

    import OpportunityAutocomplete
        from '$lib/components/crm/OpportunityAutocomplete.svelte';

    let loading = $state(false);

    let error = $state('');

    const mode =
        page.url.searchParams.get('mode')
        || 'pipeline';

    let customer_id = $state('');

    let customer_name = $state('');

    let opportunity_id = $state('');

    let opportunity_label = $state('');

    let title = $state('');

    let amount =
        $state<number | null>(null);

    let valid_until = $state('');

    // =====================================================
    // SUBMIT
    // =====================================================

    async function submit() {

        error = '';

        if (!customer_id) {

            error =
                'Customer required';

            return;
        }

        if (!title) {

            error =
                'Proposal title required';

            return;
        }

        if (
            mode === 'pipeline'
            &&
            !opportunity_id
        ) {

            error =
                'Opportunity required';

            return;
        }

        loading = true;

        try {

            await createProposal({

                customer_id,

                opportunity_id:

                    mode === 'pipeline'
                        ? opportunity_id
                        : null,

                title,

                amount:
                    amount || 0,

                valid_until
            });

            goto(
                '/app/crm/proposals'
            );

        } catch (e) {

            console.error(e);

            error =
                'Failed creating proposal';

        } finally {

            loading = false;
        }
    }

</script>

<div class="p-6 max-w-4xl mx-auto space-y-6">

    <!-- HEADER -->

    <div class="mb-8">

        <div
            class="
                inline-flex
                items-center
                px-3
                py-1
                rounded-lg
                bg-gray-800
                text-gray-300
                text-xs
                mb-4
            "
        >
            {mode === 'pipeline'
                ? 'PIPELINE PROPOSAL'
                : 'DIRECT CUSTOMER PROPOSAL'}
        </div>

        <h1
            class="text-3xl font-bold text-white"
        >
            Create Proposal
        </h1>

        <p
            class="text-sm text-gray-400 mt-2"
        >
            HVAC quotation workflow and
            commercial proposal management.
        </p>

    </div>

    <!-- FORM -->

    <div
        class="
            rounded-2xl
            border
            border-gray-800
            bg-gray-900
            p-6
            space-y-6
        "
    >

        {#if error}

            <div
                class="
                    rounded-xl
                    border
                    border-red-500/30
                    bg-red-500/10
                    p-4
                    text-red-400
                "
            >
                {error}
            </div>

        {/if}

        <!-- CUSTOMER -->

        <div>

            <label
                class="
                    text-sm
                    font-medium
                    block
                    mb-2
                    text-white
                "
            >
                Customer
            </label>

            <CustomerAutocomplete

                placeholder="
                    Search customer by name...
                "

                showEmail={true}

                onSelect={(customer) => {

                    customer_id =
                        customer.id;

                    customer_name =
                        customer.name;
                }}
            />

            {#if customer_name}

                <div
                    class="
                        mt-2
                        text-xs
                        text-emerald-400
                    "
                >
                    Selected:
                    {customer_name}
                </div>

            {/if}

        </div>

        <!-- OPPORTUNITY -->

        {#if mode === 'pipeline'}

            <div>

                <label
                    class="
                        text-sm
                        font-medium
                        block
                        mb-2
                        text-white
                    "
                >
                    Opportunity
                </label>

                <OpportunityAutocomplete

                    onSelect={(opportunity) => {

                        opportunity_id =
                            opportunity.id;

                        opportunity_label =
                            opportunity.title;
                    }}
                />

                {#if opportunity_label}

                    <div
                        class="
                            mt-2
                            text-xs
                            text-cyan-400
                        "
                    >
                        Selected:
                        {opportunity_label}
                    </div>

                {/if}

            </div>

        {/if}

        <!-- TITLE -->

        <div>

            <label
                class="
                    text-sm
                    font-medium
                    block
                    mb-2
                    text-white
                "
            >
                Proposal Title
            </label>

            <input
                bind:value={title}
                placeholder="
                    VRF System Upgrade
                "
                class="
                    w-full
                    px-4
                    py-3
                    rounded-xl
                    border
                    border-gray-700
                    bg-gray-950
                    text-white
                "
            />

        </div>

        <!-- AMOUNT -->

        <div>

            <label
                class="
                    text-sm
                    font-medium
                    block
                    mb-2
                    text-white
                "
            >
                Proposal Amount
            </label>

            <input
                type="number"
                bind:value={amount}
                placeholder="0.00"
                class="
                    w-full
                    px-4
                    py-3
                    rounded-xl
                    border
                    border-gray-700
                    bg-gray-950
                    text-white
                "
            />

        </div>

        <!-- VALID UNTIL -->

        <div>

            <label
                class="
                    text-sm
                    font-medium
                    block
                    mb-2
                    text-white
                "
            >
                Valid Until
            </label>

            <input
                type="date"
                bind:value={valid_until}
                class="
                    w-full
                    px-4
                    py-3
                    rounded-xl
                    border
                    border-gray-700
                    bg-gray-950
                    text-white
                "
            />

        </div>

        <!-- ACTIONS -->

        <div
            class="
                flex
                justify-end
                gap-3
                pt-4
            "
        >

            <button
                onclick={() =>
                    goto('/app/crm/proposals')
                }
                class="
                    px-5
                    py-3
                    rounded-xl
                    border
                    border-gray-700
                    text-white
                    hover:bg-gray-800
                    transition
                "
            >
                Cancel
            </button>

            <button
                onclick={submit}
                disabled={loading}
                class="
                    px-5
                    py-3
                    rounded-xl
                    bg-emerald-600
                    hover:bg-emerald-700
                    disabled:opacity-50
                    text-white
                    transition
                "
            >
                {loading
                    ? 'Creating...'
                    : 'Create Proposal'}
            </button>

        </div>

    </div>

</div>