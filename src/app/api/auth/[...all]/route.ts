import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";
import { toNextJsHandler } from "better-auth/next-js";

// Better Auth configuration - moved here to ensure environment variables are available at runtime
const auth = betterAuth({
  database: {
    provider: "postgresql",
    url: process.env.DATABASE_URL!,
  },
  emailAndPassword: {
    enabled: true,
    autoSignIn: true,
  },
  secret: process.env.BETTER_AUTH_SECRET!,
  trustedOrigins: ["http://localhost:3000", "http://127.0.0.1:3000"],
  plugins: [
    jwt({
      secret: process.env.AUTH_JWT_SECRET || process.env.BETTER_AUTH_SECRET!,
      expiresIn: "7d",
    })
  ]
});

export const { GET, POST } = toNextJsHandler(auth);