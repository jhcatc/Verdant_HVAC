<script lang="ts">
    import { login } from '$lib/stores/auth';
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import axios from 'axios';
    let email = $state('');
    let password = $state('');
    let error = $state('');
    let loading = $state(false);
    let emailInput: HTMLInputElement;
    let success = $state(false);

    onMount(() => {
        emailInput?.focus();
    });

    async function handleLogin() {

        if (!email.trim() || !password) {
            error = 'Please enter email and password';
            return;
        }

        loading = true;
        error = '';

        try {

            await login(email.trim(), password);

            success = true;

            window.location.href = '/app/dashboard';

            } catch (e: unknown) {

                if (axios.isAxiosError(e)) {

                    error =
                        e.response?.data?.detail ||
                        e.message ||
                        'Invalid credentials';

                } else if (e instanceof Error) {

                    error = e.message;

                } else {

                    error = 'Invalid credentials';
                }

                loading = false;
            }
    }


</script>

<div class="w-full flex flex-col items-center justify-center px-4">
    <div class="w-full max-w-md">
        <div class="text-center mb-8">
            <img src="/verdant.png" alt="Verdant" class="h-54 mx-auto mb-4 drop-shadow-lg" />
            <!--
            <h1 class="text-4xl font-light text-[#15803D] tracking-tight">
                Verdant ERP
            </h1>
            <p class="text-lg font-light text-[#15803D] mt-2">
                Sign in to your account
            </p>
            -->
        </div>

        <div class="bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm rounded-xl shadow-2xl p-8 border border-verdant-200 dark:border-gray-700">
            <form onsubmit={(e) => { e.preventDefault(); handleLogin(); }}>
                <div>

                    <div class="text-center mb-2">                        
                        <h1 class="text-4xl font-light text-[#15803D] tracking-tight">
                            Verdant ERP
                        </h1>
                        
                        <p class="text-lg font-light text-[#15803D] mt-2">
                            Sign in to your account
                        </p>
                    </div>

                    <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Email</label>
                    <input
                        bind:this={emailInput}
                        id="email"
                        type="email"
                        bind:value={email}
                        disabled={loading}
                        autocomplete="email"
                        class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-verdant-500 focus:border-transparent disabled:opacity-50 transition-colors"
                        placeholder="you@company.com"
                    />
                </div>
                
                <div class="mt-4">
                    <label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Password</label>
                    <input
                        id="password"
                        type="password"
                        bind:value={password}
                        disabled={loading}
                        autocomplete="current-password"
                        class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-verdant-500 focus:border-transparent disabled:opacity-50 transition-colors"
                        placeholder="Enter your password"
                    />
                </div>

                {#if error}
                    <div class="mt-4 text-red-600 dark:text-red-400 text-sm flex items-center gap-2 p-3 bg-red-50 dark:bg-red-900/20 rounded-lg">
                        <svg class="w-4 h-4 shrink-0" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
                        </svg>
                        {error}
                    </div>
                {/if}
                
                <button
                    type="submit"
                    disabled={loading || success}
                    class="w-full mt-6 py-3 px-4 bg-verdant-600 hover:bg-verdant-700 disabled:bg-verdant-400 text-white font-semibold rounded-lg transition-colors flex items-center justify-center gap-2 cursor-pointer"
                >
                    {#if loading || success}
                        <svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        {loading ? 'Signing in...' : 'Redirecting...'}
                    {:else}
                        Sign in
                    {/if}
                </button>

                    <footer class="mt-8 text-[13px] font-light text-[#15803D] tracking-wide">
                        Verdant HVAC · ERP · &copy 2026
                    </footer>

            </form>
        </div>

    </div>
</div>