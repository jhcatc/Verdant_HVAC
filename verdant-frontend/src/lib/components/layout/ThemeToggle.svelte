<script lang="ts">
    import { onMount } from 'svelte';

    let isDark = $state(false);

    function toggleTheme() {
        isDark = !isDark;

        if (isDark) {
            document.documentElement.classList.add('dark');
            localStorage.setItem('theme', 'dark');
        } else {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('theme', 'light');
        }
    }

    onMount(() => {
        const saved = localStorage.getItem('theme');

        if (saved === 'dark') {
            isDark = true;
            document.documentElement.classList.add('dark');
        } else {
            isDark = false;
            document.documentElement.classList.remove('dark');
        }
    });
</script>

<button
    onclick={toggleTheme}
    class="text-xl"
>
    {#if isDark}
        ☀️
    {:else}
        🌙
    {/if}
</button>