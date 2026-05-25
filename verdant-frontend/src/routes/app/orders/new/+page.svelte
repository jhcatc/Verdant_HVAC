<script lang="ts">
    import { goto } from '$app/navigation';
    import api from '$lib/api/client';
    import CustomerAutocomplete from '$lib/components/customer/CustomerAutocomplete.svelte';
    import InventoryAutocomplete from '$lib/components/InventoryAutocomplete.svelte';
    import InventoryModal from '$lib/components/InventoryModal.svelte';

    // 🔹 BASIC INFO
    let title = $state('');
    let customer_id = $state(null);
    let city = $state('');

    // 🔹 COSTOS
    let labor_cost = $state(0);

    // 🔹 MODAL (aunque ya no se usa para materiales, lo dejamos por compatibilidad)
    let showModal = $state(false);
    let draftName = $state('');
    let activeMaterialIndex = $state(null);

    // 🔹 TASKS
    let tasks = $state([{ title: '' }]);

    // 🔹 MATERIALS
    let materials = $state([
        {
            inventory_item_id: null,
            name: '',
            quantity: 1,
            unit_cost: 0,
            stock: 0
        }
    ]);

    // 🔥 DERIVED STATE (RUNES OK)
    const materialsWithState = $derived(
        materials.map(m => ({
            ...m,
            exceeds: (m.stock ?? 0) > 0 && m.quantity > (m.stock ?? 0)
        }))
    );

    // =========================================================
    // 🔹 TASKS
    // =========================================================

    function addTask() {
        tasks = [...tasks, { title: '' }];
    }

    // =========================================================
    // 🔹 MATERIALS
    // =========================================================

    function addMaterial() {
        materials = [
            ...materials,
            {
                inventory_item_id: null,
                name: '',
                quantity: 1,
                unit_cost: 0,
                stock: 0
            }
        ];
    }

    function updateMaterial(i, item) {
        if (!item) return;

        console.log('ITEM FIXED:', item);

        materials = materials.map((m, idx) =>
            idx === i
                ? {
                    inventory_item_id: item.id ?? item.inventory_item_id,
                    name: item.name ?? item.label ?? '',
                    unit_cost: item.unit_cost ?? item.cost ?? 0,
                    stock: item.stock ?? 0,
                    quantity: 1
                }
                : m
        );
    }

    // =========================================================
    // 🔹 VALIDATION (FIX PRO)
    // =========================================================

    function validateMaterials() {
        for (const m of materialsWithState) {
            if (m.inventory_item_id) {
                if (m.exceeds || m.quantity <= 0) {
                    return false;
                }
            }
        }
        return true;
    }

    // =========================================================
    // 🔹 SUBMIT (FIX COMPLETO)
    // =========================================================

    async function submit() {
        if (!validateMaterials()) return;

        const cleanMaterials = materials.filter(m => m.inventory_item_id);

        await api.post('/service-orders/', {
            title,
            customer_id,
            city,
            tasks,
            materials: cleanMaterials,
            labor_cost,
            status: 'pending' // 🔥 opcional pero sólido
        });

        goto('/app/orders');
    }
    
</script>

<h1 class="text-2xl font-bold mb-6 heading">New Service Order</h1>

<div class="card space-y-4">

    <!-- 🔹 TITLE -->
    <input class="input" placeholder="Order title" bind:value={title} />

    <!-- 🔹 CUSTOMER (SIN CREAR) -->
    <CustomerAutocomplete
        bind:value={customer_id}
        allowCreate={false}
    />

    <!-- 🔹 CITY -->
    <input class="input" placeholder="City" bind:value={city} />

    <!-- ========================================================= -->
    <!-- 🔹 TASKS -->
    <!-- ========================================================= -->

    <div>
        <h2 class="font-semibold mb-2">Tasks</h2>

        {#each tasks as t, i}
            <input
                class="input mb-2"
                placeholder="Task title"
                bind:value={tasks[i].title}
            />
        {/each}

        <button class="text-green-600" onclick={addTask}>
            + Add Task
        </button>
    </div>

    <!-- ========================================================= -->
    <!-- 🔹 MATERIALS -->
    <!-- ========================================================= -->

    <div>
        <h2 class="font-semibold mb-2">Materials</h2>

        {#each materialsWithState as m, i}
        <div class="flex flex-col mb-3">

            <div class="flex gap-2 w-full">

                <!-- 🔹 AUTOCOMPLETE (SOLO SELECCIÓN) -->
                <div class="flex-[3]">
                <InventoryAutocomplete
                    bind:selected={materials[i].name}
                    on:select={(e) => updateMaterial(i, e.detail)}
                />
                </div>

                <!-- 🔹 QUANTITY -->
                <input
                    type="number"
                    class="flex-[1] border p-2 rounded"
                    bind:value={materials[i].quantity}
                    placeholder="Qty"
                />

                <!-- 🔹 UNIT COST -->
                <input
                    type="number"
                    class="flex-[1] border p-2 rounded"
                    bind:value={materials[i].unit_cost}
                    placeholder="Cost"
                />

            </div>

            <!-- 🔴 STOCK WARNING -->
            {#if m.exceeds}
                <span class="text-red-500 text-sm mt-1">
                    Stock insuficiente (Disponible: {m.stock})
                </span>
            {/if}

        </div>
        {/each}

        <button class="text-green-600" onclick={addMaterial}>
            + Add Material
        </button>
    </div>

    <!-- ========================================================= -->
    <!-- 🔹 LABOR COST (🔥 NUEVO) -->
    <!-- ========================================================= -->

    <div>
        <h2 class="font-semibold mb-2">Labor Cost</h2>

        <input
            type="number"
            class="input"
            bind:value={labor_cost}
            placeholder="0.00"
        />
    </div>

    <!-- ========================================================= -->
    <!-- 🔹 SUBMIT -->
    <!-- ========================================================= -->

    <button
        class="bg-green-600 text-white px-4 py-2 rounded-lg disabled:opacity-50"
        disabled={!validateMaterials()}
        onclick={submit}
    >
        Crear Orden
    </button>

</div>

<!-- 🔹 MODAL (queda pero ya no se usa para materiales) -->
<InventoryModal
    open={showModal}
    initialName={draftName}
    on:created={(e) => {
        if (activeMaterialIndex !== null) {
            updateMaterial(activeMaterialIndex, e.detail);
        }
        showModal = false;
        activeMaterialIndex = null;
    }}
/>