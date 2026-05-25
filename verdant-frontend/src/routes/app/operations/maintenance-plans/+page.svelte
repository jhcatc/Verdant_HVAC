<script lang="ts">

    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import api from '$lib/api/client';

    let loading = $state(true);

    type MaintenancePlan = {
        id: string;
        name: string;
        interval: string;
        maintenance_type: string;
        created_at?: string;
    };
    let plans =
    $state<MaintenancePlan[]>([]);

    async function load() {

        loading = true;

        try {

            const res = await api.get(
                '/maintenance-plans'
            );

            plans = res.data;

        } catch (e) {

            console.error(e);

        } finally {

            loading = false;
        }
    }

    onMount(load);

    function openPlan(id: string) {

        goto(
            `/app/operations/maintenance-plans/${id}`
        );
    }

</script>

<div class="p-6 space-y-6">

    <!-- HEADER -->

    <div class="flex items-center justify-between">

        <div>

            <h1 class="text-3xl font-bold text-white">
                Maintenance Plans
            </h1>

            <p class="text-sm text-gray-400 mt-1">
                Preventive maintenance automation engine
            </p>

        </div>

        <button
            onclick={() =>
                goto(
                    '/app/operations/maintenance-plans/create'
                )
            }
            class="bg-emerald-600 hover:bg-emerald-700 text-white px-5 py-3 rounded-xl font-medium transition"
        >
            + Create Plan
        </button>

    </div>

    <!-- KPI -->

    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">

        <div class="rounded-2xl bg-[#111827] border border-gray-800 p-5">

            <p class="text-sm text-gray-400">
                Active Plans
            </p>

            <p class="mt-2 text-3xl font-bold text-white">
                {
                    plans.filter(
                        p => p.active
                    ).length
                }
            </p>

        </div>

        <div class="rounded-2xl bg-[#111827] border border-gray-800 p-5">

            <p class="text-sm text-gray-400">
                Equipment Covered
            </p>

            <p class="mt-2 text-3xl font-bold text-white">

                {
                    plans.reduce(
                        (
                            acc,
                            p
                        ) =>
                            acc +
                            (
                                p.equipment?.length || 0
                            ),
                        0
                    )
                }

            </p>

        </div>

        <div class="rounded-2xl bg-[#111827] border border-gray-800 p-5">

            <p class="text-sm text-gray-400">
                Auto Generated
            </p>

            <p class="mt-2 text-3xl font-bold text-white">

                {
                    plans.filter(
                        p =>
                            p.auto_generate_work_orders
                    ).length
                }

            </p>

        </div>

        <div class="rounded-2xl bg-[#111827] border border-gray-800 p-5">

            <p class="text-sm text-gray-400">
                PM Templates
            </p>

            <p class="mt-2 text-3xl font-bold text-white">

                {
                    plans.reduce(
                        (
                            acc,
                            p
                        ) =>
                            acc +
                            (
                                p.task_templates?.length || 0
                            ),
                        0
                    )
                }

            </p>

        </div>

    </div>

    <!-- TABLE -->

    <div class="rounded-2xl overflow-hidden border border-gray-800 bg-[#111827]">

        <table class="w-full text-sm">

            <thead class="bg-[#1f2937]">

                <tr>

                    <th class="text-left p-4 text-gray-300">
                        Plan
                    </th>

                    <th class="text-left p-4 text-gray-300">
                        Customer
                    </th>

                    <th class="text-left p-4 text-gray-300">
                        Location
                    </th>

                    <th class="text-left p-4 text-gray-300">
                        Frequency
                    </th>

                    <th class="text-left p-4 text-gray-300">
                        Equipment
                    </th>

                    <th class="text-left p-4 text-gray-300">
                        Next Run
                    </th>

                    <th class="text-left p-4 text-gray-300">
                        Status
                    </th>

                </tr>

            </thead>

            <tbody>

                {#if loading}

                    <tr>

                        <td colspan="7" class="p-6 text-gray-500">

                            Loading plans...

                        </td>

                    </tr>

                {:else if plans.length === 0}

                    <tr>

                        <td colspan="7" class="p-6 text-gray-500">

                            No maintenance plans found.

                        </td>

                    </tr>

                {:else}

                    {#each plans as plan}

                        <tr
                            onclick={() =>
                                openPlan(plan.id)
                            }
                            class="border-t border-gray-800 hover:bg-[#1f2937] cursor-pointer transition"
                        >

                            <td class="p-4">

                                <div>

                                    <div class="font-semibold text-white">
                                        {plan.name}
                                    </div>

                                    <div class="text-xs text-gray-500 mt-1">
                                        {plan.plan_type}
                                    </div>

                                </div>

                            </td>

                            <td class="p-4 text-gray-300">

                                {plan.customer?.name}

                            </td>

                            <td class="p-4 text-gray-300">

                                {plan.location?.name}

                            </td>

                            <td class="p-4 text-gray-300">

                                Every
                                {plan.frequency_days}
                                days

                            </td>

                            <td class="p-4 text-gray-300">

                                {
                                    plan.equipment?.length || 0
                                }

                            </td>

                            <td class="p-4 text-gray-300">

                                {plan.next_run_date || '-'}

                            </td>

                            <td class="p-4">

                                {#if plan.active}

                                    <span class="px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-400 text-xs">
                                        ACTIVE
                                    </span>

                                {:else}

                                    <span class="px-3 py-1 rounded-full bg-red-500/20 text-red-400 text-xs">
                                        INACTIVE
                                    </span>

                                {/if}

                            </td>

                        </tr>

                    {/each}

                {/if}

            </tbody>

        </table>

    </div>

</div>