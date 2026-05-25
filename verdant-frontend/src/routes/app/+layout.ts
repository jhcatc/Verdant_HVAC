import { browser } from '$app/environment';
import { redirect } from '@sveltejs/kit';

export const ssr = false;

export async function load({ url }) {

    if (!browser) {
        return {};
    }

    const token = localStorage.getItem('access_token');

    if (!token) {
        throw redirect(302, '/auth/login');
    }

    return {};
}