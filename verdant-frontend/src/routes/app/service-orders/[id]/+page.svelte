<script lang="ts">
    import api from '$lib/api/client';
    import { onMount } from 'svelte';
    import { page } from '$app/stores';

    type ServiceOrderDetail = {
        id: string;
        customer_id: string;
        status: string;
        priority: string;
        issue_description: string;
        created_at?: string;
    };
    let order:
        ServiceOrderDetail | null =
        null;

    onMount(async () => {
        const res = await api.get(`/service-orders/${$page.params.id}`);
        order = res.data;
    });
</script>

{#if order}
<h1 class="text-xl font-bold">{order.title}</h1>

<h2 class="mt-4 font-semibold">Tasks</h2>
<ul>
    {#each order.tasks as t}
        <li>✔ {t.title}</li>
    {/each}
</ul>

<h2 class="mt-4 font-semibold">Materials</h2>
<ul>
    {#each order.materials as m}
        <li>{m.name} ({m.quantity})</li>
    {/each}
</ul>

<h2 class="mt-4 font-semibold">Timeline</h2>
<ul>
    {#each order.logs as log}
        <li>{log.message}</li>
    {/each}
</ul>
{/if}