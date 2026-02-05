/**
 * Shared authentication types used across frontend and backend
 */

export interface UserIdentity {
  userId: string;
  email: string;
  name?: string;
}

export interface JwtPayload {
  userId: string;
  email: string;
  iat: number; // issued at
  exp: number; // expiration
  jti?: string; // JWT ID
}

export interface AuthResponse {
  token: string;
  user: UserIdentity;
  expiresIn: number;
}

export interface SignupRequest {
  email: string;
  password: string;
  name?: string;
}

export interface SigninRequest {
  email: string;
  password: string;
}

export interface SigninResponse extends AuthResponse {}

export interface TokenValidationResult {
  isValid: boolean;
  user?: UserIdentity;
  error?: string;
}