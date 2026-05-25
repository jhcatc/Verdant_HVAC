<script lang="ts">

    import { goto } from '$app/navigation';
    import {
        createLead
    } from '$lib/api/crm/leads';
    let loading = $state(false);
    let title = $state('');
    let company = $state('');
    let email = $state('');
    let city = $state('');
    let source = $state('REFERRAL');
    let estimated_value = $state<number>(0);
    let probability = $state<number>(10);
    let assigned_rep = $state('');
    async function submit() {
        if (!title.trim()) {
            alert(
                'Lead title required'
            );
            return;
        }

        if (!company.trim()) {
            alert(
                'Company required'
            );

            return;
        }
        loading = true;
        try {
            const payload = {
                title:
                    title.trim(),
                company:
                    company.trim(),
                email:
                    email.trim() || null,
                city:
                    city.trim() || null,
                source,
                estimated_value:
                    Number(estimated_value) || 0,
                probability:
                    Number(probability) || 0,
                assigned_rep:
                    assigned_rep.trim() || null
            };
            console.log(
                'Creating lead payload:',
                payload
            );
            await createLead(payload);
            await goto(
                '/app/crm/leads'
            );
        } catch (err: any) {
            console.error(
                'Lead creation error:',
                err
            );
            let message =
                'Failed creating lead';
            if (
                Array.isArray(
                    err?.response?.data?.detail
                )
            ) {
                message =
                    err.response.data.detail
                        .map((x: any) => {

                            const field =
                                x.loc?.join('.') || 'field';

                            return `${field}: ${x.msg}`;
                        })
                        .join('\n');

            } else if (
                typeof err?.response?.data?.detail
                === 'string'
            ) {

                message =
                    err.response.data.detail;
            }

            alert(message);

        } finally {

            loading = false;
        }
    }

</script>

<div
    class="
        p-6
        max-w-5xl
        mx-auto
        space-y-6
    "
>

    <div>

        <h1
            class="
                text-3xl
                font-bold
                text-white
            "
        >
            Create Lead
        </h1>

        <p
            class="
                text-sm
                text-gray-400
                mt-2
            "
        >
            Create enterprise HVAC sales leads
            and qualification opportunities.
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

            <!-- TITLE -->

            <div>

                <label
                    class="
                        block
                        text-sm
                        font-medium
                        text-gray-300
                        mb-2
                    "
                >
                    Lead Title
                </label>

                <input
                    bind:value={title}
                    placeholder="
                        HVAC Upgrade Project
                    "
                    class="
                        w-full
                        rounded-xl
                        border
                        border-gray-700
                        bg-gray-950
                        px-4
                        py-3
                        text-white
                    "
                />

            </div>

            <!-- COMPANY -->

            <div>

                <label
                    class="
                        block
                        text-sm
                        font-medium
                        text-gray-300
                        mb-2
                    "
                >
                    Company
                </label>

                <input
                    bind:value={company}
                    placeholder="
                        Customer company
                    "
                    class="
                        w-full
                        rounded-xl
                        border
                        border-gray-700
                        bg-gray-950
                        px-4
                        py-3
                        text-white
                    "
                />

            </div>

            <!-- EMAIL -->

            <div>

                <label
                    class="
                        block
                        text-sm
                        font-medium
                        text-gray-300
                        mb-2
                    "
                >
                    Email
                </label>

                <input
                    bind:value={email}
                    type="email"
                    placeholder="
                        contact@company.com
                    "
                    class="
                        w-full
                        rounded-xl
                        border
                        border-gray-700
                        bg-gray-950
                        px-4
                        py-3
                        text-white
                    "
                />

            </div>

            <!-- CITY -->

            <div>

                <label
                    class="
                        block
                        text-sm
                        font-medium
                        text-gray-300
                        mb-2
                    "
                >
                    City
                </label>

                <input
                    bind:value={city}
                    placeholder="Bogota"
                    class="
                        w-full
                        rounded-xl
                        border
                        border-gray-700
                        bg-gray-950
                        px-4
                        py-3
                        text-white
                    "
                />

            </div>

            <!-- VALUE -->

            <div>

                <label
                    class="
                        block
                        text-sm
                        font-medium
                        text-gray-300
                        mb-2
                    "
                >
                    Estimated Value
                </label>

                <input
                    bind:value={estimated_value}
                    type="number"
                    min="0"
                    class="
                        w-full
                        rounded-xl
                        border
                        border-gray-700
                        bg-gray-950
                        px-4
                        py-3
                        text-white
                    "
                />

            </div>

            <!-- PROBABILITY -->

            <div>

                <label
                    class="
                        block
                        text-sm
                        font-medium
                        text-gray-300
                        mb-2
                    "
                >
                    Probability
                </label>

                <input
                    bind:value={probability}
                    type="number"
                    min="0"
                    max="100"
                    class="
                        w-full
                        rounded-xl
                        border
                        border-gray-700
                        bg-gray-950
                        px-4
                        py-3
                        text-white
                    "
                />

            </div>

            <!-- SOURCE -->

            <div>

                <label
                    class="
                        block
                        text-sm
                        font-medium
                        text-gray-300
                        mb-2
                    "
                >
                    Source
                </label>

                <select
                    bind:value={source}
                    class="
                        w-full
                        rounded-xl
                        border
                        border-gray-700
                        bg-gray-950
                        px-4
                        py-3
                        text-white
                    "
                >

                    <option value="REFERRAL">
                        Referral
                    </option>

                    <option value="WEBSITE">
                        Website
                    </option>

                    <option value="FIELD_VISIT">
                        Field Visit
                    </option>

                    <option value="CALL">
                        Cold Call
                    </option>

                    <option value="EMAIL">
                        Email Campaign
                    </option>

                </select>

            </div>

            <!-- ASSIGNED REP -->

            <div>

                <label
                    class="
                        block
                        text-sm
                        font-medium
                        text-gray-300
                        mb-2
                    "
                >
                    Assigned Rep
                </label>

                <input
                    bind:value={assigned_rep}
                    placeholder="
                        Sales representative
                    "
                    class="
                        w-full
                        rounded-xl
                        border
                        border-gray-700
                        bg-gray-950
                        px-4
                        py-3
                        text-white
                    "
                />

            </div>

        </div>

        <div
            class="
                flex
                items-center
                justify-end
                gap-3
                mt-8
            "
        >

            <button
                type="button"
                onclick={() =>
                    goto('/app/crm/leads')
                }
                class="
                    px-5
                    py-3
                    rounded-xl
                    border
                    border-gray-700
                    hover:bg-gray-800
                    transition
                    text-white
                "
            >
                Cancel
            </button>

            <button
                type="button"
                onclick={submit}
                disabled={loading}
                class="
                    px-5
                    py-3
                    rounded-xl
                    bg-emerald-600
                    hover:bg-emerald-700
                    transition
                    text-white
                    disabled:opacity-50
                "
            >
                {loading
                    ? 'Creating Lead...'
                    : 'Create Lead'}
            </button>

        </div>

    </div>

</div>