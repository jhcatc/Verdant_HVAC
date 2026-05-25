<script lang="ts">
    import { page } from '$app/state';
</script>

<div class="p-6 text-white">
<!--
    <h1 class="text-xl font-semibold mb-4 text-emerald-400">
        Service Intelligence Layer
    </h1>
    <div class="mb-4 text-sm text-slate-400">
        {page.url.pathname}
    </div>
-->
    <slot />
</div>
