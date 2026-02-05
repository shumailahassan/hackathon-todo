# Authentication API Reference

## Overview
This document provides a reference for the authentication APIs provided by the system.

## Frontend API

### Auth Context (`src/auth/context/auth-context.tsx`)

#### `AuthProvider`
React context provider that manages authentication state.

```tsx
<AuthProvider>
  {/* Your app components */}
</AuthProvider>
```

#### `useAuth()` Hook
Provides access to authentication state and methods.

**Return Value:**
- `user: UserIdentity | null` - Current authenticated user or null
- `loading: boolean` - Whether authentication state is loading
- `isAuthenticated: boolean` - Whether user is authenticated
- `signin(email, password)` - Function to sign in user
- `signup(email, password, name?)` - Function to sign up user
- `logout()` - Function to sign out user

### Client Utilities (`src/auth/client.ts`)

#### `signIn`
Better Auth sign-in function.

#### `signUp`
Better Auth sign-up function.

#### `signOut`
Better Auth sign-out function.

#### `getJwtToken()`
Retrieves the JWT token from the current session.

**Returns:** `Promise<string | null>`

#### `getAuthHeaders()`
Gets headers with JWT token for authenticated requests.

**Returns:** `Promise<Record<string, string>>`

### Validation Utilities (`src/auth/utils/validation.ts`)

#### `validateEmail(email)`
Validates email format.

**Parameters:**
- `email: string`

**Returns:** `boolean`

#### `validatePassword(password)`
Validates password strength.

**Parameters:**
- `password: string`

**Returns:** `boolean`

#### `validateSignupRequest(data)`
Validates signup request data.

**Parameters:**
- `data: SignupRequest` - Contains email, password, name

**Returns:** `{ isValid: boolean; errors: string[] }`

#### `validateSigninRequest(data)`
Validates signin request data.

**Parameters:**
- `data: SigninRequest` - Contains email, password

**Returns:** `{ isValid: boolean; errors: string[] }`

### API Client (`src/frontend/lib/api-client.ts`)

#### `ApiClient` Class
A client for making authenticated API requests.

**Constructor:**
- `new ApiClient(baseUrl: string)`

**Methods:**
- `request<T>(endpoint, options, useAuth?)` - Generic request method
- `get<T>(endpoint, options?)` - GET request
- `post<T>(endpoint, data?, options?)` - POST request
- `put<T>(endpoint, data, options?)` - PUT request
- `delete<T>(endpoint, options?)` - DELETE request

### Shared Types (`src/shared/types/auth.ts`)

#### `UserIdentity`
Represents a user's identity.

**Properties:**
- `userId: string`
- `email: string`
- `name?: string`

#### `JwtPayload`
Structure of JWT token payload.

**Properties:**
- `userId: string`
- `email: string`
- `iat: number` - Issue timestamp
- `exp: number` - Expiration timestamp
- `jti?: string` - JWT ID

#### `AuthResponse`
Response structure for authentication requests.

**Properties:**
- `token: string` - JWT token
- `user: UserIdentity`
- `expiresIn: number` - Token expiry in seconds

#### `SignupRequest`
Request structure for signup.

**Properties:**
- `email: string`
- `password: string`
- `name?: string`

#### `SigninRequest`
Request structure for signin.

**Properties:**
- `email: string`
- `password: string`

#### `TokenValidationResult`
Result of token validation.

**Properties:**
- `isValid: boolean`
- `user?: UserIdentity`
- `error?: string`

## Backend API

### Authentication Dependencies (`src/backend/auth/deps.py`)

#### `get_current_user`
FastAPI dependency to get the current authenticated user.

**Usage:**
```python
from src.backend.auth.deps import get_current_user

async def some_endpoint(current_user = Depends(get_current_user)):
    # current_user contains user information
```

#### `get_current_active_user`
FastAPI dependency to get the current authenticated and active user.

**Usage:**
```python
from src.backend.auth.deps import get_current_active_user

async def some_endpoint(current_user = Depends(get_current_active_user)):
    # current_user contains active user information
```

#### `get_current_user_optional()`
Function that returns a dependency for getting user if authenticated, or None.

**Usage:**
```python
from src.backend.auth.deps import get_current_user_optional

async def some_endpoint(current_user = Depends(get_current_user_optional())):
    # current_user is UserIdentity if authenticated, None otherwise
```

### Authentication Utilities (`src/backend/auth/utils.py`)

#### `get_current_user_from_token`
Dependency to extract user from JWT token.

#### `validate_jwt_token(token)`
Validates a JWT token and returns user identity if valid.

**Parameters:**
- `token: str`

**Returns:** `Optional[UserIdentity]`

#### `require_authentication()`
Returns a dependency that requires authentication.

#### `get_optional_user()`
Returns a dependency for getting user if authenticated, or None.

### Security Utilities (`src/backend/core/security.py`)

#### `verify_password(plain_password, hashed_password)`
Verifies a plain password against a hashed password.

**Returns:** `bool`

#### `get_password_hash(password)`
Hashes a password.

**Returns:** `str`

#### `create_access_token(data, expires_delta=None)`
Creates a JWT access token.

**Parameters:**
- `data: dict` - Data to encode in token
- `expires_delta: Optional[timedelta]` - Token expiry time

**Returns:** `str`

#### `verify_token(token)`
Verifies a JWT token and returns payload if valid.

**Parameters:**
- `token: str`

**Returns:** `Optional[Dict[str, Any]]`

### Authentication Middleware (`src/backend/auth/middleware.py`)

#### `AuthMiddleware`
Middleware that adds current user to request state.

#### `StrictAuthMiddleware`
Strict middleware that rejects requests with invalid tokens.

**Constructor Parameters:**
- `exempt_paths: Optional[list]` - Paths that don't require authentication

#### `get_current_user_from_request(request)`
Helper to get current user from request state.

#### `is_authenticated(request)`
Checks if request is authenticated.

### Authentication Schemas (`src/backend/auth/schemas.py`)

#### `Token`
Schema for JWT token response.

**Properties:**
- `access_token: str`
- `token_type: str`

#### `UserCreate`
Schema for user creation requests.

**Properties:**
- `email: EmailStr`
- `name: Optional[str]`
- `password: str`

#### `UserLogin`
Schema for user login requests.

**Properties:**
- `email: EmailStr`
- `password: str`

#### `UserResponse`
Schema for user response.

**Properties:**
- `id: str`
- `email: EmailStr`
- `name: Optional[str]`
- `created_at: datetime`
- `updated_at: Optional[datetime]`

#### `AuthResponse`
Schema for authentication response.

**Properties:**
- `token: str`
- `user: UserIdentityResponse`
- `expires_in: int`

## Better Auth Configuration (`src/auth/better-auth.config.ts`)

#### `auth`
The Better Auth configuration object with JWT plugin enabled.

**Features:**
- JWT token generation and validation
- Database integration with Neon PostgreSQL
- Email/password authentication
- Account linking capabilities

## Environment Variables

### Frontend
- `NEXT_PUBLIC_AUTH_BASE_URL` - Base URL for authentication API
- `NEXT_PUBLIC_API_BASE_URL` - Base URL for main API

### Backend
- `AUTH_JWT_SECRET` or `AUTH_SECRET` - Secret key for JWT signing
- `DATABASE_URL` - Database connection string
- `AUTH_URL` - Base URL for authentication endpoints

## Error Responses

The authentication system returns standardized error responses:

### HTTP 400 - Bad Request
```json
{
  "detail": "Validation error",
  "errors": ["Email is required", "Invalid email format"]
}
```

### HTTP 401 - Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### HTTP 403 - Forbidden
```json
{
  "detail": "Insufficient permissions"
}
```

## Example Usage Patterns

### Frontend - Protecting Routes
```tsx
import { useAuth } from '../auth/context/auth-context';
import { useRouter } from 'next/router';

export default function ProtectedPage() {
  const { isAuthenticated, loading } = useAuth();
  const router = useRouter();

  if (loading) return <div>Loading...</div>;

  if (!isAuthenticated) {
    useEffect(() => {
      router.push('/auth/login');
    }, [router]);

    return <div>Redirecting...</div>;
  }

  return <div>This is a protected page</div>;
}
```

### Backend - Protecting Endpoints
```python
from fastapi import Depends
from src.backend.auth.deps import get_current_user

@app.get("/api/user/profile")
async def get_profile(current_user = Depends(get_current_user)):
    return {
        "user_id": current_user.user_id,
        "email": current_user.email,
        "profile": get_user_profile(current_user.user_id)
    }
```

This reference provides all the information needed to integrate with the authentication system.