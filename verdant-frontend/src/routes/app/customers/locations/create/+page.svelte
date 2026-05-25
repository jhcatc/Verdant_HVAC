<script lang="ts">

    import { goto } from '$app/navigation';

    import CustomerAutocomplete
        from '$lib/components/customer/CustomerAutocomplete.svelte';

    import { createLocation }
        from '$lib/api/customerLocations';

    let loading = $state(false);

    let selectedCustomer = $state<any>(null);

    let name = $state('');
    let code = $state('');

    let address = $state('');
    let city = $state('');
    let state = $state('');
    let zip_code = $state('');
    let country = $state('');

    let contact_name = $state('');
    let contact_phone = $state('');
    let contact_email = $state('');

    let sla_tier = $state('STANDARD');

    let access_notes = $state('');
    let refrigerant_notes = $state('');
    let technician_notes = $state('');
    let notes = $state('');

    async function submit() {

        if (!selectedCustomer) {

            alert('Select customer');
            return;
        }

        if (!name.trim()) {

            alert('Location name required');
            return;
        }

        loading = true;

        try {

            await createLocation({

                customer_id: selectedCustomer.id,

                name,
                code,

                address,
                city,
                state,
                zip_code,
                country,

                contact_name,
                contact_phone,
                contact_email,

                sla_tier,

                access_notes,
                refrigerant_notes,
                technician_notes,

                notes
            });

            goto('/app/customers/locations');

        } catch (e) {

            console.error(e);

            alert(
                'Failed to create location'
            );

        } finally {

            loading = false;
        }
    }

</script>

<div class="p-6">

    <div class="max-w-7xl mx-auto space-y-6">

        <!-- ================================================= -->
        <!-- HEADER -->
        <!-- ================================================= -->

        <div
            class="rounded-2xl border border-gray-800 bg-gray-900 p-6"
        >

            <div class="flex items-start justify-between">

                <div>

                    <h1 class="text-3xl font-bold text-white">
                        Create Facility
                    </h1>

                    <p class="text-sm text-gray-400 mt-2">
                        Register operational facilities, branches,
                        plants and HVAC service locations.
                    </p>

                </div>

                <button
                    onclick={() => goto('/app/customers/locations')}
                    class="px-4 py-2 rounded-xl bg-gray-800 hover:bg-gray-700 text-white text-sm"
                >
                    Back
                </button>

            </div>

        </div>

        <!-- ================================================= -->
        <!-- FORM -->
        <!-- ================================================= -->

        <div
            class="rounded-2xl border border-gray-800 bg-gray-900 overflow-hidden"
        >

            <div class="px-6 py-4 border-b border-gray-800">

                <h2 class="text-lg font-semibold text-white">
                    Facility Information
                </h2>

            </div>

            <div class="p-6">

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">

                    <!-- CUSTOMER -->

                    <div class="md:col-span-2">

                        <label
                            class="block text-xs uppercase tracking-wider text-gray-500 mb-2"
                        >
                            Customer
                        </label>

                        <CustomerAutocomplete
                            onSelect={(c) => selectedCustomer = c}
                        />

                    </div>

                    <!-- LOCATION NAME -->

                    <div>

                        <label
                            class="block text-xs uppercase tracking-wider text-gray-500 mb-2"
                        >
                            Facility Name
                        </label>

                        <input
                            bind:value={name}
                            placeholder="Miami Distribution Center"
                            class="w-full rounded-xl border border-gray-700 bg-gray-950 px-4 py-3 text-white outline-none focus:border-emerald-500"
                        />

                    </div>

                    <!-- CODE -->

                    <div>

                        <label
                            class="block text-xs uppercase tracking-wider text-gray-500 mb-2"
                        >
                            Facility Code
                        </label>

                        <input
                            bind:value={code}
                            placeholder="MIA-DC-01"
                            class="w-full rounded-xl border border-gray-700 bg-gray-950 px-4 py-3 text-white outline-none focus:border-emerald-500"
                        />

                    </div>

                    <!-- ADDRESS -->

                    <div class="md:col-span-2">

                        <label
                            class="block text-xs uppercase tracking-wider text-gray-500 mb-2"
                        >
                            Address
                        </label>

                        <input
                            bind:value={address}
                            class="w-full rounded-xl border border-gray-700 bg-gray-950 px-4 py-3 text-white outline-none focus:border-emerald-500"
                        />

                    </div>

                    <!-- CITY -->

                    <div>

                        <label
                            class="block text-xs uppercase tracking-wider text-gray-500 mb-2"
                        >
                            City
                        </label>

                        <input
                            bind:value={city}
                            class="w-full rounded-xl border border-gray-700 bg-gray-950 px-4 py-3 text-white outline-none focus:border-emerald-500"
                        />

                    </div>

                    <!-- STATE -->

                    <div>

                        <label
                            class="block text-xs uppercase tracking-wider text-gray-500 mb-2"
                        >
                            State
                        </label>

                        <input
                            bind:value={state}
                            class="w-full rounded-xl border border-gray-700 bg-gray-950 px-4 py-3 text-white outline-none focus:border-emerald-500"
                        />

                    </div>

                    <!-- ZIP -->

                    <div>

                        <label
                            class="block text-xs uppercase tracking-wider text-gray-500 mb-2"
                        >
                            ZIP Code
                        </label>

                        <input
                            bind:value={zip_code}
                            class="w-full rounded-xl border border-gray-700 bg-gray-950 px-4 py-3 text-white outline-none focus:border-emerald-500"
                        />

                    </div>

                    <!-- COUNTRY -->

                    <div>

                        <label
                            class="block text-xs uppercase tracking-wider text-gray-500 mb-2"
                        >
                            Country
                        </label>

                        <input
                            bind:value={country}
                            class="w-full rounded-xl border border-gray-700 bg-gray-950 px-4 py-3 text-white outline-none focus:border-emerald-500"
                        />

                    </div>

                </div>

            </div>

        </div>

        <!-- ================================================= -->
        <!-- CONTACT + SLA -->
        <!-- ================================================= -->

        <div class="grid grid-cols-1 xl:grid-cols-2 gap-6">

            <!-- CONTACT -->

            <div
                class="rounded-2xl border border-gray-800 bg-gray-900 overflow-hidden"
            >

                <div class="px-6 py-4 border-b border-gray-800">

                    <h2 class="text-lg font-semibold text-white">
                        Primary Contact
                    </h2>

                </div>

                <div class="p-6 space-y-5">

                    <div>

                        <label
                            for="contact_name"
                            class="block text-xs uppercase tracking-wider text-gray-500 mb-2"
                        >
                            Contact Name
                        </label>

                        <input
                            id="contact_name"
                            bind:value={contact_name}
                            class="w-full rounded-xl border border-gray-700 bg-gray-950 px-4 py-3 text-white"
                        />

                    </div>

                    <div>

                        <label
                            class="block text-xs uppercase tracking-wider text-gray-500 mb-2"
                        >
                            Contact Phone
                        </label>

                        <input
                            bind:value={contact_phone}
                            class="w-full rounded-xl border border-gray-700 bg-gray-950 px-4 py-3 text-white"
                        />

                    </div>

                    <div>

                        <label
                            class="block text-xs uppercase tracking-wider text-gray-500 mb-2"
                        >
                            Contact Email
                        </label>

                        <input
                            bind:value={contact_email}
                            class="w-full rounded-xl border border-gray-700 bg-gray-950 px-4 py-3 text-white"
                        />

                    </div>

                </div>

            </div>

            <!-- SLA -->

            <div
                class="rounded-2xl border border-gray-800 bg-gray-900 overflow-hidden"
            >

                <div class="px-6 py-4 border-b border-gray-800">

                    <h2 class="text-lg font-semibold text-white">
                        SLA & Compliance
                    </h2>

                </div>

                <div class="p-6 space-y-5">

                    <div>

                        <label
                            class="block text-xs uppercase tracking-wider text-gray-500 mb-2"
                        >
                            SLA Tier
                        </label>

                        <select
                            bind:value={sla_tier}
                            class="w-full rounded-xl border border-gray-700 bg-gray-950 px-4 py-3 text-white"
                        >
                            <option value="STANDARD">
                                STANDARD
                            </option>

                            <option value="GOLD">
                                GOLD
                            </option>

                            <option value="PLATINUM">
                                PLATINUM
                            </option>

                            <option value="24/7 CRITICAL">
                                24/7 CRITICAL
                            </option>

                        </select>

                    </div>

                    <div>

                        <label
                            class="block text-xs uppercase tracking-wider text-gray-500 mb-2"
                        >
                            Refrigerant Compliance
                        </label>

                        <textarea
                            bind:value={refrigerant_notes}
                            rows="4"
                            class="w-full rounded-xl border border-gray-700 bg-gray-950 px-4 py-3 text-white"
                        ></textarea>

                    </div>

                </div>

            </div>

        </div>

        <!-- ================================================= -->
        <!-- SITE NOTES -->
        <!-- ================================================= -->

        <div
            class="rounded-2xl border border-gray-800 bg-gray-900 overflow-hidden"
        >

            <div class="px-6 py-4 border-b border-gray-800">

                <h2 class="text-lg font-semibold text-white">
                    Site Access & Operational Notes
                </h2>

            </div>

            <div class="p-6 grid grid-cols-1 xl:grid-cols-3 gap-6">

                <div>

                    <label
                        class="block text-xs uppercase tracking-wider text-gray-500 mb-2"
                    >
                        Site Access Notes
                    </label>

                    <textarea
                        bind:value={access_notes}
                        rows="6"
                        class="w-full rounded-xl border border-gray-700 bg-gray-950 px-4 py-3 text-white"
                    ></textarea>

                </div>

                <div>

                    <label
                        class="block text-xs uppercase tracking-wider text-gray-500 mb-2"
                    >
                        Technician Notes
                    </label>

                    <textarea
                        bind:value={technician_notes}
                        rows="6"
                        class="w-full rounded-xl border border-gray-700 bg-gray-950 px-4 py-3 text-white"
                    ></textarea>

                </div>

                <div>

                    <label
                        class="block text-xs uppercase tracking-wider text-gray-500 mb-2"
                    >
                        Internal Notes
                    </label>

                    <textarea
                        bind:value={notes}
                        rows="6"
                        class="w-full rounded-xl border border-gray-700 bg-gray-950 px-4 py-3 text-white"
                    ></textarea>

                </div>

            </div>

        </div>

        <!-- ================================================= -->
        <!-- ACTIONS -->
        <!-- ================================================= -->

        <div class="flex justify-end gap-3">

            <button
                onclick={() => goto('/app/customers/locations')}
                class="px-5 py-3 rounded-xl border border-gray-700 bg-gray-900 hover:bg-gray-800 text-white"
            >
                Cancel
            </button>

            <button
                onclick={submit}
                disabled={loading}
                class="px-5 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white disabled:opacity-50"
            >
                {loading ? 'Creating Facility...' : 'Create Facility'}
            </button>

        </div>

    </div>

</div>