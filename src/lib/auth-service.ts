export interface User {
  id: string;
  email: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface RegisterData {
  email: string;
  password: string;
}

export interface LoginData {
  email: string;
  password: string;
}

class AuthService {
  private API_BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'; // Updated to point to backend

  // For BetterAuth integration, we'll rely on the auth context to manage sessions
  // and make authenticated API calls using the JWT token from BetterAuth

  async register(userData: RegisterData): Promise<AuthResponse> {
    // This would be handled by the auth context using BetterAuth
    // For now, we'll keep this as a placeholder
    throw new Error('Registration should be handled by auth context using BetterAuth');
  }

  async login(credentials: LoginData): Promise<AuthResponse> {
    // This would be handled by the auth context using BetterAuth
    // For now, we'll keep this as a placeholder
    throw new Error('Login should be handled by auth context using BetterAuth');
  }

  async logout(): Promise<void> {
    // This would be handled by the auth context using BetterAuth
    // For now, we'll keep this as a placeholder
    throw new Error('Logout should be handled by auth context using BetterAuth');
  }

  async getCurrentUser(): Promise<User> {
    // Get JWT token from BetterAuth session
    const token = await this.getAccessToken();

    if (!token) {
      throw new Error('No access token found');
    }

    const response = await fetch(`${this.API_BASE_URL}/users/me`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error('Failed to fetch user data');
    }

    return response.json();
  }

  isAuthenticated(): boolean {
    // Check if we have a valid session by making a request to the session endpoint
    // This is a simplified approach - in practice, you'd check with the auth context
    return typeof window !== 'undefined' && !!localStorage.getItem('better-auth.session_token');
  }

  // Get access token - for BetterAuth with JWT, we need to access it properly
  async getAccessToken(): Promise<string | null> {
    // Get the session from BetterAuth's existing API
    try {
      // Better Auth stores session in cookies, so we need to access it differently
      // We'll use the auth client to get the session
      const sessionResponse = await fetch('/api/auth/session', {
        credentials: 'include',
      });

      if (!sessionResponse.ok) {
        return null;
      }

      const sessionData = await sessionResponse.json();
      
      // Better Auth typically stores the JWT in the session object
      // The exact property name may vary depending on Better Auth's implementation
      return sessionData?.session?.accessToken || sessionData?.session?.jwt || sessionData?.token || null;
    } catch (error) {
      console.error('Error getting access token:', error);
      return null;
    }
  }

  getRefreshToken(): string | null {
    return null;
  }

  // Method to refresh access token
  async refreshAccessToken(): Promise<string> {
    // BetterAuth handles session refreshing automatically
    const token = await this.getAccessToken();
    if (!token) {
      throw new Error('Could not refresh token');
    }
    return token;
  }

  // Generic method to make authenticated API calls to the backend
  async makeAuthenticatedRequest(endpoint: string, options: RequestInit = {}) {
    const url = `${this.API_BASE_URL}${endpoint}`;

    // Get the JWT token from BetterAuth
    const token = await this.getAccessToken();

    if (!token) {
      throw new Error('No authentication token available');
    }

    const authenticatedOptions: RequestInit = {
      ...options,
      headers: {
        ...options.headers,
        'Authorization': `Bearer ${token}`,
      }
    };

    const response = await fetch(url, authenticatedOptions);

    if (!response.ok) {
      if (response.status === 401) {
        // Unauthorized - possibly session expired
        throw new Error('Session expired. Please log in again.');
      }
      throw new Error(`API request failed: ${response.statusText}`);
    }

    return response;
  }
}

export default new AuthService();