<script lang="ts">

    import { onMount } from 'svelte';

    import {
        getEquipmentPhotos,
        uploadEquipmentPhoto,
        deleteEquipmentPhoto
    } from '$lib/api/equipmentPhotos';

    let {
        equipmentId
    } = $props<{
        equipmentId: string;
    }>();

    type EquipmentPhoto = {
        id: string;
        image_url: string;
        uploaded_at: string;
        caption?: string;
    };

    let photos =
        $state<EquipmentPhoto[]>([]);

    let loading = $state(false);

    async function loadPhotos() {

        loading = true;

        try {

            photos =
                await getEquipmentPhotos(
                    equipmentId
                );

        } finally {

            loading = false;
        }
    }

    async function onUpload(
        event: Event
    ) {

        const target =
            event.target as HTMLInputElement;

        const file =
            target.files?.[0];

        if (!file) return;

        await uploadEquipmentPhoto(
            equipmentId,
            file
        );

        await loadPhotos();
    }

    async function removePhoto(
        photoId: string
    ) {

        await deleteEquipmentPhoto(
            photoId
        );

        await loadPhotos();
    }

    onMount(loadPhotos);

</script>

<div class="space-y-6">

    <div
        class="flex items-center justify-between"
    >

        <div>

            <h3
                class="text-xl font-semibold"
            >
                Equipment Photos
            </h3>

            <p
                class="text-sm text-gray-500"
            >
                Lifecycle visual history
            </p>

        </div>

        <label
            class="px-4 py-2 rounded-xl bg-emerald-600 text-white cursor-pointer"
        >

            Upload Photo

            <input
                type="file"
                class="hidden"
                accept="image/*"
                onchange={onUpload}
            />

        </label>

    </div>

    {#if loading}

    <div
        class="rounded-2xl border p-10 text-center"
    >
        Loading photos...
    </div>

    {:else if photos.length === 0}

    <div
        class="rounded-2xl border border-dashed p-10 text-center text-gray-500"
    >
        No photos uploaded yet
    </div>

    {:else}

    <div
        class="grid grid-cols-2 md:grid-cols-4 gap-4"
    >

        {#each photos as photo}

        <div
            class="relative rounded-2xl overflow-hidden border"
        >

            <img
                src={`http://localhost:8000/${photo.file_path}`}
                alt={photo.file_name}
                class="w-full h-52 object-cover"
            />

            <button
                onclick={() => removePhoto(photo.id)}
                class="absolute top-2 right-2 bg-red-600 text-white rounded-lg px-2 py-1 text-xs"
            >
                Delete
            </button>

        </div>

        {/each}

    </div>

    {/if}

</div>