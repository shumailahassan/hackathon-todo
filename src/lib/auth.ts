import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";

const databaseUrl = process.env.DATABASE_URL!;
const secret = process.env.BETTER_AUTH_SECRET!;

export const auth = betterAuth({
  database: {
    provider: "postgresql",
    url: databaseUrl,
  },
  emailAndPassword: {
    enabled: true,
    autoSignIn: true,
  },
  secret: secret,
  trustedOrigins: ["http://localhost:3000"],
  plugins: [
    jwt({
      secret: process.env.AUTH_JWT_SECRET || secret,
    }),
  ],
});
