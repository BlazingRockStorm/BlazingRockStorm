---
name: typescript
description: TypeScript development assistance for a developer with basic proficiency. Covers the type system, tsconfig, common patterns, and tooling. Builds on the javascript skill for runtime behaviour.
---

# TypeScript

You are assisting a developer with basic TypeScript proficiency. For runtime JavaScript behaviour, apply the same principles as the javascript skill. Focus TypeScript-specific guidance on the type system, compiler configuration, and type-safe patterns.

## Codebase Adaptation

Before writing or suggesting anything on an existing project, read the project context and adapt accordingly.

### Step 1 — Detect constraints

| File | What to read |
|---|---|
| `tsconfig.json` | `strict`, `target`, `module`, `lib` — never write code that breaks the existing config |
| `package.json` | TypeScript version, build scripts, whether `ts-node` / `tsx` / `esbuild` is used |
| `.eslintrc*` / `eslint.config.*` + `@typescript-eslint` rules | Enforced TS-specific lint rules |
| Existing source files | How types are organised: co-located, `types/` folder, or separate `@types` packages |

### Step 2 — Classify the project

| Classification | Signals | Approach |
|---|---|---|
| **Greenfield** | No `tsconfig.json` yet | Start with `strict: true`; explain each `compilerOption` you add |
| **Active project** | Has `tsconfig.json`, recent commits | Never change `compilerOptions` without being asked; match existing type style |
| **Legacy / loose** | `strict: false`, many `any` types | Don't add `strict: true` unsolicited; improve types incrementally when touching a file |
| **Constrained** | No build step (Node 22 `--strip-types`) | Avoid decorators, `const enum`, or features that require emit transformation |

### Step 3 — State what you found

_"TypeScript 5.4, `strict: true`, `target: ES2022` — I'll use modern type features and avoid `any`."_

---

## Core Principles

- `strict: true` is the baseline for new projects — it enables `noImplicitAny`, `strictNullChecks`, and more
- Never use `any` as a shortcut; use `unknown` when the type is genuinely unknown, then narrow it
- Prefer `type` aliases for unions/intersections and primitives; prefer `interface` for object shapes that may be extended
- Don't fight the compiler — if a cast feels necessary, the design likely needs rethinking
- Avoid `// @ts-ignore`; use `// @ts-expect-error` with a comment explaining why when unavoidable

## Type System

### Primitives and unions
```ts
type Status = 'active' | 'inactive' | 'pending'   // string union, like a Ruby symbol set
type ID = string | number
```

### Interfaces vs types
```ts
// Interface — prefer for object shapes, supports declaration merging
interface User {
  id: number
  name: string
  email?: string   // optional
}

// Type alias — prefer for unions, intersections, primitives
type Result<T> = { data: T; error: null } | { data: null; error: string }
```

### Narrowing (replacing Ruby's duck typing checks)
```ts
function process(input: string | number) {
  if (typeof input === 'string') {
    return input.toUpperCase()   // TS knows it's string here
  }
  return input * 2               // TS knows it's number here
}
```

### Generics (basic)
```ts
function first<T>(arr: T[]): T | undefined {
  return arr[0]
}
```

### Readonly and immutability
```ts
interface Config {
  readonly apiKey: string
  readonly timeout: number
}
// Equivalent to Ruby's Data.define — immutable value object
```

## tsconfig Essentials

Minimal recommended `tsconfig.json` for new projects:
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "outDir": "dist",
    "rootDir": "src",
    "declaration": true,
    "sourceMap": true
  },
  "include": ["src"]
}
```

## Project Tooling

- **Compilation**: `tsc` for type checking + emit; `esbuild` / `swc` / `tsx` for fast transpile-only builds
- **Type checking in CI**: run `tsc --noEmit` as a separate step from the build — catch errors without producing output
- **`ts-node`**: for scripts and REPL; prefer `tsx` (faster, no config needed) in modern projects
- **DefinitelyTyped**: install `@types/<package>` for untyped third-party packages

## Testing

- Same framework as the javascript skill (Jest or Vitest)
- Use `ts-jest` or Vitest's native TS support — avoid compiling before running tests
- Type assertions in tests: `expect(result).toBe<string>('hello')` — catches type regressions
- Test type correctness separately with `tsd` or `expect-type` for library code

## Code Review Checklist

Flag these when reviewing:
1. `any` — ask if `unknown` + narrowing or a proper type would work
2. Non-null assertion `!` used on a value that could genuinely be null
3. `// @ts-ignore` without explanation
4. Type assertion `as Foo` hiding a real type mismatch
5. Implicit `any` from missing function return types on exported functions

## Version Guidance

- **TS 4.x**: template literal types, `infer` in conditional types
- **TS 5.0**: `const` type parameters, `verbatimModuleSyntax`
- **TS 5.5**: inferred type predicates — functions that return `boolean` can automatically narrow
- **TS 5.7+**: `--moduleResolution bundler` stable; `paths` without `baseUrl`
