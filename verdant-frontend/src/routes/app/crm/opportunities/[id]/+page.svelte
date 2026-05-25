<script lang="ts">

    import { onMount } from 'svelte';
    import { page } from '$app/state';
    import { goto } from '$app/navigation';
    import {
        getOpportunity
    } from '$lib/api/crm/opportunities';
    import type {
        Opportunity
    } from '$lib/types/crm';

    let loading = $state(true);

    let error = $state('');

    let opportunity =
        $state<Opportunity | null>(null);

    const id =
        page.params.id;

    async function loadOpportunity() {

        loading = true;
        error = '';

        try {

            opportunity =
                await getOpportunity(id);

        } catch (err) {

            console.error(err);

            error =
                'Failed loading opportunity';

        } finally {

            loading = false;
        }
    }

    onMount(async () => {

        await loadOpportunity();
    });

</script>

<div class="p-6 space-y-6">

    {#if loading}

        <div class="text-gray-400">
            Loading opportunity...
        </div>

    {:else if error}

        <div class="text-red-400">
            {error}
        </div>

    {:else if opportunity}

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
                    flex
                    items-start
                    justify-between
                "
            >

                <div>


                    <p
                        class="
                            text-gray-400
                            mt-2
                        "
                    >
                        {opportunity.customer_name}
                    </p>

                </div>

                <div>

                    <h1
                        class="
                            text-3xl
                            font-bold
                            text-white
                        "
                    >
                        {opportunity.title}
                    </h1>


                </div>

                <span
                    class="
                        px-3
                        py-2
                        rounded-xl
                        bg-cyan-500/20
                        text-cyan-400
                        text-sm
                    "
                >
                    {opportunity.stage}
                </span>

                <button
                    onclick={() =>
                        goto('/app/crm/opportunities')
                    }
                    class="
                        px-4
                        py-2
                        rounded-xl
                        border
                        border-gray-700
                        hover:bg-gray-800
                        transition
                        text-white
                    "
                >
                    Back
                </button>

            </div>

        </div>

        <div
            class="
                grid
                grid-cols-1
                md:grid-cols-3
                gap-6
            "
        >

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
                        text-xs
                        uppercase
                        text-gray-500
                    "
                >
                    Forecast Revenue
                </div>

                <div
                    class="
                        mt-3
                        text-3xl
                        font-bold
                        text-emerald-400
                    "
                >
                    ${Number(
                        opportunity.estimated_value || 0
                    ).toLocaleString()}
                </div>

            </div>

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
                        text-xs
                        uppercase
                        text-gray-500
                    "
                >
                    Probability
                </div>

                <div
                    class="
                        mt-3
                        text-3xl
                        font-bold
                        text-cyan-400
                    "
                >
                    {opportunity.probability || 0}%
                </div>

            </div>

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
                        text-xs
                        uppercase
                        text-gray-500
                    "
                >
                    Expected Close
                </div>

                <div
                    class="
                        mt-3
                        text-2xl
                        font-bold
                        text-white
                    "
                >
                    {opportunity.close_date
                        ? new Date(
                            opportunity.close_date
                        ).toLocaleDateString()
                        : '—'}
                </div>

            </div>

        </div>

    {/if}

</div>