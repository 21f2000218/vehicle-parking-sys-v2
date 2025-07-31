import axios from 'axios';
import store from '@/store';
import { toastService } from './toastService';

const http = axios.create({
    baseURL: process.env.VUE_APP_API_BASE_URL || '',
    headers: { 'Content-Type': 'application/json' },
});

let isRefreshing = false;
let subscribers = [];

function subscribe(cb) { subscribers.push(cb); }

function onRefreshed(token) {
    subscribers.forEach(cb => cb(token));
    subscribers = [];
}

http.interceptors.request.use(config => {
    const token = store.state.auth.accessToken;

    const isAuthRoute = config.url.includes('/auth/login') || config.url.includes('/auth/register');

    if (token && !config.__isRetryRequest) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

http.interceptors.response.use(
    res => {
        if (res.config.showToastSuccess && res.data?.msg) {
            console.log(res.data)
            toastService.success(res.data.msg);
        }
        return res;
    },
    err => {
        const { config, response } = err;

        const message = response?.data?.msg || response?.data?.err || 'Something went wrong';

        const isPublicRoute =
            config?.url?.includes('/auth/login') || config?.url?.includes('/auth/register');

        if (response?.status === 401 && !isPublicRoute) {
            toastService.warning('Unauthorized. Please login again.');
            store.dispatch('auth/logout');
        } else if (response?.status === 422) {
            toastService.error('Validation failed.');
        } else {
            toastService.error(message);
        }

        const isAuthRoute = config.url.includes('/auth/login') || config.url.includes('/auth/register');

        if (response?.status === 401 && !config.__isRetryRequest && !isAuthRoute) {
            if (!isRefreshing) {
                isRefreshing = true;
                store.dispatch('auth/refreshToken')
                    .then(newToken => {
                        isRefreshing = false;
                        onRefreshed(newToken);
                    })
                    .catch(() => {
                        isRefreshing = false;
                        subscribers = [];
                        store.dispatch('auth/logout');
                    });
            }
            return new Promise((resolve, reject) => {
                subscribe(token => {
                    config.__isRetryRequest = true;
                    config.headers.Authorization = `Bearer ${token}`;
                    resolve(http(config));
                });
            });
        }
        return Promise.reject(err);
    }
);

export default http;
