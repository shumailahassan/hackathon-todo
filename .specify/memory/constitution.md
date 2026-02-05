<!-- SYNC IMPACT REPORT
Version change: 1.0.0 -> 2.0.0
Modified principles: Updated all principles to reflect Phase-II requirements
Added sections: Agent responsibilities, Skill usage rules, Security rules, Collaboration rules
Removed sections: N/A
Templates requiring updates:
- .specify/templates/plan-template.md ⚠ pending
- .specify/templates/spec-template.md ⚠ pending
- .specify/templates/tasks-template.md ⚠ pending
- .specify/templates/commands/*.md ⚠ pending
Follow-up TODOs: None
-->
# Todo Full-Stack Web Application Constitution - Phase II

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)
All development begins with a clear, detailed specification; Specifications must define requirements, interfaces, and acceptance criteria before implementation; No code changes without corresponding spec updates; Claude Code and Spec-Kit Plus workflow strictly followed.
<!-- Rationale: Ensures clarity of requirements and prevents scope creep -->

### II. Agentic Development Workflow
Development follows a structured agent-based approach; Each agent has defined responsibilities and code ownership; Agents collaborate through well-defined interfaces and shared skills; No manual coding allowed - all implementation through agents.
<!-- Rationale: Enables scalable, organized development with clear ownership and accountability -->

### III. Agent-Specific Responsibilities
Auth Agent manages authentication flows and JWT management; Frontend Agent handles Next.js application and UI components; Backend Agent implements FastAPI endpoints and business logic; DB Agent manages database design and CRUD operations.
<!-- Rationale: Ensures specialized expertise and clear ownership of different application layers -->

### IV. Skill-Based Implementation (NON-NEGOTIABLE)
Auth Skill for authentication functionality; Validation Skill for input validation; Frontend Skill for UI components; Security Skill for security measures; DB Skill for database operations; API Skill for endpoint development; Skills must be used appropriately by assigned agents.
<!-- Rationale: Ensures proper tool usage and adherence to established patterns -->

### V. Security-First Architecture
Authentication and authorization implemented from the start; Better Auth with JWT used for multi-user support; All user inputs validated and sanitized; Secrets managed through environment variables, never hardcoded; Data isolation between users enforced.
<!-- Rationale: Prevents security vulnerabilities from being introduced during development -->

### VI. Full-Stack Consistency
Frontend and backend APIs designed in coordination; Consistent data models across client and server; Shared validation logic where applicable; Next.js 16+ with App Router on frontend; Python FastAPI with SQLModel ORM on backend.
<!-- Rationale: Ensures seamless integration between frontend and backend components -->

### VII. Persistent Storage Implementation
Neon Serverless PostgreSQL for database storage; SQLModel for ORM operations; Proper data relationships and constraints defined; Migration strategies planned for schema evolution.
<!-- Rationale: Ensures reliable and scalable data persistence for multi-user application -->

### VIII. Performance Optimization
Database queries optimized with proper indexing; API responses minimized for efficiency; Frontend components optimized for fast loading; Efficient authentication token management.
<!-- Rationale: Maintains responsive user experience and reduces resource consumption -->

## Technology Standards

### Frontend Requirements
Next.js 16+ with App Router; TypeScript for type safety; Responsive design following accessibility standards; Client-side caching for improved performance; Integration with Better Auth for authentication.
<!-- Rationale: Ensures modern, accessible, and performant frontend application -->

### Backend Requirements
Python FastAPI for API endpoints; Neon Serverless PostgreSQL for database; SQLModel for ORM; Better Auth with JWT for authentication; Proper middleware for security and validation.
<!-- Rationale: Provides scalable, efficient backend with modern development practices -->

### Deployment Standards
Containerized deployment with Docker; Environment-specific configurations; Automated testing in CI/CD pipeline; Monitoring and logging implemented; Neon PostgreSQL connection management.
<!-- Rationale: Ensures consistent, reliable, and observable deployments -->

### Agent and Skill Standards
All development must be performed through designated agents; No manual coding allowed; Agents must use appropriate skills for their tasks; Claude Code and Spec-Kit Plus workflow strictly followed.
<!-- Rationale: Ensures adherence to agentic development workflow -->

## Development Workflow

### Spec-Kit Plus Workflow (MANDATORY)
Spec → Plan → Tasks → Implement cycle strictly followed; All work must begin with a specification; Planning phase defines architecture and approach; Tasks break down implementation into manageable units; Implementation executed via Claude Code agents.
<!-- Rationale: Ensures structured, predictable development process -->

### Agent Collaboration Process
Auth Agent coordinates with Backend Agent for authentication endpoints; Frontend Agent collaborates with Backend Agent for API contracts; DB Agent works with Backend Agent for data models and queries; All agents use shared skills appropriately.
<!-- Rationale: Ensures coordinated development across all application layers -->

### Code Review Process
All changes require peer review before merging; PRs must include updated documentation; Automated tests must pass before approval; Clear commit messages following conventional format; Reviews verify constitutional compliance.
<!-- Rationale: Maintains code quality and knowledge sharing across the team -->

### Quality Gates
No merge without passing tests; Code coverage minimum of 80% for new features; Security scanning passes; Performance benchmarks met; Constitutional compliance verified.
<!-- Rationale: Ensures high-quality deliverables with minimal defects -->

### Branch Management
Feature branches for all work; Main branch protected with required reviews; Release branches for versioned deployments; Clear branching strategy documented; Branch names follow agent-specific conventions.
<!-- Rationale: Prevents unstable code from reaching production and enables parallel development -->

## Governance

All implementations must comply with these principles; No manual coding allowed - all work through agents; Amendments require team consensus and documented approval; Code reviews verify constitutional compliance; Deviations must be justified and approved; All development follows Claude Code and Spec-Kit Plus workflow.
<!-- Rationale: Ensures consistent application of principles across the entire project -->

**Version**: 2.0.0 | **Ratified**: 2026-02-05 | **Last Amended**: 2026-02-05