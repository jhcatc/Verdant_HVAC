import { writable } from 'svelte/store';

import * as apiAuth from '$lib/api/auth';

export const user = writable(null);

const TOKEN_KEY = 'access_token';

export function getToken(): string | null {
    return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string) {
    localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken() {
    localStorage.removeItem(TOKEN_KEY);
}

export async function fetchMe() {

    try {

        const me = await apiAuth.getMe();

        user.set(me);

        return me;

    } catch (err) {

        console.error('fetchMe failed', err);

        clearToken();

        user.set(null);

        return null;
    }
}

export async function initializeAuth() {

    const token = getToken();

    if (!token) {
        user.set(null);
        return null;
    }

    return await fetchMe();
}

export async function login(email: string, password: string) {

    const data = await apiAuth.login(email, password);

    setToken(data.access_token);

    const me = await fetchMe();

    return me;
}

export async function logout() {

    clearToken();

    user.set(null);
}