<script lang="ts">

    import api from '$lib/api/client';

    type Customer = {

        id: string;
        name: string;
        city?: string | null;
        email?: string | null;
    };

    let {
        value = '',
        placeholder = 'Search customer...',
        showEmail = false,
        showCity = true,
        onSelect
    } = $props<{
        value?: string;
        placeholder?: string;
        showEmail?: boolean;
        showCity?: boolean;
        onSelect: (
            customer: Customer
        ) => void;
    }>();

    let query = $state(value);

    let customers =
        $state<Customer[]>([]);

    let loading =
        $state(false);

    let open =
        $state(false);

    async function search() {

        if (query.length < 2) {

            customers = [];

            return;
        }

        loading = true;

        try {

            const res = await api.get(

                `/customers/search?q=${query}`
            );

            customers = res.data;

        } catch (e) {

            console.error(e);

        } finally {

            loading = false;
        }
    }

    function selectCustomer(
        customer: Customer
    ) {

        query = customer.name;

        open = false;

        customers = [];

        onSelect(customer);
    }

</script>

<div class="relative">

    <input
        bind:value={query}
        oninput={search}
        onfocus={() => open = true}
        placeholder={placeholder}
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

    {#if loading}

        <div
            class="
                absolute
                right-3
                top-3
                text-xs
                text-gray-500
            "
        >
            Searching...
        </div>

    {/if}

    {#if open && customers.length > 0}

        <div
            class="
                absolute
                z-50
                mt-1
                w-full
                overflow-y-auto
                rounded-xl
                border
                border-gray-700
                bg-gray-900
                shadow-xl
                max-h-64
            "
        >

            {#each customers as customer}

                <button
                    type="button"
                    class="
                        w-full
                        px-4
                        py-3
                        text-left
                        hover:bg-gray-800
                    "
                    onclick={() =>
                        selectCustomer(customer)
                    }
                >

                    <div
                        class="
                            font-medium
                            text-white
                        "
                    >
                        {customer.name}
                    </div>

                    <div
                        class="
                            flex
                            gap-3
                            text-xs
                            text-gray-500
                            mt-1
                        "
                    >
                        {#if showCity}
                            <span>
                                {customer.city || '—'}
                            </span>
                        {/if}
                        {#if showEmail && customer.email}
                            <span>
                                {customer.email}
                            </span>

                        {/if}

                    </div>

                </button>

            {/each}

        </div>

    {/if}

</div>