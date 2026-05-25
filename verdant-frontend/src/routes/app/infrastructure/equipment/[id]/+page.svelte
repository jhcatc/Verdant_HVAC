<script lang="ts">

    import AddMaintenanceLogModal
        from '$lib/components/hvac/AddMaintenanceLogModal.svelte';
    import { onMount } from 'svelte';
    import QRCode from 'qrcode';
    import * as maintenanceApi
        from '$lib/api/maintenanceLogs';
    import * as equipmentApi
        from '$lib/api/equipment';
    import * as equipmentQrApi
        from '$lib/api/equipmentQr';
    import DataTable
    from '$lib/components/data-table/DataTable.svelte';
    import type {
        DataTableColumn,
        DataTableAction
    } from '$lib/types/data-table';
    import * as componentApi
    from '$lib/api/equipmentComponents';
    import EquipmentIntelligenceCard
    from '$lib/components/hvac/EquipmentIntelligenceCard.svelte';
    import * as documentsApi
    from '$lib/api/equipmentDocuments';

    import * as photosApi
    from '$lib/api/equipmentPhotos';

    let { params } = $props();
    let loading = $state(true);
    let equipment = $state<Equipment | null>(null);
    let activeTab = $state('overview');
    type MaintenanceLog = {
        id: string;
        maintenance_type: string;
        technician?: string;
        equipment_condition?: string;
        created_at: string;
    };
    let maintenanceLogs =
        $state<MaintenanceLog[]>([]);
    let maintenanceLoading = $state(false);
    let showMaintenanceModal = $state(false);
    type EquipmentQrPayload = {
        equipment_id: string;
        asset_tag: string;
        serial_number?: string;
    };
    let qrPayload =
        $state<EquipmentQrPayload | null>(
            null
        );
    let qrImage = $state('');
    import type {
        EquipmentComponent
    } from '$lib/types/components';
    let components =
        $state<EquipmentComponent[]>([]);
    let componentsLoading = $state(false);
    let documents = $state<any[]>([]);
    let photos = $state<any[]>([]);

    let documentsLoading = $state(false);
    let photosLoading = $state(false);

    async function loadComponents() {

        componentsLoading = true;

        try {

            components =
                await componentApi.getComponents(
                    params.id
                );

        } catch (err) {

            console.error(err);

        } finally {

            componentsLoading = false;
        }
    }

    async function loadEquipment() {

        try {

            equipment = await equipmentApi.getEquipmentById(
                params.id
            );

        } catch (err) {

            console.error(err);

        } finally {

            loading = false;
        }
    }

    async function loadQr() {

        try {

            qrPayload =
                await equipmentQrApi.getEquipmentQr(
                    params.id
                );

            qrImage =
                await QRCode.toDataURL(
                    JSON.stringify(qrPayload)
                );

        } catch (err) {

            console.error(err);
        }
    }

    const tabs = [
        'overview',
        'maintenance',
        'workorders',
        'measurements',
        'documents',
        'photos',
        'components',
        'intelligence'
    ];

    const maintenanceColumns:
    DataTableColumn<MaintenanceLog>[] = [

        {
            key: 'maintenance_type',
            label: 'Type'
        },
        {
            key: 'technician',
            label: 'Technician'
        },
        {
            key: 'equipment_condition',
            label: 'Condition'
        },
        {
            id: 'intelligence',
            label: 'Asset Intelligence'
        },
        {
            key: 'created_at',
            label: 'Date',

            render: (row) =>
                new Date(
                    row.created_at
                ).toLocaleDateString()
        }
    ];

    const maintenanceActions:
    DataTableAction<MaintenanceLog>[] = [

        {
            label: 'View',

            onClick: (row) => {

                console.log(
                    'VIEW LOG',
                    row
                );
            }
        }
    ];

    async function loadMaintenanceLogs() {

        maintenanceLoading = true;

        try {

            maintenanceLogs =
                await maintenanceApi.getEquipmentLogs(
                    params.id
                );

        } catch (err) {

            console.error(err);

        } finally {

            maintenanceLoading = false;
        }
    }

    async function handleMaintenanceCreated() {

        showMaintenanceModal = false;

        await loadMaintenanceLogs();
    }

    onMount(async () => {
        await loadComponents();
        await loadEquipment();
        await loadMaintenanceLogs();
        await loadQr();
        await loadDocuments();
        await loadPhotos();
    });

    async function loadDocuments() {

        documentsLoading = true;
        try {
            documents =
                await documentsApi.getEquipmentDocuments(
                    params.id
                );
        } catch (err) {
            console.error(err);
        } finally {
            documentsLoading = false;
        }
    }

    async function loadPhotos() {
        photosLoading = true;
        try {
            photos =
                await photosApi.getEquipmentPhotos(
                    params.id
                );
        } catch (err) {
            console.error(err);
        } finally {
            photosLoading = false;
        }
    }



</script>

{#if loading}

<div class="p-6 text-gray-500">
    Loading equipment...
</div>

{:else if !equipment}

<div class="p-6 text-red-500">
    Equipment not found
</div>

{:else}

<div class="p-6 space-y-6">

    <!-- HEADER -->
    <div class="bg-white dark:bg-gray-900 rounded-2xl shadow border border-gray-200 dark:border-gray-800 p-6">

        <div class="flex items-start justify-between">

            <div>

                <div class="flex items-center gap-3">

                    <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
                        {equipment.asset_tag}
                    </h1>

                    <span class="px-3 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-700">
                        {equipment.status?.name ?? 'ACTIVE'}
                    </span>

                </div>

                <p class="mt-2 text-gray-600 dark:text-gray-400">
                    {equipment.brand?.name}
                    —
                    {equipment.model}
                </p>

                <div class="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4">

                    <div>
                        <p class="text-xs text-gray-400">
                            Customer
                        </p>

                        <p class="font-medium text-gray-800 dark:text-white">
                            {equipment.customer?.name ?? '-'}
                        </p>
                    </div>

                    <div>
                        <p class="text-xs text-gray-400">
                            Location
                        </p>

                        <p class="font-medium text-gray-800 dark:text-white">
                            {equipment.location?.name ?? '-'}
                        </p>
                    </div>

                    <div>
                        <p class="text-xs text-gray-400">
                            Serial Number
                        </p>

                        <p class="font-medium text-gray-800 dark:text-white">
                            {equipment.serial_number ?? '-'}
                        </p>
                    </div>

                    <div>
                        <p class="text-xs text-gray-400">
                            Warranty
                        </p>

                        <p class="font-medium text-gray-800 dark:text-white">
                            {equipment.warranty_expiration ?? '-'}
                        </p>
                    </div>

                </div>

            </div>

            <!-- QR -->
            <div class="flex flex-col items-center gap-3">

                <div
                    class="p-3 rounded-2xl border border-gray-200 dark:border-gray-700 bg-white shadow-sm"
                >

                    {#if qrImage}

                        <img
                            src={qrImage}
                            alt="Equipment QR"
                            class="w-32 h-32"
                        />

                    {:else}

                        <div
                            class="w-32 h-32 flex items-center justify-center text-xs text-gray-400"
                        >
                            QR Loading...
                        </div>

                    {/if}

                </div>

                <div class="text-center">

                    <p class="text-xs font-semibold text-gray-700 dark:text-gray-300">
                        Asset Identity
                    </p>

                    <p class="text-[11px] text-gray-400">
                        Technician Scan Access
                    </p>

                </div>

            </div>

        </div>

    </div>

    <!-- TABS -->
    <div class="bg-white dark:bg-gray-900 rounded-2xl shadow border border-gray-200 dark:border-gray-800">

        <div class="border-b border-gray-200 dark:border-gray-800 px-4">

            <div class="flex gap-2 overflow-x-auto py-3">

                {#each tabs as tab}

                <button
                    onclick={() => activeTab = tab}
                    class={`px-4 py-2 rounded-lg text-sm whitespace-nowrap transition
                    ${
                        activeTab === tab
                        ? 'bg-emerald-600 text-white'
                        : 'hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-700 dark:text-gray-300'
                    }`}
                >
                    {tab}
                </button>

                {/each}

            </div>

        </div>

        <!-- CONTENT -->
        <div class="p-6">

            <!-- OVERVIEW -->
            {#if activeTab === 'overview'}

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

                <div class="space-y-2">

                    <h3 class="font-semibold text-gray-900 dark:text-white">
                        General
                    </h3>

                    <div class="text-sm space-y-1">

                        <p>
                            <span class="text-gray-500">
                                Category:
                            </span>

                            {equipment.category?.name ?? '-'}
                        </p>

                        <p>
                            <span class="text-gray-500">
                                Type:
                            </span>

                            {equipment.equipment_type?.name ?? '-'}
                        </p>

                        <p>
                            <span class="text-gray-500">
                                Refrigerant:
                            </span>

                            {equipment.refrigerant?.name ?? '-'}
                        </p>

                        <p>
                            <span class="text-gray-500">
                                Voltage:
                            </span>

                            {equipment.voltage?.name ?? '-'}
                        </p>

                    </div>

                </div>

                <div class="space-y-2">

                    <h3 class="font-semibold text-gray-900 dark:text-white">
                        Technical Specs
                    </h3>

                    <div class="text-sm space-y-1">

                        <p>
                            <span class="text-gray-500">
                                Capacity:
                            </span>

                            {equipment.capacity ?? '-'}
                        </p>

                        <p>
                            <span class="text-gray-500">
                                SEER:
                            </span>

                            {equipment.seer_rating ?? '-'}
                        </p>

                        <p>
                            <span class="text-gray-500">
                                EER:
                            </span>

                            {equipment.eer_rating ?? '-'}
                        </p>

                    </div>

                </div>

                <div class="space-y-2">

                    <h3 class="font-semibold text-gray-900 dark:text-white">
                        Installation
                    </h3>

                    <div class="text-sm space-y-1">

                        <p>
                            <span class="text-gray-500">
                                Install Date:
                            </span>

                            {equipment.installation_date ?? '-'}
                        </p>

                        <p>
                            <span class="text-gray-500">
                                Manufacture Year:
                            </span>

                            {equipment.manufacture_year ?? '-'}
                        </p>

                    </div>

                </div>

            </div>

            {/if}

            <!-- MAINTENANCE -->
            {#if activeTab === 'maintenance'}

            <div class="space-y-6">

                <div class="flex items-center justify-between">

                    <div>

                        <h2 class="text-lg font-semibold text-gray-900 dark:text-white">
                            Maintenance History
                        </h2>

                        <p class="text-sm text-gray-500">
                            Technical service timeline
                        </p>

                    </div>

                    <button
                        onclick={() => showMaintenanceModal = true}
                        class="px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-sm transition"
                    >
                        Add Maintenance Log
                    </button>

                </div>

                {#if maintenanceLoading}

                <div class="border rounded-xl p-6 text-gray-500">

                    Loading maintenance logs...

                </div>

                {:else if maintenanceLogs.length === 0}

                <div class="border rounded-xl p-6 text-gray-500">

                    No maintenance history found.

                </div>

                {:else}

                <DataTable
                    columns={maintenanceColumns}
                    rows={maintenanceLogs}
                    loading={maintenanceLoading}
                    emptyTitle="No maintenance history"
                    emptyDescription="Maintenance logs will appear here"
                    rowActions={maintenanceActions}
                />

                {/if}

            </div>

            {/if}

            <!-- WORK ORDERS -->
            {#if activeTab === 'workorders'}

            <div class="space-y-4">

                <div class="flex items-center justify-between">

                    <h2 class="text-lg font-semibold">
                        Work Orders
                    </h2>

                    <button class="px-4 py-2 rounded-lg bg-emerald-600 text-white text-sm">
                        Create Work Order
                    </button>

                </div>

                <div class="border rounded-xl p-6 text-gray-500">

                    Future work orders table

                </div>

            </div>

            {/if}

            <!-- MEASUREMENTS -->
            {#if activeTab === 'measurements'}

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">

                <div class="border rounded-xl p-4">
                    <p class="text-sm text-gray-500">Temperature</p>
                    <p class="text-2xl font-bold">--</p>
                </div>

                <div class="border rounded-xl p-4">
                    <p class="text-sm text-gray-500">Pressure</p>
                    <p class="text-2xl font-bold">--</p>
                </div>

                <div class="border rounded-xl p-4">
                    <p class="text-sm text-gray-500">Voltage</p>
                    <p class="text-2xl font-bold">--</p>
                </div>

                <div class="border rounded-xl p-4">
                    <p class="text-sm text-gray-500">Amperage</p>
                    <p class="text-2xl font-bold">--</p>
                </div>

            </div>

            {/if}

            <!-- DOCUMENTS -->
            {#if activeTab === 'documents'}

            <div class="space-y-4">

                <div class="space-y-4">

                    <div class="flex items-center justify-between">

                        <div>

                            <h2 class="text-lg font-semibold">
                                Documents
                            </h2>

                            <p class="text-sm text-gray-500">
                                Manuals, warranties,
                                invoices and compliance files.
                            </p>

                        </div>

                        <input
                            type="file"
                            onchange={async (e) => {

                                const file =
                                    e.currentTarget.files?.[0];

                                if (!file) {
                                    return;
                                }

                                await documentsApi.uploadEquipmentDocument(
                                    equipment.id,
                                    file
                                );

                                await loadDocuments();
                            }}
                            class="text-sm"
                        />

                    </div>

                    {#if documentsLoading}

                        <div class="border rounded-xl p-6 text-gray-500">
                            Loading documents...
                        </div>

                    {:else if documents.length === 0}

                        <div class="border rounded-xl p-6 text-gray-500">
                            No documents uploaded.
                        </div>

                    {:else}

                        <div class="space-y-3">

                            {#each documents as doc}

                                <div
                                    class="rounded-xl border border-gray-200 dark:border-gray-800 p-4 flex items-center justify-between"
                                >

                                    <div>

                                        <div class="font-medium">
                                            {doc.filename}
                                        </div>

                                        <div class="text-xs text-gray-500">
                                            {doc.created_at}
                                        </div>

                                    </div>

                                    <a
                                        href={doc.url}
                                        target="_blank"
                                        class="px-3 py-2 rounded-lg bg-emerald-600 text-white text-sm"
                                    >
                                        Open
                                    </a>

                                </div>

                            {/each}

                        </div>

                    {/if}

                </div>

                <div class="border rounded-xl p-6 text-gray-500">

                    Future documents grid

                </div>

            </div>

            {/if}

            <!-- PHOTOS -->
            {#if activeTab === 'photos'}

            <div class="space-y-4">

                <div class="flex items-center justify-between">

                    <div>

                        <h2 class="text-lg font-semibold">
                            Photos
                        </h2>

                        <p class="text-sm text-gray-500">
                            Field evidence and equipment imagery.
                        </p>

                    </div>

                    <input
                        type="file"
                        accept="image/*"
                        onchange={async (e) => {

                            const file =
                                e.currentTarget.files?.[0];

                            if (!file) {
                                return;
                            }

                            await photosApi.uploadEquipmentPhoto(
                                equipment.id,
                                file
                            );

                            await loadPhotos();
                        }}
                        class="text-sm"
                    />

                </div>

                {#if photosLoading}

                    <div class="border rounded-xl p-6 text-gray-500">
                        Loading photos...
                    </div>

                {:else if photos.length === 0}

                    <div class="border rounded-xl p-6 text-gray-500">
                        No photos uploaded.
                    </div>

                {:else}

                    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">

                        {#each photos as photo}

                            <div
                                class="rounded-2xl overflow-hidden border border-gray-200 dark:border-gray-800"
                            >

                                <img
                                    src={photo.url}
                                    alt={photo.filename}
                                    class="w-full h-52 object-cover"
                                />

                            </div>

                        {/each}

                    </div>

                {/if}

            </div>

            {/if}

            <!-- COMPONENTS -->
            {#if activeTab === 'components'}

            <div class="space-y-6">

                <!-- ===================================================== -->
                <!-- HEADER -->
                <!-- ===================================================== -->

                <div class="flex items-center justify-between">

                    <div>

                        <h2 class="text-xl font-semibold text-gray-900 dark:text-white">
                            Component Registry
                        </h2>

                        <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
                            Serialized HVAC component lifecycle management,
                            warranty tracking, replacement history and
                            predictive maintenance foundation.
                        </p>

                    </div>

                    <button
                        class="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-sm transition"
                    >
                        Add Component
                    </button>

                </div>

                <!-- ===================================================== -->
                <!-- LOADING -->
                <!-- ===================================================== -->

                {#if componentsLoading}

                <div class="border rounded-xl p-6 text-gray-500">

                    Loading components...

                </div>

                <!-- ===================================================== -->
                <!-- EMPTY -->
                <!-- ===================================================== -->

                {:else if components.length === 0}

                <div
                    class="rounded-2xl border border-dashed border-gray-300 dark:border-gray-700 p-10 text-center bg-white dark:bg-gray-900"
                >

                    <div class="text-5xl">
                        ⚙️
                    </div>

                    <h3 class="mt-4 text-lg font-semibold text-gray-800 dark:text-white">
                        No Components Registered
                    </h3>

                    <p class="mt-2 text-sm text-gray-500 dark:text-gray-400 max-w-xl mx-auto leading-relaxed">
                        Register compressors, blower motors, capacitors,
                        filters, coils and serialized HVAC components for
                        lifecycle, warranty and predictive maintenance tracking.
                    </p>

                </div>

                <!-- ===================================================== -->
                <!-- GRID -->
                <!-- ===================================================== -->

                {:else}

                <div class="grid grid-cols-1 xl:grid-cols-2 gap-5">

                    {#each components as component}

                    <div
                        class="rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-5 shadow-sm hover:shadow-lg transition-all"
                    >

                        <!-- TOP -->
                        <div class="flex items-start justify-between gap-4">

                            <div>

                                <div class="flex items-center gap-2 flex-wrap">

                                    <h3 class="font-semibold text-gray-900 dark:text-white text-lg">
                                        {component.component_name}
                                    </h3>

                                    {#if component.is_critical}

                                    <span
                                        class="px-2 py-1 rounded-full text-[10px] font-semibold bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300"
                                    >
                                        CRITICAL
                                    </span>

                                    {/if}

                                </div>

                                <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
                                    {component.component_type}
                                </p>

                            </div>

                            <span
                                class="px-3 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300"
                            >
                                {component.status}
                            </span>

                        </div>

                        <!-- INFO -->
                        <div class="mt-6 grid grid-cols-2 gap-5 text-sm">

                            <div>

                                <p class="text-gray-400 text-xs uppercase tracking-wider">
                                    Manufacturer
                                </p>

                                <p class="font-medium text-gray-800 dark:text-white mt-1">
                                    {component.manufacturer ?? '-'}
                                </p>

                            </div>

                            <div>

                                <p class="text-gray-400 text-xs uppercase tracking-wider">
                                    Model
                                </p>

                                <p class="font-medium text-gray-800 dark:text-white mt-1">
                                    {component.model_number ?? '-'}
                                </p>

                            </div>

                            <div>

                                <p class="text-gray-400 text-xs uppercase tracking-wider">
                                    Serial Number
                                </p>

                                <p class="font-medium text-gray-800 dark:text-white mt-1">
                                    {component.serial_number ?? '-'}
                                </p>

                            </div>

                            <div>

                                <p class="text-gray-400 text-xs uppercase tracking-wider">
                                    Warranty
                                </p>

                                <p class="font-medium text-gray-800 dark:text-white mt-1">
                                    {component.warranty_expiration ?? '-'}
                                </p>

                            </div>

                        </div>

                        <!-- FOOTER -->
                        <div
                            class="mt-6 pt-4 border-t border-gray-200 dark:border-gray-800 flex items-center justify-between"
                        >

                            <div class="text-xs text-gray-500">

                                Installed:
                                <span class="font-medium text-gray-700 dark:text-gray-300">
                                    {component.installation_date ?? '-'}
                                </span>

                            </div>

                            <button
                                class="px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-800 text-sm transition"
                            >
                                Open Lifecycle
                            </button>

                        </div>

                    </div>

                    {/each}

                </div>

                {/if}

            </div>

            {/if}

            <!-- INTELLIGENCE -->
            {#if activeTab === 'intelligence'}

            <EquipmentIntelligenceCard
                equipmentId={equipment.id}
            />

            {/if}

        </div>

    </div>

</div>

{/if}


{#if showMaintenanceModal}

<AddMaintenanceLogModal
    equipmentId={params.id}
    on:created={handleMaintenanceCreated}
    on:close={() => showMaintenanceModal = false}
/>

{/if}