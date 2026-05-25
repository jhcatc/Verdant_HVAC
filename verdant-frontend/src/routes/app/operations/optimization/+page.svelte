<!--
FILE:
C:\Users\jhcat\Documents\Verdant_HVAC\verdant-frontend\src\routes\app\operations\optimization\+page.svelte
-->

<script lang="ts">
    const engines = [
        {
            name: 'Technician Assignment AI',
            description:
                'Auto technician selection, workload balancing and smart dispatch orchestration.',
            status: 'Active',
            health: '98%',
            color: 'emerald'
        },

        {
            name: 'Route Optimization Engine',
            description:
                'Traffic-aware routing, stop sequencing and travel minimization.',
            status: 'Active',
            health: '94%',
            color: 'blue'
        },

        {
            name: 'Enterprise Scheduling Engine',
            description:
                'Recurring PM waves, blackout windows and AI rebalance.',
            status: 'Active',
            health: '96%',
            color: 'purple'
        },

        {
            name: 'SLA Engine',
            description:
                'SLA breach detection, escalation workflows and compliance scoring.',
            status: 'Monitoring',
            health: '91%',
            color: 'orange'
        },

        {
            name: 'PM Forecasting',
            description:
                'Seasonal PM forecasting and predictive maintenance orchestration.',
            status: 'Learning',
            health: '87%',
            color: 'yellow'
        },

        {
            name: 'Capacity Planning',
            description:
                'Technician utilization and operational capacity simulation.',
            status: 'Active',
            health: '95%',
            color: 'cyan'
        }
    ];

    function badgeClasses(color: string) {
        switch (color) {
            case 'emerald':
                return 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300';

            case 'blue':
                return 'bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-300';

            case 'purple':
                return 'bg-purple-100 text-purple-700 dark:bg-purple-900/40 dark:text-purple-300';

            case 'orange':
                return 'bg-orange-100 text-orange-700 dark:bg-orange-900/40 dark:text-orange-300';

            case 'yellow':
                return 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/40 dark:text-yellow-300';

            case 'cyan':
                return 'bg-cyan-100 text-cyan-700 dark:bg-cyan-900/40 dark:text-cyan-300';

            default:
                return 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300';
        }
    }

    function borderClasses(color: string) {
        switch (color) {
            case 'emerald':
                return 'hover:border-emerald-500';

            case 'blue':
                return 'hover:border-blue-500';

            case 'purple':
                return 'hover:border-purple-500';

            case 'orange':
                return 'hover:border-orange-500';

            case 'yellow':
                return 'hover:border-yellow-500';

            case 'cyan':
                return 'hover:border-cyan-500';

            default:
                return 'hover:border-gray-500';
        }
    }
</script>

<div class="space-y-6">

    <!-- HEADER -->
    <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">

        <div>
            <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
                Optimization Center
            </h1>

            <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
                Central orchestration for enterprise optimization engines.
            </p>
        </div>

        <div class="flex items-center gap-3">

            <button
                class="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-medium transition"
            >
                Run AI Rebalance
            </button>

            <button
                class="px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-800 text-sm transition"
            >
                Refresh Engines
            </button>

        </div>

    </div>

    <!-- KPI ROW -->
    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">

        <div class="rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-5">
            <div class="text-sm text-gray-500 dark:text-gray-400">
                Optimization Score
            </div>

            <div class="text-3xl font-bold text-emerald-600 mt-2">
                94%
            </div>
        </div>

        <div class="rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-5">
            <div class="text-sm text-gray-500 dark:text-gray-400">
                Travel Reduction
            </div>

            <div class="text-3xl font-bold text-blue-600 mt-2">
                -21%
            </div>
        </div>

        <div class="rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-5">
            <div class="text-sm text-gray-500 dark:text-gray-400">
                SLA Protection
            </div>

            <div class="text-3xl font-bold text-orange-600 mt-2">
                97%
            </div>
        </div>

        <div class="rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-5">
            <div class="text-sm text-gray-500 dark:text-gray-400">
                AI Dispatch Success
            </div>

            <div class="text-3xl font-bold text-purple-600 mt-2">
                93%
            </div>
        </div>

    </div>

    <!-- ENGINE GRID -->
    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">

        {#each engines as engine}

            <div
                class="
                    rounded-2xl
                    border
                    border-gray-200
                    dark:border-gray-800
                    bg-white
                    dark:bg-gray-900
                    p-5
                    transition
                    shadow-sm
                    hover:shadow-lg
                    {borderClasses(engine.color)}
                "
            >

                <!-- TOP -->
                <div class="flex items-start justify-between gap-3">

                    <div>
                        <h2 class="font-semibold text-gray-900 dark:text-white">
                            {engine.name}
                        </h2>

                        <p class="text-sm text-gray-500 dark:text-gray-400 mt-2 leading-relaxed">
                            {engine.description}
                        </p>
                    </div>

                    <div
                        class="
                            text-xs
                            px-2
                            py-1
                            rounded-full
                            whitespace-nowrap
                            {badgeClasses(engine.color)}
                        "
                    >
                        {engine.status}
                    </div>

                </div>

                <!-- METRICS -->
                <div class="mt-6 grid grid-cols-2 gap-4">

                    <div class="rounded-xl bg-gray-50 dark:bg-gray-800 p-3">

                        <div class="text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wide">
                            Engine Health
                        </div>

                        <div class="text-xl font-bold text-gray-900 dark:text-white mt-1">
                            {engine.health}
                        </div>

                    </div>

                    <div class="rounded-xl bg-gray-50 dark:bg-gray-800 p-3">

                        <div class="text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wide">
                            Runtime
                        </div>

                        <div class="text-xl font-bold text-gray-900 dark:text-white mt-1">
                            Live
                        </div>

                    </div>

                </div>

                <!-- ACTIONS -->
                <div class="mt-6 flex items-center gap-2">

                    <button
                        class="
                            flex-1
                            px-3
                            py-2
                            rounded-xl
                            bg-emerald-600
                            hover:bg-emerald-700
                            text-white
                            text-sm
                            transition
                        "
                    >
                        Open Engine
                    </button>

                    <button
                        class="
                            px-3
                            py-2
                            rounded-xl
                            border
                            border-gray-300
                            dark:border-gray-700
                            hover:bg-gray-100
                            dark:hover:bg-gray-800
                            text-sm
                            transition
                        "
                    >
                        Logs
                    </button>

                </div>

            </div>

        {/each}

    </div>

    <!-- ORCHESTRATION PANEL -->
    <div
        class="
            rounded-2xl
            border
            border-gray-200
            dark:border-gray-800
            bg-white
            dark:bg-gray-900
            overflow-hidden
        "
    >

        <div class="p-5 border-b border-gray-200 dark:border-gray-800">

            <h2 class="font-semibold text-gray-900 dark:text-white">
                Enterprise Orchestration Pipeline
            </h2>

            <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
                Optimization lifecycle across dispatch, SLA and scheduling engines.
            </p>

        </div>

        <div class="p-5 grid grid-cols-1 md:grid-cols-2 xl:grid-cols-5 gap-4">

            <div class="rounded-xl bg-gray-50 dark:bg-gray-800 p-4">
                <div class="text-xs uppercase tracking-wide text-gray-500">
                    Intake
                </div>

                <div class="font-semibold mt-2 text-gray-900 dark:text-white">
                    Service Orders
                </div>
            </div>

            <div class="rounded-xl bg-gray-50 dark:bg-gray-800 p-4">
                <div class="text-xs uppercase tracking-wide text-gray-500">
                    Assignment AI
                </div>

                <div class="font-semibold mt-2 text-gray-900 dark:text-white">
                    Technician Matching
                </div>
            </div>

            <div class="rounded-xl bg-gray-50 dark:bg-gray-800 p-4">
                <div class="text-xs uppercase tracking-wide text-gray-500">
                    Routing
                </div>

                <div class="font-semibold mt-2 text-gray-900 dark:text-white">
                    Route Compression
                </div>
            </div>

            <div class="rounded-xl bg-gray-50 dark:bg-gray-800 p-4">
                <div class="text-xs uppercase tracking-wide text-gray-500">
                    Scheduling
                </div>

                <div class="font-semibold mt-2 text-gray-900 dark:text-white">
                    SLA Reservation
                </div>
            </div>

            <div class="rounded-xl bg-gray-50 dark:bg-gray-800 p-4">
                <div class="text-xs uppercase tracking-wide text-gray-500">
                    Intelligence
                </div>

                <div class="font-semibold mt-2 text-gray-900 dark:text-white">
                    Continuous Optimization
                </div>
            </div>

        </div>

    </div>

</div>