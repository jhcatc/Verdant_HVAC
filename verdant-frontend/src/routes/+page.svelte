<script lang="ts">
    import { browser } from '$app/environment';
    import { goto } from '$app/navigation';
    import { storage } from '$lib/stores/storage';
    import { getToken } from '$lib/stores/auth';
    
    if (browser) {
        const token = getToken();
        if (token) {
            goto('/app/dashboard');
        } else {
            goto('/auth/login');
        }
    }
</script>

<div class="flex items-center justify-center min-h-screen">
    <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-verdant-600"></div>
</div>