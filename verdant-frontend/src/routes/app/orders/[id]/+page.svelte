<script lang="ts">
    import { onMount } from 'svelte';
    import { page } from '$app/state';
    import api from '$lib/api/client';
    import { goto } from '$app/navigation';
    import OrderHeader from './OrderHeader.svelte';
    import TaskList from './TaskList.svelte';
    import MaterialList from './MaterialList.svelte';
    import Timeline from './Timeline.svelte';
    import SidePanel from './SidePanel.svelte';

    let order = $state(null);
    let loading = $state(true);
    let dispatching = $state(false);
    let saving = $state(false);

    const orderId = $derived(page.params.id);

    onMount(load);

    async function load() {
        loading = true;
        const res = await api.get(`/service-orders/${orderId}`);
        order = res.data;
        loading = false;
    }

    // 🔥 logs en vivo
    function addLog(log) {
        order.logs = [log, ...order.logs];
        order = { ...order };
    }

    // =========================================================
    // 🔹 AUTO DISPATCH
    // =========================================================

    async function autoDispatch() {
        if (!order) return;

        dispatching = true;

        try {
            const res = await api.get(`/service-orders/${order.id}/suggest`);
            const suggestion = res.data;

            await api.patch(`/service-orders/${order.id}/dispatch`, {
                technician_id: suggestion.technician_id,
                scheduled_at: suggestion.scheduled_at,
                duration_hours: order.duration_hours ?? 1
            });

            await load();

        } catch (err) {
            console.error(err);
        } finally {
            dispatching = false;
        }
    }

    // =========================================================
    // 🔹 SAVE (🔥 NUEVO)
    // =========================================================

    async function save() {
        if (!order) return;

        saving = true;

        try {
            const cleanMaterials =
                order.materials?.filter(m => m.inventory_item_id) ?? [];

            await api.put(`/service-orders/${order.id}`, {
                title: order.title,
                city: order.city,
                labor_cost: order.labor_cost ?? 0,
                materials: cleanMaterials
            });

            // 🔥 UX PRO: volver al listado
            goto('/app/orders');

        } catch (err) {
            console.error(err);
            alert('Error saving order');
        } finally {
            saving = false;
        }
    }  
    
</script>

{#if loading}
<p class="p-6">Loading...</p>

{:else if order}

<div class="p-6 space-y-6">

    <!-- 🔥 HEADER + BOTONES -->
    <div class="flex justify-between items-center">
        <OrderHeader {order} on:updateLog={(e) => addLog(e.detail)} />

        <div class="flex gap-2">

            <button
                class="bg-blue-600 text-white px-4 py-2 rounded-lg disabled:opacity-50"
                onclick={autoDispatch}
                disabled={dispatching}
            >
                {dispatching ? 'Dispatching...' : 'Auto Dispatch'}
            </button>

            <!-- 🔥 SAVE -->
            <button
                class="bg-green-600 text-white px-4 py-2 rounded-lg disabled:opacity-50"
                onclick={save}
                disabled={saving}
            >
                {saving ? 'Saving...' : 'Save'}
            </button>

        </div>
    </div>

    <div class="grid grid-cols-12 gap-6">

        <!-- ========================================================= -->
        <!-- 🔹 MAIN -->
        <!-- ========================================================= -->

        <div class="col-span-8 space-y-6">

            <!-- 🔥 EDITABLE TITLE -->
            <div class="card">
                <label class="text-sm text-gray-400">Title</label>
                <input
                    class="input mt-1"
                    bind:value={order.title}
                />
            </div>

            <!-- 🔥 EDITABLE CITY -->
            <div class="card">
                <label class="text-sm text-gray-400">City</label>
                <input
                    class="input mt-1"
                    bind:value={order.city}
                />
            </div>

            <!-- 🔥 TASKS (ya editable por bind) -->
            <TaskList bind:tasks={order.tasks} orderId={order.id} />

            <!-- 🔥 MATERIALS (solo display por ahora) -->
            <MaterialList materials={order.materials} />

            <!-- 🔥 TIMELINE -->
            <Timeline logs={order.logs} orderId={order.id} />

        </div>

        <!-- ========================================================= -->
        <!-- 🔹 SIDE PANEL -->
        <!-- ========================================================= -->

        <div class="col-span-4 space-y-6">

            <SidePanel
                {order}
                on:updateLog={(e) => addLog(e.detail)}
            />

            <!-- 🔥 LABOR COST (EDITABLE) -->
            <div class="card">
                <label class="text-sm text-gray-400">Labor Cost</label>
                <input
                    type="number"
                    class="input mt-1"
                    bind:value={order.labor_cost}
                />
            </div>

            <!-- 🔥 COST SUMMARY -->
            <div class="card">
                <h3 class="font-semibold mb-2">Costs</h3>

                <div class="flex justify-between text-sm">
                    <span>Estimated</span>
                    <span>${order.estimated_cost ?? 0}</span>
                </div>

                <div class="flex justify-between text-sm">
                    <span>Actual</span>
                    <span>${order.actual_cost ?? 0}</span>
                </div>
            </div>

        </div>

    </div>

</div>

{/if}