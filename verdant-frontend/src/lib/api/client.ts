import axios from 'axios';
import { browser } from '$app/environment';
const api = axios.create({

    baseURL:

        import.meta.env.VITE_API_URL ||

        'http://localhost:8000',

    withCredentials: true
});

// =====================================================
// REQUEST INTERCEPTOR
// =====================================================

api.interceptors.request.use(

    (config) => {

        if (browser) {

            const token =
                localStorage.getItem(
                    'access_token'
                );

            if (token) {

                config.headers.Authorization =
                    `Bearer ${token}`;
            }
        }

        return config;
    }
);

// =====================================================
// RESPONSE INTERCEPTOR
// =====================================================

api.interceptors.response.use(

    (response) => response,

    async (error) => {

        if (
            error.response?.status === 401 &&
            browser
        ) {

            localStorage.removeItem(
                'access_token'
            );

            if (
                window.location.pathname.startsWith(
                    '/app'
                )
            ) {

                window.location.href =
                    '/auth/login';
            }
        }

        return Promise.reject(error);
    }
);

export default api;