import { browser } from '$app/environment';
import { redirect } from '@sveltejs/kit';

export const ssr = false;

export async function load({ url }) {

    if (!browser) {
        return {};
    }

    const token = localStorage.getItem('access_token');

    // SOLO bloquear si YA está logueado
    if (token && url.pathname === '/auth/login') {
        throw redirect(302, '/app/dashboard');
    }

    return {};
}