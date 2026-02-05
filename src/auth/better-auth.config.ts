import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";

// Better Auth configuration with JWT support
export const auth = betterAuth({
  database: {
    provider: "postgresql",
    url: process.env.DATABASE_URL!,
  },
  plugins: [
    jwt({
      secret: process.env.AUTH_JWT_SECRET || process.env.AUTH_SECRET!,
      expiresIn: "7d", // Token expires in 7 days
    }),
  ],
  account: {
    accountLinking: {
      enabled: true,
    },
  },
  socialProviders: {
    // Add social providers if needed
  },
  emailAndPassword: {
    enabled: true,
    autoSignIn: true,
  },
  advanced: {
    version: "v1",
  },
});

// Export types for use in frontend and backend
export type { User } from "better-auth/types";