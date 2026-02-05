import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

interface ApiResponse<T = any> {
  data?: T;
  message?: string;
  error?: string;
}

class ApiClient {
  private client: AxiosInstance;

  constructor(baseURL: string = process.env.NEXT_PUBLIC_API_BASE_URL || '/api') {
    this.client = axios.create({
      baseURL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add request interceptor to include auth token
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Add response interceptor to handle token refresh
    this.client.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config;

        // If token is expired and not retrying
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;

          try {
            const refreshToken = localStorage.getItem('refresh_token');
            if (!refreshToken) {
              throw new Error('No refresh token available');
            }

            // Attempt to refresh the token
            const refreshResponse = await axios.post('/api/auth/refresh', {
              refresh_token: refreshToken,
            });

            const newAccessToken = refreshResponse.data.access_token;
            localStorage.setItem('access_token', newAccessToken);

            // Retry the original request with the new token
            originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
            return this.client(originalRequest);
          } catch (refreshError) {
            // If refresh fails, clear tokens and redirect to login
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            window.location.href = '/login';
            return Promise.reject(refreshError);
          }
        }

        return Promise.reject(error);
      }
    );
  }

  // Authentication methods
  async register(userData: {
    email: string;
    password: string;
    first_name?: string;
    last_name?: string;
  }): Promise<ApiResponse<{ user: any; access_token: string; refresh_token: string }>> {
    try {
      const response = await this.client.post('/auth/register', userData);
      // Store tokens
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('refresh_token', response.data.refresh_token);
      return response.data;
    } catch (error: any) {
      return { error: error.response?.data?.detail || error.message };
    }
  }

  async login(credentials: {
    email: string;
    password: string;
  }): Promise<ApiResponse<{ user: any; access_token: string; refresh_token: string }>> {
    try {
      const response = await this.client.post('/auth/login', credentials);
      // Store tokens
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('refresh_token', response.data.refresh_token);
      return response.data;
    } catch (error: any) {
      return { error: error.response?.data?.detail || error.message };
    }
  }

  async logout(): Promise<ApiResponse> {
    try {
      await this.client.post('/auth/logout');
      // Clear tokens
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      return { message: 'Successfully logged out' };
    } catch (error: any) {
      // Even if logout fails, clear local tokens
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      return { message: 'Logged out locally' };
    }
  }

  async forgotPassword(email: string): Promise<ApiResponse> {
    try {
      const response = await this.client.post('/auth/forgot-password', { email });
      return response.data;
    } catch (error: any) {
      return { error: error.response?.data?.detail || error.message };
    }
  }

  async resetPassword(token: string, newPassword: string): Promise<ApiResponse> {
    try {
      const response = await this.client.post('/auth/reset-password', {
        token,
        new_password: newPassword,
      });
      return response.data;
    } catch (error: any) {
      return { error: error.response?.data?.detail || error.message };
    }
  }

  // Generic request method
  async request<T>(config: AxiosRequestConfig): Promise<AxiosResponse<T>> {
    return this.client.request<T>(config);
  }
}

export const apiClient = new ApiClient();

export default ApiClient;