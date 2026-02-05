# Authentication System Integration Guide

## Overview
This guide explains how to integrate with the authentication system using Better Auth and JWT tokens in both frontend and backend applications.

## Frontend Integration

### 1. Setting up the Auth Provider
Wrap your application with the `AuthProvider` to enable authentication context:

```tsx
// In your _app.tsx or root layout
import { AuthProvider } from '../auth/context/auth-context';

export default function App({ Component, pageProps }) {
  return (
    <AuthProvider>
      <Component {...pageProps} />
    </AuthProvider>
  );
}
```

### 2. Using the Authentication Context
Access authentication state and methods using the `useAuth` hook:

```tsx
import { useAuth } from '../auth/context/auth-context';

export default function MyComponent() {
  const { user, loading, isAuthenticated, signin, signup, logout } = useAuth();

  if (loading) return <div>Loading...</div>;

  if (!isAuthenticated) {
    return (
      <div>
        <h2>Please sign in</h2>
        {/* Signin/Signup forms */}
      </div>
    );
  }

  return (
    <div>
      <h2>Welcome, {user?.name || user?.email}!</h2>
      <button onClick={logout}>Logout</button>
    </div>
  );
}
```

### 3. Making Authenticated API Requests
Use the `apiClient` to make requests with automatic JWT inclusion:

```tsx
import { apiClient } from '../frontend/lib/api-client';

// The API client automatically includes the JWT token in requests
const fetchUserData = async () => {
  try {
    const userData = await apiClient.get('/users/me');
    return userData;
  } catch (error) {
    console.error('Error fetching user data:', error);
    throw error;
  }
};

// Or make a POST request
const createUser = async (userData) => {
  try {
    const result = await apiClient.post('/users', userData);
    return result;
  } catch (error) {
    console.error('Error creating user:', error);
    throw error;
  }
};
```

### 4. Validation Functions
Use the provided validation functions to validate user input:

```tsx
import { validateSignupRequest, validateSigninRequest, validateEmail, validatePassword } from '../auth/utils/validation';

// Validate signup data
const signupData = { email: 'user@example.com', password: 'SecurePass123!' };
const validationResult = validateSignupRequest(signupData);

if (validationResult.isValid) {
  // Proceed with signup
} else {
  // Show validation errors
  console.log('Validation errors:', validationResult.errors);
}
```

## Backend Integration

### 1. Protected Routes
Use the authentication dependencies to protect your routes:

```python
from fastapi import Depends
from src.backend.auth.deps import get_current_user, get_current_active_user

@app.get("/protected-endpoint")
async def protected_endpoint(current_user = Depends(get_current_user)):
    # current_user contains user identity information
    return {"user_id": current_user.user_id, "email": current_user.email}
```

### 2. Accessing Current User Information
The authentication system provides the current user information to route handlers:

```python
from src.backend.auth.deps import get_current_user
from src.shared.types.auth import UserIdentity

@app.get("/dashboard")
async def get_dashboard_data(current_user: UserIdentity = Depends(get_current_user)):
    # Access user information
    user_id = current_user.user_id
    user_email = current_user.email

    # Use user information in your business logic
    user_data = get_user_specific_data(user_id)

    return {"user_data": user_data, "user_info": {"id": user_id, "email": user_email}}
```

### 3. Optional Authentication
For routes that work differently based on authentication status:

```python
from src.backend.auth.deps import get_current_user_optional

@app.get("/homepage")
async def get_homepage(current_user = Depends(get_current_user_optional())):
    if current_user:
        # User is authenticated - return personalized content
        return {"content": "Personalized homepage", "user": current_user.email}
    else:
        # User is not authenticated - return generic content
        return {"content": "Public homepage", "user": None}
```

### 4. Backend Agent Integration
Backend Agent can access authenticated user information through the dependency injection system:

```python
@app.get("/backend-agent-feature")
async def backend_agent_feature(current_user: UserIdentity = Depends(get_current_user)):
    # Backend Agent can access all user information through current_user
    # This enables user-specific business logic
    user_permissions = get_user_permissions(current_user.user_id)
    user_data = get_user_data(current_user.user_id)

    return {
        "user_data": user_data,
        "permissions": user_permissions,
        "user_id": current_user.user_id
    }
```

## Environment Variables

### Frontend
- `NEXT_PUBLIC_AUTH_BASE_URL` - Base URL for authentication API
- `NEXT_PUBLIC_API_BASE_URL` - Base URL for your main API

### Backend
- `AUTH_JWT_SECRET` or `AUTH_SECRET` - Secret key for JWT signing
- `DATABASE_URL` - Database connection string

## Error Handling

### Frontend
The authentication system handles errors appropriately:

```tsx
const handleSignup = async () => {
  try {
    await signup(email, password, name);
    // Success - user is now logged in
    onSuccess();
  } catch (error) {
    // Error is automatically handled by the auth system
    console.error('Signup failed:', error);
    onError(error.message);
  }
};
```

### Backend
The authentication system returns appropriate HTTP status codes:
- `401 Unauthorized` - Invalid or missing authentication
- `400 Bad Request` - Invalid input data
- `422 Unprocessable Entity` - Validation errors

## Security Best Practices

1. **Always use HTTPS in production** - Never transmit JWT tokens over unencrypted connections
2. **Store JWT secrets securely** - Use environment variables or secret management systems
3. **Validate all inputs** - Use the provided validation functions
4. **Handle token expiration** - Implement token refresh mechanisms when needed
5. **Sanitize user inputs** - The authentication system handles this automatically
6. **Log authentication events** - For security monitoring and audit trails

## Testing

### Frontend Tests
```tsx
// Example test for authentication
import { renderHook, act } from '@testing-library/react';
import { useAuth } from '../auth/context/auth-context';

test('should handle user authentication', async () => {
  const { result } = renderHook(() => useAuth());

  // Test authentication flow
  await act(async () => {
    await result.current.signin('test@example.com', 'password');
  });

  expect(result.current.isAuthenticated).toBe(true);
  expect(result.current.user.email).toBe('test@example.com');
});
```

### Backend Tests
```python
# Example test for protected route
def test_protected_route_requires_auth(client):
    response = client.get("/protected-endpoint")
    assert response.status_code == 401  # Unauthorized without token

def test_protected_route_with_valid_token(client, valid_token):
    response = client.get(
        "/protected-endpoint",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 200  # Success with valid token
    assert "user_id" in response.json()
```

## Common Integration Patterns

### 1. Conditional Rendering Based on Auth State
```tsx
import { useAuth } from '../auth/context/auth-context';

export default function ConditionalComponent() {
  const { isAuthenticated, user } = useAuth();

  if (!isAuthenticated) {
    return <LoginForm />;
  }

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Welcome back, {user?.name || user?.email}!</p>
    </div>
  );
}
```

### 2. Authorization Checks
```python
from src.backend.auth.deps import get_current_user

def check_user_permission(current_user, required_permission):
    # Implement your permission logic here
    user_perms = get_user_permissions(current_user.user_id)
    return required_permission in user_perms

@app.get("/admin-panel")
async def admin_panel(current_user = Depends(get_current_user)):
    if not check_user_permission(current_user, "admin"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    return {"message": "Welcome to admin panel"}
```

This guide provides everything needed to integrate with the authentication system effectively.