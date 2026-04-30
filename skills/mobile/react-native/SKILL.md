---
name: react-native
description: React Native development assistance for building iOS and Android apps. Covers Expo and bare workflows, JSX in RN, components, navigation, state, lists/performance, native modules, and deployment to test environments. For deployment to TestFlight, Play Console, EAS Build/Submit, or OTA updates, load `references/deployment.md`. Builds on existing React, JavaScript, and TypeScript knowledge.
---

# React Native

You are assisting a System/DevOps engineer with strong React experience, expert Ruby knowledge, and basic TypeScript/JavaScript proficiency. React Native is a direct extension of their React skills onto mobile — lean on JSX, hooks, and component thinking they already know, and focus the skill's value on what is actually different: the workflow choice (Expo vs bare), native build pipeline, navigation library, list performance, and platform integration.

## Skill Delegation

| Question type | Skill to apply |
|---|---|
| iOS TestFlight, Android Play Console, EAS Build/Submit, OTA updates | Load `references/deployment.md` |
| Generic React component design, hooks, JSX patterns | `frontend` skill (React reference) |
| Pure JavaScript runtime questions | `javascript` skill |
| TypeScript type-system questions | `typescript` skill |
| Flutter (not React Native) | Out of scope — flag and switch to the `flutter` skill |

---

## Codebase Adaptation

### Step 1 — Detect constraints

| File | What to read |
|---|---|
| `package.json` | `react-native` version, `expo` SDK version (if any), scripts, navigation/state libs already chosen |
| `app.json` / `app.config.{js,ts}` | Expo configuration — bundle IDs, plugins, runtime version |
| `metro.config.js` | Bundler customizations (monorepo, SVG, asset extensions) |
| `babel.config.js` | Reanimated plugin, NativeWind, Expo Router preset |
| `tsconfig.json` | Strictness, path aliases — match what's there |
| `.eslintrc*` / `eslint.config.*` | Lint rules (typically `@react-native/eslint-config` or `eslint-config-expo`) |
| `ios/Podfile` | iOS deployment target, use_frameworks, Hermes |
| `android/app/build.gradle` | `minSdkVersion`, `targetSdkVersion`, `applicationId`, Hermes/New Arch flags |
| `app/` vs `src/` layout | Expo Router (`app/`) vs classic (`src/screens/`) |

### Step 2 — Classify the project

| Classification | Signals | Approach |
|---|---|---|
| **Greenfield** | No source yet | Default to **Expo (managed)** with TypeScript + Expo Router; confirm before scaffolding |
| **Expo managed** | `expo` in deps, no `ios/` or `android/` dirs (or generated under `.expo/`) | Use Expo APIs first; reach for config plugins before ejecting |
| **Expo with development build** | `expo` + `ios/` and `android/` dirs both present | Treat as Expo — use config plugins, run via `expo run:ios`/`run:android` |
| **Bare React Native** | No `expo`, full `ios/` and `android/` projects | Use community libraries directly; native config is hand-edited |
| **Legacy** | RN < 0.71, no Hermes, old arch only | Stay within existing version; flag migrations only when asked |
| **Constrained** | No npm registry access, corporate proxy | Use a private registry (`.npmrc`), confirm before `npm install` |

### Step 3 — State what you found

_"RN 0.76 with Expo SDK 52, Expo Router, Zustand, NativeWind — I'll use file-based routes under `app/`, server state via TanStack Query, and avoid suggesting React Navigation directly."_

---

## Expo vs Bare — The First Decision

| Factor | Expo (managed + dev build) | Bare React Native |
|---|---|---|
| Setup time | Minutes (`npx create-expo-app`) | Hours (Xcode + Gradle config) |
| Native module support | Most via Expo SDK + config plugins; custom needs a dev build | Anything — direct native code access |
| Build pipeline | EAS Build (cloud) or local | `xcodebuild` + `gradle` directly |
| OTA updates | EAS Update built-in | CodePush (deprecating) or self-host |
| When to pick | New projects, teams without iOS/Android specialists, fast iteration | Heavy native customization, existing native codebase to embed in |

**Default for greenfield: Expo with a development build.** It supports any native module while keeping EAS, prebuild, and Expo Router. Going fully bare should be a deliberate decision driven by a concrete native need.

---

## JavaScript / TypeScript in React Native

RN runs on Hermes (JavaScriptCore on legacy iOS). Most modern JS works, with caveats:

- No DOM, no `window`, no `document` — only the JS runtime + React Native APIs.
- `fetch`, `URL`, `Promise`, `async/await`, `WeakMap`, `Intl` (mostly) all work on Hermes.
- `localStorage` does **not** exist — use `@react-native-async-storage/async-storage` or `react-native-mmkv`.
- File system access is via `expo-file-system` or `react-native-fs`, not `fs`.
- Default to TypeScript with `strict: true` for new projects. The community templates ship TS by default.

```ts
// Path aliases — set in tsconfig.json AND babel.config.js (via babel-plugin-module-resolver
// or Metro's resolver) — RN does not honour tsconfig paths alone.
import { Button } from '@/components/Button';
```

---

## Components — Leveraging React Knowledge

Everything you know about React function components, hooks, context, and Suspense applies. The differences are:

| Web React | React Native |
|---|---|
| `<div>` | `<View>` |
| `<span>` / inline text | `<Text>` (all text **must** be inside `<Text>`) |
| `<button>` | `<Pressable>` (preferred) or `<TouchableOpacity>` |
| `<input>` | `<TextInput>` |
| `<img>` | `<Image>` from RN, or `expo-image` (preferred — caching, blurhash) |
| `<a href>` | `Linking.openURL()` or navigation library |
| CSS file / className | `StyleSheet.create()` or NativeWind (`className=` via Tailwind) |
| `onClick` | `onPress` |
| `onChange` | `onChangeText` (for TextInput) |
| Scrollable | `<ScrollView>`, or `<FlatList>` for lists |

```tsx
// All text inside <Text>. Forgetting this is the #1 RN footgun — you get a red screen.
function UserCard({ user }: { user: User }) {
  return (
    <Pressable
      onPress={() => navigation.navigate('User', { id: user.id })}
      style={({ pressed }) => [styles.card, pressed && styles.cardPressed]}
    >
      <Image source={{ uri: user.avatarUrl }} style={styles.avatar} />
      <View style={styles.body}>
        <Text style={styles.name}>{user.name}</Text>
        <Text style={styles.email}>{user.email}</Text>
      </View>
    </Pressable>
  );
}
```

---

## Styling

| Approach | When to pick |
|---|---|
| `StyleSheet.create()` | Default for the RN ecosystem; zero deps; good perf |
| **NativeWind** | You like Tailwind on web — same DX on native, Babel-compiled to RN styles |
| `styled-components` / `emotion` | If existing web codebase shares styling abstractions you want to reuse |
| Restyle (Shopify) | Theme-driven, type-safe design systems |

```tsx
import { StyleSheet, View, Text } from 'react-native';

const styles = StyleSheet.create({
  card: { padding: 16, borderRadius: 8, backgroundColor: '#fff' },
  title: { fontSize: 18, fontWeight: '600' },
});
```

```tsx
// NativeWind — same className DX as Tailwind web
<View className="p-4 rounded-lg bg-white">
  <Text className="text-lg font-semibold">Hello</Text>
</View>
```

**Layout:** Flexbox is the only layout system. Defaults differ from web — `flexDirection` defaults to `column`, not `row`.

---

## State Management

Match the project's existing choice. For greenfield, the modern default is **Zustand for client state + TanStack Query for server state**.

| Scope | Recommended tool |
|---|---|
| Local UI state | `useState` / `useReducer` |
| Cross-tree shared state | Zustand (lightweight) or Jotai (atomic) |
| Server state, caching, mutations | TanStack Query (`@tanstack/react-query`) |
| Complex business logic | Redux Toolkit if the team already uses Redux; otherwise Zustand slices |
| Forms | `react-hook-form` + `zod` |

```tsx
// Zustand — no Provider, no boilerplate
import { create } from 'zustand';

export const useAuthStore = create<{
  user: User | null;
  signIn: (u: User) => void;
  signOut: () => void;
}>((set) => ({
  user: null,
  signIn: (user) => set({ user }),
  signOut: () => set({ user: null }),
}));
```

```tsx
// TanStack Query — server state with caching, refetch, retries
const { data, isLoading, error } = useQuery({
  queryKey: ['user', userId],
  queryFn: () => api.fetchUser(userId),
});
```

---

## Navigation

Two real choices — pick one and stay consistent.

### Expo Router (file-based, default for new Expo apps)

```
app/
  _layout.tsx           // Stack root
  index.tsx             // → /
  (tabs)/
    _layout.tsx         // Tab bar
    home.tsx            // → /home
    profile.tsx         // → /profile
  users/
    [id].tsx            // → /users/123
```

```tsx
// app/users/[id].tsx
import { useLocalSearchParams, router } from 'expo-router';

export default function UserScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  return <Text onPress={() => router.back()}>User {id}</Text>;
}
```

### React Navigation (imperative, default for bare RN)

```tsx
const Stack = createNativeStackNavigator<RootStackParamList>();

function RootNavigator() {
  return (
    <Stack.Navigator>
      <Stack.Screen name="Home" component={HomeScreen} />
      <Stack.Screen name="User" component={UserScreen} />
    </Stack.Navigator>
  );
}

// Navigate
navigation.navigate('User', { id: userId });
navigation.goBack();
```

Define a typed `RootStackParamList` — without it, route params are `any`.

---

## Lists & Performance

Lists are where RN apps live or die. The hierarchy:

| Use | Reason |
|---|---|
| `<ScrollView>` | Small, finite content. Renders everything. |
| `<FlatList>` | Default for variable-length lists. Virtualized. |
| `<SectionList>` | Grouped lists (headers per section). |
| **`<FlashList>`** (Shopify) | High-performance replacement for FlatList. Use for any list >50 items. |

```tsx
// FlashList — drop-in for FlatList, much better scroll perf
import { FlashList } from '@shopify/flash-list';

<FlashList
  data={users}
  keyExtractor={(item) => item.id}
  renderItem={({ item }) => <UserCard user={item} />}
  estimatedItemSize={80}
/>
```

**Render perf rules:**
- Memoize row components with `React.memo`.
- Stable `keyExtractor` — never index-based unless the list is truly static.
- Move expensive work off the JS thread with Reanimated worklets when animating.

---

## Platform Integration

### Platform-specific code

```ts
import { Platform } from 'react-native';

const padding = Platform.OS === 'ios' ? 20 : 16;

// Or via file extension — Metro auto-resolves
// Button.ios.tsx, Button.android.tsx, Button.tsx (fallback)
```

### Permissions

Use `expo-camera`, `expo-location`, etc. (Expo) or `react-native-permissions` (bare). Manifest/Info.plist entries are required **and** runtime requests — both, not one or the other.

```xml
<!-- android/app/src/main/AndroidManifest.xml -->
<uses-permission android:name="android.permission.CAMERA" />
```

```xml
<!-- ios/{App}/Info.plist -->
<key>NSCameraUsageDescription</key>
<string>Required to scan QR codes</string>
```

In Expo, declare these via `app.json` or config plugins instead of editing the native files directly.

### Native modules

| Need | Reach |
|---|---|
| Existing community lib | Look on react.dev/community → most needs are covered |
| Custom native code (Expo) | Write an [Expo Module](https://docs.expo.dev/modules/overview/) — works in managed dev builds |
| Custom native code (bare) | Turbomodule via codegen (new arch) or legacy bridge module |

Avoid hand-rolling a native module if a community library exists — the maintenance cost is real.

### New Architecture (Fabric + TurboModules)

Default-on for RN 0.76+. For older projects, check `newArchEnabled=true` in `gradle.properties` and the iOS Podfile. Most modern libraries are now compatible; flag any that are not.

---

## Project Structure

### Expo Router project

```
app/                     # file-based routes (Expo Router)
  _layout.tsx
  (tabs)/
  ...
src/                     # everything else
  components/            # reusable UI
  features/              # feature-scoped (auth/, profile/)
  lib/                   # api client, query client, storage
  hooks/
  stores/                # Zustand stores
  types/
assets/                  # images, fonts
app.config.ts            # Expo config (prefer .ts over app.json)
```

### Bare RN project

```
src/
  navigation/            # navigators, param lists
  screens/               # one folder per screen
  components/
  features/
  services/              # api, storage, analytics
  hooks/
  stores/
  types/
ios/                     # Xcode project — touch sparingly
android/                 # Gradle project — touch sparingly
```

---

## Common Patterns

### API client with TanStack Query

```ts
// src/lib/api.ts
import ky from 'ky';

export const api = ky.create({
  prefixUrl: process.env.EXPO_PUBLIC_API_URL,
  hooks: {
    beforeRequest: [
      async (req) => {
        const token = await getToken();
        if (token) req.headers.set('Authorization', `Bearer ${token}`);
      },
    ],
  },
});

export const fetchUser = (id: string) =>
  api.get(`users/${id}`).json<User>();
```

```tsx
// In a component
const { data: user } = useQuery({
  queryKey: ['user', id],
  queryFn: () => fetchUser(id),
  staleTime: 60_000,
});
```

### Persistent storage — MMKV

```ts
import { MMKV } from 'react-native-mmkv';

export const storage = new MMKV();

storage.set('token', value);            // sync, fast
const token = storage.getString('token');
```

MMKV is ~30× faster than AsyncStorage and synchronous. Prefer it unless the project is locked to Expo Go (no native modules → use AsyncStorage).

### Safe area + keyboard

```tsx
import { SafeAreaView } from 'react-native-safe-area-context';
import { KeyboardAvoidingView, Platform } from 'react-native';

<SafeAreaView style={{ flex: 1 }}>
  <KeyboardAvoidingView
    behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    style={{ flex: 1 }}
  >
    {children}
  </KeyboardAvoidingView>
</SafeAreaView>
```

### Reanimated worklet

```tsx
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
} from 'react-native-reanimated';

const offset = useSharedValue(0);
const animatedStyle = useAnimatedStyle(() => ({
  transform: [{ translateX: offset.value }],
}));

// Animations run on the UI thread — no JS-bridge stutter
<Animated.View style={animatedStyle} />
<Pressable onPress={() => (offset.value = withSpring(100))} />
```

---

## Testing

| Type | Tool | Notes |
|---|---|---|
| Unit / component | Jest + `@testing-library/react-native` | Standard React Testing Library API |
| E2E (preferred) | **Maestro** | YAML flows, simple, runs on real builds |
| E2E (legacy) | Detox | More setup; reach for it only if Maestro can't cover the case |
| Mocking | `jest.fn()`, `msw` for HTTP | Same as web React |

```tsx
import { render, screen, fireEvent } from '@testing-library/react-native';

test('UserCard shows name', () => {
  render(<UserCard user={{ id: '1', name: 'Alice', email: 'a@x.com' }} />);
  expect(screen.getByText('Alice')).toBeTruthy();
});
```

```yaml
# Maestro — flows/login.yaml
appId: com.example.app
---
- launchApp
- tapOn: 'Sign in'
- inputText: 'alice@example.com'
- tapOn: 'Continue'
- assertVisible: 'Welcome, Alice'
```

---

## Lint — eslint.config.js

Expo:

```js
// eslint.config.js
const expoConfig = require('eslint-config-expo/flat');

module.exports = [
  ...expoConfig,
  { rules: { 'react/jsx-uses-react': 'off' } },
];
```

Bare RN:

```js
module.exports = {
  root: true,
  extends: '@react-native',
};
```

Auto-fix: `npm run lint -- --fix`

---

## CLI Reference

| Task | Command |
|---|---|
| Create Expo project | `npx create-expo-app@latest my-app -t default` |
| Create bare RN project | `npx @react-native-community/cli init MyApp` |
| Install JS deps | `npm install` (or `bun install`, `pnpm install`) |
| Install iOS pods | `npx pod-install` (bare) — Expo dev builds run this automatically |
| Run on iOS (Expo) | `npx expo run:ios` |
| Run on Android (Expo) | `npx expo run:android` |
| Run on iOS (bare) | `npx react-native run-ios` |
| Run on Android (bare) | `npx react-native run-android` |
| Start Metro bundler | `npx expo start` (Expo) / `npx react-native start` (bare) |
| Run tests | `npm test` |
| Type-check | `npx tsc --noEmit` |
| Lint | `npm run lint` |
| Clear Metro cache | `npx expo start -c` / `npx react-native start --reset-cache` |
| Regenerate native dirs (Expo) | `npx expo prebuild --clean` |
| Build for store (Expo) | `eas build --platform all` — see `references/deployment.md` |
