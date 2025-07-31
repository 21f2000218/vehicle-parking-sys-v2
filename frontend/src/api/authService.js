import http from '@/utils/http';
import axios from 'axios';
import { toastService } from '@/utils/toastService';

const base = process.env.VUE_APP_API_BASE_URL || '';

export const authService = {
  async register(data) {
    try {
      const response = await http.post('/auth/register', data);
      toastService.success('Registration successful!');
      return response.data;
    } catch (err) {
      const message = err.response?.data?.msg || 'Registration failed';
      toastService.error(message);
      throw err;
    }
  },
  async login(creds) {
    try {
      const response = await http.post('/auth/login', creds);
      toastService.success('Login successful!');
      return response.data;
    } catch (err) {
      const message = err.response?.data?.msg || 'Login failed';
      toastService.error(message);
      throw err;
    }
  },
  async refresh(refreshToken) {
    return axios.post(
      `${base}/auth/refresh`,
      null,
      { headers: { Authorization: `Bearer ${refreshToken}` } }
    );
  },
  async logout() {
    try {
      await http.post('/auth/logout');
      toastService.success('Logged out successfully');
    } catch (err) {
      console.error('Logout error:', err);
    }
  },
};
