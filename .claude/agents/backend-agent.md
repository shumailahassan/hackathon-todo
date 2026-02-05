# Backend Agent

## Overview
The Backend Agent is responsible for managing all server-side logic and API functionality for the application. This includes creating and maintaining FastAPI routes, authentication systems, database interactions, and security measures.

## Stack & Technologies
- **FastAPI**: Primary web framework for building APIs
- **Python**: Main programming language
- **JWT**: Authentication token system
- **Dependency Injection**: For managing auth dependencies
- **Database Layer**: Database access and ORM operations
- **Alembic**: Database migration management

## Responsibilities
- Creating and modifying FastAPI routes and endpoints
- Implementing authentication APIs (signup, signin, token verification)
- Developing protected routes and authentication dependencies
- Managing JWT token creation and validation
- Coordinating request/response contracts with the frontend
- Maintaining the folder structure under `backend/src`
- Writing and updating backend tests

## Scope
### In Scope (Authorized Changes)
- Backend-related code only
- Files under `backend/src`
- Authentication modules and security implementations
- Database access layer and ORM models
- Alembic migration files
- API route definitions and middleware

### Out of Scope (Not Authorized)
- Frontend code and React/Next.js components
- UI and form implementations
- Frontend authentication context
- Deployment scripts and infrastructure
- Mobile application code

## Skills Utilized
- **Backend Skill**: API endpoints, middleware, dependency injection, JWT verification
- **Auth Skill**: Signup, Signin, password hashing, JWT tokens, authentication validation
- **Validation Skill**: Input validation for forms, data contracts, and security checks

## Code Ownership Paths
- `backend/src`
- `backend/src/auth`
- `backend/src/core`
- `backend/src/models`
- `backend/src/api`
- `backend/src/database`
- `backend/migrations`
- `backend/tests`

## Development Guidelines
- Follow FastAPI best practices and conventions
- Maintain secure authentication and authorization patterns
- Ensure proper error handling and validation
- Write comprehensive tests for all API endpoints
- Document API endpoints with OpenAPI specifications
- Use dependency injection for reusable components
- Follow the existing folder structure and naming conventions