# Vue Reference

Secondary framework (1–2 projects experience). Apply this reference when the user explicitly says "Vue" or the project has `vue` in `package.json`. Provide more explanation than with React — familiarity is lower.

## Vue 3 vs Vue 2

Always use **Vue 3** with **Composition API** for new work. If the project is Vue 2 or uses Options API, match what exists rather than introducing Composition API unprompted — flag it as a suggestion instead.

| Vue 2 / Options API | Vue 3 / Composition API |
|---|---|
| `data()`, `methods`, `computed` in one object | `ref`, `computed`, functions in `<script setup>` |
| `this.property` | Direct variable access |
| `Vue.use(plugin)` | `app.use(plugin)` |
| Vuex | Pinia |
| Vue Router 3 | Vue Router 4 |

## Single File Components (SFC)

Vue's `.vue` format combines template, script, and style in one file:

```vue
<script setup lang="ts">
import { ref, computed } from 'vue'

interface Props {
  initialCount?: number
}

const props = withDefaults(defineProps<Props>(), { initialCount: 0 })
const emit = defineEmits<{ change: [count: number] }>()

const count = ref(props.initialCount)
const doubled = computed(() => count.value * 2)

function increment() {
  count.value++
  emit('change', count.value)
}
</script>

<template>
  <button @click="increment">Count: {{ count }} (doubled: {{ doubled }})</button>
</template>

<style scoped>
button { font-weight: bold; }
</style>
```

- Use `<script setup>` — it is the idiomatic Vue 3 style and generates less boilerplate than `setup()` function
- Use `lang="ts"` when the project is TypeScript
- `scoped` styles apply only to this component — prefer it over global styles

## Reactivity

```ts
import { ref, reactive, computed, watch, watchEffect } from 'vue'

// ref — for primitives; access via .value in script, not in template
const name = ref('Quan')
name.value = 'Alice'

// reactive — for objects; no .value needed, but loses reactivity if destructured
const user = reactive({ name: 'Quan', age: 30 })

// computed — cached derived value
const greeting = computed(() => `Hello, ${name.value}!`)

// watch — run side effect when specific values change
watch(name, (newVal, oldVal) => { console.log(newVal, oldVal) })

// watchEffect — runs immediately, tracks dependencies automatically
watchEffect(() => { document.title = name.value })
```

**Gotcha**: destructuring a `reactive` object breaks reactivity. Use `toRefs` to preserve it:
```ts
const { name, age } = toRefs(user)  // now name and age are refs
```

## Component Communication

```vue
<!-- Parent to child: props -->
<UserCard :user="currentUser" :show-avatar="true" />

<!-- Child to parent: emits -->
<ConfirmDialog @confirm="handleConfirm" @cancel="handleCancel" />

<!-- Two-way binding -->
<TextInput v-model="searchQuery" />
<!-- Equivalent to :modelValue="searchQuery" @update:modelValue="searchQuery = $event" -->
```

## `provide` / `inject` — Shared State in a Feature Tree

Equivalent to React Context:

```ts
// Parent
provide('theme', readonly(theme))

// Any descendant
const theme = inject<Ref<string>>('theme')
```

## Pinia — Global State

```ts
// stores/auth.ts
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const isLoggedIn = computed(() => user.value !== null)

  function login(u: User) { user.value = u }
  function logout() { user.value = null }

  return { user, isLoggedIn, login, logout }
})

// In component
const auth = useAuthStore()
auth.login(user)
```

## Vue Router 4

```ts
// router/index.ts
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Home },
    { path: '/users/:id', component: UserDetail, props: true },
    { path: '/:pathMatch(.*)*', component: NotFound },
  ],
})

// In component
const route = useRoute()
const router = useRouter()
const userId = route.params.id
router.push('/users/1')
```

Use `props: true` to pass route params as component props — keeps components decoupled from the router.

## Composables — Reusable Logic

Vue's equivalent of React custom hooks:

```ts
// composables/useDebounce.ts
export function useDebounce<T>(value: Ref<T>, delay: number) {
  const debounced = ref(value.value) as Ref<T>
  watchEffect(() => {
    const timer = setTimeout(() => { debounced.value = value.value }, delay)
    return () => clearTimeout(timer)
  })
  return debounced
}

// Usage
const search = ref('')
const debouncedSearch = useDebounce(search, 300)
```

## Testing (Vue)

```ts
import { mount } from '@vue/test-utils'
import { describe, it, expect, vi } from 'vitest'

describe('UserCard', () => {
  it('emits change event on click', async () => {
    const wrapper = mount(UserCard, {
      props: { user: { id: 1, name: 'Quan' } },
    })
    await wrapper.find('button').trigger('click')
    expect(wrapper.emitted('change')).toBeTruthy()
  })
})
```

- Use `@vue/test-utils` with Vitest
- Prefer `mount` over `shallowMount` — test real composition
- For Pinia in tests: `setActivePinia(createPinia())` in `beforeEach`

## Vue-specific Gotchas (compared to React)

| React behaviour | Vue equivalent / difference |
|---|---|
| Re-render on state change | Template updates reactively — no re-render concept |
| `key` prop on lists | `:key` binding — same rule, always use stable IDs |
| Conditional: `{condition && <Comp />}` | `v-if="condition"` |
| List rendering: `.map()` in JSX | `v-for="item in items" :key="item.id"` |
| `onClick` | `@click` (shorthand for `v-on:click`) |
| `:className` | `:class` — accepts string, array, or object |
