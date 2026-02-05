# DB Skill 🗄️

## Description
Ye skill database operations aur schema management ke liye reusable methods provide karta hai, specifically Neon Serverless PostgreSQL ke liye.

## Objective
Ensure reliable aur efficient database interactions with FastAPI backend aur frontend integration.

## Capabilities

1. **Database Connection**
   - Establish connection using SQLModel
   - Uses environment variable `DATABASE_URL` for connection string
   - Connection pooling aur retry mechanisms support

2. **CRUD Operations**
   - Generic methods for Create, Read, Update, Delete
   - Task aur User related operations
   - Supports filtering, sorting aur pagination

3. **Relationships & Constraints**
   - Enforce foreign key relationships (e.g., tasks.user_id -> users.id)
   - Handle unique constraints, indexes

4. **Timestamps & Auditing**
   - Auto-manage `created_at` and `updated_at` fields
   - Optional auditing/logging for critical operations

5. **Validation Integration**
   - Uses Validation Skill to validate input before DB operations

## Usage
- Used by DB Agent
- Backend endpoints interact with DB via DB Skill
- Ensures secure aur consistent database transactions

## Notes
- Modular aur reusable
- Integrates seamlessly with Auth Skill, API Skill, and Backend Agent
