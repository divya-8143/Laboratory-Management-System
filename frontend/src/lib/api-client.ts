import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to attach JWT token
apiClient.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('lms_access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

// Response interceptor for token refresh or error catching
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      if (typeof window !== 'undefined') {
        const refreshToken = localStorage.getItem('lms_refresh_token');
        if (refreshToken) {
          try {
            const res = await axios.post(`${API_BASE_URL}/auth/refresh`, {
              refresh_token: refreshToken,
            });
            const { access_token, refresh_token: newRefresh } = res.data;
            localStorage.setItem('lms_access_token', access_token);
            localStorage.setItem('lms_refresh_token', newRefresh);
            originalRequest.headers.Authorization = `Bearer ${access_token}`;
            return apiClient(originalRequest);
          } catch (refreshErr) {
            localStorage.removeItem('lms_access_token');
            localStorage.removeItem('lms_refresh_token');
            localStorage.removeItem('lms_user');
          }
        }
      }
    }
    return Promise.reject(error);
  }
);
