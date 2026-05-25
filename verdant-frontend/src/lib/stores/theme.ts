import { browser } from '$app/environment';
import { writable, get } from 'svelte/store';
import { storage } from './storage';

type Theme = 'light' | 'dark';

function getStoredTheme(): Theme {
    if (browser) {
        const stored = storage.getItem('theme', 'light');
        return (stored as Theme) || 'light';
    }
    return 'light';
}

function applyTheme(value: Theme) {
    if (browser) {
        if (value === 'dark') {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
    }
}

function createThemeStore() {
    const initial = getStoredTheme();
    if (browser && initial === 'dark') {
        applyTheme('dark');
    }
    
    const { subscribe, set } = writable<Theme>(initial);

    return {
        subscribe,
        set: (value: Theme) => {
            set(value);
            applyTheme(value);
            storage.setItem('theme', value);
        },
        update: (fn: (value: Theme) => Theme) => {
            const newValue = fn(get({ subscribe }));
            set(newValue);
            applyTheme(newValue);
            storage.setItem('theme', newValue);
        },
        get: () => get({ subscribe })
    };
}

export const theme = createThemeStore();

export function toggleTheme() {
    theme.update(current => current === 'light' ? 'dark' : 'light');
}

export function initTheme() {
    const stored = getStoredTheme();
    applyTheme(stored);
}