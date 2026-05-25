<script lang="ts">
  import TimeSlot from "./TimeSlot.svelte";
  import OrderChip from "./OrderChip.svelte";

  let { technician, orders, slots, reload } = $props();
</script>

<div class="flex border-b border-gray-200 dark:border-gray-700 min-h-[1920px]">

  <!-- 👤 TECH -->
  <div class="w-48 p-2 text-sm font-medium text-gray-700 dark:text-gray-200 border-r border-gray-200 dark:border-gray-700">
    <div class="sticky top-0">
      {technician.name}
    </div>
  </div>

  <!-- 📅 GRID -->
  <div class="flex-1 relative">

    <!-- SLOT GRID -->
    <div class="absolute inset-0">

      {#each slots as slot}
        <TimeSlot
          {technician}
          slotTime={slot}
          {reload}
        />
      {/each}

    </div>

    <!-- ORDERS -->
    {#each orders as o (o.id)}
      <OrderChip order={o} />
    {/each}

  </div>

</div>