import { browser } from '$app/environment';
import { writable } from 'svelte/store';
import type { Writable } from 'svelte/store';

type CookieOptions = {
    expires?: number;
    path?: string;
};

function parseCookie(cookieString: string, key: string): string | null {
    const match = cookieString.match(new RegExp(`(?:^|;\\s*)${key}=([^;]*)`));
    return match ? decodeURIComponent(match[1]) : null;
}

function createCookieStore(key: string, defaultValue: string, options: CookieOptions = {}) {
    const { path = '/' } = options;
    let _value = defaultValue;

    if (browser) {
        const cookieValue = parseCookie(document.cookie, key);
        if (cookieValue !== null) {
            _value = cookieValue;
        }
    }

    const store: Writable<string> & { get: () => string } = writable(_value);

    store.subscribe((value) => {
        _value = value;
    });

    store.get = () => _value;

    return {
        subscribe: store.subscribe,
        set: (value: string) => {
            store.set(value);
            if (browser) {
                const expires = options.expires
                    ? `; expires=${new Date(Date.now() + options.expires * 864e5).toUTCString()}`
                    : '';
                document.cookie = `${key}=${encodeURIComponent(value)}; path=${path}${expires}; SameSite=Lax`;
            }
        },
        update: store.update,
        get: () => _value
    };
}

export const storage = {
    getItem: (key: string, defaultValue = ''): string => {
        if (browser) {
            const value = parseCookie(document.cookie, key);
            if (value !== null) return value;
        }
        return defaultValue;
    },
    setItem: (key: string, value: string, options?: CookieOptions) => {
        if (browser) {
            const path = options?.path ?? '/';
            const expires = options?.expires
                ? `; expires=${new Date(Date.now() + options.expires * 864e5).toUTCString()}`
                : '';
            document.cookie = `${key}=${encodeURIComponent(value)}; path=${path}${expires}; SameSite=Lax`;
        }
    },
    removeItem: (key: string, path = '/') => {
        if (browser) {
            document.cookie = `${key}=; path=${path}; expires=Thu, 01 Jan 1970 00:00:00 GMT; SameSite=Lax`;
        }
    },
    local: {
        getItem: (key: string): string | null => {
            if (browser) return localStorage.getItem(key);
            return null;
        },
        setItem: (key: string, value: string) => {
            if (browser) localStorage.setItem(key, value);
        },
        removeItem: (key: string) => {
            if (browser) localStorage.removeItem(key);
        }
    },
};