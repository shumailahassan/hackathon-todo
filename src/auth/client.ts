import { createAuthClient } from "better-auth/client";
import { jwt } from "better-auth/plugins";

// Initialize Better Auth client
export const {
  signIn,
  signUp,
  signOut,
  useSession,
  getClientUser,
  getCsrf,
  forgotPassword,
  resetPassword,
} = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_AUTH_BASE_URL || "http://localhost:3000/api/auth",
  plugins: [
    jwt(),
  ],
});

// Helper function to get JWT token from session
export const getJwtToken = async (): Promise<string | null> => {
  try {
    const session = await getClientUser();
    if (session?.jwt) {
      return session.jwt;
    }
    return null;
  } catch (error) {
    console.error("Error getting JWT token:", error);
    return null;
  }
};

// Helper function to include auth headers in API requests
export const getAuthHeaders = async (): Promise<Record<string, string>> => {
  const token = await getJwtToken();
  return {
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
};