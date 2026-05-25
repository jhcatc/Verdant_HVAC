<script lang="ts">

    import { onMount } from 'svelte';
    import { page } from '$app/state';
    import { goto } from '$app/navigation';
    import api from '$lib/api/client';
    let loading = $state(true);
    let error = $state('');
    let lead = $state<any>(null);
    async function loadLead() {

        loading = true;
        error = '';
        try {

            const res = await api.get(
                `/crm/leads/${page.params.id}`
            );

            lead = res.data;

        } catch (e: any) {

            console.error(e);
            error =
                e?.response?.data?.detail ||
                'Failed loading lead';

        } finally {

            loading = false;
        }
    }

    onMount(async () => {

        await loadLead();
    });

</script>

<div class="p-6 max-w-6xl mx-auto">

    {#if loading}

        <div class="text-gray-400">
            Loading lead...
        </div>

    {:else if error}

        <div
            class="
                rounded-2xl
                border
                border-red-500/30
                bg-red-500/10
                p-4
                text-red-400
            "
        >
            {error}
        </div>

    {:else if lead}

        <div class="space-y-6">

            <div
                class="
                    flex
                    items-center
                    justify-between
                "
            >

                <div>

                    <h1
                        class="
                            text-3xl
                            font-bold
                            text-white
                        "
                    >
                        {lead.company}
                    </h1>

                    <p
                        class="
                            text-sm
                            text-gray-400
                            mt-2
                        "
                    >
                        {lead.title}
                    </p>

                </div>

                <button
                    onclick={() =>
                        goto('/app/crm/leads')
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

            <div
                class="
                    grid
                    grid-cols-1
                    md:grid-cols-2
                    xl:grid-cols-3
                    gap-4
                "
            >

                <div
                    class="
                        rounded-2xl
                        border
                        border-gray-800
                        bg-gray-900
                        p-5
                    "
                >

                    <div
                        class="
                            text-xs
                            uppercase
                            text-gray-500
                        "
                    >
                        Status
                    </div>

                    <div
                        class="
                            mt-3
                            text-2xl
                            font-bold
                            text-cyan-400
                        "
                    >
                        {lead.status}
                    </div>

                </div>

                <div
                    class="
                        rounded-2xl
                        border
                        border-gray-800
                        bg-gray-900
                        p-5
                    "
                >

                    <div
                        class="
                            text-xs
                            uppercase
                            text-gray-500
                        "
                    >
                        Estimated Value
                    </div>

                    <div
                        class="
                            mt-3
                            text-2xl
                            font-bold
                            text-emerald-400
                        "
                    >
                        ${Number(
                            lead.estimated_value || 0
                        ).toLocaleString()}
                    </div>

                </div>

                <div
                    class="
                        rounded-2xl
                        border
                        border-gray-800
                        bg-gray-900
                        p-5
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
                            text-2xl
                            font-bold
                            text-yellow-400
                        "
                    >
                        {lead.probability}%
                    </div>

                </div>

            </div>

            <div
                class="
                    rounded-2xl
                    border
                    border-gray-800
                    bg-gray-900
                    p-6
                    space-y-5
                "
            >

                <h2
                    class="
                        text-xl
                        font-semibold
                        text-white
                    "
                >
                    Lead Information
                </h2>

                <div
                    class="
                        grid
                        grid-cols-1
                        md:grid-cols-2
                        gap-5
                    "
                >

                    <div>

                        <div
                            class="
                                text-xs
                                uppercase
                                text-gray-500
                            "
                        >
                            Company
                        </div>

                        <div
                            class="
                                mt-2
                                text-white
                            "
                        >
                            {lead.company || '—'}
                        </div>

                    </div>

                    <div>

                        <div
                            class="
                                text-xs
                                uppercase
                                text-gray-500
                            "
                        >
                            Email
                        </div>

                        <div
                            class="
                                mt-2
                                text-white
                            "
                        >
                            {lead.email || '—'}
                        </div>

                    </div>

                    <div>

                        <div
                            class="
                                text-xs
                                uppercase
                                text-gray-500
                            "
                        >
                            City
                        </div>

                        <div
                            class="
                                mt-2
                                text-white
                            "
                        >
                            {lead.city || '—'}
                        </div>

                    </div>

                    <div>

                        <div
                            class="
                                text-xs
                                uppercase
                                text-gray-500
                            "
                        >
                            Source
                        </div>

                        <div
                            class="
                                mt-2
                                text-white
                            "
                        >
                            {lead.source || '—'}
                        </div>

                    </div>

                </div>

            </div>

        </div>

    {/if}

</div>