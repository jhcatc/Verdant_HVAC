<script lang="ts">
    import Sidebar from '$lib/components/layout/Sidebar.svelte';
    import Header from '$lib/components/layout/Header.svelte';
    import { onMount } from 'svelte';
    import { initializeAuth } from '$lib/stores/auth';
    import { logout, user } from '$lib/stores/auth';

    let { data, children } = $props();

    $effect(() => {

        if (data?.user) {
            user.set(data.user);
        }

    });

    async function handleLogout() {

        await logout();

        window.location.href = '/auth/login';
    }

    onMount(() => {
        initializeAuth();
    });
    
</script>

<div class="h-screen flex bg-gray-50 dark:bg-gray-900">

    <Sidebar />

    <div class="flex-1 flex flex-col overflow-hidden">

        <Header onLogout={handleLogout} />

        <main class="flex-1 overflow-auto p-6">
            {@render children()}
        </main>

    </div>

</div>