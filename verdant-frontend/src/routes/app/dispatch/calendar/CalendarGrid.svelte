<script lang="ts">
  import TechnicianRow from "./TechnicianRow.svelte";
  import dayjs from "dayjs";

  let { technicians, orders, reload } = $props();

  const start = dayjs().hour(8).minute(0);
  const end = dayjs().hour(18).minute(0);

  let slots = [];

  let current = start;

  while (current.isBefore(end)) {

    slots.push(current.toDate());

    current = current.add(15, "minute");
  }

  function ordersByTech(techId) {

    return orders.filter(o =>
      o.assignments?.some(a => a.user_id === techId)
    );
  }
</script>

<!-- HEADER -->
<div class="flex border-b border-gray-300 dark:border-gray-700 sticky top-0 z-30 bg-white dark:bg-gray-900">

  <!-- LEFT -->
  <div class="w-48 shrink-0 border-r border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900"></div>

  <!-- HOURS -->
  <div class="flex-1 flex">

    {#each slots as slot}

      <div class="flex-1 min-w-[48px] text-center text-xs py-2 border-l border-gray-200 dark:border-gray-700 text-gray-500 dark:text-gray-400">
        {new Date(slot).toLocaleTimeString([], {
          hour: '2-digit',
          minute: '2-digit'
        })}
      </div>

    {/each}

  </div>

</div>

<!-- BODY -->
<div class="overflow-auto bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700">

  {#each technicians as tech}

    <TechnicianRow
      technician={tech}
      orders={ordersByTech(tech.id)}
      {slots}
      {reload}
    />

  {/each}

</div>