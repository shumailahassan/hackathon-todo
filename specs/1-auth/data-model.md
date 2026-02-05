# Data Model: User Authentication

## User Entity

**Description**: Represents a registered user in the system

**Fields**:
- `id` (UUID/string): Unique identifier for the user
- `email` (string): User's email address (must be unique, validated format)
- `password_hash` (string): BCrypt hash of the user's password (never store plain text)
- `first_name` (string, optional): User's first name
- `last_name` (string, optional): User's last name
- `is_active` (boolean): Whether the account is active/enabled
- `is_verified` (boolean): Whether the email has been verified
- `created_at` (timestamp): When the account was created
- `updated_at` (timestamp): When the account was last updated
- `last_login_at` (timestamp, optional): When the user last logged in

**Validation Rules**:
- Email must follow standard email format
- Email must be unique across all users
- Password must meet strength requirements (min length, complexity)
- Email must not be empty
- Account must be active to log in

**State Transitions**:
- `inactive` → `active` when account is created
- `active` → `inactive` when account is deactivated
- `unverified` → `verified` when email verification is completed

## Session Entity

**Description**: Represents an active user session/token

**Fields**:
- `id` (UUID/string): Unique identifier for the session
- `user_id` (UUID/string): Reference to the associated user
- `token` (string): JWT token or session identifier
- `expires_at` (timestamp): When the session expires
- `created_at` (timestamp): When the session was created
- `last_accessed_at` (timestamp): When the session was last used
- `device_info` (string, optional): Information about the device used
- `ip_address` (string, optional): IP address of the client

**Validation Rules**:
- Session must be linked to an active user
- Session must not be expired
- Session can be invalidated on logout

**State Transitions**:
- `active` → `expired` when session reaches expiration time
- `active` → `invalidated` when user logs out

## PasswordResetToken Entity

**Description**: Temporary token for password reset functionality

**Fields**:
- `id` (UUID/string): Unique identifier for the token
- `user_id` (UUID/string): Reference to the associated user
- `token` (string): Unique token for password reset
- `expires_at` (timestamp): When the token expires (typically 1 hour)
- `used_at` (timestamp, optional): When the token was used (null if unused)
- `created_at` (timestamp): When the token was created

**Validation Rules**:
- Token must be unique
- Token must not be expired
- Token must not have been used already
- Token must be linked to an active user

**State Transitions**:
- `valid` → `used` when password reset is completed
- `valid` → `expired` when token reaches expiration time