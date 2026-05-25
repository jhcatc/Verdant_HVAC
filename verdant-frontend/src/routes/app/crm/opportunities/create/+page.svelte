<script lang="ts">

    import { goto } from '$app/navigation';

    import {
        createOpportunity
    } from '$lib/api/crm/opportunities';

    import CustomerAutocomplete
        from '$lib/components/customer/CustomerAutocomplete.svelte';

    import type {
        OpportunityCreate
    } from '$lib/types/crm';

    let loading = $state(false);

    let error = $state<string | null>(null);

    // =====================================================
    // CUSTOMER
    // =====================================================

    let customer_id = $state('');

    let customer_name = $state('');

    // =====================================================
    // FORM
    // =====================================================

    let title = $state('');

    let stage = $state('DISCOVERY');

    let estimated_value = $state<number>(0);

    let probability = $state<number>(25);

    let close_date = $state('');

    let notes = $state('');

    // =====================================================
    // CUSTOMER SELECT
    // =====================================================

    function handleCustomerSelect(customer: any) {

        customer_id = customer.id;

        customer_name = customer.name;
    }

    // =====================================================
    // SUBMIT
    // =====================================================

    async function submit() {

        error = null;

        if (!customer_id) {

            error = 'Customer is required';

            return;
        }

        if (!title) {

            error = 'Opportunity title required';

            return;
        }

        loading = true;

        try {

            const payload: OpportunityCreate = {

                customer_id,

                title,

                stage,

                estimated_value,

                probability,

                close_date:
                    close_date || null,

                notes:
                    notes || null
            };

            await createOpportunity(
                payload
            );

            goto(
                '/app/crm/opportunities'
            );

        } catch (err) {

            console.error(err);

            error =
                'Failed creating opportunity';

        } finally {

            loading = false;
        }
    }

</script>

<div
    class="p-6 max-w-4xl mx-auto space-y-6"
>

    <!-- HEADER -->

    <div>

        <h1
            class="text-3xl font-bold text-white"
        >
            Create Opportunity
        </h1>

        <p
            class="text-sm text-gray-400 mt-2"
        >
            Create HVAC revenue opportunities,
            PM agreements and SLA sales pipeline.
        </p>

    </div>

    <!-- ERROR -->

    {#if error}

        <div
            class="
                rounded-xl
                border
                border-red-500/30
                bg-red-500/10
                p-4
                text-red-300
                text-sm
            "
        >
            {error}
        </div>

    {/if}

    <!-- FORM -->

    <div
        class="
            rounded-2xl
            border
            border-gray-800
            bg-gray-900
            p-6
        "
    >

        <div
            class="
                grid
                grid-cols-1
                md:grid-cols-2
                gap-5
            "
        >

            <!-- CUSTOMER ID -->

            <div>

                <label
                    class="
                        block
                        text-sm
                        text-gray-300
                        mb-2
                    "
                >
                    Customer ID
                </label>

                <input
                    readonly
                    value={customer_id}
                    class="
                        w-full
                        rounded-xl
                        border
                        border-gray-700
                        bg-gray-800
                        px-4
                        py-3
                        text-gray-300
                    "
                    placeholder="Customer selected automatically"
                />

            </div>

            <!-- CUSTOMER SEARCH -->

            <div>

                <label
                    class="
                        block
                        text-sm
                        text-gray-300
                        mb-2
                    "
                >
                    Customer
                </label>

                <CustomerAutocomplete
                    onSelect={handleCustomerSelect}
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

            <!-- TITLE -->

            <div>

                <label
                    class="
                        block
                        text-sm
                        text-gray-300
                        mb-2
                    "
                >
                    Opportunity Title
                </label>

                <input
                    bind:value={title}
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
                    placeholder="HVAC Upgrade"
                />

            </div>

            <!-- STAGE -->

            <div>

                <label
                    class="
                        block
                        text-sm
                        text-gray-300
                        mb-2
                    "
                >
                    Stage
                </label>

                <select
                    bind:value={stage}
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
                >

                    <option value="DISCOVERY">
                        DISCOVERY
                    </option>

                    <option value="QUALIFICATION">
                        QUALIFICATION
                    </option>

                    <option value="PROPOSAL">
                        PROPOSAL
                    </option>

                    <option value="NEGOTIATION">
                        NEGOTIATION
                    </option>

                </select>

            </div>

            <!-- PROBABILITY -->

            <div>

                <label
                    class="
                        block
                        text-sm
                        text-gray-300
                        mb-2
                    "
                >
                    Probability %
                </label>

                <input
                    bind:value={probability}
                    type="number"
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

            </div>

            <!-- ESTIMATED VALUE -->

            <div>

                <label
                    class="
                        block
                        text-sm
                        text-gray-300
                        mb-2
                    "
                >
                    Estimated Revenue
                </label>

                <input
                    bind:value={estimated_value}
                    type="number"
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

            </div>

            <!-- CLOSE DATE -->

            <div>

                <label
                    class="
                        block
                        text-sm
                        text-gray-300
                        mb-2
                    "
                >
                    Expected Close Date
                </label>

                <input
                    bind:value={close_date}
                    type="date"
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

            </div>

            <!-- NOTES -->

            <div class="md:col-span-2">

                <label
                    class="
                        block
                        text-sm
                        text-gray-300
                        mb-2
                    "
                >
                    Notes
                </label>

                <textarea
                    bind:value={notes}
                    rows="6"
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
                ></textarea>

            </div>

        </div>

        <!-- ACTIONS -->

        <div
            class="
                flex
                justify-end
                gap-3
                mt-8
            "
        >

            <button
                onclick={() =>
                    goto(
                        '/app/crm/opportunities'
                    )
                }
                class="
                    px-5
                    py-3
                    rounded-xl
                    border
                    border-gray-700
                    text-white
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
                "
            >
                {loading
                    ? 'Creating...'
                    : 'Create Opportunity'}
            </button>

        </div>

    </div>

</div>