<script lang="ts">

    import { onMount } from 'svelte';

    type EquipmentIntelligence = {

        health_score: number;

        maintenance_frequency: number;

        anomaly_risk: string;

        predicted_failure?: string;

        refrigerant_events: number;

        component_failures: number;

        recent_failures: {
            component: string;
            date: string;
            severity: string;
        }[];
    };

    let {
        equipmentId
    } = $props<{
        equipmentId: string;
    }>();

    let loading = $state(true);

    let intelligence =
        $state<EquipmentIntelligence | null>(null);

    async function load() {

        try {

            loading = true;

            const res = await fetch(
                `/api/hvac/equipment/${equipmentId}/intelligence`
            );

            if (!res.ok) {

                throw new Error(
                    'Failed equipment intelligence'
                );
            }

            intelligence = await res.json();

        } finally {

            loading = false;
        }
    }

    onMount(load);

</script>

<div
    class="rounded-2xl border border-gray-800 bg-gray-900 p-6 space-y-6"
>

    <div>

        <h2
            class="text-2xl font-bold text-white"
        >
            Asset Intelligence
        </h2>

        <p
            class="text-sm text-gray-400 mt-1"
        >
            Predictive maintenance and equipment health intelligence.
        </p>

    </div>

    {#if loading}

        <div
            class="rounded-xl border border-gray-800 p-6 text-gray-400"
        >
            Loading intelligence...
        </div>

    {:else if intelligence}

        <div
            class="grid grid-cols-1 md:grid-cols-3 gap-4"
        >

            <div
                class="rounded-xl border border-gray-800 bg-gray-950 p-5"
            >
                <div class="text-sm text-gray-400">
                    Health Score
                </div>

                <div
                    class="text-4xl font-bold text-emerald-500 mt-2"
                >
                    {intelligence.health_score}%
                </div>
            </div>

            <div
                class="rounded-xl border border-gray-800 bg-gray-950 p-5"
            >
                <div class="text-sm text-gray-400">
                    Maintenance Frequency
                </div>

                <div
                    class="text-4xl font-bold text-cyan-400 mt-2"
                >
                    {intelligence.maintenance_frequency}
                </div>

                <div
                    class="text-xs text-gray-500 mt-1"
                >
                    logs / year
                </div>
            </div>

            <div
                class="rounded-xl border border-gray-800 bg-gray-950 p-5"
            >
                <div class="text-sm text-gray-400">
                    Anomaly Risk
                </div>

                <div
                    class="text-4xl font-bold text-red-500 mt-2"
                >
                    {intelligence.anomaly_risk}
                </div>
            </div>

        </div>

        <div
            class="grid grid-cols-1 md:grid-cols-2 gap-4"
        >

            <div
                class="rounded-xl border border-gray-800 bg-gray-950 p-5"
            >

                <div class="text-sm text-gray-400">
                    Component Failures
                </div>

                <div
                    class="text-3xl font-bold text-orange-400 mt-2"
                >
                    {intelligence.component_failures}
                </div>

            </div>

            <div
                class="rounded-xl border border-gray-800 bg-gray-950 p-5"
            >

                <div class="text-sm text-gray-400">
                    Refrigerant Events
                </div>

                <div
                    class="text-3xl font-bold text-blue-400 mt-2"
                >
                    {intelligence.refrigerant_events}
                </div>

            </div>

        </div>

        <div
            class="rounded-xl border border-gray-800 bg-gray-950 p-5"
        >

            <div
                class="text-sm text-gray-400"
            >
                Predicted Failure
            </div>

            <div
                class="text-xl font-semibold text-yellow-400 mt-2"
            >
                {intelligence.predicted_failure ?? 'No prediction'}
            </div>

        </div>

        <div
            class="rounded-xl border border-gray-800 overflow-hidden"
        >

            <div
                class="px-5 py-4 border-b border-gray-800 bg-gray-950"
            >
                <h3
                    class="text-lg font-semibold text-white"
                >
                    Recent Failures
                </h3>
            </div>

            <table class="w-full">

                <thead
                    class="bg-gray-950"
                >
                    <tr>

                        <th
                            class="px-4 py-3 text-left text-xs uppercase text-gray-500"
                        >
                            Component
                        </th>

                        <th
                            class="px-4 py-3 text-left text-xs uppercase text-gray-500"
                        >
                            Date
                        </th>

                        <th
                            class="px-4 py-3 text-left text-xs uppercase text-gray-500"
                        >
                            Severity
                        </th>

                    </tr>
                </thead>

                <tbody>

                    {#each intelligence.recent_failures as failure}

                        <tr
                            class="border-t border-gray-800"
                        >

                            <td
                                class="px-4 py-3 text-white"
                            >
                                {failure.component}
                            </td>

                            <td
                                class="px-4 py-3 text-gray-300"
                            >
                                {failure.date}
                            </td>

                            <td
                                class="px-4 py-3"
                            >

                                <span
                                    class="px-2 py-1 rounded-lg bg-red-600 text-white text-xs"
                                >
                                    {failure.severity}
                                </span>

                            </td>

                        </tr>

                    {/each}

                </tbody>

            </table>

        </div>

    {/if}

</div>