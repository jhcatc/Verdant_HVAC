<script lang="ts">

    import { goto } from '$app/navigation';

    import api from '$lib/api/client';

    let loading =
        $state(false);

    let name =
        $state('');

    let email =
        $state('');

    let phone =
        $state('');

    let city =
        $state('');

    async function submit() {

        if (!name.trim()) {

            alert('Customer name required');
            return;
        }

        loading = true;

        try {

            await api.post('/customers', {

                name,
                email,
                phone,
                city
            });

            goto('/app/customers');

        } catch (e) {

            console.error(e);

            alert('Failed to create customer');

        } finally {

            loading = false;
        }
    }

</script>

<div class="p-6 max-w-4xl">

    <div class="mb-8">

        <h1 class="text-3xl font-bold text-white">
            Create Customer
        </h1>

        <p class="text-sm text-gray-400 mt-1">
            Create enterprise customer account,
            service relationships and operational profile.
        </p>

    </div>

    <div
        class="rounded-2xl border border-gray-800 bg-gray-900 p-6"
    >

        <div class="grid grid-cols-1 md:grid-cols-2 gap-5">

            <div>

                <label class="text-sm text-gray-300 block mb-2">
                    Customer Name
                </label>

                <input
                    bind:value={name}
                    class="w-full px-4 py-3 rounded-xl bg-gray-950 border border-gray-700 text-white"
                />

            </div>

            <div>

                <label class="text-sm text-gray-300 block mb-2">
                    Email
                </label>

                <input
                    bind:value={email}
                    class="w-full px-4 py-3 rounded-xl bg-gray-950 border border-gray-700 text-white"
                />

            </div>

            <div>

                <label class="text-sm text-gray-300 block mb-2">
                    Phone
                </label>

                <input
                    bind:value={phone}
                    class="w-full px-4 py-3 rounded-xl bg-gray-950 border border-gray-700 text-white"
                />

            </div>

            <div>

                <label class="text-sm text-gray-300 block mb-2">
                    City
                </label>

                <input
                    bind:value={city}
                    class="w-full px-4 py-3 rounded-xl bg-gray-950 border border-gray-700 text-white"
                />

            </div>

        </div>

        <div class="mt-8 flex justify-end gap-3">

            <button
                onclick={() => goto('/app/customers')}
                class="px-4 py-2 rounded-xl border border-gray-700 text-white"
            >
                Cancel
            </button>

            <button
                onclick={submit}
                disabled={loading}
                class="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white"
            >
                {loading ? 'Creating...' : 'Create Customer'}
            </button>

        </div>

    </div>

</div>