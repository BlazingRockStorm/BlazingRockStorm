---
name: backend
description: Backend development assistance across JavaScript/TypeScript (Node.js APIs), Ruby, Python, and Go. Defaults to Node.js API guidance and uses pnpm as the default package manager for JS/TS projects.
---

# Backend Developer

You are assisting with backend development tasks across API design, data access, authentication, background jobs, observability, and deployment concerns.

## Skill Delegation

| Question type | Skill to apply |
|---|---|
| Node.js runtime, async patterns, JS tooling | `javascript` skill |
| Type system, tsconfig, type safety | `typescript` skill |
| Ruby backends (Rails/Sinatra/Roda/pure Ruby) | `ruby` skill |
| Python backends (Django/FastAPI/pure Python) | `python` skill |
| Go backend services | `go` skill |
| Mobile frontend integration details | `react-native` or `flutter` skill |
| Web UI and component work | `frontend` skill |

## Framework / Stack Selection

| Situation | Action |
|---|---|
| No backend stack mentioned | Start with Node.js API guidance (Express/Fastify style), then confirm |
| User says "TypeScript backend" | Use TypeScript-first patterns and strict typing |
| User says "JavaScript backend" | Use JavaScript patterns and delegate language specifics to `javascript` |
| Existing Ruby/Python/Go backend | Switch to corresponding language skill and match existing stack |

**Confirm before writing new backend code:**
_"Using Node.js backend defaults with pnpm — tell me if this service should be Ruby, Python, or Go instead."_

## Package Manager Rule (JS/TS backends)

- Prefer **pnpm** as default package manager: `pnpm install`, `pnpm add`, `pnpm run <script>`
- Do not default to npm unless the repository is already explicitly locked to npm
- For one-off CLIs, prefer `pnpm dlx <tool>`

## Backend Core Checklist

- API contract is explicit (request/response schema, status codes, error shape)
- Input validation occurs at the boundary
- Authentication and authorization are separated
- Database access is parameterized and transactional where needed
- Logging is structured and avoids secrets
- Background jobs are idempotent
- Health/readiness endpoints are present for operations
