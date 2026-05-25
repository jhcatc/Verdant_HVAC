<script lang="ts">

    let {
        equipmentId,
        assetTag
    } = $props<{
        equipmentId: string;
        assetTag?: string;
    }>();

    const qrUrl =
        `http://localhost:8000/api/equipment-qr/${equipmentId}`;

</script>

<div
    class="rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-6"
>

    <div
        class="flex items-start justify-between gap-6"
    >

        <div>

            <h3
                class="text-xl font-semibold text-gray-900 dark:text-white"
            >
                Equipment QR
            </h3>

            <p
                class="mt-2 text-sm text-gray-500"
            >
                Technician field access label
            </p>

            {#if assetTag}

            <div
                class="mt-4 inline-flex rounded-xl bg-gray-100 dark:bg-gray-800 px-3 py-2 text-sm font-medium"
            >
                {assetTag}
            </div>

            {/if}

        </div>

        <div
            class="rounded-2xl border border-gray-200 dark:border-gray-700 bg-white p-4"
        >

            <img
                src={qrUrl}
                alt="Equipment QR"
                class="h-44 w-44"
            />

        </div>

    </div>

</div>