---
name: frontend
description: Frontend development assistance covering React (default, primary experience) and Vue (secondary). Handles JSX and TSX. Delegates JS language questions to the javascript skill and TS type questions to the typescript skill.
---

# Frontend Developer

You are assisting a developer with strong React experience (primary) and basic Vue experience (1–2 projects). They are comfortable with both JSX and TSX.

## Skill Delegation

This skill covers frontend-specific concerns only. For underlying language questions, defer to:

| Question type | Skill to apply |
|---|---|
| JavaScript runtime, async, ES6+, Node tooling | `javascript` skill |
| TypeScript types, tsconfig, type narrowing | `typescript` skill |
| This skill | Component design, state, routing, build tools, styling, frontend testing, deployment |

## Framework Selection

| Situation | Action |
|---|---|
| No framework mentioned, or existing React project | Load `references/react.md` **(default)** |
| User says "React" | Load `references/react.md` |
| User says "Vue", or project has `vue` in `package.json` | Load `references/vue.md` |
| Another framework (Svelte, Angular, etc.) | Apply core frontend principles; state you have no dedicated reference and ask for context |
| Deployment to Vercel, Netlify, or AWS Amplify | Load `references/deployment.md` alongside the framework reference |

**Confirm before writing framework code:**
_"Using React (default) — let me know if this is a Vue project instead."_

---

## Codebase Adaptation

### Step 1 — Detect constraints

| File | What to read |
|---|---|
| `package.json` | Framework version, existing dependencies (router, state lib, UI lib) |
| `tsconfig.json` / `jsconfig.json` | Whether the project uses TypeScript — use TSX/TS if so |
| `vite.config.*` / `webpack.config.*` / `next.config.*` | Build tool and framework meta-framework in use |
| `.eslintrc*` / `eslint.config.*` | Lint rules, including framework-specific plugins |
| `src/` file extensions | `.jsx` vs `.tsx` vs `.js` vs `.ts` — match what already exists |
| Existing components | Naming conventions, folder structure, styling approach |

### Step 2 — Classify the project

| Classification | Signals | Approach |
|---|---|---|
| **Greenfield** | No `src/`, empty `package.json` | Apply defaults; ask JSX or TSX preference upfront |
| **Active project** | Has components, recent commits | Match existing file extension, folder structure, and component style |
| **Legacy project** | Class components, `createReactClass`, Vue 2 Options API | Stay within existing patterns; don't introduce hooks or Composition API unprompted |
| **Constrained** | No new packages allowed, locked versions | Work with installed libraries only |

### Step 3 — State what you found

_"React 18, TypeScript, Vite, no state management library — I'll use TSX, built-in hooks, and avoid adding new dependencies."_

---

## Core Frontend Principles

- **Components do one thing** — if a component needs a long description, split it
- **Co-locate related files** — keep a component's styles, tests, and types next to it, not in separate top-level folders
- **Lift state only as far as needed** — start with local state; move up only when siblings need it
- **Avoid prop drilling beyond 2 levels** — use context or a state library at that point
- **No direct DOM manipulation** — use framework reactivity; `document.querySelector` is a last resort
- **Accessibility by default** — use semantic HTML elements; add `aria-*` only when semantic HTML isn't enough

## File and Folder Conventions

```
src/
  components/        # shared, reusable UI components
    Button/
      Button.tsx
      Button.test.tsx
      index.ts       # re-export: export { Button } from './Button'
  features/          # feature-scoped components and logic (preferred over pages/ + components/ split)
    auth/
    dashboard/
  hooks/             # custom hooks shared across features
  lib/               # framework-agnostic utilities
  types/             # shared TypeScript types and interfaces
```

## JSX / TSX

- Use TSX when the project is TypeScript; JSX for JavaScript projects — never mix in the same project
- Prop types: use TypeScript interfaces in TSX (`interface ButtonProps`); avoid `PropTypes` in new code
- Self-close tags with no children: `<Icon />` not `<Icon></Icon>`
- Keep JSX readable — extract complex expressions into named variables above the `return`
- One component per file; filename matches the component name exactly

```tsx
interface CardProps {
  title: string
  description?: string
  onClick: () => void
}

export function Card({ title, description, onClick }: CardProps) {
  const hasDescription = Boolean(description)

  return (
    <div className="card" onClick={onClick}>
      <h2>{title}</h2>
      {hasDescription && <p>{description}</p>}
    </div>
  )
}
```

## State Management

Choose based on scope:

| Scope | Tool |
|---|---|
| Local UI state | `useState` / `ref` |
| Complex local logic | `useReducer` / `computed` |
| Shared across a feature tree | React Context / Vue `provide`/`inject` |
| Global app state | Zustand (React) / Pinia (Vue) — prefer over Redux/Vuex for new projects |
| Server state (fetch, cache, sync) | TanStack Query — don't hand-roll fetch logic |

## Styling

Match whatever the project already uses. For greenfield:
- **CSS Modules** — scoped by default, no runtime, works with any build tool
- **Tailwind CSS** — utility-first, pairs well with component libraries
- **Styled-components / Emotion** — CSS-in-JS; only add if the team is already comfortable with the tradeoffs

Never mix styling approaches in the same project.

## Build Tooling

- **Vite** — default for new projects; fast dev server, ESM-native
- **Next.js** — when SSR, SSG, or file-based routing is needed (React)
- **Nuxt** — equivalent for Vue
- **Webpack** — legacy; match existing config, don't migrate unprompted

## Frontend Testing

- **Unit/component**: Vitest + Testing Library (`@testing-library/react` or `@testing-library/vue`)
- **E2E**: Playwright (preferred over Cypress for new projects)
- Test behaviour, not implementation — query by role/label, not by class or test ID
- Avoid snapshot tests for logic; use them sparingly for stable UI components

```tsx
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

test('calls onClick when button is clicked', async () => {
  const handleClick = vi.fn()
  render(<Button onClick={handleClick}>Submit</Button>)
  await userEvent.click(screen.getByRole('button', { name: 'Submit' }))
  expect(handleClick).toHaveBeenCalledOnce()
})
```

## Performance Basics

- Lazy-load routes and heavy components with `React.lazy` / Vue's `defineAsyncComponent`
- `useMemo` / `useCallback` only when a profiler shows it helps — don't add them preemptively
- Images: use correct `width`/`height` to prevent layout shift; lazy-load below-the-fold images
- Avoid re-renders from object/array literals in JSX — define outside the component or memoize

## Code Review Checklist

Flag these when reviewing:
1. `key` prop using array index — use a stable unique ID
2. `useEffect` with missing or incorrect dependencies
3. Inline object/function creation as props causing unnecessary re-renders
4. Direct state mutation (`state.items.push(...)` instead of returning new array)
5. Missing `alt` on `<img>` or interactive element not reachable by keyboard
