<script lang="ts">

    import {
        proposalSaving
    } from '$lib/stores/proposal.store';

</script>

{#if $proposalSaving}

<div
    class="
        text-xs
        text-amber-400
    "
>
    Saving...
</div>

{:else}

<div
    class="
        text-xs
        text-emerald-400
    "
>
    Saved
</div>

{/if}