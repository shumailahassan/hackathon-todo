'use client';

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { useSession, signIn, signOut, signUp } from '../client';
import { UserIdentity } from '../../shared/types/auth';

interface AuthContextType {
  user: UserIdentity | null;
  loading: boolean;
  isAuthenticated: boolean;
  signin: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string, name?: string) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<UserIdentity | null>(null);
  const [loading, setLoading] = useState(true);
  const { data: session, isLoading } = useSession();

  useEffect(() => {
    if (!isLoading) {
      if (session?.user) {
        // Map session user to our UserIdentity type
        setUser({
          userId: session.user.id,
          email: session.user.email,
          name: session.user.name,
        });
      } else {
        setUser(null);
      }
      setLoading(false);
    }
  }, [session, isLoading]);

  const signin = async (email: string, password: string) => {
    setLoading(true);
    try {
      await signIn['email-password']({ email, password });
    } finally {
      setLoading(false);
    }
  };

  const signup = async (email: string, password: string, name?: string) => {
    setLoading(true);
    try {
      await signUp.email({
        email,
        password,
        name: name || email.split('@')[0], // Use email prefix as name if not provided
      });
      // Automatically sign in after successful signup
      await signin(email, password);
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    setLoading(true);
    try {
      await signOut();
    } finally {
      setUser(null);
      setLoading(false);
    }
  };

  const value: AuthContextType = {
    user,
    loading: loading || isLoading,
    isAuthenticated: !!user,
    signin,
    signup,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;