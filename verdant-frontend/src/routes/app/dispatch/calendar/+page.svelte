<script lang="ts">
  import { onMount } from 'svelte';
  import api from '$lib/api/client';
  import CalendarGrid from './CalendarGrid.svelte';

  import { page } from '$app/state';

  let technicians = $state([]);
  let orders = $state([]);
  let loading = $state(true);

  const currentPath = $derived(page.url.pathname);

  async function loadData() {
    loading = true;

    const [techs, ords] = await Promise.all([
      api.get('/users/technicians'),
      api.get('/service-orders/')
    ]);

    technicians = techs.data;
    orders = ords.data;

    loading = false;
  }

  onMount(loadData);
</script>

<!-- 🔥 NAV -->

<!-- 🔥 TÍTULO -->
<h1 class="text-2xl font-bold mb-6 text-gray-900 dark:text-gray-100">
  Dispatch Calendar
</h1>

<!-- 🔥 CONTENIDO -->
{#if loading}
  <p class="text-gray-500">Loading...</p>
{:else}
  <CalendarGrid
    {technicians}
    {orders}
    reload={loadData}
  />
{/if}