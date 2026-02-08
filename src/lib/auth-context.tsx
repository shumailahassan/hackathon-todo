"use client";

import React, { createContext, useContext, ReactNode, useEffect, useState } from "react";
import { useBetterSession, signIn as betterSignIn, signUp as betterSignUp, signOut as betterSignOut } from "./auth-client";

interface User {
  id: string;
  email: string;
  name: string;
  image?: string;
  emailVerified: boolean;
  createdAt: Date;
  updatedAt: Date;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<{ success: boolean; error?: string }>;
  register: (data: { email: string; password: string }) => Promise<{ success: boolean; error?: string }>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const sessionAtom = useBetterSession; // **don't call it**
  const { data: session, isPending } = sessionAtom;

  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setIsLoading(isPending);
  }, [isPending]);

  const login = async (email: string, password: string) => {
    try {
      const result = await betterSignIn.email({ email, password });

      if (result?.error) {
        return { success: false, error: result.error.message || "Login failed" };
      }

      return { success: true };
    } catch (err: any) {
      console.error("Login error:", err);
      return { success: false, error: err.message || "Login failed. Please try again." };
    }
  };

  const register = async (data: { email: string; password: string }) => {
    try {
      const result = await betterSignUp.email({
        email: data.email,
        password: data.password,
        name: data.email, // Better Auth requires a name field; using email as placeholder
      });

      if (result?.error) {
        return { success: false, error: result.error.message || "Registration failed" };
      }

      return { success: true };
    } catch (err: any) {
      console.error("Registration error:", err);
      return { success: false, error: err.message || "Registration failed. Please try again." };
    }
  };

  const logout = async () => {
    await betterSignOut(); // redirect can be handled in your page
  };

  return (
    <AuthContext.Provider
      value={{
        user: session?.user || null,
        isAuthenticated: !!session?.user,
        isLoading,
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within an AuthProvider");
  return context;
};
