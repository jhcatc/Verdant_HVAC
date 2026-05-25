<script lang="ts">
    import { createCustomer } from '$lib/api/customers';

    let { open, onClose, onCreated, initialName = '' } = $props();

    let name = $state(initialName);
    let email = $state('');
    let city = $state('');
    let phone = $state('');
    let loading = $state(false);

    async function submit() {
        if (!name) return;

        loading = true;

        try {
            const customer = await createCustomer({
                name,
                email,
                city,
                phone
            });

            on:Created(customer);

            // reset
            name = '';
            email = '';
            city = '';
            phone = '';

        } finally {
            loading = false;
        }
    }
</script>

{#if open}
<div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">

    <div class="bg-white dark:bg-gray-900 p-6 rounded-xl w-full max-w-md space-y-4">

        <h2 class="text-lg font-semibold text-gray-900 dark:text-white">
            Create Customer
        </h2>

        <!-- NAME -->
        <input
            class="w-full border p-2 rounded bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
            placeholder="Customer Name"
            bind:value={name}
        />

        <!-- EMAIL -->
        <input
            class="w-full border p-2 rounded bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
            placeholder="Email"
            bind:value={email}
        />

        <!-- CITY -->
        <input
            class="w-full border p-2 rounded bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
            placeholder="City"
            bind:value={city}
        />

        <!-- PHONE -->
        <input
            class="w-full border p-2 rounded bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
            placeholder="Phone"
            bind:value={phone}
        />

        <div class="flex justify-end gap-2">

            <button
                onclick={onClose}
                class="text-gray-500"
            >
                Cancel
            </button>

            <button
                onclick={submit}
                class="bg-blue-600 text-white px-4 py-2 rounded"
                disabled={loading}
            >
                {loading ? 'Saving...' : 'Create'}
            </button>

        </div>

    </div>
</div>
{/if}