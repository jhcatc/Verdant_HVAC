<script lang="ts">
    import { user } from '$lib/stores/auth';
    import ThemeToggle from './ThemeToggle.svelte';

    let { onLogout = null } = $props();

    function getAvatar(role?: string) {

        switch (role) {

            case 'CEO':
                return '👑';

            case 'OPERATIONAL_DIRECTOR':
                return '🧠';

            case 'COMMERCIAL_DIRECTOR':
                return '📈';

            case 'ADMIN_SUPPORT':
                return '🗂️';

            case 'DISPATCHER':
                return '🚚';

            case 'TECHNICIAN':
                return '🛠️';

            default:
                return '👤';
        }
    }

    function getRoleLabel(role?: string) {

        if (!role) {
            return 'Staff';
        }

        return role.replaceAll('_', ' ');
    }

    function handleLogout() {

        if (onLogout) {
            onLogout();
        }
    }
</script>

<header class="h-16 shrink-0 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between px-6">

    <!-- LEFT -->
    <div class="flex items-center">
        <h1 class="text-lg font-semibold text-gray-800 dark:text-white">
            Verdant ERP
        </h1>
    </div>

    <!-- RIGHT -->
    <div class="flex items-center space-x-4">

        <ThemeToggle />

        <div class="flex items-center space-x-3 pl-4 border-l border-gray-200 dark:border-gray-700">

            <!-- USER -->
            <div class="text-right">

                <p class="text-sm font-medium text-gray-800 dark:text-white">
                    {$user?.full_name ?? 'User'}
                </p>

                <p class="text-xs text-gray-500 dark:text-gray-400">
                    {getRoleLabel($user?.role?.name)}
                </p>

            </div>

            <!-- AVATAR -->
            <div class="w-10 h-10 rounded-full bg-emerald-100 dark:bg-emerald-900 flex items-center justify-center text-lg">
                {getAvatar($user?.role?.name)}
            </div>

        </div>

        {#if onLogout}

            <button
                onclick={handleLogout}
                class="text-sm text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 transition-colors"
            >
                Logout
            </button>

        {/if}

    </div>

</header>