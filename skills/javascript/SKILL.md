---
name: javascript
description: JavaScript development assistance for a developer with basic proficiency. Covers modern ES6+, Node.js, async patterns, tooling, and testing.
---

# JavaScript

You are assisting a developer with basic JavaScript proficiency. Explain non-obvious concepts clearly and concisely.

## Codebase Adaptation

Before writing or suggesting anything on an existing project, read the project context and adapt accordingly.

### Step 1 — Detect constraints

| File | What to read |
|---|---|
| `package.json` | Node version (`engines`), available scripts, existing dependencies |
| `.nvmrc` / `.node-version` / `.tool-versions` | Target Node version |
| `.eslintrc*` / `eslint.config.*` | Enforced lint rules — follow them even if they differ from defaults |
| `.prettierrc*` | Formatting rules — never reformat code in a way that conflicts |
| `tsconfig.json` | Whether TypeScript is in play (switch to typescript skill if so) |
| Existing source files | Module style (`require` vs `import`), quote style, semicolons, framework in use |

### Step 2 — Classify the project

| Classification | Signals | Approach |
|---|---|---|
| **Greenfield** | Empty `package.json`, no source files | Apply defaults from this skill |
| **Active project** | Has source, recent commits, modern Node | Match existing style; suggest improvements only when asked |
| **Legacy project** | CommonJS (`require`), no `async/await`, Node < 12 | Stay within existing patterns; avoid ESM syntax |
| **Constrained** | No npm access, vendored `node_modules`, locked lockfile | Never suggest adding packages; work with what exists |

### Step 3 — State what you found

_"Node 18, ESM modules, ESLint with Airbnb config — I'll use `import/export` and match the existing style."_

---

## Core Principles

- Prefer `const` over `let`; never use `var`
- Use `===` / `!==` always — never `==` / `!=`
- Avoid implicit type coercion; be explicit (`String(x)`, `Number(x)`)
- Prefer `async/await` over raw `.then()` chains for readability
- Never swallow errors: always `catch` and handle or rethrow

## Language Features (ES6+)

- **Destructuring**: `const { name, age } = user` / `const [first, ...rest] = arr`
- **Spread / rest**: `{ ...defaults, ...overrides }` for merging; `...args` in function params
- **Optional chaining**: `user?.address?.city` — equivalent to Ruby's `&.`
- **Nullish coalescing**: `value ?? 'default'` — only falls back on `null`/`undefined`, not `0` or `''`
- **Template literals**: `` `Hello, ${name}!` `` — equivalent to Ruby's `"Hello, #{name}!"`
- **Short-circuit assignment**: `config.timeout ??= 5000`

## Async Patterns

```js
// Prefer async/await
async function fetchUser(id) {
  const response = await fetch(`/users/${id}`)
  if (!response.ok) throw new Error(`HTTP ${response.status}`)
  return response.json()
}

// Always handle errors
try {
  const user = await fetchUser(1)
} catch (err) {
  console.error('Failed to fetch user:', err.message)
}

// Parallel async — like Ruby's parallel map
const [users, posts] = await Promise.all([fetchUsers(), fetchPosts()])
```

## Modules

- Default to **ESM** (`import`/`export`) for new projects; CommonJS (`require`) only for legacy Node or when the project already uses it
- One primary export per file; named exports for utilities
- Avoid `export default` for objects — named exports are easier to tree-shake and refactor

## Project Tooling

- **npm scripts**: define all common tasks in `package.json` `scripts`; never rely on global CLIs that aren't in `devDependencies`
- **ESLint**: run `eslint --fix` for auto-correct; configure in `eslint.config.mjs` (flat config, modern) or `.eslintrc.json`
- **Prettier**: formatting only — do not mix lint and format rules; integrate with `eslint-config-prettier`
- **Node version**: pin with `.nvmrc` or `engines` field in `package.json`

## Testing

- Default to **Jest** for Node projects; **Vitest** for Vite-based projects (faster, same API)
- Structure: `describe` for module/class, `it`/`test` for behaviour — mirrors RSpec
- Use `beforeEach`/`afterEach` for setup/teardown (equivalent to RSpec `before`/`after`)
- Mock external calls with `jest.mock()` or `vi.mock()`; restore with `jest.restoreAllMocks()`
- Prefer `expect(fn).toThrow()` over catching errors manually

## Code Review Checklist

Flag these when reviewing:
1. `var` — replace with `const`/`let`
2. `==` loose equality — replace with `===`
3. Unhandled promise rejections — every `async` call needs a `catch` path
4. `console.log` left in production paths
5. Mutating function arguments — return new values instead

## Version Guidance

- **Node 16**: `fetch` not built-in (use `node-fetch`); `--experimental-vm-modules` for ESM in Jest
- **Node 18**: `fetch` built-in (experimental), `test` runner built-in
- **Node 20 LTS**: `fetch` stable, `test` runner stable — prefer for new projects
- **Node 22**: `require(esm)` supported; `--experimental-strip-types` for TypeScript without compile step
