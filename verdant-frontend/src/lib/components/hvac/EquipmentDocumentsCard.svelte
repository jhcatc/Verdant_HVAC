<script lang="ts">

    import {
        onMount
    } from 'svelte';

    import {
        Upload,
        Trash2,
        FileText
    } from 'lucide-svelte';

    import {
        getEquipmentDocuments,
        uploadEquipmentDocument,
        deleteEquipmentDocument
    } from '$lib/api/equipmentDocuments';

    import ConfirmDialog
    from '$lib/components/ui/modal/ConfirmDialog.svelte';

    let {
        equipmentId
    } = $props<{
        equipmentId: string;
    }>();

    let loading =
        $state(true);

    let uploading =
        $state(false);

    type EquipmentDocument = {
        id: string;
        file_name: string;
        file_url: string;
        uploaded_at: string;
        document_type?: string;
    };

    let documents =
        $state<EquipmentDocument[]>([]);

    let deleteId =
        $state<string | null>(null);

    async function load() {

        try {

            loading = true;

            documents =
                await getEquipmentDocuments(
                    equipmentId
                );

        } finally {

            loading = false;
        }
    }

    async function handleUpload(
        event: Event
    ) {

        const input =
            event.target
            as HTMLInputElement;

        const file =
            input.files?.[0];

        if (!file) return;

        try {

            uploading = true;

            await uploadEquipmentDocument({

                equipment_id:
                    equipmentId,

                file
            });

            await load();

        } finally {

            uploading = false;
        }
    }

    async function confirmDelete() {

        if (!deleteId) return;

        await deleteEquipmentDocument(
            deleteId
        );

        deleteId = null;

        await load();
    }

    onMount(load);

</script>

<div
    class="rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-6 space-y-6"
>

    <div
        class="flex items-center justify-between"
    >

        <div>

            <h2
                class="text-xl font-semibold"
            >
                Documents
            </h2>

            <p
                class="text-sm text-gray-500"
            >
                Manuals, warranties, invoices,
                maintenance attachments
            </p>

        </div>

        <label
            class="cursor-pointer px-4 py-2 rounded-xl bg-emerald-600 text-white flex items-center gap-2"
        >

            <Upload size={18} />

            <span>
                {uploading
                    ? 'Uploading...'
                    : 'Upload'}
            </span>

            <input
                type="file"
                class="hidden"
                onchange={handleUpload}
            />

        </label>

    </div>

    {#if loading}

        <div
            class="text-sm text-gray-500"
        >
            Loading documents...
        </div>

    {:else if documents.length === 0}

        <div
            class="rounded-xl border border-dashed border-gray-300 dark:border-gray-700 p-10 text-center"
        >

            <FileText
                class="mx-auto mb-4"
                size={40}
            />

            <p
                class="text-sm text-gray-500"
            >
                No documents uploaded
            </p>

        </div>

    {:else}

        <div
            class="space-y-3"
        >

            {#each documents as document}

                <div
                    class="flex items-center justify-between rounded-xl border border-gray-200 dark:border-gray-800 px-4 py-3"
                >

                    <div>

                        <p
                            class="font-medium"
                        >
                            {document.file_name}
                        </p>

                        <p
                            class="text-xs text-gray-500"
                        >
                            {document.document_type ?? 'General'}
                        </p>

                    </div>

                    <button
                        onclick={() => deleteId = document.id}
                        class="text-red-500 hover:text-red-600"
                    >

                        <Trash2 size={18} />

                    </button>

                </div>

            {/each}

        </div>

    {/if}

</div>

<ConfirmDialog
    open={!!deleteId}
    title="Delete Document"
    message="This action cannot be undone."
    confirmText="Delete"
    cancelText="Cancel"
    onConfirm={confirmDelete}
    onCancel={() => deleteId = null}
/>