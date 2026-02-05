# API Skill 🌐

## Description
Ye skill FastAPI endpoints aur RESTful API best practices ke liye reusable patterns aur methods define karta hai.

## Objective
Build secure, maintainable aur scalable APIs jo frontend aur agents ke saath easily communicate kar sake.

## Capabilities

1. **Endpoint Structure**
   - Consistent route naming and versioning (e.g., /api/v1/tasks)
   - CRUD endpoints for tasks and users

2. **Authentication**
   - Integrates with Auth Skill for JWT validation
   - Secures endpoints using dependency injection or middleware

3. **Request & Response Handling**
   - Pydantic models for request validation and response formatting
   - Error handling with HTTPException
   - Consistent status codes (200, 201, 400, 401, 404)

4. **Filtering, Sorting & Pagination**
   - Support query parameters for tasks filtering and sorting
   - Optional pagination for large datasets

5. **Middleware & Logging**
   - Request/response logging
   - Performance monitoring hooks

6. **Integration with DB Skill**
   - Uses DB Skill for database interactions
   - Ensures input validated by Validation Skill before DB operations

## Usage
- Used by Backend Agent
- Provides standard API patterns for all other agents and frontend integration

## Notes
- Modular aur reusable
- Always integrates with Auth Skill, DB Skill, and Security Skill
