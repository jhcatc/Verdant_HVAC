<script lang="ts">

    import { onMount } from 'svelte';

    import { goto } from '$app/navigation';

    import * as equipmentApi from '$lib/api/equipment';

    import {
        catalogsStore
    } from '$lib/stores/catalogs.store';

    /*
    =========================================
    LOAD CATALOGS
    =========================================
    */

    onMount(async () => {

        await catalogsStore.load();
    });

    /*
    =========================================
    FORM
    =========================================
    */

    let form = {

        asset_tag: '',
        customer_id: '',
        location_id: '',
        category: '',
        type: '',
        brand: '',
        model: '',
        serial_number: '',
        manufacture_year: '',
        installation_date: '',
        refrigerant: '',
        capacity: '',
        capacity_unit: 'BTU',
        voltage: '',
        phase: '',
        power_source: '',
        installation_type: '',
        status: '',
        equipment_location: '',
        maintenance_interval: '',
        warranty_expiration: '',
        notes: '',

        /*
        HVAC
        */

        seer_rating: '',
        eer_rating: '',
        cooling_capacity: '',
        heating_capacity: '',
        line_set_size: '',
        drain_type: '',

        /*
        BOILER
        */

        water_capacity: '',
        max_temperature: '',
        working_pressure: '',
        fuel_type: '',
        burner_type: '',

        /*
        VENTILATION
        */

        airflow_cfm: '',
        static_pressure: '',
        duct_size: '',
        fan_speed_rpm: '',
        motor_hp: ''
    };

    const maintenanceIntervals = [

        '30 Days',
        '60 Days',
        '90 Days',
        '180 Days',
        '365 Days'
    ];

    /*
    =========================================
    HELPERS
    =========================================
    */

    function getSelectedEquipmentType() {

        return catalogsStore.catalogs
            ?.equipment_types
            ?.find(
                (type) =>
                    type.id === Number(form.type)
            );
    }

    function isCoolingEquipment() {

        const type =
            getSelectedEquipmentType();

        if (!type) {
            return false;
        }

        return [
            'Mini Split',
            'Multi Split',
            'VRF',
            'VRV',
            'Rooftop',
            'Chiller',
            'Package Unit',
            'Cassette',
            'PTAC',
            'Window AC',
            'Portable AC'
        ].includes(type.name);
    }

    function isBoiler() {

        const type =
            getSelectedEquipmentType();

        return type?.name === 'Boiler';
    }

    function isVentilation() {

        const type =
            getSelectedEquipmentType();

        if (!type) {
            return false;
        }

        return [
            'Extractor',
            'Air Handler',
            'Fan Coil'
        ].includes(type.name);
    }

    function equipmentTypes() {

        if (!form.category) {
            return [];
        }

        return catalogsStore.getEquipmentTypesByCategory(
            Number(form.category)
        ) || [];
    }

    /*
    =========================================
    SAVE
    =========================================
    */

    async function saveEquipment() {

        try {

            const payload = {

                customer_id: null,
                location_id: null,

                equipment_category_id:
                    form.category
                        ? Number(form.category)
                        : null,

                equipment_type_id:
                    form.type
                        ? Number(form.type)
                        : null,

                brand_id:
                    form.brand
                        ? Number(form.brand)
                        : null,

                refrigerant_type_id:
                    form.refrigerant
                        ? Number(form.refrigerant)
                        : null,

                voltage_type_id:
                    form.voltage
                        ? Number(form.voltage)
                        : null,

                power_source_id:
                    form.power_source
                        ? Number(form.power_source)
                        : null,

                installation_type_id:
                    form.installation_type
                        ? Number(form.installation_type)
                        : null,

                equipment_status_id:
                    form.status
                        ? Number(form.status)
                        : null,

                asset_tag:
                    form.asset_tag,

                model:
                    form.model,

                serial_number:
                    form.serial_number,

                manufacture_year:
                    form.manufacture_year
                        ? Number(form.manufacture_year)
                        : null,

                installation_date:
                    form.installation_date || null,

                warranty_expiration:
                    form.warranty_expiration || null,

                maintenance_interval_days: 90,

                capacity:
                    form.capacity,

                capacity_unit:
                    form.capacity_unit,

                phase_type:
                    form.phase,

                equipment_location:
                    form.equipment_location,

                notes:
                    form.notes,

                /*
                HVAC
                */

                seer_rating:
                    form.seer_rating
                        ? Number(form.seer_rating)
                        : null,

                eer_rating:
                    form.eer_rating
                        ? Number(form.eer_rating)
                        : null,

                cooling_capacity:
                    form.cooling_capacity,

                heating_capacity:
                    form.heating_capacity,

                line_set_size:
                    form.line_set_size,

                drain_type:
                    form.drain_type,

                /*
                BOILER
                */

                water_capacity:
                    form.water_capacity,

                max_temperature:
                    form.max_temperature,

                working_pressure:
                    form.working_pressure,

                fuel_type:
                    form.fuel_type,

                burner_type:
                    form.burner_type,

                /*
                VENTILATION
                */

                airflow_cfm:
                    form.airflow_cfm,

                static_pressure:
                    form.static_pressure,

                duct_size:
                    form.duct_size,

                fan_speed_rpm:
                    form.fan_speed_rpm,

                motor_hp:
                    form.motor_hp
            };

            await equipmentApi.createEquipment(
                payload
            );

            alert('Equipment saved');

            goto(
                '/app/infrastructure/equipment'
            );

        } catch (error) {

            console.error(error);

            alert(
                'Failed to save equipment'
            );
        }
    }

</script>
{#if catalogsStore.loading}

<div class="p-10 flex items-center justify-center">

    <div class="text-sm text-gray-500">

        Loading catalogs...

    </div>

</div>

{:else}
<div class="p-6 space-y-6">

    <!-- HEADER -->
    <div class="flex items-center justify-between">

        <div>
            <h1 class="text-2xl font-bold text-gray-800 dark:text-white">
                Create Equipment
            </h1>

            <p class="text-sm text-gray-500 dark:text-gray-400">
                Enterprise HVAC Asset Registration
            </p>
        </div>

        <button
            on:click={() => goto('/app/infrastructure/equipment')}
            class="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-800"
        >
            Back
        </button>

    </div>

    <!-- FORM -->
    <div class="bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-800 p-6">

        <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">

            <!-- ASSET TAG -->
            <div>
                <label class="block mb-2 text-sm font-medium">
                    Asset Tag
                </label>

                <input
                    bind:value={form.asset_tag}
                    placeholder="AC-001"
                    class="w-full px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
                />
            </div>

            <!-- CUSTOMER -->
            <div>
                <label class="block mb-2 text-sm font-medium">
                    Customer
                </label>

                <select
                    bind:value={form.customer_id}
                    class="w-full px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
                >
                    <option value="">Select Customer</option>
                </select>
            </div>

            <!-- LOCATION -->
            <div>
                <label class="block mb-2 text-sm font-medium">
                    Location / Headquarters
                </label>

                <select
                    bind:value={form.location_id}
                    class="w-full px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
                >
                    <option value="">Select Location</option>
                </select>
            </div>

            <!-- CATEGORY -->
            <div>
                <label class="block mb-2 text-sm font-medium">
                    Category
                </label>

                <select
                    bind:value={form.category}
                    class="w-full px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
                >
                    <option value="">Select Category</option>

                    {#each catalogsStore.catalogs?.equipment_categories ?? [] as category}
                        <option value={category.id}>
                            {category.name}
                        </option>
                    {/each}
                </select>
            </div>

            <!-- TYPE -->
            <div>
                <label class="block mb-2 text-sm font-medium">
                    Equipment Type
                </label>

                <select
                    bind:value={form.type}
                    class="w-full px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
                >
                    <option value="">Select Type</option>

                    {#each equipmentTypes() as type}

                        <option value={type.id}>
                            {type.name}
                        </option>

                    {/each}
                </select>
            </div>

            <!-- BRAND -->
            <div>
                <label class="block mb-2 text-sm font-medium">
                    Brand
                </label>

                <select
                    bind:value={form.brand}
                    class="w-full px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
                >
                    <option value="">Select Brand</option>

                    {#each catalogsStore.catalogs?.brands ?? [] as brand}

                    <option value={brand.id}>
                        {brand.name}
                    </option>

                    {/each}
                                    </select>
            </div>

            <!-- MODEL -->
            <div>
                <label class="block mb-2 text-sm font-medium">
                    Model
                </label>

                <input
                    bind:value={form.model}
                    placeholder="MSZ-GL12NA"
                    class="w-full px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
                />
            </div>

            <!-- SERIAL -->
            <div>
                <label class="block mb-2 text-sm font-medium">
                    Serial Number
                </label>

                <input
                    bind:value={form.serial_number}
                    placeholder="SN-0001"
                    class="w-full px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
                />
            </div>

            <!-- YEAR -->
            <div>
                <label class="block mb-2 text-sm font-medium">
                    Manufacture Year
                </label>

                <input
                    bind:value={form.manufacture_year}
                    type="number"
                    class="w-full px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
                />
            </div>

            <!-- INSTALL DATE -->
            <div>
                <label class="block mb-2 text-sm font-medium">
                    Installation Date
                </label>

                <input
                    bind:value={form.installation_date}
                    type="date"
                    class="w-full px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
                />
            </div>

            <!-- REFRIGERANT -->
            <div>
                <label class="block mb-2 text-sm font-medium">
                    Refrigerant
                </label>

                <select
                    bind:value={form.refrigerant}
                    class="w-full px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
                >
                    <option value="">
                        Select Refrigerant
                    </option>

                    {#each catalogsStore.catalogs?.refrigerants ?? [] as refrigerant}

                        <option value={refrigerant.id}>
                            {refrigerant.name}
                        </option>

                    {/each}
                </select>
            </div>

            <!-- CAPACITY -->
            <div>
                <label class="block mb-2 text-sm font-medium">
                    Capacity
                </label>

                <input
                    bind:value={form.capacity}
                    placeholder="12000"
                    class="w-full px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
                />
            </div>

            <!-- VOLTAGE -->
            <div>
                <label class="block mb-2 text-sm font-medium">
                    Voltage
                </label>

                <select
                    bind:value={form.voltage}
                    class="w-full px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
                >
                    <option value="">Select Voltage</option>

                    {#each catalogsStore.catalogs?.voltages ?? [] as voltage}
                        <option value={voltage.id}>
                             {voltage.name}
                        </option>
                    {/each}
                </select>
            </div>

            <!-- POWER SOURCE -->
            <div>
                <label class="block mb-2 text-sm font-medium">
                    Power Source
                </label>

                <select
                    bind:value={form.power_source}
                    class="w-full px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
                >
                    <option value="">Select Power Source</option>

                    <option value="">
                        Select Power Source
                    </option>

                    {#each catalogsStore.catalogs?.power_sources ?? [] as source}

                        <option value={source.id}>
                            {source.name}
                        </option>

                    {/each}
                </select>
            </div>

            <!-- STATUS -->
            <div>
                <label class="block mb-2 text-sm font-medium">
                    Status
                </label>

                <select
                    bind:value={form.status}
                    class="w-full px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
                >
                    <option value="">
                        Select Status
                    </option>

                    {#each catalogsStore.catalogs?.statuses ?? [] as status}

                        <option value={status.id}>
                            {status.name}
                        </option>

                    {/each}
                </select>
            </div>

            <!-- INSTALLATION TYPE -->
            <div>
                <label class="block mb-2 text-sm font-medium">
                    Installation Type
                </label>

                <select
                    bind:value={form.installation_type}
                    class="w-full px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
                >
                    <option value="">Select Installation Type</option>

                    {#each catalogsStore.catalogs?.installation_types ?? [] as type}
                        <option value={type.id}>
                            {type.name}
                        </option>
                    {/each}
                </select>
            </div>

            <!-- LOCATION -->
            <div>
                <label class="block mb-2 text-sm font-medium">
                    Equipment Location
                </label>

                <input
                    bind:value={form.equipment_location}
                    placeholder="Roof / Mechanical Room"
                    class="w-full px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
                />
            </div>

            <!-- MAINTENANCE -->
            <div>
                <label class="block mb-2 text-sm font-medium">
                    Maintenance Interval
                </label>

                <select
                    bind:value={form.maintenance_interval}
                    class="w-full px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
                >
                    <option value="">Select Interval</option>

                    {#each maintenanceIntervals as interval}
                        <option value={interval}>
                            {interval}
                        </option>
                    {/each}
                </select>
            </div>

            <!-- WARRANTY -->
            <div>
                <label class="block mb-2 text-sm font-medium">
                    Warranty Expiration
                </label>

                <input
                    bind:value={form.warranty_expiration}
                    type="date"
                    class="w-full px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
                />
            </div>

        </div>

        <!-- HVAC -->
        {#if isCoolingEquipment()}

            <div class="mt-10">

                <h2 class="text-xl font-semibold mb-5">
                    HVAC Specifications
                </h2>

                <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">

                    <input
                        bind:value={form.seer_rating}
                        placeholder="SEER Rating"
                        class="px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
                    />

                    <input
                        bind:value={form.eer_rating}
                        placeholder="EER Rating"
                        class="px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
                    />

                    <input
                        bind:value={form.cooling_capacity}
                        placeholder="Cooling Capacity"
                        class="px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
                    />

                    <input
                        bind:value={form.heating_capacity}
                        placeholder="Heating Capacity"
                        class="px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
                    />

                    <input
                        bind:value={form.line_set_size}
                        placeholder="Line Set Size"
                        class="px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
                    />

                    <input
                        bind:value={form.drain_type}
                        placeholder="Drain Type"
                        class="px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
                    />

                </div>

            </div>

        {/if}

        <!-- BOILER -->
        {#if isBoiler()}

            <div class="mt-10">

                <h2 class="text-xl font-semibold mb-5">
                    Boiler Specifications
                </h2>

                <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">

                    <input
                        bind:value={form.water_capacity}
                        placeholder="Water Capacity"
                        class="px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
                    />

                    <input
                        bind:value={form.max_temperature}
                        placeholder="Max Temperature"
                        class="px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
                    />

                    <input
                        bind:value={form.working_pressure}
                        placeholder="Working Pressure"
                        class="px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
                    />

                    <input
                        bind:value={form.fuel_type}
                        placeholder="Fuel Type"
                        class="px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
                    />

                    <input
                        bind:value={form.burner_type}
                        placeholder="Burner Type"
                        class="px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
                    />

                </div>

            </div>

        {/if}

        <!-- VENTILATION -->
        {#if isVentilation()}

            <div class="mt-10">

                <h2 class="text-xl font-semibold mb-5">
                    Ventilation Specifications
                </h2>

                <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">

                    <input
                        bind:value={form.airflow_cfm}
                        placeholder="Airflow CFM"
                        class="px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
                    />

                    <input
                        bind:value={form.static_pressure}
                        placeholder="Static Pressure"
                        class="px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
                    />

                    <input
                        bind:value={form.duct_size}
                        placeholder="Duct Size"
                        class="px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
                    />

                    <input
                        bind:value={form.fan_speed_rpm}
                        placeholder="Fan Speed RPM"
                        class="px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
                    />

                    <input
                        bind:value={form.motor_hp}
                        placeholder="Motor HP"
                        class="px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
                    />

                </div>

            </div>

        {/if}

        <!-- NOTES -->
        <div class="mt-10">

            <label class="block mb-2 text-sm font-medium">
                Notes
            </label>

            <textarea
                bind:value={form.notes}
                rows="5"
                class="w-full px-4 py-3 rounded-2xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
            ></textarea>

        </div>

        <!-- ACTIONS -->
        <div class="mt-10 flex items-center justify-end gap-3">

            <button
                on:click={() => goto('/app/infrastructure/equipment')}
                class="px-5 py-2 rounded-xl border border-gray-300 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-800"
            >
                Cancel
            </button>

            <button
                on:click={saveEquipment}
                class="px-5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white"
            >
                Save Equipment
            </button>

        </div>

    </div>

</div>

{/if}