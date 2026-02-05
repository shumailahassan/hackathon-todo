# Authentication System

This document describes the authentication system implemented for the application.

## Overview

The authentication system provides secure user registration, login, logout, and password reset functionality. It implements industry-standard security practices including password hashing, JWT-based session management, and rate limiting.

## Features

### User Registration
- Email and password validation
- Password strength requirements
- Secure password hashing using bcrypt
- Duplicate email prevention

### User Login
- Secure email/password authentication
- JWT token generation for session management
- Refresh token support
- Last login tracking

### User Logout
- Session invalidation
- Token cleanup

### Password Reset
- Secure password reset via email
- Time-limited reset tokens
- Password strength validation

## Architecture

### Backend (FastAPI)

#### Models
- `User`: Stores user information (email, hashed password, profile data)
- `Session`: Tracks active sessions (though JWT is stateless, this could be extended for session management)
- `PasswordResetToken`: Temporary tokens for password reset functionality

#### Services
- `UserService`: Handles user-related operations
- `AuthService`: Handles authentication logic
- `EmailService`: Sends emails for password reset

#### Endpoints
- `POST /api/auth/register`: User registration
- `POST /api/auth/login`: User login
- `POST /api/auth/logout`: User logout
- `POST /api/auth/refresh`: Token refresh
- `POST /api/auth/forgot-password`: Initiate password reset
- `POST /api/auth/reset-password`: Complete password reset

### Frontend (Next.js/React)

#### Components
- `RegisterForm`: Registration form with validation
- `LoginForm`: Login form with validation
- `PasswordResetForm`: Password reset form
- `AuthProvider`: Authentication context provider

#### Pages
- `/signup`: Registration page
- `/login`: Login page
- `/reset-password`: Password reset page

## Security Measures

- Passwords are hashed using bcrypt with salt
- JWT tokens with configurable expiration times
- Password strength validation
- Rate limiting (implementation pending)
- Secure token storage in browser
- Protected routes and authentication middleware

## Configuration

The system can be configured via environment variables:

```env
# Database
DATABASE_URL="postgresql://username:password@localhost:5432/auth_db"

# JWT Configuration
JWT_SECRET_KEY="your-super-secret-jwt-key-here-make-it-long-and-random"
JWT_REFRESH_SECRET_KEY="your-super-secret-refresh-key-here-make-it-long-and-random"
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Password Requirements
MIN_PASSWORD_LENGTH=8
REQUIRE_UPPERCASE=true
REQUIRE_LOWERCASE=true
REQUIRE_NUMBERS=true
REQUIRE_SPECIAL_CHARS=true

# Email Configuration (for password reset)
EMAIL_HOST="smtp.gmail.com"
EMAIL_PORT=587
EMAIL_USER="your-email@gmail.com"
EMAIL_PASSWORD="your-app-password"
```

## API Usage

### Registration
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePassword123!",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePassword123!"
  }'
```

## Frontend Integration

The authentication context provides methods for:

- `login(email, password)`: Authenticate user
- `register(userData)`: Create new user
- `logout()`: End user session
- `forgotPassword(email)`: Request password reset
- `resetPassword(token, newPassword)`: Complete password reset