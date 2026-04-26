# React Reference

Primary framework. Apply this reference for all React projects unless Vue is specified.

## Component Patterns

### Function components only
Class components are legacy — never write new ones. All components are functions:

```tsx
export function UserCard({ user }: { user: User }) {
  return <div>{user.name}</div>
}
```

### Component composition over configuration
Prefer composing small components over large components with many props:

```tsx
// Prefer this
<Card>
  <CardHeader>Title</CardHeader>
  <CardBody>Content</CardBody>
</Card>

// Over this
<Card title="Title" body="Content" hasHeader showBorder ... />
```

## Hooks

### Built-in hooks — when to use each

| Hook | Use for |
|---|---|
| `useState` | Simple local state |
| `useReducer` | State with multiple sub-values or complex transitions |
| `useEffect` | Syncing with external systems (API, subscriptions, timers) |
| `useContext` | Reading shared state without prop drilling |
| `useRef` | DOM references or mutable values that don't trigger re-renders |
| `useMemo` | Expensive derived values (profile first) |
| `useCallback` | Stable function identity for child components or effects (profile first) |
| `useId` | Unique IDs for accessibility labels |

### `useEffect` rules
- One effect per concern — split unrelated logic into separate `useEffect` calls
- Always return a cleanup function when subscribing or setting timers
- If the effect fetches data, use TanStack Query instead

```tsx
useEffect(() => {
  const controller = new AbortController()
  fetch('/api/data', { signal: controller.signal })
    .then(r => r.json())
    .then(setData)
  return () => controller.abort()
}, [])
```

### Custom hooks
Extract reusable stateful logic into custom hooks — prefix with `use`:

```tsx
function useDebounce<T>(value: T, delay: number): T {
  const [debounced, setDebounced] = useState(value)
  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay)
    return () => clearTimeout(timer)
  }, [value, delay])
  return debounced
}
```

## State Management in React

### Local state
```tsx
const [count, setCount] = useState(0)
// Always use functional update when new state depends on old
setCount(prev => prev + 1)
```

### `useReducer` for complex state
```tsx
type Action = { type: 'increment' } | { type: 'reset' }

function reducer(state: number, action: Action): number {
  switch (action.type) {
    case 'increment': return state + 1
    case 'reset': return 0
  }
}

const [count, dispatch] = useReducer(reducer, 0)
```

### Context — for shared state within a feature tree
```tsx
const ThemeContext = createContext<'light' | 'dark'>('light')

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<'light' | 'dark'>('light')
  return <ThemeContext.Provider value={theme}>{children}</ThemeContext.Provider>
}

export const useTheme = () => useContext(ThemeContext)
```

### Zustand — for global app state
```tsx
import { create } from 'zustand'

interface AuthStore {
  user: User | null
  login: (user: User) => void
  logout: () => void
}

const useAuthStore = create<AuthStore>(set => ({
  user: null,
  login: user => set({ user }),
  logout: () => set({ user: null }),
}))
```

### TanStack Query — for server state
```tsx
const { data, isLoading, error } = useQuery({
  queryKey: ['users', userId],
  queryFn: () => fetch(`/api/users/${userId}`).then(r => r.json()),
})

const mutation = useMutation({
  mutationFn: (data: UserCreate) => fetch('/api/users', { method: 'POST', body: JSON.stringify(data) }),
  onSuccess: () => queryClient.invalidateQueries({ queryKey: ['users'] }),
})
```

## Routing (React Router v6+)

```tsx
// main.tsx
createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      { index: true, element: <Home /> },
      { path: 'users/:id', element: <UserDetail /> },
      { path: '*', element: <NotFound /> },
    ],
  },
])

// In component
const { id } = useParams<{ id: string }>()
const navigate = useNavigate()
```

## Forms

- Use **React Hook Form** for non-trivial forms — it avoids re-renders on every keystroke
- Pair with **Zod** for schema validation

```tsx
const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
})

const { register, handleSubmit, formState: { errors } } = useForm({
  resolver: zodResolver(schema),
})
```

## Performance

- `React.memo` — wrap components that receive stable props but re-render from parent updates
- `React.lazy` + `Suspense` — lazy-load routes and heavy components
- React DevTools Profiler — profile before adding `useMemo`/`useCallback`

```tsx
const HeavyChart = React.lazy(() => import('./HeavyChart'))

<Suspense fallback={<Spinner />}>
  <HeavyChart data={data} />
</Suspense>
```

## React-specific Testing

```tsx
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

// Wrap with providers your component needs
function renderWithProviders(ui: React.ReactElement) {
  return render(<QueryClientProvider client={testQueryClient}>{ui}</QueryClientProvider>)
}

test('submits form with valid data', async () => {
  const user = userEvent.setup()
  renderWithProviders(<LoginForm onSuccess={vi.fn()} />)

  await user.type(screen.getByLabelText('Email'), 'quan@example.com')
  await user.type(screen.getByLabelText('Password'), 'secret123')
  await user.click(screen.getByRole('button', { name: 'Log in' }))

  await waitFor(() => expect(screen.getByText('Welcome')).toBeInTheDocument())
})
```

## Version Notes

- **React 18**: concurrent rendering, `useTransition`, `useDeferredValue`, automatic batching
- **React 19**: `use()` hook for promises/context, Server Actions, `useActionState`, `useOptimistic`
- For Next.js 13+: distinguish between Server Components (no hooks, no interactivity) and Client Components (`'use client'`)
