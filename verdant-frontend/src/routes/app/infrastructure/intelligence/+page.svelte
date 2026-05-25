<script lang="ts">

    import { onMount } from 'svelte';

    import {
        getIntelligenceSnapshot,
        getCorrelationSnapshot,
        getVisualSnapshot
    } from '$lib/api/intelligence';

    import InfrastructureKpiCard
    from '$lib/components/infrastructure/InfrastructureKpiCard.svelte';

    let snapshot = $state(null);

    let correlations = $state(null);

    let visual = $state(null);

    let loading = $state(true);

    async function load() {

        try {

            const [
                intelligence,
                correlation,
                visualSnapshot
            ] = await Promise.all([

                getIntelligenceSnapshot(),
                getCorrelationSnapshot(),
                getVisualSnapshot()
            ]);

            snapshot = intelligence;

            correlations = correlation;

            visual = visualSnapshot;

        } finally {

            loading = false;
        }
    }

    onMount(load);

</script>

<div class="space-y-6 p-6">

    <div>

        <h1
            class="text-3xl font-bold text-white"
        >
            Infrastructure Intelligence
        </h1>

        <p
            class="text-sm text-gray-400 mt-1"
        >
            Enterprise HVAC operational intelligence,
            risk concentration and infrastructure health.
        </p>

    </div>

    {#if loading}

        <div
            class="rounded-2xl border border-gray-800 bg-gray-900 p-8"
        >
            Loading intelligence...
        </div>

    {:else}

        <!-- KPIs -->

        <div
            class="grid grid-cols-1 md:grid-cols-4 gap-4"
        >

            <InfrastructureKpiCard
                title="Critical Equipment"
                value={snapshot.critical_equipment}
                color="red"
            />

            <InfrastructureKpiCard
                title="Failure Risk"
                value={`${snapshot.failure_risk_score}%`}
                color="orange"
            />

            <InfrastructureKpiCard
                title="Infrastructure Health"
                value={`${snapshot.health_score}%`}
                color="emerald"
            />

            <InfrastructureKpiCard
                title="Facilities"
                value={snapshot.total_facilities}
                color="blue"
            />

        </div>

        <!-- VISUAL -->

        <div
            class="rounded-2xl border border-gray-800 bg-gray-900 p-6"
        >

            <h2
                class="text-xl font-semibold text-white"
            >
                Visual Intelligence
            </h2>

            <div
                class="mt-6 grid grid-cols-2 md:grid-cols-4 gap-4"
            >

                {#each visual.facilities as facility}

                    <div
                        class="rounded-xl border border-gray-800 bg-gray-950 p-4"
                    >

                        <div
                            class="text-sm text-gray-400"
                        >
                            {facility.name}
                        </div>

                        <div
                            class="text-2xl font-bold text-white mt-2"
                        >
                            {facility.health_score}%
                        </div>

                    </div>

                {/each}

            </div>

        </div>

        <!-- CORRELATIONS -->

        <div
            class="rounded-2xl border border-gray-800 bg-gray-900 p-6"
        >

            <h2
                class="text-xl font-semibold text-white"
            >
                Failure Correlations
            </h2>

            <div
                class="mt-6 space-y-3"
            >

                {#each correlations.items as item}

                    <div
                        class="rounded-xl border border-gray-800 bg-gray-950 p-4"
                    >

                        <div
                            class="flex items-center justify-between"
                        >

                            <div
                                class="font-medium text-white"
                            >
                                {item.label}
                            </div>

                            <div
                                class="text-sm text-emerald-400"
                            >
                                {item.score}%
                            </div>

                        </div>

                    </div>

                {/each}

            </div>

        </div>

    {/if}

</div>