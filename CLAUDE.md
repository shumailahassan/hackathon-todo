# Claude Code Rules - Phase II Todo Full-Stack Web Application

This file serves as the comprehensive guide for the Phase II Todo Full-Stack Web Application project using Spec-Driven Development (SDD) with the Agentic Dev Stack. Your primary goal is to build a robust, scalable todo application using modern web technologies.

## Project Overview

**Application:** Todo Full-Stack Web Application
**Tech Stack:**
- Frontend: Next.js 16+ (App Router)
- Backend: Python FastAPI
- Database: Neon Serverless PostgreSQL
- ORM: SQLModel
- Authentication: Better Auth with JWT

## Authentication Flow

The application implements a secure authentication system using Better Auth with JWT tokens:
1. **Signup**: User registers with email/password, password is hashed and stored securely
2. **Signin**: User authenticates, receives JWT token for session management
3. **Protected Routes**: JWT verification middleware protects sensitive endpoints
4. **Token Management**: Secure storage and refresh strategy for frontend applications

## Task Context

**Your Surface:** You operate on a project level, providing guidance to users and executing development tasks via a defined set of specialized agents and skills.

**Your Success is Measured By:**
- All outputs strictly follow the user intent.
- Proper routing of tasks to designated agents.
- Effective utilization of specialized skills for specific functions.
- Adherence to the Spec-Driven Development workflow.
- Creation of accurate Prompt History Records (PHRs) for every user prompt.
- Intelligent identification and suggestion of Architectural Decision Records (ADRs).

## Core Development Workflow

The development process follows the Spec-Driven Development methodology with agentic workflow:

1. **Write Specification** → Define requirements using `/sp.specify`
2. **Generate Plan** → Create architectural plan using `/sp.plan`
3. **Break into Tasks** → Generate actionable tasks using `/sp.tasks`
4. **Implement** → Execute via Claude Code agents using `/sp.implement`

### Agent-Skills Assignment Matrix

| Agent | Primary Skills | Secondary Skills |
|-------|----------------|------------------|
| Auth Agent | Auth Skill | Validation Skill, Security Skill, Backend Skill |
| Frontend Agent | Frontend Skill | Validation Skill, Security Skill, API Skill |
| DB Agent | DB Skill | Validation Skill, Security Skill |
| Backend Agent | Backend Skill, API Skill | Validation Skill, Security Skill, Auth Skill, DB Skill |

### Development Phases

#### Phase 1: Foundation
- Set up project structure and dependencies
- Configure database connections and initial schema
- Implement basic authentication system
- Establish API endpoints for core functionality

#### Phase 2: Core Features
- Develop todo management functionality
- Implement user-specific data isolation
- Add advanced authentication features
- Optimize database queries and API performance

#### Phase 3: Enhancement
- Add advanced features (filtering, sorting, categorization)
- Implement comprehensive error handling
- Add monitoring and observability
- Performance optimization and security hardening

## Agents & Responsibilities

### 1. Auth Agent
- **Primary Role:** Handles secure user authentication flows
- **Scope:** Authentication endpoints, JWT management, user session handling, password hashing, token validation
- **Code Ownership:** `backend/src/auth`, `frontend/src/auth`
- **Key Responsibilities:** Secure signup/signin flows, JWT token generation/verification, session management, password security

### 2. Frontend Agent
- **Primary Role:** Manages Next.js application, layouts, forms, API calls, protected routes, token storage
- **Scope:** UI components, user interactions, client-side routing, API integration, responsive design
- **Code Ownership:** `frontend/src/app`, `frontend/src/components`, `frontend/src/lib`
- **Key Responsibilities:** Component development, form handling, API consumption, protected route implementation, token management

### 3. DB Agent
- **Primary Role:** Manages database design, schema, and CRUD operations
- **Scope:** Database models, migrations, connection management, query optimization, relationship mapping
- **Code Ownership:** `backend/src/models`, `backend/src/database`, `backend/src/migrations`
- **Key Responsibilities:** Schema design, relationship modeling, query optimization, migration management, data integrity

### 4. Backend Agent
- **Primary Role:** Implements FastAPI endpoints, integrates DB + Auth + API Skills
- **Scope:** API routes, business logic, data validation, authentication middleware, error handling
- **Code Ownership:** `backend/src/api`, `backend/src/core`, `backend/src/schemas`
- **Key Responsibilities:** API endpoint development, business logic implementation, request/response validation, error handling

## Skills & Capabilities

### Auth Skill
- **Purpose:** Secure authentication implementation
- **Capabilities:** Signup, Signin, password hashing, JWT token generation/verification, Better Auth integration, session management
- **Usage:** All authentication-related functionality

### Validation Skill
- **Purpose:** Input validation and sanitization
- **Capabilities:** Validates all user input and form data, email validation, password strength, security checks, request/response validation
- **Usage:** All data entry points and API endpoints

### Frontend Skill
- **Purpose:** Next.js application development
- **Capabilities:** Next.js patterns, layouts, forms, API integration, protected routes, token management, responsive design, component development
- **Usage:** All frontend components and user interface elements

### Security Skill
- **Purpose:** Security best practices and implementation
- **Capabilities:** CORS configuration, HTTPS assumptions, JWT expiry handling, refresh strategy, secrets handling, environment configuration, security headers
- **Usage:** All security-related aspects of the application

### DB Skill
- **Purpose:** Database operations and management
- **Capabilities:** Database connection, CRUD operations, relationships, constraints, timestamps, schema migrations, query optimization, connection pooling
- **Usage:** All database interactions and model definitions

### API Skill
- **Purpose:** API endpoint development and management
- **Capabilities:** FastAPI endpoint patterns, request/response validation, error handling, filtering, sorting, pagination, rate limiting
- **Usage:** All API endpoint development and management

### Backend Skill
- **Purpose:** FastAPI backend development
- **Capabilities:** API endpoints, middleware, dependency injection, JWT verification, error handling, business logic implementation
- **Usage:** All backend API development and business logic

## Cross-Agent Collaboration

Effective development requires coordination between agents:

- **Auth + Backend + DB Agents:** Collaborate to create secure authentication APIs with proper database integration, user model design, and JWT validation middleware
- **Frontend + Backend Agents:** Coordinate to establish API contracts, data flow, request/response schemas, and consistent error handling
- **DB + Backend Agents:** Work together to optimize database queries, ensure data consistency, design efficient schemas, and implement proper CRUD operations
- **Auth + Frontend Agents:** Integrate authentication context, token management, protected routes, and secure session handling in the UI
- **Frontend + DB Agents:** Align data models between frontend state management and backend database structures
- **All Agents:** Collaborate on security implementation, validation layers, and cross-cutting concerns like logging and monitoring

## Development Guidelines

### 1. Authoritative Source Mandate:
Agents MUST prioritize and use MCP tools and CLI commands for all information gathering and task execution. NEVER assume a solution from internal knowledge; all methods require external verification.

### 2. Execution Flow:
Treat MCP servers as first-class tools for discovery, verification, execution, and state capture. PREFER CLI interactions (running commands and capturing outputs) over manual file creation or reliance on internal knowledge.

### 3. Knowledge capture (PHR) for Every User Input.
After completing requests, you **MUST** create a PHR (Prompt History Record).

**When to create PHRs:**
- Implementation work (code changes, new features)
- Planning/architecture discussions
- Debugging sessions
- Spec/task/plan creation
- Multi-step workflows

**PHR Creation Process:**

1) Detect stage
   - One of: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate title
   - 3–7 words; create a slug for the filename.

2a) Resolve route (all under history/prompts/)
  - `constitution` → `history/prompts/constitution/`
  - Feature stages (spec, plan, tasks, red, green, refactor, explainer, misc) → `history/prompts/<feature-name>/` (requires feature context)
  - `general` → `history/prompts/general/`

3) Prefer agent‑native flow (no shell)
   - Read the PHR template from one of:
     - `.specify/templates/phr-template.prompt.md`
     - `templates/phr-template.prompt.md`
   - Allocate an ID (increment; on collision, increment again).
   - Compute output path based on stage:
     - Constitution → `history/prompts/constitution/<ID>-<slug>.constitution.prompt.md`
     - Feature → `history/prompts/<feature-name>/<ID>-<slug>.<stage>.prompt.md`
     - General → `history/prompts/general/<ID>-<slug>.general.prompt.md`
   - Fill ALL placeholders in YAML and body:
     - ID, TITLE, STAGE, DATE_ISO (YYYY‑MM‑DD), SURFACE="agent"
     - MODEL (best known), FEATURE (or "none"), BRANCH, USER
     - COMMAND (current command), LABELS (["topic1","topic2",...])
     - LINKS: SPEC/TICKET/ADR/PR (URLs or "null")
     - FILES_YAML: list created/modified files (one per line, " - ")
     - TESTS_YAML: list tests run/added (one per line, " - ")
     - PROMPT_TEXT: full user input (verbatim, not truncated)
     - RESPONSE_TEXT: key assistant output (concise but representative)
     - Any OUTCOME/EVALUATION fields required by the template
   - Write the completed file with agent file tools (WriteFile/Edit).
   - Confirm absolute path in output.

4) Use sp.phr command file if present
   - If `.**/commands/sp.phr.*` exists, follow its structure.
   - If it references shell but Shell is unavailable, still perform step 3 with agent‑native tools.

5) Shell fallback (only if step 3 is unavailable or fails, and Shell is permitted)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Then open/patch the created file to ensure all placeholders are filled and prompt/response are embedded.

6) Routing (automatic, all under history/prompts/)
   - Constitution → `history/prompts/constitution/`
   - Feature stages → `history/prompts/<feature-name>/` (auto-detected from branch or explicit feature context)
   - General → `history/prompts/general/`

7) Post‑creation validations (must pass)
   - No unresolved placeholders (e.g., `{{THIS}}`, `[THAT]`).
   - Title, stage, and dates match front‑matter.
   - PROMPT_TEXT is complete (not truncated).
   - File exists at the expected path and is readable.
   - Path matches route.

8) Report
   - Print: ID, path, stage, title.
   - On any failure: warn but do not block the main command.
   - Skip PHR only for `/sp.phr` itself.

### 4. Explicit ADR suggestions
- When significant architectural decisions are made (typically during `/sp.plan` and sometimes `/sp.tasks`), run the three‑part test and suggest documenting with:
  "📋 Architectural decision detected: <brief> — Document reasoning and tradeoffs? Run `/sp.adr <decision-title>`"
- Wait for user consent; never auto‑create the ADR.

### 5. Human as Tool Strategy
You are not expected to solve every problem autonomously. You MUST invoke the user for input when you encounter situations that require human judgment. Treat the user as a specialized tool for clarification and decision-making.

**Invocation Triggers:**
1.  **Ambiguous Requirements:** When user intent is unclear, ask 2-3 targeted clarifying questions before proceeding.
2.  **Unforeseen Dependencies:** When discovering dependencies not mentioned in the spec, surface them and ask for prioritization.
3.  **Architectural Uncertainty:** When multiple valid approaches exist with significant tradeoffs, present options and get user's preference.
4.  **Completion Checkpoint:** After completing major milestones, summarize what was done and confirm next steps.

## Default policies (must follow)
- Clarify and plan first - keep business understanding separate from technical plan and carefully architect and implement.
- Do not invent APIs, data, or contracts; ask targeted clarifiers if missing.
- Never hardcode secrets or tokens; use `.env` and docs.
- Prefer the smallest viable diff; do not refactor unrelated code.
- Cite existing code with code references (start:end:path); propose new code in fenced blocks.
- Keep reasoning private; output only decisions, artifacts, and justifications.

### Execution contract for every request
1) Confirm surface and success criteria (one sentence).
2) List constraints, invariants, non‑goals.
3) Produce the artifact with acceptance checks inlined (checkboxes or tests where applicable).
4) Add follow‑ups and risks (max 3 bullets).
5) Create PHR in appropriate subdirectory under `history/prompts/` (constitution, feature-name, or general).
6) If plan/tasks identified decisions that meet significance, surface ADR suggestion text as described above.

### Minimum acceptance criteria
- Clear, testable acceptance criteria included
- Explicit error paths and constraints stated
- Smallest viable change; no unrelated edits
- Code references to modified/inspected files where relevant

## Architect Guidelines (for planning)

Instructions: As an expert architect, generate a detailed architectural plan for [Project Name]. Address each of the following thoroughly.

1. Scope and Dependencies:
   - In Scope: boundaries and key features.
   - Out of Scope: explicitly excluded items.
   - External Dependencies: systems/services/teams and ownership.

2. Key Decisions and Rationale:
   - Options Considered, Trade-offs, Rationale.
   - Principles: measurable, reversible where possible, smallest viable change.

3. Interfaces and API Contracts:
   - Public APIs: Inputs, Outputs, Errors.
   - Versioning Strategy.
   - Idempotency, Timeouts, Retries.
   - Error Taxonomy with status codes.

4. Non-Functional Requirements (NFRs) and Budgets:
   - Performance: p95 latency, throughput, resource caps.
   - Reliability: SLOs, error budgets, degradation strategy.
   - Security: AuthN/AuthZ, data handling, secrets, auditing.
   - Cost: unit economics.

5. Data Management and Migration:
   - Source of Truth, Schema Evolution, Migration and Rollback, Data Retention.

6. Operational Readiness:
   - Observability: logs, metrics, traces.
   - Alerting: thresholds and on-call owners.
   - Runbooks for common tasks.
   - Deployment and Rollback strategies.
   - Feature Flags and compatibility.

7. Risk Analysis and Mitigation:
   - Top 3 Risks, blast radius, kill switches/guardrails.

8. Evaluation and Validation:
   - Definition of Done (tests, scans).
   - Output Validation for format/requirements/safety.

9. Architectural Decision Record (ADR):
   - For each significant decision, create an ADR and link it.

### Architecture Decision Records (ADR) - Intelligent Suggestion

After design/architecture work, test for ADR significance:

- Impact: long-term consequences? (e.g., framework, data model, API, security, platform)
- Alternatives: multiple viable options considered?
- Scope: cross‑cutting and influences system design?

If ALL true, suggest:
📋 Architectural decision detected: [brief-description]
   Document reasoning and tradeoffs? Run `/sp.adr [decision-title]`

Wait for consent; never auto-create ADRs. Group related decisions (stacks, authentication, deployment) into one ADR when appropriate.

## Project Structure & File Organization

### Root Directory Structure
```
todo-app/
├── .specify/                 # Spec-Driven Development artifacts
│   ├── memory/              # Project constitution and principles
│   ├── templates/           # Template files for various artifacts
│   └── agents/              # Agent definitions and configurations
├── specs/                   # Feature specifications and plans
│   └── <feature>/          # Individual feature artifacts
│       ├── spec.md         # Feature requirements
│       ├── plan.md         # Architecture decisions
│       └── tasks.md        # Testable tasks with cases
├── history/                 # Historical records
│   ├── prompts/            # Prompt History Records (PHRs)
│   └── adr/                # Architecture Decision Records
├── frontend/                # Next.js frontend application
│   ├── src/
│   │   ├── app/            # App Router pages and layouts
│   │   ├── components/     # Reusable UI components
│   │   ├── lib/            # Utilities and API clients
│   │   └── auth/           # Authentication-related components
│   ├── public/             # Static assets
│   ├── package.json        # Frontend dependencies
│   └── next.config.js      # Next.js configuration
├── backend/                 # FastAPI backend application
│   ├── src/
│   │   ├── auth/           # Authentication modules
│   │   ├── models/         # Database models and schemas
│   │   ├── api/            # API endpoints
│   │   ├── database/       # Database connection and utilities
│   │   ├── migrations/     # Alembic migration files
│   │   ├── core/           # Core utilities and security
│   │   └── schemas/        # Pydantic schemas
│   ├── requirements.txt    # Backend dependencies
│   └── alembic.ini         # Alembic configuration
├── docs/                    # Documentation and guides
├── .claude/                 # Claude Code agent and skill definitions
├── docker-compose.yml      # Container orchestration
└── CLAUDE.md               # This file - project guidelines
```

### File Organization Principles
- **Feature-first**: Organize code around business features rather than technical layers
- **Co-location**: Related functionality should be located in the same directory
- **Consistency**: Follow consistent naming and structural patterns
- **Separation of Concerns**: Separate business logic, presentation, and data layers appropriately

## Code Standards
See `.specify/memory/constitution.md` for code quality, testing, performance, security, and architecture principles.

## Development Commands

### Environment Setup
```bash
# Install frontend dependencies
cd frontend
npm install

# Install backend dependencies
cd ../backend
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env  # Then update with actual values
```

### Frontend Development
```bash
# Start frontend development server
cd frontend
npm run dev

# Build for production
npm run build

# Run tests
npm run test
```

### Backend Development
```bash
# Start backend development server
cd backend
python -m uvicorn main:app --reload

# Run backend tests
python -m pytest

# Format code
black .
```

### Database Management
```bash
# Initialize database
cd backend
alembic upgrade head

# Create migration
alembic revision --autogenerate -m "migration message"

# Run migrations
alembic upgrade head
```

### Combined Development (Docker)
```bash
# Start all services
docker-compose up --build

# Stop services
docker-compose down

# View logs
docker-compose logs -f
```

### Authentication Setup
```bash
# Configure Better Auth
# Set up JWT tokens and session management
# Implement protected routes
# Configure environment variables for auth
```

### Testing Commands
```bash
# Run all tests (frontend + backend)
npm run test:all

# Run specific tests
npm run test:unit
npm run test:integration

# Generate coverage reports
npm run test:coverage
```

### Deployment Commands
```bash
# Build and deploy frontend
npm run build && npm run start

# Deploy backend to production
python deploy.py --env production

# Deploy with Docker
docker-compose -f docker-compose.prod.yml up -d
```

## Project Agents and Skills Mapping

### Agents
- **Auth Agent** → Handles user authentication flows (signup, signin, JWT, password hashing, session management).
- **Frontend Agent** → Handles Next.js frontend components, UI, user interactions, API integration, and protected routes.
- **Backend Agent** → Handles FastAPI backend logic, API endpoints, authentication validation, business logic, and middleware.
- **DB Agent** → Handles Neon PostgreSQL database design, queries, migrations, relationships, and data operations.

### Skills
- **Auth Skill** → Signup, Signin, password hashing, JWT tokens, Better Auth integration, session management.
- **Validation Skill** → Input validation for email, password, and forms; security checks; request/response validation.
- **Frontend Skill** → Next.js patterns, layouts, forms, API integration, protected routes, token management, responsive design.
- **Security Skill** → CORS, HTTPS assumptions, JWT expiry, refresh strategy, secrets handling, env config, security headers.
- **DB Skill** → Database connection, CRUD operations, relationships, constraints, timestamps, schema migrations, query optimization.
- **API Skill** → FastAPI endpoint patterns, request/response validation, error handling, filtering, sorting, pagination, rate limiting.
- **Backend Skill** → API endpoints, middleware, dependency injection, JWT verification, error handling, business logic implementation.

### Instruction to Claude:
1. Always route tasks to the designated agent based on code ownership and responsibility.
2. Agents must only use their assigned skills for tasks (refer to Agent-Skills Assignment Matrix).
3. Follow the project folder structure for all artifacts:
   - `frontend/src/app` → Next.js pages and layout
   - `frontend/src/components` → React components (TodoList, TodoItem, etc.)
   - `frontend/src/lib` → API client and utilities
   - `frontend/src/auth` → Authentication-related components and context
   - `backend/src/auth` → FastAPI auth dependencies, middleware, schemas
   - `backend/src/models` → Database models
   - `backend/src/api` → API endpoints
   - `backend/src/database` → Database connection and utilities
   - `backend/src/migrations` → Alembic migration files
   - `backend/src/core` → Security utilities
   - `backend/src/schemas` → Pydantic schemas
   - `specs/<feature>` → spec.md, plan.md, tasks.md
   - `docs/` → Integration guides, API references
4. Create Prompt History Records (PHRs) for every user input and task as per standard flow.

## Notes & Best Practices

### Security Considerations
- Always validate and sanitize user inputs on both frontend and backend
- Implement proper authentication and authorization for all endpoints
- Use HTTPS in production environments
- Store sensitive data securely and never expose secrets in code
- Implement rate limiting to prevent abuse
- Regularly update dependencies to address security vulnerabilities

### Performance Optimization
- Implement efficient database queries with proper indexing
- Use caching strategies for frequently accessed data
- Optimize API responses to minimize payload sizes
- Implement lazy loading for UI components when appropriate
- Monitor application performance and identify bottlenecks

### Error Handling & Logging
- Implement comprehensive error handling with appropriate status codes
- Log errors with sufficient context for debugging
- Use structured logging for better analysis
- Handle edge cases and unexpected inputs gracefully
- Provide meaningful error messages to users without exposing system details

### Testing Strategy
- Write unit tests for individual functions and components
- Implement integration tests for API endpoints and database operations
- Use end-to-end tests for critical user flows
- Maintain high test coverage for critical functionality
- Automate testing in CI/CD pipeline

### Code Quality & Maintenance
- Follow consistent coding standards across the team
- Write clear, descriptive comments and documentation
- Refactor code regularly to maintain readability
- Conduct code reviews to ensure quality
- Use linting and formatting tools consistently

### Deployment & Operations
- Implement blue-green deployments to minimize downtime
- Set up monitoring and alerting for critical metrics
- Maintain environment parity between development, staging, and production
- Implement proper backup and recovery procedures
- Document operational procedures and runbooks
