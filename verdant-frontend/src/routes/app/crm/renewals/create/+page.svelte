<script lang="ts">

    import { goto } from '$app/navigation';

    let loading = $state(false);

    let customer = $state('');
    let contract = $state('');

    let expiration_date = $state('');
    let renewal_value = $state<number | null>(null);

    let churn_risk = $state('MEDIUM');
    let renewal_probability = $state<number | null>(70);

    let sla_exposure = $state('HIGH');

    let assigned_manager = $state('');

    let follow_up_strategy = $state('');
    let notes = $state('');

    async function submit() {

        if (!customer) {
            alert('Customer required');
            return;
        }

        if (!contract) {
            alert('Contract required');
            return;
        }

        loading = true;

        try {

            console.log({

                customer,
                contract,
                expiration_date,
                renewal_value,
                churn_risk,
                renewal_probability,
                sla_exposure,
                assigned_manager,
                follow_up_strategy,
                notes
            });

            goto('/app/crm/renewals');

        } catch (e) {

            console.error(e);

            alert(
                'Failed to create renewal campaign'
            );

        } finally {

            loading = false;
        }
    }

</script>

<div class="p-6 max-w-5xl space-y-6">

    <!-- HEADER -->

    <div>

        <h1
            class="text-3xl font-bold text-white"
        >
            Create Renewal Campaign
        </h1>

        <p
            class="text-sm text-gray-400 mt-2"
        >
            Build contract renewal pipelines, churn prevention strategies and SLA retention workflows.
        </p>

    </div>

    <!-- FORM -->

    <div
        class="rounded-2xl border border-gray-800 bg-gray-900 p-6"
    >

        <div
            class="grid grid-cols-1 md:grid-cols-2 gap-5"
        >

            <!-- CUSTOMER -->

            <div>

                <label
                    class="block text-sm text-gray-300 mb-2"
                >
                    Customer
                </label>

                <input
                    bind:value={customer}
                    placeholder="Summit Medical"
                    class="w-full rounded-xl border border-gray-700 bg-gray-950 px-4 py-3 text-white"
                />

            </div>

            <!-- CONTRACT -->

            <div>

                <label
                    class="block text-sm text-gray-300 mb-2"
                >
                    Contract
                </label>

                <input
                    bind:value={contract}
                    placeholder="Enterprise Cooling SLA"
                    class="w-full rounded-xl border border-gray-700 bg-gray-950 px-4 py-3 text-white"
                />

            </div>

            <!-- EXPIRATION -->

            <div>

                <label
                    class="block text-sm text-gray-300 mb-2"
                >
                    Expiration Date
                </label>

                <input
                    type="date"
                    bind:value={expiration_date}
                    class="w-full rounded-xl border border-gray-700 bg-gray-950 px-4 py-3 text-white"
                />

            </div>

            <!-- VALUE -->

            <div>

                <label
                    class="block text-sm text-gray-300 mb-2"
                >
                    Renewal Value
                </label>

                <input
                    type="number"
                    bind:value={renewal_value}
                    placeholder="150000"
                    class="w-full rounded-xl border border-gray-700 bg-gray-950 px-4 py-3 text-white"
                />

            </div>

            <!-- CHURN -->

            <div>

                <label
                    class="block text-sm text-gray-300 mb-2"
                >
                    Churn Risk
                </label>

                <select
                    bind:value={churn_risk}
                    class="w-full rounded-xl border border-gray-700 bg-gray-950 px-4 py-3 text-white"
                >

                    <option>
                        LOW
                    </option>

                    <option>
                        MEDIUM
                    </option>

                    <option>
                        HIGH
                    </option>

                </select>

            </div>

            <!-- PROBABILITY -->

            <div>

                <label
                    class="block text-sm text-gray-300 mb-2"
                >
                    Renewal Probability (%)
                </label>

                <input
                    type="number"
                    bind:value={renewal_probability}
                    placeholder="70"
                    class="w-full rounded-xl border border-gray-700 bg-gray-950 px-4 py-3 text-white"
                />

            </div>

            <!-- SLA -->

            <div>

                <label
                    class="block text-sm text-gray-300 mb-2"
                >
                    SLA Exposure
                </label>

                <select
                    bind:value={sla_exposure}
                    class="w-full rounded-xl border border-gray-700 bg-gray-950 px-4 py-3 text-white"
                >

                    <option>
                        LOW
                    </option>

                    <option>
                        HIGH
                    </option>

                    <option>
                        CRITICAL
                    </option>

                </select>

            </div>

            <!-- MANAGER -->

            <div>

                <label
                    class="block text-sm text-gray-300 mb-2"
                >
                    Account Manager
                </label>

                <input
                    bind:value={assigned_manager}
                    placeholder="Sarah Chen"
                    class="w-full rounded-xl border border-gray-700 bg-gray-950 px-4 py-3 text-white"
                />

            </div>

            <!-- FOLLOW UP -->

            <div class="md:col-span-2">

                <label
                    class="block text-sm text-gray-300 mb-2"
                >
                    Follow-up Strategy
                </label>

                <textarea
                    rows="4"
                    bind:value={follow_up_strategy}
                    placeholder="PM upgrade + SLA extension + refrigerant compliance optimization..."
                    class="w-full rounded-xl border border-gray-700 bg-gray-950 px-4 py-3 text-white"
                ></textarea>

            </div>

            <!-- NOTES -->

            <div class="md:col-span-2">

                <label
                    class="block text-sm text-gray-300 mb-2"
                >
                    Internal Notes
                </label>

                <textarea
                    rows="5"
                    bind:value={notes}
                    placeholder="Customer retention observations..."
                    class="w-full rounded-xl border border-gray-700 bg-gray-950 px-4 py-3 text-white"
                ></textarea>

            </div>

        </div>

    </div>

    <!-- ACTIONS -->

    <div
        class="flex justify-end gap-3"
    >

        <button
            onclick={() =>
                goto('/app/crm/renewals')
            }
            class="px-5 py-3 rounded-xl border border-gray-700 text-gray-300 hover:bg-gray-800"
        >
            Cancel
        </button>

        <button
            onclick={submit}
            disabled={loading}
            class="px-5 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-medium disabled:opacity-50"
        >
            {loading
                ? 'Creating...'
                : 'Create Renewal Campaign'}
        </button>

    </div>

</div>