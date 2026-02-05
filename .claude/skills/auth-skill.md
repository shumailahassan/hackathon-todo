# Auth Skill 🔑

## Description
Ye skill multi-user web application ke liye complete authentication layer provide karta hai: signup, signin, JWT token management, password hashing, aur Better Auth integration.

## Objective
Reusable authentication layer create karna jo frontend (Next.js) aur backend (FastAPI) dono ke liye secure access control, user session management, aur token-based authentication ensure kare.

## Capabilities

1. **User Signup**
   - Accepts user email and password
   - Validates email format aur password strength (Validation Skill use kare)
   - Password securely hash karta hai before storing in Neon PostgreSQL
   - Integrates with Better Auth for session management

2. **User Signin**
   - Accepts user credentials
   - Verifies password against hashed value
   - Generates JWT token with user identity payload
   - Issues token to frontend via Better Auth session

3. **JWT Token Management**
   - Generate secure JWT tokens on login
   - Verify token signature aur expiration
   - Decode token to extract user information
   - Use tokens to authorize API requests

4. **Password Security**
   - Hash passwords using industry-standard algorithm (bcrypt recommended)
   - Verify hashed passwords during signin
   - Ensure passwords never stored or logged in plain text

5. **Better Auth Integration**
   - Connects with Better Auth for session handling
   - Automatically refreshes tokens if needed
   - Provides frontend-friendly APIs to access session information

6. **Validation Integration**
   - Input validation ke liye Validation Skill use kare
   - Ensure secure aur consistent authentication workflow

## Usage
- **Used By:** Auth Agent
- Frontend: Next.js app, React authentication context, signup/signin forms
- Backend: FastAPI endpoints, JWT validation, middleware, dependencies
- Reusable for other agents requiring authentication

## Notes
- Must follow security best practices: input validation, hashing, token signing
- Modular aur easily extendable
- Seamless integration with database, frontend, aur Validation Skill
