<script lang="ts">
    import { onMount } from 'svelte';
    import api from '$lib/api/client';
    let { proposalId } = $props();
    let versions = $state([]);
    async function load() {

        const res = await api.get(
            `/crm/proposals/${proposalId}/versions`
        );

        versions = res.data;
    }

    async function createSnapshot() {

        await api.post(
            `/crm/proposals/${proposalId}/versions`
        );

        await load();
    }

    onMount(load);

</script>

<div
    class="
        rounded-2xl
        border
        border-gray-800
        bg-gray-950
        p-5
        space-y-4
    "
>

    <div
        class="
            flex
            items-center
            justify-between
        "
    >

        <div
            class="
                text-sm
                uppercase
                tracking-wider
                text-gray-500
            "
        >
            Versions
        </div>

        <button
            onclick={createSnapshot}
            class="
                px-3
                py-2
                rounded-lg
                bg-cyan-600
                hover:bg-cyan-700
                text-sm
            "
        >
            Snapshot
        </button>

    </div>

    <div class="space-y-3">

        {#each versions as version}

            <div
                class="
                    rounded-xl
                    border
                    border-gray-800
                    p-4
                "
            >

                <div
                    class="
                        flex
                        items-center
                        justify-between
                    "
                >

                    <div
                        class="
                            font-semibold
                        "
                    >
                        V{version.version_number}
                    </div>

                    <div
                        class="
                            text-xs
                            text-gray-500
                        "
                    >
                        {
                            new Date(
                                version.created_at
                            ).toLocaleString()
                        }
                    </div>

                </div>

                <div
                    class="
                        mt-2
                        text-sm
                        text-gray-400
                    "
                >
                    ${version.total?.toLocaleString()}
                </div>

            </div>

        {/each}

    </div>

</div>