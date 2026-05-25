<script lang="ts">
    import { onMount } from 'svelte';
    import { getTechnicians } from '$lib/api/users';

    import AIAssignmentPanel from './AIAssignmentPanel.svelte';

    let {
        selectedOrder,
        onConfirm,
        onClose
    } = $props();

    let technicians = $state([]);
    let technician_id = $state('');
    let scheduled_at = $state('');
    let duration_hours = $state(1);

    onMount(async () => {

        technicians = await getTechnicians();
    });

    function submit() {

        if (!technician_id || !scheduled_at) {
            return;
        }

        onConfirm?.({
            technicianId: technician_id,
            scheduledAt: scheduled_at,
            durationHours: duration_hours
        });
    }
</script>

<div
    class="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-[9999]"
>

    <div
        class="bg-[#0f172a] border border-slate-800 w-[1200px] max-h-[90vh] overflow-auto rounded-3xl shadow-2xl"
    >

        <div class="grid grid-cols-2">

            <!-- LEFT -->
            <div class="p-8 border-r border-slate-800">

                <div class="mb-6">

                    <h2 class="text-2xl font-bold text-white">
                        Manual Assignment
                    </h2>

                    <p class="text-slate-400 mt-2">
                        Traditional dispatch workflow
                    </p>

                </div>

                <div class="space-y-5">

                    <div>

                        <label class="text-sm text-slate-400">
                            Technician
                        </label>

                        <select
                            bind:value={technician_id}
                            class="w-full mt-2 bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-white"
                        >
                            <option value="">
                                Select technician
                            </option>

                            {#each technicians as t}
                                <option value={t.id}>
                                    {t.full_name}
                                </option>
                            {/each}

                        </select>

                    </div>

                    <div>

                        <label class="text-sm text-slate-400">
                            Schedule
                        </label>

                        <input
                            type="datetime-local"
                            bind:value={scheduled_at}
                            class="w-full mt-2 bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-white"
                        />

                    </div>

                    <div>

                        <label class="text-sm text-slate-400">
                            Duration Hours
                        </label>

                        <input
                            type="number"
                            bind:value={duration_hours}
                            class="w-full mt-2 bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-white"
                        />

                    </div>

                    <div class="flex justify-end gap-3 pt-6">

                        <button
                            onclick={onClose}
                            class="px-4 py-2 rounded-xl border border-slate-700 text-slate-300"
                        >
                            Cancel
                        </button>

                        <button
                            onclick={submit}
                            class="px-5 py-2 rounded-xl bg-emerald-600 text-white"
                        >
                            Assign
                        </button>

                    </div>

                </div>

            </div>

            <!-- RIGHT -->
            <div class="p-8">

                <AIAssignmentPanel
                    orderId={selectedOrder.id}
                    onAssign={onConfirm}
                />

            </div>

        </div>

    </div>

</div>