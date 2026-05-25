<script lang="ts">
    import { onMount } from 'svelte';
    import api from '$lib/api/client';

    let { orderId, onAssign } = $props();

    let loading = $state(true);
    let recommendations = $state([]);

    async function loadAI() {

        loading = true;

        try {

            const res = await api.get(
                `/service-orders/${orderId}/ai-dispatch`
            );

            recommendations = res.data;

        } catch (err) {

            console.error(err);

        } finally {

            loading = false;
        }
    }

    async function assign(tech) {

        const dt = new Date();

        dt.setHours(
            dt.getHours() + 1
        );

        await onAssign?.({
            technicianId: tech.technician_id,
            scheduledAt: dt.toISOString(),
            durationHours: 2
        });
    }

    onMount(loadAI);
</script>

<div class="space-y-4">

    <div class="flex items-center justify-between">

        <div>
            <h2 class="text-xl font-semibold text-white">
                AI Technician Assignment
            </h2>

            <p class="text-sm text-slate-400 mt-1">
                Smart dispatch optimization engine
            </p>
        </div>

        <div class="px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-400 text-xs">
            Enterprise AI
        </div>

    </div>

    {#if loading}

        <div class="bg-slate-900 rounded-2xl p-10 text-center text-slate-400">
            Analyzing technicians...
        </div>

    {:else}

        <div class="space-y-3">

            {#each recommendations as tech}

                <div
                    class="bg-slate-900 border border-slate-800 rounded-2xl p-5"
                >

                    <div class="flex items-start justify-between">

                        <div>

                            <div class="text-lg font-semibold text-white">
                                {tech.technician_name}
                            </div>

                            <div class="mt-2 flex flex-wrap gap-2">

                                <div class="px-2 py-1 rounded bg-blue-500/20 text-blue-300 text-xs">
                                    Distance Score:
                                    {tech.distance_score}
                                </div>

                                <div class="px-2 py-1 rounded bg-yellow-500/20 text-yellow-300 text-xs">
                                    Workload:
                                    {tech.workload_hours}h
                                </div>

                                <div class="px-2 py-1 rounded bg-purple-500/20 text-purple-300 text-xs">
                                    Regional Density:
                                    {tech.region_score}
                                </div>

                                <div class="px-2 py-1 rounded bg-emerald-500/20 text-emerald-300 text-xs">
                                    Final AI Score:
                                    {tech.final_score}
                                </div>

                            </div>

                        </div>

                        <button
                            onclick={() => assign(tech)}
                            class="bg-emerald-600 hover:bg-emerald-500 transition px-4 py-2 rounded-xl text-white font-medium"
                        >
                            Auto Assign
                        </button>

                    </div>

                </div>

            {/each}

        </div>

    {/if}

</div>