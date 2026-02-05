# Quickstart Guide: Authentication Module

## Overview
This guide explains how to set up and use the authentication module for user registration, login, logout, and password reset functionality.

## Prerequisites
- Node.js v16+ (for frontend)
- Python 3.9+ (for backend)
- PostgreSQL or Neon PostgreSQL database
- Environment variables configured (see below)

## Setup

### 1. Environment Variables
Create a `.env` file with the following variables:

```bash
# Database Configuration
DATABASE_URL="postgresql://username:password@localhost:5432/auth_db"

# JWT Configuration
JWT_SECRET="your-super-secret-jwt-key-here-make-it-long-and-random"
JWT_EXPIRATION="24h"  # Access token expiration
REFRESH_TOKEN_EXPIRATION="7d"  # Refresh token expiration

# Email Configuration (for password reset)
EMAIL_HOST="smtp.gmail.com"
EMAIL_PORT=587
EMAIL_USER="your-email@gmail.com"
EMAIL_PASSWORD="your-app-password"

# Password Requirements
MIN_PASSWORD_LENGTH=8
REQUIRE_UPPERCASE=true
REQUIRE_LOWERCASE=true
REQUIRE_NUMBERS=true
REQUIRE_SPECIAL_CHARS=true

# Rate Limiting
LOGIN_ATTEMPTS_LIMIT=5
LOGIN_ATTEMPTS_WINDOW=900  # 15 minutes in seconds
```

### 2. Database Setup
Run the following SQL commands to create the necessary tables:

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP WITH TIME ZONE
);

-- Sessions table
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR(500) NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_accessed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    device_info TEXT,
    ip_address INET
);

-- Password reset tokens table
CREATE TABLE password_reset_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    used_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### 3. Installation
```bash
# Backend (FastAPI)
pip install fastapi uvicorn bcrypt python-jose[cryptography] passlib[bcrypt] python-multipart

# Frontend (Next.js)
npm install axios react-hook-form @hookform/resolvers yup
```

## API Endpoints

### User Registration
- **POST** `/api/auth/register`
- Request body:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "first_name": "John",
  "last_name": "Doe"
}
```
- Response: User object with JWT token

### User Login
- **POST** `/api/auth/login`
- Request body:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```
- Response: User object with access and refresh tokens

### User Logout
- **POST** `/api/auth/logout`
- Headers: Authorization: Bearer {access_token}
- Response: Success message

### Password Reset Request
- **POST** `/api/auth/forgot-password`
- Request body:
```json
{
  "email": "user@example.com"
}
```
- Response: Success message (without indicating if email exists)

### Password Reset
- **POST** `/api/auth/reset-password`
- Request body:
```json
{
  "token": "reset-token-from-email",
  "new_password": "NewSecurePassword123!"
}
```
- Response: Success message

## Frontend Components

### Register Form Component
```jsx
// src/components/auth/RegisterForm.jsx
import { useForm } from 'react-hook-form';
import { registerUser } from '@/lib/api-client';

export default function RegisterForm() {
  const { register, handleSubmit, formState: { errors } } = useForm();

  const onSubmit = async (data) => {
    try {
      await registerUser(data);
      // Redirect to login or dashboard
    } catch (error) {
      // Handle error
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* Form fields */}
    </form>
  );
}
```

### Login Form Component
```jsx
// src/components/auth/LoginForm.jsx
import { useForm } from 'react-hook-form';
import { loginUser } from '@/lib/api-client';
import { useAuth } from '@/lib/auth-context';

export default function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const { login } = useAuth;

  const onSubmit = async (data) => {
    try {
      const response = await loginUser(data);
      login(response.token);
      // Redirect to dashboard
    } catch (error) {
      // Handle error
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* Form fields */}
    </form>
  );
}
```

## Error Handling

Common error responses:
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Invalid credentials
- `403 Forbidden`: Account inactive or rate limited
- `404 Not Found`: Resource not found
- `409 Conflict`: Email already exists
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Unexpected server error

## Security Best Practices

1. Never log sensitive information like passwords
2. Use HTTPS in production
3. Implement CSRF protection
4. Sanitize all user inputs
5. Regularly rotate JWT secrets
6. Monitor for suspicious activities