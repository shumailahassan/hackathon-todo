# Data Model: Web Application Conversion

## Entities

### User
**Description**: Represents a registered user account with authentication credentials and profile information

**Fields**:
- id (UUID/Integer): Unique identifier for the user
- email (String): User's email address (unique, indexed)
- password_hash (String): Hashed password for authentication
- created_at (DateTime): Timestamp when account was created
- updated_at (DateTime): Timestamp when account was last updated
- is_active (Boolean): Whether the account is active

**Relationships**:
- One-to-Many: User → UserData (via user_id foreign key)
- One-to-Many: User → Sessions (via user_id foreign key)

**Validation Rules**:
- Email must be valid email format
- Email must be unique across all users
- Password must meet security requirements (length, complexity)
- Email and password are required for registration

### UserData
**Description**: Represents personal data records owned by a specific user

**Fields**:
- id (UUID/Integer): Unique identifier for the data record
- user_id (UUID/Integer): Foreign key linking to User
- title (String): Title or name of the data record
- content (Text): Content of the data record
- created_at (DateTime): Timestamp when record was created
- updated_at (DateTime): Timestamp when record was last updated
- is_public (Boolean): Whether the data is publicly accessible (default: false)

**Relationships**:
- Many-to-One: UserData → User (via user_id foreign key)

**Validation Rules**:
- user_id must reference an existing User
- title is required
- content length must be within limits
- Only the owning user can modify the record

### Session
**Description**: Represents an authenticated user session with security tokens

**Fields**:
- id (UUID): Unique identifier for the session
- user_id (UUID/Integer): Foreign key linking to User
- token (String): Session token (JWT or random string)
- expires_at (DateTime): Expiration timestamp for the session
- created_at (DateTime): Timestamp when session was created
- ip_address (String): IP address of the client (for security tracking)
- user_agent (String): Browser/device information (for security tracking)

**Relationships**:
- Many-to-One: Session → User (via user_id foreign key)

**Validation Rules**:
- user_id must reference an existing User
- token must be unique
- expires_at must be in the future
- Session must be validated for each authenticated request

### AuthToken
**Description**: Represents authentication and authorization tokens used for securing API communications

**Fields**:
- id (UUID): Unique identifier for the token
- user_id (UUID/Integer): Foreign key linking to User
- token_type (String): Type of token (e.g., "access", "refresh")
- token_value (String): Encrypted/encoded token value
- expires_at (DateTime): Expiration timestamp for the token
- created_at (DateTime): Timestamp when token was created
- revoked (Boolean): Whether the token has been revoked

**Relationships**:
- Many-to-One: AuthToken → User (via user_id foreign key)

**Validation Rules**:
- user_id must reference an existing User
- token_value must be unique
- expires_at must be in the future
- Revoked tokens cannot be used for authentication

## State Transitions

### User Account States
- **Pending**: After registration but before email verification
- **Active**: After email verification, normal operating state
- **Suspended**: Temporarily disabled (admin action)
- **Deactivated**: Permanently closed (user request)

### Session States
- **Active**: Valid and usable for authentication
- **Expired**: Token has passed expiration time
- **Revoked**: Explicitly invalidated by user or system

## Relationships

### User ↔ UserData
- One-to-Many relationship
- UserData.user_id references User.id
- Cascade delete: When User is deleted, all their UserData is also deleted
- All UserData access must be filtered by user_id for security

### User ↔ Session
- One-to-Many relationship
- Session.user_id references User.id
- Sessions are invalidated when User account is deactivated

### User ↔ AuthToken
- One-to-Many relationship
- AuthToken.user_id references User.id
- AuthTokens are revoked when User account is deactivated

## Indexes

### Required Indexes
- User.email: Unique index for fast lookup and uniqueness enforcement
- UserData.user_id: Index for efficient filtering by user
- Session.token: Index for fast session lookup
- AuthToken.token_value: Index for fast token validation
- Session.expires_at: Index for efficient cleanup of expired sessions
- AuthToken.expires_at: Index for efficient cleanup of expired tokens

## Constraints

### Data Integrity
- User.email: UNIQUE constraint to prevent duplicate accounts
- UserData.user_id: FOREIGN KEY constraint to ensure referential integrity
- Session.user_id: FOREIGN KEY constraint to ensure referential integrity
- AuthToken.user_id: FOREIGN KEY constraint to ensure referential integrity

### Business Logic
- UserData.is_public: Only the owning user can set this to true
- Session.expires_at: Cannot be in the past when creating a new session
- AuthToken.revoked: Once revoked, cannot be un-revoked