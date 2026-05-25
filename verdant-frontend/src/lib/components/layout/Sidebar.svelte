<script lang="ts">
    import { goto } from '$app/navigation';
    import { page } from '$app/state';

    let collapsed = $state(false);

    let openMenu = $state<
        null |
        'operations' |
        'inventory' |
        'customers' |
        'infrastructure'|
        'crm'
    >(null);

    function navigate(path: string) {
        goto(path);
    }

    function isActive(path: string) {
        return page.url.pathname.startsWith(path);
    }

    function toggleSidebar() {

        collapsed = !collapsed;

        if (collapsed) {
            openMenu = null;
        }
    }

    function toggleMenu(
        menu:
            | 'operations'
            | 'inventory'
            | 'customers'
            | 'infrastructure'
            | 'crm'
    ) {

        openMenu = openMenu === menu
            ? null
            : menu;
    }
</script>

<aside
    class={`h-full bg-[#0f172a] text-white flex flex-col transition-all duration-300 ${
        collapsed ? 'w-16' : 'w-80'
    }`}
>

    <!-- ===================================================== -->
    <!-- HEADER -->
    <!-- ===================================================== -->

    <div class="p-4 flex items-center justify-between border-b border-slate-700">

        {#if !collapsed}

            <div>

                <div class="font-bold text-emerald-400 tracking-wide">
                    VERDANT ERP
                </div>

                <div class="text-[11px] text-slate-400 mt-1">
                    Enterprise Field Operations
                </div>

            </div>

        {/if}

        <button
            onclick={toggleSidebar}
            class="text-sm text-gray-300 hover:text-white"
        >
            {collapsed ? '>>' : '<<'}
        </button>

    </div>

    <!-- ===================================================== -->
    <!-- NAV -->
    <!-- ===================================================== -->

    <nav class="flex-1 overflow-y-auto px-2 py-3 space-y-3">

        <!-- ===================================================== -->
        <!-- DASHBOARD -->
        <!-- ===================================================== -->

        <button
            class={`w-full flex items-center px-3 py-2 rounded-xl transition ${
                isActive('/app/dashboard')
                    ? 'bg-green-600'
                    : 'hover:bg-slate-700'
            }`}
            onclick={() => navigate('/app/dashboard')}
        >
            <span>🏠</span>

            {#if !collapsed}
                <span class="ml-3">
                    Dashboard
                </span>
            {/if}
        </button>

        <!-- ===================================================== -->
        <!-- OPERATIONS -->
        <!-- ===================================================== -->

        <button
            class={`w-full flex items-center justify-between px-3 py-2 rounded-xl transition ${
                isActive('/app/dispatch') ||
                isActive('/app/orders') ||
                isActive('/app/operations')
                    ? 'bg-green-600'
                    : 'hover:bg-slate-700'
            }`}
            onclick={() => toggleMenu('operations')}
        >

            <div class="flex items-center">

                <span>⚙️</span>

                {#if !collapsed}

                    <div class="ml-3 text-left">

                        <div>
                            Operations
                        </div>

                        <div class="text-[10px] text-slate-300">
                            Dispatch · PM · SLA · Optimization
                        </div>

                    </div>

                {/if}

            </div>

        </button>

        {#if openMenu === 'operations' && !collapsed}

            <div class="ml-4 flex flex-col space-y-1">

                <!-- DISPATCH -->

                <div class="text-[11px] uppercase tracking-wider text-slate-400 px-2 pt-2">
                    Dispatch
                </div>

                <button
                    class={`px-3 py-2 rounded-lg text-left transition ${
                        isActive('/app/dispatch') &&
                        !isActive('/app/dispatch/calendar') &&
                        !isActive('/app/dispatch/routes')
                            ? 'bg-emerald-500'
                            : 'hover:bg-slate-700'
                    }`}
                    onclick={() => navigate('/app/dispatch')}
                >
                    Dispatch Board
                </button>

                <button
                    class={`px-3 py-2 rounded-lg text-left transition ${
                        isActive('/app/dispatch/calendar')
                            ? 'bg-emerald-500'
                            : 'hover:bg-slate-700'
                    }`}
                    onclick={() => navigate('/app/dispatch/calendar')}
                >
                    Dispatch Calendar
                </button>

                <button
                    class={`px-3 py-2 rounded-lg text-left transition ${
                        isActive('/app/operations/route-optimization')
                            ? 'bg-emerald-500'
                            : 'hover:bg-slate-700'
                    }`}
                    onclick={() => navigate('/app/operations/route-optimization')}
                >
                    Route Optimization
                </button>

                <button
                    class={`px-3 py-2 rounded-lg text-left transition ${
                        isActive('/app/operations/route-heatmaps')
                            ? 'bg-emerald-500'
                            : 'hover:bg-slate-700'
                    }`}
                    onclick={() => navigate('/app/operations/route-heatmaps')}
                >
                    Route Heatmaps
                </button>

                <!-- SCHEDULING -->

                <div class="text-[11px] uppercase tracking-wider text-slate-400 px-2 pt-5">
                    Scheduling
                </div>

                <button
                    class={`px-3 py-2 rounded-lg text-left transition ${
                        isActive('/app/operations/schedule-engine')
                            ? 'bg-emerald-500'
                            : 'hover:bg-slate-700'
                    }`}
                    onclick={() => navigate('/app/operations/schedule-engine')}
                >
                    Scheduling Engine
                </button>

                <button
                    class={`px-3 py-2 rounded-lg text-left transition ${
                        isActive('/app/operations/maintenance-plans/calendar')
                            ? 'bg-emerald-500'
                            : 'hover:bg-slate-700'
                    }`}
                    onclick={() =>
                        navigate('/app/operations/maintenance-plans/calendar')
                    }
                >
                    PM Calendar Engine
                </button>

                <!-- MAINTENANCE -->

                <div class="text-[11px] uppercase tracking-wider text-slate-400 px-2 pt-5">
                    Preventive Maintenance
                </div>

                <button
                    class={`px-3 py-2 rounded-lg text-left transition ${
                        isActive('/app/operations/maintenance-plans') &&
                        !isActive('/app/operations/maintenance-plans/calendar')
                            ? 'bg-emerald-500'
                            : 'hover:bg-slate-700'
                    }`}
                    onclick={() => navigate('/app/operations/maintenance-plans')}
                >
                    Maintenance Plans
                </button>

                <button
                    class={`px-3 py-2 rounded-lg text-left transition ${
                        isActive('/app/orders')
                            ? 'bg-emerald-500'
                            : 'hover:bg-slate-700'
                    }`}
                    onclick={() => navigate('/app/orders')}
                >
                    Service Orders
                </button>

                <!-- COMPLIANCE -->

                <div class="text-[11px] uppercase tracking-wider text-slate-400 px-2 pt-5">
                    Compliance & SLA
                </div>

                <button
                    class={`px-3 py-2 rounded-lg text-left transition ${
                        isActive('/app/operations/sla')
                            ? 'bg-emerald-500'
                            : 'hover:bg-slate-700'
                    }`}
                    onclick={() => navigate('/app/operations/sla')}
                >
                    SLA & Compliance
                </button>

                <!-- AI + OPTIMIZATION -->

                <div class="text-[11px] uppercase tracking-wider text-slate-400 px-2 pt-5">
                    Optimization & AI
                </div>

                <button
                    class={`px-3 py-2 rounded-lg text-left transition ${
                        isActive('/app/operations/intelligence')
                            ? 'bg-emerald-500'
                            : 'hover:bg-slate-700'
                    }`}
                    onclick={() => navigate('/app/operations/intelligence')}
                >
                    Operations Intelligence
                </button>

                <button
                    class={`px-3 py-2 rounded-lg text-left transition ${
                        isActive('/app/operations/optimization')
                            ? 'bg-emerald-500'
                            : 'hover:bg-slate-700'
                    }`}
                    onclick={() => navigate('/app/operations/optimization')}
                >
                    Optimization Center
                </button>

            </div>

        {/if}

        <!-- ===================================================== -->
        <!-- INFRASTRUCTURE -->
        <!-- ===================================================== -->

        <button
            class={`w-full flex items-center justify-between px-3 py-2 rounded-xl transition ${
                isActive('/app/infrastructure')
                    ? 'bg-green-600'
                    : 'hover:bg-slate-700'
            }`}
            onclick={() => toggleMenu('infrastructure')}
        >

            <div class="flex items-center">

                <span>🏗️</span>

                {#if !collapsed}

                    <div class="ml-3 text-left">

                        <div>
                            Infrastructure
                        </div>

                        <div class="text-[10px] text-slate-300">
                            Assets · Facilities · Intelligence
                        </div>

                    </div>

                {/if}

            </div>

        </button>

        {#if openMenu === 'infrastructure' && !collapsed}

            <div class="ml-6 flex flex-col space-y-1">

                <!-- CORE -->

                <div class="text-[11px] uppercase tracking-wider text-slate-400 px-2 pt-3">
                    Core Assets
                </div>

                <button
                    class={`px-3 py-2 rounded text-left transition ${
                        isActive('/app/infrastructure/equipment')
                            ? 'bg-emerald-500'
                            : 'hover:bg-slate-700'
                    }`}
                    onclick={() => navigate('/app/infrastructure/equipment')}
                >
                    All Equipment
                </button>

                <button
                    class={`px-3 py-2 rounded text-left transition ${
                        isActive('/app/infrastructure/facilities')
                            ? 'bg-emerald-500'
                            : 'hover:bg-slate-700'
                    }`}
                    onclick={() => navigate('/app/infrastructure/facilities')}
                >
                    Facilities
                </button>

                <!-- COMPONENTS -->

                <div class="text-[11px] uppercase tracking-wider text-slate-400 px-2 pt-5">
                    Components & Traceability
                </div>

                <button
                    class={`px-3 py-2 rounded text-left transition ${
                        isActive('/app/infrastructure/components')
                            ? 'bg-emerald-500'
                            : 'hover:bg-slate-700'
                    }`}
                    onclick={() => navigate('/app/infrastructure/components')}
                >
                    Component Registry
                </button>

                <button
                    class={`px-3 py-2 rounded text-left transition ${
                        isActive('/app/infrastructure/qr')
                            ? 'bg-emerald-500'
                            : 'hover:bg-slate-700'
                    }`}
                    onclick={() => navigate('/app/infrastructure/qr')}
                >
                    QR Registry
                </button>

                <!-- MAINTENANCE -->

                <div class="text-[11px] uppercase tracking-wider text-slate-400 px-2 pt-5">
                    Maintenance
                </div>

                <button
                    class={`px-3 py-2 rounded text-left transition ${
                        isActive('/app/infrastructure/maintenance-logs')
                            ? 'bg-emerald-500'
                            : 'hover:bg-slate-700'
                    }`}
                    onclick={() => navigate('/app/infrastructure/maintenance-logs')}
                >
                    Maintenance Logs
                </button>

                <!-- INTELLIGENCE -->

                <div class="text-[11px] uppercase tracking-wider text-slate-400 px-2 pt-5">
                    Intelligence
                </div>

                <button
                    class={`px-3 py-2 rounded text-left transition ${
                        page.url.pathname === '/app/infrastructure/intelligence'
                            ? 'bg-emerald-500'
                            : 'hover:bg-slate-700'
                    }`}
                    onclick={() => navigate('/app/infrastructure/intelligence')}
                >
                    Intelligence Center
                </button>

                <button
                    class={`px-3 py-2 rounded text-left transition ${
                        isActive('/app/infrastructure/intelligence/clusters')
                            ? 'bg-emerald-500'
                            : 'hover:bg-slate-700'
                    }`}
                    onclick={() => navigate('/app/infrastructure/intelligence/clusters')}
                >
                    Failure Clusters
                </button>

                <!-- ANOMALIES -->

                <div class="text-[11px] uppercase tracking-wider text-slate-400 px-2 pt-5">
                    Monitoring
                </div>

                <button
                    class={`px-3 py-2 rounded text-left transition ${
                        isActive('/app/infrastructure/anomalies')
                            ? 'bg-emerald-500'
                            : 'hover:bg-slate-700'
                    }`}
                    onclick={() => navigate('/app/infrastructure/anomalies')}
                >
                    Anomalies (beta)
                </button>

            </div>

        {/if}


        <!-- ===================================================== -->
        <!-- INVENTORY -->
        <!-- ===================================================== -->

        <button
            class={`w-full flex items-center justify-between px-3 py-2 rounded-xl transition ${
                isActive('/app/inventory')
                    ? 'bg-green-600'
                    : 'hover:bg-slate-700'
            }`}
            onclick={() => toggleMenu('inventory')}
        >

            <div class="flex items-center">

                <span>📦</span>

                {#if !collapsed}
                    <span class="ml-3">
                        Inventory
                    </span>
                {/if}

            </div>

        </button>

        {#if openMenu === 'inventory' && !collapsed}

            <div class="ml-6 flex flex-col space-y-1">

                <button
                    class="px-3 py-2 rounded text-left hover:bg-slate-700 transition"
                    onclick={() => navigate('/app/inventory/items')}
                >
                    Items
                </button>

                <button
                    class="px-3 py-2 rounded text-left hover:bg-slate-700 transition"
                    onclick={() => navigate('/app/inventory/movements')}
                >
                    Movements
                </button>

                <button
                    class="px-3 py-2 rounded text-left hover:bg-slate-700 transition"
                    onclick={() => navigate('/app/inventory/adjustments')}
                >
                    Adjustments
                </button>

                <button
                    class="px-3 py-2 rounded text-left hover:bg-slate-700 transition"
                    onclick={() => navigate('/app/inventory/locations')}
                >
                    Locations
                </button>

                <button
                    class="px-3 py-2 rounded text-left hover:bg-slate-700 transition"
                    onclick={() => navigate('/app/inventory/ira')}
                >
                    IRA
                </button>

            </div>

        {/if}

        <!-- ===================================================== -->
        <!-- CUSTOMERS -->
        <!-- ===================================================== -->

        <button
            class={`w-full flex items-center justify-between px-3 py-2 rounded-xl transition ${
                isActive('/app/customers')
                    ? 'bg-green-600'
                    : 'hover:bg-slate-700'
            }`}
            onclick={() => toggleMenu('customers')}
        >

            <div class="flex items-center">

                <span>🏗️</span>

                {#if !collapsed}

                    <div class="ml-3 text-left">

                        <div>
                            Customers
                        </div>

                        <div class="text-[10px] text-slate-300">
                            Customer · Locations · Risk Profiles
                        </div>

                    </div>

                {/if}

            </div>

        </button>

        {#if openMenu === 'customers' && !collapsed}

            <div class="ml-6 flex flex-col space-y-1">

                <!-- ================================================= -->
                <!-- CUSTOMER MANAGEMENT -->
                <!-- ================================================= -->

                <div
                    class="px-3 pt-3 pb-1 text-[10px] uppercase tracking-widest text-slate-500"
                >
                    Customer Management
                </div>

                <button
                    class={`px-3 py-2 rounded-lg text-left transition ${
                        page.url.pathname === '/app/customers'
                            ? 'bg-emerald-500'
                            : 'hover:bg-slate-700'
                    }`}
                    onclick={() => navigate('/app/customers')}
                >
                    Customer List
                </button>

                <button
                    class={`px-3 py-2 rounded-lg text-left transition ${
                        isActive('/app/customers/create')
                            ? 'bg-emerald-500'
                            : 'hover:bg-slate-700'
                    }`}
                    onclick={() => navigate('/app/customers/create')}
                >
                    Create Customer
                </button>

                <!-- ================================================= -->
                <!-- LOCATIONS -->
                <!-- ================================================= -->

                <div
                    class="px-3 pt-5 pb-1 text-[10px] uppercase tracking-widest text-slate-500"
                >
                    Locations
                </div>

                <button
                    class={`px-3 py-2 rounded-lg text-left transition ${
                        page.url.pathname === '/app/customers/locations'
                            ? 'bg-emerald-500'
                            : 'hover:bg-slate-700'
                    }`}
                    onclick={() => navigate('/app/customers/locations')}
                >
                    Location List
                </button>

                <button
                    class={`px-3 py-2 rounded-lg text-left transition ${
                        isActive('/app/customers/locations/create')
                            ? 'bg-emerald-500'
                            : 'hover:bg-slate-700'
                    }`}
                    onclick={() => navigate('/app/customers/locations/create')}
                >
                    Create Location
                </button>

                <!-- ================================================= -->
                <!-- CUSTOMER INTELLIGENCE -->
                <!-- ================================================= -->

                <div
                    class="px-3 pt-5 pb-1 text-[10px] uppercase tracking-widest text-slate-500"
                >
                    Customer Intelligence
                </div>

                <button
                    class={`px-3 py-2 rounded-lg text-left transition ${
                        isActive('/app/customers/risk')
                            ? 'bg-emerald-500'
                            : 'hover:bg-slate-700'
                    }`}
                    onclick={() => navigate('/app/customers/risk')}
                >
                    Customer Risk Profiles
                </button>

                <button
                    class={`px-3 py-2 rounded-lg text-left transition ${
                        isActive('/app/customers/equipment')
                            ? 'bg-emerald-500'
                            : 'hover:bg-slate-700'
                    }`}
                    onclick={() => navigate('/app/customers/equipment')}
                >
                    Customer Equipment Overview
                </button>

                <button
                    class={`px-3 py-2 rounded-lg text-left transition ${
                        isActive('/app/customers/sla')
                            ? 'bg-emerald-500'
                            : 'hover:bg-slate-700'
                    }`}
                    onclick={() => navigate('/app/customers/sla')}
                >
                    SLA Customers
                </button>

            </div>

        {/if}


        <!-- ===================================================== -->
        <!-- CRM -->
        <!-- ===================================================== -->

        <button
            class={`w-full flex items-center justify-between px-3 py-2 rounded-xl transition ${
                isActive('/app/crm')
                    ? 'bg-green-600'
                    : 'hover:bg-slate-700'
            }`}
            onclick={() => toggleMenu('crm')}
        >

            <div class="flex items-center">

                <span>📊</span>

                {#if !collapsed}

                    <div class="ml-3 text-left">

                        <div>
                            CRM
                        </div>

                        <div class="text-[10px] text-slate-300">
                            Pipeline · Contracts · Renewals
                        </div>

                    </div>

                {/if}

            </div>

        </button>

        {#if openMenu === 'crm' && !collapsed}

            <div class="ml-6 flex flex-col space-y-1">

                <!-- ================================================= -->
                <!-- CRM COMMAND -->
                <!-- ================================================= -->

                <div
                    class="px-3 pt-3 pb-1 text-[10px] uppercase tracking-widest text-slate-500"
                >
                    CRM Command
                </div>

                <button
                    class={`px-3 py-2 rounded-lg text-left transition ${
                        page.url.pathname === '/app/crm'
                            ? 'bg-emerald-500'
                            : 'hover:bg-slate-700'
                    }`}
                    onclick={() => navigate('/app/crm')}
                >
                    CRM Dashboard
                </button>

                <!-- ================================================= -->
                <!-- LEADS PIPELINE -->
                <!-- ================================================= -->

                <div
                    class="px-3 pt-5 pb-1 text-[10px] uppercase tracking-widest text-slate-500"
                >
                    Leads Pipeline
                </div>

                <button
                    class={`px-3 py-2 rounded-lg text-left transition ${
                        page.url.pathname === '/app/crm/leads'
                            ? 'bg-emerald-500'
                            : 'hover:bg-slate-700'
                    }`}
                    onclick={() => navigate('/app/crm/leads')}
                >
                    Leads Registry
                </button>
                <!--
                <button
                    class={`px-3 py-2 rounded-lg text-left transition ${
                        isActive('/app/crm/leads/create')
                            ? 'bg-emerald-500'
                            : 'hover:bg-slate-700'
                    }`}
                    onclick={() => navigate('/app/crm/leads/create')}
                >
                    Create Lead
                </button>
                -->
                <!-- ================================================= -->
                <!-- SALES -->
                <!-- ================================================= -->

                <div
                    class="px-3 pt-5 pb-1 text-[10px] uppercase tracking-widest text-slate-500"
                >
                    Sales & Contracts
                </div>

                <button
                    class={`px-3 py-2 rounded-lg text-left transition ${
                        isActive('/app/crm/opportunities')
                            ? 'bg-emerald-500'
                            : 'hover:bg-slate-700'
                    }`}
                    onclick={() => navigate('/app/crm/opportunities')}
                >
                    Opportunities
                </button>

                <button
                    class={`px-3 py-2 rounded-lg text-left transition ${
                        isActive('/app/crm/proposals')
                            ? 'bg-emerald-500'
                            : 'hover:bg-slate-700'
                    }`}
                    onclick={() => navigate('/app/crm/proposals')}
                >
                    Proposals
                </button>

                <button
                    class={`px-3 py-2 rounded-lg text-left transition ${
                        isActive('/app/crm/contracts')
                            ? 'bg-emerald-500'
                            : 'hover:bg-slate-700'
                    }`}
                    onclick={() => navigate('/app/crm/contracts')}
                >
                    Service Contracts
                </button>

                <!-- ================================================= -->
                <!-- RENEWALS -->
                <!-- ================================================= -->

                <div
                    class="px-3 pt-5 pb-1 text-[10px] uppercase tracking-widest text-slate-500"
                >
                    Renewals & Retention
                </div>

                <button
                    class={`px-3 py-2 rounded-lg text-left transition ${
                        isActive('/app/crm/renewals')
                            ? 'bg-emerald-500'
                            : 'hover:bg-slate-700'
                    }`}
                    onclick={() => navigate('/app/crm/renewals')}
                >
                    Renewals Pipeline
                </button>


                <!-- ================================================= -->
                <!-- CRM INTELLIGENCE -->
                <!-- ================================================= -->

                <div
                    class="px-3 pt-5 pb-1 text-[10px] uppercase tracking-widest text-slate-500"
                >
                    CRM Intelligence
                </div>

                <button
                    class={`px-3 py-2 rounded-lg text-left transition ${
                        isActive('/app/crm/intelligence')
                            ? 'bg-emerald-500'
                            : 'hover:bg-slate-700'
                    }`}
                    onclick={() => navigate('/app/crm/intelligence')}
                >
                    CRM Intelligence Center
                </button>

                <!-- ================================================= -->
                <!-- CUSTOMER 360 -->
                <!-- ================================================= -->

                <div
                    class="px-3 pt-5 pb-1 text-[10px] uppercase tracking-widest text-slate-500"
                >
                    Customer 360
                </div>

                <button
                    class={`px-3 py-2 rounded-lg text-left transition ${
                        isActive('/app/crm/customers')
                            ? 'bg-emerald-500'
                            : 'hover:bg-slate-700'
                    }`}
                    onclick={() => navigate('/app/crm/customers/1')}
                >
                    Customer 360 Profile
                </button>

            </div>

        {/if}

        <!-- INVOICES -->

        <button
            class={`w-full flex items-center px-3 py-2 rounded-xl transition ${
                isActive('/app/invoices')
                    ? 'bg-green-600'
                    : 'hover:bg-slate-700'
            }`}
            onclick={() => navigate('/app/invoices')}
        >

            <span>💰</span>

            {#if !collapsed}
                <span class="ml-3">
                    Invoices
                </span>
            {/if}

        </button>

        <!-- REPORTS -->

        <button
            class="w-full flex items-center px-3 py-2 rounded-xl hover:bg-slate-700 transition"
        >

            <span>📈</span>

            {#if !collapsed}
                <span class="ml-3">
                    A&A Reports
                </span>
            {/if}

        </button>

        <button
            class="w-full flex items-center px-3 py-2 rounded-xl hover:bg-slate-700 transition"
        >

            <span>📊</span>

            {#if !collapsed}
                <span class="ml-3">
                    Operations Report
                </span>
            {/if}

        </button>

        <!-- SETTINGS -->

        <button
            class="w-full flex items-center px-3 py-2 rounded-xl hover:bg-slate-700 transition"
        >

            <span>⚙️</span>

            {#if !collapsed}
                <span class="ml-3">
                    Settings
                </span>
            {/if}

        </button>

    </nav>

    <!-- ===================================================== -->
    <!-- FOOTER -->
    <!-- ===================================================== -->

    {#if !collapsed}

        <div class="p-2 border-t border-slate-700">

            <img
                src="/verdant.png"
                alt="Verdant ERP"
                class="w-full object-contain opacity-100 mt-4"
            />

        </div>

    {/if}

</aside>