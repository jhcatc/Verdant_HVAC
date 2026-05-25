<script lang="ts">

    import { goto } from '$app/navigation';

    import CustomerAutocomplete
        from '$lib/components/customer/CustomerAutocomplete.svelte';

    import LocationAutocomplete
        from '$lib/components/customer/LocationAutocomplete.svelte';

    import {
        getCustomerLocations
    } from '$lib/api/customerLocations';

    import {
        getEquipment
    } from '$lib/api/equipment';

    import {
        createMaintenancePlan
    } from '$lib/api/maintenancePlans';

    type Customer = {
        id: string;
        name: string;
    };

    type Location = {
        id: string;
        name: string;
    };

    type Equipment = {
        id: string;
        asset_tag: string;
        model: string;
    };

    type Task = {
        title: string;
    };

    let selectedCustomer = $state<Customer | null>(null);

    let selectedLocation = $state<Location | null>(null);

    let locations = $state<Location[]>([]);

    let equipment = $state<Equipment[]>([]);

    let selectedEquipmentIds = $state<string[]>([]);

    let loading = $state(false);

    let name = $state('');

    let description = $state('');

    let frequency_days = $state(90);

    let start_date = $state('');

    let recurring = $state(true);

    let auto_generate_work_orders = $state(true);

    let tasks = $state<Task[]>([
        {
            title: ''
        }
    ]);

    async function loadLocations() {

        if (!selectedCustomer) {
            return;
        }

        locations =
            await getCustomerLocations(
                selectedCustomer.id
            );
    }

    async function loadEquipment() {

        if (
            !selectedCustomer ||
            !selectedLocation
        ) {
            return;
        }

        equipment = await getEquipment({

            customer_id:
                selectedCustomer.id,

            location_id:
                selectedLocation.id
        });
    }

    function toggleEquipment(
        equipmentId: string
    ) {

        if (
            selectedEquipmentIds.includes(
                equipmentId
            )
        ) {

            selectedEquipmentIds =
                selectedEquipmentIds.filter(
                    id => id !== equipmentId
                );

            return;
        }

        selectedEquipmentIds = [
            ...selectedEquipmentIds,
            equipmentId
        ];
    }

    function addTask() {

        tasks = [
            ...tasks,
            {
                title: ''
            }
        ];
    }

    function updateTask(
        index: number,
        value: string
    ) {

        tasks[index].title = value;

        tasks = [...tasks];
    }

    async function submit() {

        if (!selectedCustomer) {
            alert('Select customer');
            return;
        }

        if (!selectedLocation) {
            alert('Select location');
            return;
        }

        if (!start_date) {
            alert('Select start date');
            return;
        }

        loading = true;

        try {

            await createMaintenancePlan({

                customer_id:
                    selectedCustomer.id,

                location_id:
                    selectedLocation.id,

                name,

                description,

                frequency_days,

                start_date,

                recurring,

                auto_generate_work_orders,

                equipment_ids:
                    selectedEquipmentIds,

                tasks: tasks.filter(
                    t =>
                        t.title.trim() !== ''
                )
            });

            goto(
                '/app/operations/maintenance-plans'
            );

        } catch (e) {

            console.error(e);

            alert(
                'Failed creating maintenance plan'
            );

        } finally {

            loading = false;
        }
    }

</script>

<div class="p-6 max-w-7xl mx-auto space-y-6">

    <div>

        <h1 class="text-3xl font-bold text-white">
            Create Maintenance Plan
        </h1>

        <p class="text-gray-400 mt-2">
            Preventive maintenance configuration
        </p>

    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-5">

        <div class="md:col-span-2">

            <label class="block text-sm mb-2">
                Customer
            </label>

            <CustomerAutocomplete
                onSelect={async (c: Customer) => {

                    selectedCustomer = c;

                    selectedLocation = null;

                    equipment = [];

                    await loadLocations();
                }}
            />

        </div>

        <div class="md:col-span-2">

            <label class="block text-sm mb-2">
                Location
            </label>

            <LocationAutocomplete
                locations={locations}
                onSelect={async (l: Location) => {

                    selectedLocation = l;

                    await loadEquipment();
                }}
            />

        </div>

        <div>

            <label class="block text-sm mb-2">
                Plan Name
            </label>

            <input
                bind:value={name}
                class="w-full rounded-xl border border-gray-700 bg-[#111827] p-3"
            />

        </div>

        <div>

            <label class="block text-sm mb-2">
                Frequency Days
            </label>

            <input
                type="number"
                bind:value={frequency_days}
                class="w-full rounded-xl border border-gray-700 bg-[#111827] p-3"
            />

        </div>

        <div>

            <label class="block text-sm mb-2">
                Start Date
            </label>

            <input
                type="date"
                bind:value={start_date}
                class="w-full rounded-xl border border-gray-700 bg-[#111827] p-3"
            />

        </div>

        <div class="flex items-center gap-6 mt-8">

            <label class="flex items-center gap-2">

                <input
                    type="checkbox"
                    bind:checked={recurring}
                />

                <span>
                    Recurring
                </span>

            </label>

            <label class="flex items-center gap-2">

                <input
                    type="checkbox"
                    bind:checked={auto_generate_work_orders}
                />

                <span>
                    Auto Generate WO
                </span>

            </label>

        </div>

        <div class="md:col-span-2">

            <label class="block text-sm mb-2">
                Equipment
            </label>

            <div class="rounded-2xl border border-gray-800 p-5 max-h-[320px] overflow-y-auto bg-[#111827]">

                <div class="grid grid-cols-1 md:grid-cols-2 gap-3">

                    {#each equipment as eq}

                        <label class="flex items-center gap-3 rounded-xl border border-gray-700 p-4 hover:border-emerald-500 transition">

                            <input
                                type="checkbox"
                                checked={selectedEquipmentIds.includes(eq.id)}
                                onchange={() =>
                                    toggleEquipment(eq.id)
                                }
                            />

                            <div>

                                <div class="font-medium text-white">
                                    {eq.asset_tag}
                                </div>

                                <div class="text-xs text-gray-500">
                                    {eq.model}
                                </div>

                            </div>

                        </label>

                    {/each}

                </div>

            </div>

        </div>

        <div class="md:col-span-2">

            <div class="flex items-center justify-between mb-3">

                <label class="block text-sm">
                    PM Task Templates
                </label>

                <button
                    type="button"
                    onclick={addTask}
                    class="text-emerald-500 text-sm"
                >
                    + Add Task
                </button>

            </div>

            <div class="space-y-3">

                {#each tasks as task, index}

                    <input
                        value={task.title}
                        oninput={(e) =>
                            updateTask(
                                index,
                                (e.currentTarget as HTMLInputElement).value
                            )
                        }
                        placeholder="Replace filters"
                        class="w-full rounded-xl border border-gray-700 bg-[#111827] p-3"
                    />

                {/each}

            </div>

        </div>

    </div>

    <div class="flex justify-end">

        <button
            onclick={submit}
            disabled={loading}
            class="bg-emerald-600 hover:bg-emerald-700 px-6 py-3 rounded-xl text-white"
        >
            {
                loading
                    ? 'Creating...'
                    : 'Create Maintenance Plan'
            }
        </button>

    </div>

</div>