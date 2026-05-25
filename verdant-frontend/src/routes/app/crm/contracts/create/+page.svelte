<script lang="ts">

    import { goto } from '$app/navigation';

    import {
        createContract
    } from '$lib/api/crm/contracts';

    let loading = $state(false);

    let customer_id = $state('');

    let status = $state('ACTIVE');

    let total_value =
        $state<number | null>(null);

    let sla_tier = $state('STANDARD');

    let start_date = $state('');

    let end_date = $state('');

    let renewal_date = $state('');

    async function submit() {

        if (!customer_id) {

            alert('Customer ID required');

            return;
        }

        loading = true;

        try {

            await createContract({

                customer_id,

                status,

                total_value:
                    total_value || 0,

                sla_tier,

                start_date:
                    start_date || null,

                end_date:
                    end_date || null,

                renewal_date:
                    renewal_date || null
            });

            goto('/app/crm/contracts');

        } catch (e) {

            console.error(e);

            alert(
                'Failed creating contract'
            );

        } finally {

            loading = false;
        }
    }

</script>

<div class="p-6 max-w-4xl">

    <div class="mb-8">

        <h1
            class="text-3xl font-bold text-white"
        >
            Create Contract
        </h1>

        <p
            class="text-sm text-gray-400 mt-2"
        >
            Create enterprise HVAC contracts
            using the normalized CRM DTO flow.
        </p>

    </div>

    <div
        class="
            rounded-2xl
            border
            border-gray-800
            bg-gray-900
            p-6
        "
    >

        <div
            class="
                grid
                grid-cols-1
                md:grid-cols-2
                gap-5
            "
        >

            <div>

                <label
                    class="
                        block
                        mb-2
                        text-sm
                        text-white
                    "
                >
                    Customer ID
                </label>

                <input
                    bind:value={customer_id}
                    class="
                        w-full
                        px-4
                        py-3
                        rounded-xl
                        border
                        border-gray-700
                        bg-gray-950
                        text-white
                    "
                />

            </div>

            <div>

                <label
                    class="
                        block
                        mb-2
                        text-sm
                        text-white
                    "
                >
                    Status
                </label>

                <select
                    bind:value={status}
                    class="
                        w-full
                        px-4
                        py-3
                        rounded-xl
                        border
                        border-gray-700
                        bg-gray-950
                        text-white
                    "
                >

                    <option value="ACTIVE">
                        ACTIVE
                    </option>

                    <option value="RENEWAL">
                        RENEWAL
                    </option>

                    <option value="EXPIRED">
                        EXPIRED
                    </option>

                </select>

            </div>

            <div>

                <label
                    class="
                        block
                        mb-2
                        text-sm
                        text-white
                    "
                >
                    SLA Tier
                </label>

                <select
                    bind:value={sla_tier}
                    class="
                        w-full
                        px-4
                        py-3
                        rounded-xl
                        border
                        border-gray-700
                        bg-gray-950
                        text-white
                    "
                >

                    <option value="STANDARD">
                        STANDARD
                    </option>

                    <option value="HIGH">
                        HIGH
                    </option>

                    <option value="CRITICAL">
                        CRITICAL
                    </option>

                </select>

            </div>

            <div>

                <label
                    class="
                        block
                        mb-2
                        text-sm
                        text-white
                    "
                >
                    Total Value
                </label>

                <input
                    type="number"
                    bind:value={total_value}
                    class="
                        w-full
                        px-4
                        py-3
                        rounded-xl
                        border
                        border-gray-700
                        bg-gray-950
                        text-white
                    "
                />

            </div>

            <div>

                <label
                    class="
                        block
                        mb-2
                        text-sm
                        text-white
                    "
                >
                    Start Date
                </label>

                <input
                    type="date"
                    bind:value={start_date}
                    class="
                        w-full
                        px-4
                        py-3
                        rounded-xl
                        border
                        border-gray-700
                        bg-gray-950
                        text-white
                    "
                />

            </div>

            <div>

                <label
                    class="
                        block
                        mb-2
                        text-sm
                        text-white
                    "
                >
                    End Date
                </label>

                <input
                    type="date"
                    bind:value={end_date}
                    class="
                        w-full
                        px-4
                        py-3
                        rounded-xl
                        border
                        border-gray-700
                        bg-gray-950
                        text-white
                    "
                />

            </div>

            <div>

                <label
                    class="
                        block
                        mb-2
                        text-sm
                        text-white
                    "
                >
                    Renewal Date
                </label>

                <input
                    type="date"
                    bind:value={renewal_date}
                    class="
                        w-full
                        px-4
                        py-3
                        rounded-xl
                        border
                        border-gray-700
                        bg-gray-950
                        text-white
                    "
                />

            </div>

        </div>

        <div
            class="
                flex
                justify-end
                gap-3
                mt-8
            "
        >

            <button
                onclick={() =>
                    goto('/app/crm/contracts')
                }
                class="
                    px-5
                    py-3
                    rounded-xl
                    border
                    border-gray-700
                    text-white
                "
            >
                Cancel
            </button>

            <button
                onclick={submit}
                disabled={loading}
                class="
                    px-5
                    py-3
                    rounded-xl
                    bg-emerald-600
                    hover:bg-emerald-700
                    text-white
                "
            >
                {loading
                    ? 'Creating...'
                    : 'Create Contract'}
            </button>

        </div>

    </div>

</div>