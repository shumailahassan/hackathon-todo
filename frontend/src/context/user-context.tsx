import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { TokenManager } from '../lib/token-manager';
import { User } from '../lib/auth-service';

interface UserContextType {
  user: User | null;
  loading: boolean;
  isAuthenticated: boolean;
  login: (userData: { user: User; accessToken: string; refreshToken: string }) => void;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

interface UserProviderProps {
  children: ReactNode;
}

export function UserProvider({ children }: UserProviderProps) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for existing user session on initial load
    const initializeUserSession = async () => {
      try {
        if (TokenManager.hasAccessToken() && !TokenManager.isAccessTokenExpired()) {
          // Try to get user info from token or API
          // For now, we'll just set isAuthenticated to true
          // In a real app, you'd fetch user details from the API
        }
      } catch (error) {
        console.error('Error initializing user session:', error);
        // Clear invalid tokens
        TokenManager.removeTokens();
      } finally {
        setLoading(false);
      }
    };

    initializeUserSession();
  }, []);

  const login = (userData: { user: User; accessToken: string; refreshToken: string }) => {
    TokenManager.storeTokens(userData.accessToken, userData.refreshToken);
    setUser(userData.user);
  };

  const logout = () => {
    TokenManager.removeTokens();
    setUser(null);
  };

  const refreshUser = async () => {
    // In a real implementation, you would fetch updated user data
    // For now, just a placeholder
  };

  const value: UserContextType = {
    user,
    loading,
    isAuthenticated: !!user && TokenManager.hasAccessToken() && !TokenManager.isAccessTokenExpired(),
    login,
    logout,
    refreshUser,
  };

  return <UserContext.Provider value={value}>{children}</UserContext.Provider>;
}

export function useUser() {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
}