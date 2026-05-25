<script lang="ts">

    import { createEventDispatcher } from 'svelte';

    import ModalShell
    from '$lib/components/ui/modal/ModalShell.svelte';

    import ModalHeader
    from '$lib/components/ui/modal/ModalHeader.svelte';

    import ModalFooter
    from '$lib/components/ui/modal/ModalFooter.svelte';

    import * as maintenanceApi
    from '$lib/api/maintenanceLogs';

    import {
        catalogsStore
    } from '$lib/stores/catalogs.store';

    const dispatch =
        createEventDispatcher();

    let {
        open = false,
        equipmentId
    } = $props<{
        open: boolean;
        equipmentId: string;
    }>();

    /*
    =========================================
    CATALOGS
    =========================================
    */

    const catalogs =
        catalogsStore;

    /*
    =========================================
    FORM
    =========================================
    */

    let saving =
        $state(false);

    let form = $state({

        maintenance_type_id: '',

        notes: '',

        equipment_condition: '',

        refrigerant_added: 0,

        measurements: [],

        components: []
    });

    /*
    =========================================
    MEASUREMENTS
    =========================================
    */

    function addMeasurement() {

        form.measurements = [

            ...form.measurements,

            {
                measurement_type: '',
                value: '',
                unit: ''
            }
        ];
    }

    function removeMeasurement(
        index: number
    ) {

        form.measurements =
            form.measurements.filter(
                (_, i) => i !== index
            );
    }

    /*
    =========================================
    COMPONENTS
    =========================================
    */

    function addComponent() {

        form.components = [

            ...form.components,

            {
                component_name: '',
                status: '',
                notes: ''
            }
        ];
    }

    function removeComponent(
        index: number
    ) {

        form.components =
            form.components.filter(
                (_, i) => i !== index
            );
    }

    /*
    =========================================
    SAVE
    =========================================
    */

    async function save() {

        try {

            saving = true;

            await maintenanceApi
                .createMaintenanceLog({

                    equipment_id:
                        equipmentId,

                    maintenance_type_id:
                        form.maintenance_type_id
                            ? Number(
                                form.maintenance_type_id
                            )
                            : null,

                    notes:
                        form.notes,

                    equipment_condition:
                        form.equipment_condition,

                    refrigerant_added:
                        Number(
                            form.refrigerant_added
                        ),

                    measurements:
                        form.measurements,

                    components:
                        form.components
                });

            dispatch('saved');

            close();

        } catch (error) {

            console.error(error);

        } finally {

            saving = false;
        }
    }

    /*
    =========================================
    CLOSE
    =========================================
    */

    function close() {

        dispatch('close');
    }

</script>

<ModalShell
    {open}
    width="max-w-6xl"
>

    <ModalHeader
        title="Add Maintenance Log"
        subtitle="HVAC enterprise maintenance record"
    />

    <!-- BODY -->

    <div
        class="max-h-[85vh] overflow-y-auto p-6 space-y-8"
    >

        <!-- GENERAL -->

        <div
            class="grid grid-cols-1 md:grid-cols-2 gap-6"
        >

            <!-- MAINTENANCE TYPE -->

            <div>

                <label
                    class="block text-sm font-medium mb-2"
                >
                    Maintenance Type
                </label>

                <select
                    bind:value={form.maintenance_type_id}
                    class="w-full rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 px-4 py-3"
                >

                    <option value="">
                        Select maintenance type
                    </option>

                    {#each $catalogs.maintenance_types as type}

                        <option
                            value={type.id}
                        >
                            {type.name}
                        </option>

                    {/each}

                </select>

            </div>

            <!-- CONDITION -->

            <div>

                <label
                    class="block text-sm font-medium mb-2"
                >
                    Equipment Condition
                </label>

                <select
                    bind:value={form.equipment_condition}
                    class="w-full rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 px-4 py-3"
                >

                    <option value="">
                        Select condition
                    </option>

                    <option value="Excellent">
                        Excellent
                    </option>

                    <option value="Good">
                        Good
                    </option>

                    <option value="Fair">
                        Fair
                    </option>

                    <option value="Critical">
                        Critical
                    </option>

                </select>

            </div>

        </div>

        <!-- NOTES -->

        <div>

            <label
                class="block text-sm font-medium mb-2"
            >
                Technician Notes
            </label>

            <textarea
                bind:value={form.notes}
                rows="5"
                class="w-full rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 px-4 py-3"
            />

        </div>

        <!-- REFRIGERANT -->

        <div>

            <label
                class="block text-sm font-medium mb-2"
            >
                Refrigerant Added
            </label>

            <input
                type="number"
                step="0.01"
                bind:value={form.refrigerant_added}
                class="w-full rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 px-4 py-3"
            />

        </div>

        <!-- MEASUREMENTS -->

        <div class="space-y-4">

            <div
                class="flex items-center justify-between"
            >

                <h3
                    class="text-lg font-semibold"
                >
                    Measurements
                </h3>

                <button
                    type="button"
                    onclick={addMeasurement}
                    class="px-4 py-2 rounded-xl bg-emerald-600 text-white text-sm"
                >
                    Add Measurement
                </button>

            </div>

            {#each form.measurements as measurement, index}

                <div
                    class="grid grid-cols-1 md:grid-cols-4 gap-4 border border-gray-200 dark:border-gray-800 rounded-2xl p-4"
                >

                    <input
                        bind:value={measurement.measurement_type}
                        placeholder="Measurement Type"
                        class="rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 px-4 py-3"
                    />

                    <input
                        bind:value={measurement.value}
                        placeholder="Value"
                        class="rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 px-4 py-3"
                    />

                    <input
                        bind:value={measurement.unit}
                        placeholder="Unit"
                        class="rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 px-4 py-3"
                    />

                    <button
                        onclick={() => removeMeasurement(index)}
                        class="rounded-xl bg-red-500 text-white"
                    >
                        Remove
                    </button>

                </div>

            {/each}

        </div>

        <!-- COMPONENTS -->

        <div class="space-y-4">

            <div
                class="flex items-center justify-between"
            >

                <h3
                    class="text-lg font-semibold"
                >
                    Components
                </h3>

                <button
                    type="button"
                    onclick={addComponent}
                    class="px-4 py-2 rounded-xl bg-emerald-600 text-white text-sm"
                >
                    Add Component
                </button>

            </div>

            {#each form.components as component, index}

                <div
                    class="grid grid-cols-1 md:grid-cols-4 gap-4 border border-gray-200 dark:border-gray-800 rounded-2xl p-4"
                >

                    <input
                        bind:value={component.component_name}
                        placeholder="Component"
                        class="rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 px-4 py-3"
                    />

                    <input
                        bind:value={component.status}
                        placeholder="Status"
                        class="rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 px-4 py-3"
                    />

                    <input
                        bind:value={component.notes}
                        placeholder="Notes"
                        class="rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 px-4 py-3"
                    />

                    <button
                        onclick={() => removeComponent(index)}
                        class="rounded-xl bg-red-500 text-white"
                    >
                        Remove
                    </button>

                </div>

            {/each}

        </div>

    </div>

    <!-- FOOTER -->

    <ModalFooter>

        <button
            onclick={close}
            class="px-5 py-3 rounded-xl border border-gray-300 dark:border-gray-700"
        >
            Cancel
        </button>

        <button
            onclick={save}
            disabled={saving}
            class="px-5 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white"
        >
            {saving
                ? 'Saving...'
                : 'Save Maintenance Log'}
        </button>

    </ModalFooter>

</ModalShell>