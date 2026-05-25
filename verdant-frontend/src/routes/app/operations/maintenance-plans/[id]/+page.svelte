<script lang="ts">

    import { onMount } from 'svelte';

    let { params } = $props();

    let loading = $state(true);

    type MaintenancePlanDetail = {
        id: string;
        name: string;
        interval: string;
        maintenance_type: string;
        equipment?: unknown[];
        tasks?: unknown[];
    };
    let plan =
        $state<MaintenancePlanDetail | null>(
            null
        );

    let error = $state('');

    let activeTab = $state('overview');

    const tabs = [
        'overview',
        'equipment',
        'tasks',
        'timeline',
        'workorders',
        'analytics'
    ];

    async function loadPlan() {

        loading = true;

        error = '';

        try {

            const response = await fetch(
                `http://localhost:8000/maintenance-plans/${params.id}`
            );

            if (!response.ok) {

                throw new Error(
                    'Failed loading maintenance plan'
                );
            }

            plan = await response.json();

        } catch (err: unknown) {

            console.error(err);

            if (err instanceof Error) {
                error = err.message;
            } else {
                error =
                    'Unknown error loading maintenance plan';
            }

        } finally {

            loading = false;
        }
    }

    function getFrequencyLabel(days: number) {

        if (days === 30) {
            return 'Monthly';
        }

        if (days === 60) {
            return 'Bi-Monthly';
        }

        if (days === 90) {
            return 'Quarterly';
        }

        if (days === 180) {
            return 'Semi-Annual';
        }

        if (days === 365) {
            return 'Annual';
        }

        return `${days} Days`;
    }

    function getCompletionRate() {

        if (!plan?.task_templates?.length) {
            return 0;
        }

        return Math.min(
            100,
            Math.round(
                (
                    plan.task_templates.length * 7
                )
            )
        );
    }

    onMount(async () => {

        await loadPlan();
    });

</script>

{#if loading}

<div class="p-8 text-gray-400">
    Loading maintenance plan...
</div>

{:else if error}

<div class="p-8 text-red-500">
    {error}
</div>

{:else if !plan}

<div class="p-8 text-gray-400">
    Maintenance plan not found
</div>

{:else}

<div class="p-6 space-y-6">

    <!-- ===================================================== -->
    <!-- HERO -->
    <!-- ===================================================== -->

    <div class="rounded-2xl border border-gray-800 bg-[#0f172a] overflow-hidden">

        <div class="p-8">

            <div class="flex items-start justify-between gap-6 flex-wrap">

                <div>

                    <div class="flex items-center gap-3 flex-wrap">

                        <h1 class="text-3xl font-bold text-white">
                            {plan.name}
                        </h1>

                        <span class="px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/20 text-emerald-400 border border-emerald-500/20">

                            {plan.active
                                ? 'ACTIVE'
                                : 'INACTIVE'}

                        </span>

                    </div>

                    <p class="mt-3 text-gray-400 max-w-3xl">

                        {plan.description || 'Preventive maintenance automation plan for HVAC assets and service execution workflow.'}

                    </p>

                </div>

                <div class="flex gap-3">

                    <button
                        class="px-5 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white transition"
                    >
                        Run PM Generator
                    </button>

                    <button
                        class="px-5 py-3 rounded-xl border border-gray-700 hover:bg-gray-800 text-white transition"
                    >
                        Edit Plan
                    </button>

                </div>

            </div>

            <!-- KPIs -->

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mt-8">

                <div class="rounded-2xl bg-[#111827] border border-gray-800 p-5">

                    <p class="text-xs uppercase tracking-wide text-gray-500">
                        Customer
                    </p>

                    <p class="mt-2 text-lg font-semibold text-white">
                        {plan.customer?.name || '-'}
                    </p>

                </div>

                <div class="rounded-2xl bg-[#111827] border border-gray-800 p-5">

                    <p class="text-xs uppercase tracking-wide text-gray-500">
                        Location
                    </p>

                    <p class="mt-2 text-lg font-semibold text-white">
                        {plan.location?.name || '-'}
                    </p>

                </div>

                <div class="rounded-2xl bg-[#111827] border border-gray-800 p-5">

                    <p class="text-xs uppercase tracking-wide text-gray-500">
                        Frequency
                    </p>

                    <p class="mt-2 text-lg font-semibold text-white">
                        {getFrequencyLabel(plan.frequency_days)}
                    </p>

                </div>

                <div class="rounded-2xl bg-[#111827] border border-gray-800 p-5">

                    <p class="text-xs uppercase tracking-wide text-gray-500">
                        Equipment
                    </p>

                    <p class="mt-2 text-lg font-semibold text-white">
                        {plan.equipment?.length || 0}
                    </p>

                </div>

                <div class="rounded-2xl bg-[#111827] border border-gray-800 p-5">

                    <p class="text-xs uppercase tracking-wide text-gray-500">
                        PM Tasks
                    </p>

                    <p class="mt-2 text-lg font-semibold text-white">
                        {plan.task_templates?.length || 0}
                    </p>

                </div>

            </div>

        </div>

    </div>

    <!-- ===================================================== -->
    <!-- TABS -->
    <!-- ===================================================== -->

    <div class="rounded-2xl border border-gray-800 bg-[#0f172a] overflow-hidden">

        <!-- TAB HEADER -->

        <div class="border-b border-gray-800 px-4">

            <div class="flex gap-2 overflow-x-auto py-4">

                {#each tabs as tab}

                    <button
                        onclick={() => activeTab = tab}
                        class={`px-5 py-2 rounded-xl text-sm capitalize transition whitespace-nowrap ${
                            activeTab === tab
                                ? 'bg-emerald-600 text-white'
                                : 'text-gray-300 hover:bg-gray-800'
                        }`}
                    >

                        {tab}

                    </button>

                {/each}

            </div>

        </div>

        <!-- ===================================================== -->
        <!-- OVERVIEW -->
        <!-- ===================================================== -->

        {#if activeTab === 'overview'}

            <div class="p-6 grid grid-cols-1 xl:grid-cols-3 gap-6">

                <!-- LEFT -->

                <div class="xl:col-span-2 space-y-6">

                    <!-- PLAN INFO -->

                    <div class="rounded-2xl border border-gray-800 bg-[#111827] p-6">

                        <h2 class="text-xl font-semibold text-white">
                            Plan Information
                        </h2>

                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">

                            <div>

                                <p class="text-xs text-gray-500 uppercase">
                                    Plan Type
                                </p>

                                <p class="mt-1 text-white font-medium">
                                    {plan.plan_type || 'preventive'}
                                </p>

                            </div>

                            <div>

                                <p class="text-xs text-gray-500 uppercase">
                                    Start Date
                                </p>

                                <p class="mt-1 text-white font-medium">
                                    {plan.start_date || '-'}
                                </p>

                            </div>

                            <div>

                                <p class="text-xs text-gray-500 uppercase">
                                    Next Run
                                </p>

                                <p class="mt-1 text-emerald-400 font-semibold">
                                    {plan.next_run_date || '-'}
                                </p>

                            </div>

                            <div>

                                <p class="text-xs text-gray-500 uppercase">
                                    Auto Generate WO
                                </p>

                                <p class="mt-1 text-white font-medium">
                                    {plan.auto_generate_work_orders
                                        ? 'Enabled'
                                        : 'Disabled'}
                                </p>

                            </div>

                        </div>

                    </div>

                    <!-- TASK SUMMARY -->

                    <div class="rounded-2xl border border-gray-800 bg-[#111827] p-6">

                        <div class="flex items-center justify-between">

                            <h2 class="text-xl font-semibold text-white">
                                PM Task Templates
                            </h2>

                            <button
                                class="text-sm text-emerald-400"
                            >
                                + Add Task
                            </button>

                        </div>

                        <div class="mt-6 space-y-3">

                            {#if !plan.task_templates?.length}

                                <div class="text-sm text-gray-500">
                                    No PM tasks configured
                                </div>

                            {/if}

                            {#each plan.task_templates || [] as task, index}

                                <div class="rounded-xl border border-gray-800 bg-[#0b1220] p-4">

                                    <div class="flex items-center justify-between gap-4">

                                        <div>

                                            <div class="flex items-center gap-3">

                                                <div class="w-8 h-8 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-sm font-bold">

                                                    {index + 1}

                                                </div>

                                                <div>

                                                    <h3 class="font-medium text-white">

                                                        {task.title}

                                                    </h3>

                                                    <p class="text-xs text-gray-500 mt-1">

                                                        {task.description || 'No description'}

                                                    </p>

                                                </div>

                                            </div>

                                        </div>

                                        <div class="text-right">

                                            <div class="text-xs text-gray-500">
                                                Required
                                            </div>

                                            <div class="text-sm text-white">
                                                {task.is_required
                                                    ? 'Yes'
                                                    : 'No'}
                                            </div>

                                        </div>

                                    </div>

                                </div>

                            {/each}

                        </div>

                    </div>

                </div>

                <!-- RIGHT -->

                <div class="space-y-6">

                    <!-- NEXT EXECUTION -->

                    <div class="rounded-2xl border border-gray-800 bg-[#111827] p-6">

                        <h2 class="text-lg font-semibold text-white">
                            Next PM Execution
                        </h2>

                        <div class="mt-6">

                            <div class="text-4xl font-bold text-emerald-400">

                                {plan.next_run_date || '--'}

                            </div>

                            <p class="mt-2 text-sm text-gray-500">

                                Next preventive maintenance generation cycle

                            </p>

                        </div>

                        <button
                            class="mt-6 w-full rounded-xl bg-emerald-600 hover:bg-emerald-700 py-3 text-white transition"
                        >
                            Generate Work Order
                        </button>

                    </div>

                    <!-- HEALTH -->

                    <div class="rounded-2xl border border-gray-800 bg-[#111827] p-6">

                        <h2 class="text-lg font-semibold text-white">
                            PM Health
                        </h2>

                        <div class="mt-6">

                            <div class="flex items-center justify-between mb-2">

                                <span class="text-sm text-gray-400">
                                    Completion Score
                                </span>

                                <span class="text-sm text-white">

                                    {getCompletionRate()}%

                                </span>

                            </div>

                            <div class="h-3 rounded-full bg-gray-800 overflow-hidden">

                                <div
                                    class="h-full bg-emerald-500"
                                    style={`width:${getCompletionRate()}%`}
                                ></div>

                            </div>

                        </div>

                        <div class="mt-6 space-y-4">

                            <div class="flex items-center justify-between">

                                <span class="text-sm text-gray-400">
                                    Active Assets
                                </span>

                                <span class="text-sm text-white">

                                    {plan.equipment?.length || 0}

                                </span>

                            </div>

                            <div class="flex items-center justify-between">

                                <span class="text-sm text-gray-400">
                                    PM Tasks
                                </span>

                                <span class="text-sm text-white">

                                    {plan.task_templates?.length || 0}

                                </span>

                            </div>

                            <div class="flex items-center justify-between">

                                <span class="text-sm text-gray-400">
                                    Recurrence
                                </span>

                                <span class="text-sm text-white">

                                    {getFrequencyLabel(plan.frequency_days)}

                                </span>

                            </div>

                        </div>

                    </div>

                </div>

            </div>

        {/if}

        <!-- ===================================================== -->
        <!-- EQUIPMENT -->
        <!-- ===================================================== -->

        {#if activeTab === 'equipment'}

            <div class="p-6">

                <div class="flex items-center justify-between mb-6">

                    <div>

                        <h2 class="text-xl font-semibold text-white">
                            Linked Equipment
                        </h2>

                        <p class="text-sm text-gray-500 mt-1">
                            Assets covered under this PM contract
                        </p>

                    </div>

                    <button
                        class="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white transition"
                    >
                        + Add Equipment
                    </button>

                </div>

                {#if !plan.equipment?.length}

                    <div class="rounded-2xl border border-gray-800 bg-[#111827] p-8 text-gray-500">

                        No linked equipment

                    </div>

                {:else}

                    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">

                        {#each plan.equipment as item}

                            <div class="rounded-2xl border border-gray-800 bg-[#111827] p-5">

                                <div class="flex items-start justify-between">

                                    <div>

                                        <h3 class="text-lg font-semibold text-white">

                                            {item.equipment?.asset_tag}

                                        </h3>

                                        <p class="text-sm text-gray-400 mt-1">

                                            {item.equipment?.brand?.name || '-'}
                                            —
                                            {item.equipment?.model || '-'}

                                        </p>

                                    </div>

                                    <div class="w-3 h-3 rounded-full bg-emerald-500"></div>

                                </div>

                                <div class="mt-6 space-y-3 text-sm">

                                    <div class="flex items-center justify-between">

                                        <span class="text-gray-500">
                                            Serial
                                        </span>

                                        <span class="text-white">

                                            {item.equipment?.serial_number || '-'}

                                        </span>

                                    </div>

                                    <div class="flex items-center justify-between">

                                        <span class="text-gray-500">
                                            Status
                                        </span>

                                        <span class="text-white">

                                            {item.equipment?.status?.name || '-'}

                                        </span>

                                    </div>

                                </div>

                                <button
                                    class="mt-6 w-full rounded-xl border border-gray-700 hover:bg-gray-800 py-3 text-white transition"
                                >
                                    Open Equipment
                                </button>

                            </div>

                        {/each}

                    </div>

                {/if}

            </div>

        {/if}

        <!-- ===================================================== -->
        <!-- TASKS -->
        <!-- ===================================================== -->

        {#if activeTab === 'tasks'}

            <div class="p-6">

                <div class="rounded-2xl border border-gray-800 overflow-hidden">

                    <table class="w-full text-sm">

                        <thead class="bg-[#111827]">

                            <tr>

                                <th class="text-left p-4 text-gray-400">
                                    Task
                                </th>

                                <th class="text-left p-4 text-gray-400">
                                    Description
                                </th>

                                <th class="text-left p-4 text-gray-400">
                                    Required
                                </th>

                                <th class="text-left p-4 text-gray-400">
                                    Estimated Time
                                </th>

                            </tr>

                        </thead>

                        <tbody>

                            {#each plan.task_templates || [] as task}

                                <tr class="border-t border-gray-800 bg-[#0f172a]">

                                    <td class="p-4 text-white">
                                        {task.title}
                                    </td>

                                    <td class="p-4 text-gray-400">
                                        {task.description || '-'}
                                    </td>

                                    <td class="p-4 text-white">
                                        {task.is_required
                                            ? 'Required'
                                            : 'Optional'}
                                    </td>

                                    <td class="p-4 text-white">
                                        {task.estimated_minutes || '-'}
                                    </td>

                                </tr>

                            {/each}

                        </tbody>

                    </table>

                </div>

            </div>

        {/if}

        <!-- ===================================================== -->
        <!-- TIMELINE -->
        <!-- ===================================================== -->

        {#if activeTab === 'timeline'}

            <div class="p-6">

                <div class="rounded-2xl border border-gray-800 bg-[#111827] p-8">

                    <h2 class="text-xl font-semibold text-white">
                        PM Recurrence Timeline
                    </h2>

                    <p class="mt-2 text-gray-500">
                        Future PM execution engine timeline
                    </p>

                    <div class="mt-10 space-y-6">

                        <div class="flex items-start gap-4">

                            <div class="w-4 h-4 rounded-full bg-emerald-500 mt-1"></div>

                            <div>

                                <h3 class="text-white font-medium">
                                    Current PM Cycle
                                </h3>

                                <p class="text-sm text-gray-500 mt-1">
                                    Active recurring preventive maintenance plan
                                </p>

                            </div>

                        </div>

                        <div class="flex items-start gap-4">

                            <div class="w-4 h-4 rounded-full bg-blue-500 mt-1"></div>

                            <div>

                                <h3 class="text-white font-medium">
                                    Next Scheduled Generation
                                </h3>

                                <p class="text-sm text-gray-500 mt-1">

                                    {plan.next_run_date || '-'}

                                </p>

                            </div>

                        </div>

                        <div class="flex items-start gap-4">

                            <div class="w-4 h-4 rounded-full bg-yellow-500 mt-1"></div>

                            <div>

                                <h3 class="text-white font-medium">
                                    Auto Work Order Creation
                                </h3>

                                <p class="text-sm text-gray-500 mt-1">

                                    PM engine generates service orders automatically

                                </p>

                            </div>

                        </div>

                    </div>

                </div>

            </div>

        {/if}

        <!-- ===================================================== -->
        <!-- WORK ORDERS -->
        <!-- ===================================================== -->

        {#if activeTab === 'workorders'}

            <div class="p-6">

                <div class="rounded-2xl border border-gray-800 bg-[#111827] p-8">

                    <h2 class="text-xl font-semibold text-white">
                        Generated Work Orders
                    </h2>

                    <p class="mt-2 text-gray-500">
                        Future PM generated service orders
                    </p>

                    <div class="mt-8 rounded-2xl border border-dashed border-gray-700 p-12 text-center text-gray-500">

                        PM Generator integration coming next

                    </div>

                </div>

            </div>

        {/if}

        <!-- ===================================================== -->
        <!-- ANALYTICS -->
        <!-- ===================================================== -->

        {#if activeTab === 'analytics'}

            <div class="p-6 grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-5">

                <div class="rounded-2xl border border-gray-800 bg-[#111827] p-6">

                    <p class="text-sm text-gray-500">
                        Completion Rate
                    </p>

                    <p class="mt-3 text-4xl font-bold text-white">
                        98%
                    </p>

                </div>

                <div class="rounded-2xl border border-gray-800 bg-[#111827] p-6">

                    <p class="text-sm text-gray-500">
                        Generated Orders
                    </p>

                    <p class="mt-3 text-4xl font-bold text-white">
                        24
                    </p>

                </div>

                <div class="rounded-2xl border border-gray-800 bg-[#111827] p-6">

                    <p class="text-sm text-gray-500">
                        Assets Covered
                    </p>

                    <p class="mt-3 text-4xl font-bold text-white">

                        {plan.equipment?.length || 0}

                    </p>

                </div>

                <div class="rounded-2xl border border-gray-800 bg-[#111827] p-6">

                    <p class="text-sm text-gray-500">
                        Technician Visits
                    </p>

                    <p class="mt-3 text-4xl font-bold text-white">
                        41
                    </p>

                </div>

            </div>

        {/if}

    </div>

</div>

{/if}