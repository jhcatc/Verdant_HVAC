import { browser } from '$app/environment';
import { redirect } from '@sveltejs/kit';

export function load() {

    if (!browser) {
        return {};
    }

    const token = localStorage.getItem('access_token');

    if (token) {
        throw redirect(302, '/app/dashboard');
    }

    return {};
}