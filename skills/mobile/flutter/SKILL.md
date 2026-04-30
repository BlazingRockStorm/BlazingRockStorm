---
name: flutter
description: Flutter development assistance for building iOS and Android apps. Covers Dart, the widget tree, state management, navigation, platform integration, and deployment to test environments. For deployment to TestFlight, Firebase App Distribution, or Play Console, load `references/deployment.md`. Builds on existing TypeScript, JavaScript, React, Ruby, and Go knowledge.
---

# Flutter

You are assisting a System/DevOps engineer with expert Ruby knowledge, strong React experience, and basic Go and TypeScript/JavaScript proficiency. Flutter is in their stack but is not their primary focus — explain Flutter-specific concepts clearly and map Dart/widget concepts to React, TypeScript, and Ruby analogues where they make the idea click faster.

## Skill Delegation

| Question type | Skill to apply |
|---|---|
| iOS TestFlight, Android Play Console, Firebase App Distribution | Load `references/deployment.md` |
| Pure JavaScript runtime questions surfacing in Dart code | `javascript` skill |
| TypeScript type-system questions about a TS backend the app talks to | `typescript` skill |
| React Native (not Flutter) | Out of scope — flag and ask the user to confirm |

---

## Codebase Adaptation

### Step 1 — Detect constraints

| File | What to read |
|---|---|
| `pubspec.yaml` | Flutter/Dart SDK version constraints, existing dependencies — never suggest packages that duplicate what is already there |
| `analysis_options.yaml` | Lint rules (typically `flutter_lints` or `very_good_analysis`) — follow them |
| `android/app/build.gradle` | `minSdkVersion`, `targetSdkVersion`, `applicationId`, Kotlin version |
| `ios/Podfile` | `platform :ios` deployment target, existing CocoaPods dependencies |
| `ios/Runner.xcodeproj/` | Bundle identifier, signing configuration, enabled capabilities |
| `lib/` structure | State management choice (Riverpod, Bloc, Provider, `setState`), folder conventions |

### Step 2 — Classify the project

| Classification | Signals | Approach |
|---|---|---|
| **Greenfield** | Only `pubspec.yaml`, no `lib/` code | Apply defaults from this skill; confirm state management preference |
| **Active project** | Has `lib/`, recent commits | Match existing folder structure, state solution, and widget style strictly |
| **Legacy project** | Flutter < 3.0, null safety opt-out, deprecated APIs | Stay within existing SDK constraints; flag migration only when asked |
| **Constrained** | No pub.dev access, corporate proxy, air-gapped | Use a private pub mirror via `PUB_HOSTED_URL` or vendored `path:` dependencies; confirm before running `dart pub get` |

### Step 3 — State what you found

_"Flutter 3.22, Riverpod 2, `flutter_lints`, iOS 16 / Android API 24 min — I'll use `ConsumerWidget`, null-safe Dart, and match the existing feature folder layout."_

---

## Dart — Mental Models

Dart is statically typed with sound null safety, compiled to native on mobile — think TypeScript strictness with Go's native compilation.

### TypeScript → Dart

| TypeScript | Dart |
|---|---|
| `string` | `String` |
| `number` | `int` / `double` |
| `boolean` | `bool` |
| `null` / `undefined` | `null` (null-safe: `String?` for nullable) |
| `any` | `dynamic` — avoid for the same reasons as TS `any` |
| `interface` / `type` | `abstract class` / `class` with named fields |
| `enum` | `enum` (enhanced enums with fields in Dart 2.17+) |
| `T \| null` | `T?` |
| `Promise<T>` | `Future<T>` |
| `async / await` | `async / await` — identical syntax |
| `Array<T>` | `List<T>` |
| `Record<string, T>` | `Map<String, T>` |
| `readonly` field | `final` (runtime) / `const` (compile-time) |
| Arrow `(x) => x * 2` | `(x) => x * 2` — identical |
| Optional chaining `a?.b` | `a?.b` — identical |
| Nullish coalescing `a ?? b` | `a ?? b` — identical |
| Template literal `` `Hi ${name}` `` | `'Hi $name'` or `'Hi ${expr}'` |

### Ruby → Dart

| Ruby | Dart |
|---|---|
| `nil` | `null` |
| `freeze` | `const` constructor |
| `Struct` / `Data` | `class` with `final` fields + `const` constructor |
| `begin / rescue` | `try / catch` |
| Block `{ \|x\| ... }` | `(x) { ... }` or `(x) => ...` |
| `module` / mixin | `mixin` keyword |
| `Enumerable#map` | `list.map((x) => ...)` |
| `Enumerable#where` | `list.where((x) => ...)` |
| `respond_to?` | No runtime equivalent — declare an `abstract class` or `mixin` interface and use `is` to type-check |

### Null Safety

```dart
String name = 'Alice';          // non-nullable — compiler enforces it is never null
String? nickname;               // nullable

// Null-aware operators (same as TypeScript)
print(nickname?.toUpperCase()); // null-safe call
print(nickname ?? 'anon');      // fallback value
nickname ??= 'Buddy';           // assign only if null

// Late fields — like TS definite assignment assertion
late final String config;       // assigned before first read, not at declaration
```

### Async / Await

Dart `Future<T>` = JavaScript `Promise<T>`. The syntax is identical.

```dart
Future<User> fetchUser(String id) async {
  final response = await http.get(Uri.parse('/users/$id'));
  if (response.statusCode != 200) {
    throw HttpException('Failed to load user', uri: Uri.parse('/users/$id'));
  }
  return User.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
}

// Parallel — equivalent to Promise.all
final results = await Future.wait([fetchUsers(), fetchPosts()]);

// Stream<T> — like RxJS Observable
Stream<int> countdown(int from) async* {
  for (var i = from; i >= 0; i--) {
    yield i;
    await Future.delayed(const Duration(seconds: 1));
  }
}
```

---

## Widget System

Flutter's widget tree maps directly to React's component tree.

| React / Vue | Flutter |
|---|---|
| Functional component (no state) | `StatelessWidget` |
| Component with `useState` | `StatefulWidget` |
| `useEffect` + cleanup | `initState` / `dispose` |
| `props` | Constructor named parameters |
| `children` prop | `child:` / `children:` parameter |
| Context / Provider | `InheritedWidget`, `Provider`, Riverpod |
| JSX `return (...)` | `Widget build(BuildContext context)` |
| CSS flexbox | `Row` / `Column` / `Flex` |
| CSS box model | `Container`, `Padding`, `SizedBox` |
| Conditional render | Ternary or `if (cond) widget` inside a `children` list |
| `list.map(item => <Item />)` | `items.map((item) => ItemWidget(item: item)).toList()` |

### StatelessWidget

```dart
class UserCard extends StatelessWidget {
  const UserCard({super.key, required this.user});

  final User user;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        leading: CircleAvatar(child: Text(user.name[0])),
        title: Text(user.name),
        subtitle: Text(user.email),
      ),
    );
  }
}
```

### StatefulWidget

```dart
class Counter extends StatefulWidget {
  const Counter({super.key});

  @override
  State<Counter> createState() => _CounterState();
}

class _CounterState extends State<Counter> {
  int _count = 0;

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Text('Count: $_count', style: Theme.of(context).textTheme.headlineMedium),
        ElevatedButton(
          onPressed: () => setState(() => _count++),
          child: const Text('Increment'),
        ),
      ],
    );
  }

  @override
  void dispose() {
    // Release resources (controllers, subscriptions) — like useEffect cleanup
    super.dispose();
  }
}
```

### Core Layout Widgets

| Goal | Widget |
|---|---|
| Horizontal | `Row(children: [...])` |
| Vertical | `Column(children: [...])` |
| Overlap layers | `Stack(children: [...])` |
| Fixed spacing | `SizedBox(width: 8)` / `SizedBox(height: 16)` |
| Padding | `Padding(padding: EdgeInsets.symmetric(horizontal: 16))` |
| Expand to fill | `Expanded(child: ...)` |
| Scrollable list | `ListView.builder(itemCount: n, itemBuilder: (ctx, i) => ...)` |
| Scrollable grid | `GridView.builder(gridDelegate: ..., itemBuilder: ...)` |
| Rounded corners / clip | `ClipRRect(borderRadius: BorderRadius.circular(8), child: ...)` |
| Tap target | `GestureDetector(onTap: ..., child: ...)` / `InkWell` |

---

## State Management

Match the state solution already used in the project. For greenfield, default to **Riverpod**.

| Scope | Recommended tool |
|---|---|
| Simple local UI | `setState` in `StatefulWidget` |
| Complex local logic | `ValueNotifier` + `ValueListenableBuilder` |
| Shared across a feature | Riverpod `Provider` / `StateProvider` |
| Async server state | Riverpod `FutureProvider` / `AsyncNotifier` |
| Complex business logic | Riverpod `Notifier` / `AsyncNotifier`, or `Bloc` / `Cubit` |

### Riverpod (default for new projects)

```dart
// providers/user_provider.dart
final userProvider = FutureProvider.family<User, String>((ref, id) {
  return ref.watch(userRepositoryProvider).fetchUser(id);
});

// Consume in a widget — no BuildContext boilerplate
class UserScreen extends ConsumerWidget {
  const UserScreen({super.key, required this.userId});

  final String userId;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final userAsync = ref.watch(userProvider(userId));

    return userAsync.when(
      data:    (user)  => UserCard(user: user),
      loading: ()     => const CircularProgressIndicator(),
      error:   (e, _) => Text('Error: $e'),
    );
  }
}
```

---

## Navigation — GoRouter

GoRouter is Flutter's standard routing library (like React Router). Use it for all non-trivial navigation.

```dart
// router.dart
final routerProvider = Provider<GoRouter>((ref) {
  return GoRouter(
    initialLocation: '/',
    routes: [
      GoRoute(
        path: '/',
        builder: (context, state) => const HomeScreen(),
      ),
      GoRoute(
        path: '/users/:id',
        builder: (context, state) {
          final id = state.pathParameters['id']!;
          return UserDetailScreen(userId: id);
        },
      ),
      ShellRoute(
        builder: (context, state, child) => AppShell(child: child),
        routes: [/* tab routes */],
      ),
    ],
  );
});

// Navigate
context.push('/users/$userId');     // push onto stack
context.go('/home');                // replace (no back button)
context.pop();                      // go back
context.push('/detail', extra: obj); // pass non-URL data
```

---

## Platform Integration

### iOS key files

| File | Purpose |
|---|---|
| `ios/Runner/Info.plist` | Permissions, URL schemes, display name |
| `ios/Runner/AppDelegate.swift` | App entry, plugin registration |
| `ios/Podfile` | Deployment target, CocoaPods deps |
| `ios/Runner.xcodeproj/project.pbxproj` | Build settings, signing, capabilities |
| `ios/Runner/Assets.xcassets` | App icon, launch image |

### Android key files

| File | Purpose |
|---|---|
| `android/app/build.gradle` | App ID, SDK versions, signing config |
| `android/app/src/main/AndroidManifest.xml` | Permissions, activities, intent filters |
| `android/app/src/main/res/` | Icons, launch screen drawables |
| `android/key.properties` | Keystore credentials — **gitignore this file** |

### Declaring permissions

```xml
<!-- android/app/src/main/AndroidManifest.xml -->
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.CAMERA" />
```

```xml
<!-- ios/Runner/Info.plist -->
<key>NSCameraUsageDescription</key>
<string>Required to scan QR codes</string>
```

Always request runtime permissions via the `permission_handler` package — manifest-only declarations are not enough on modern Android and iOS.

### Platform channel (native bridge)

```dart
// Call native Kotlin/Swift code from Dart
const _channel = MethodChannel('com.example.app/native');

Future<String> getNativeValue() async {
  return await _channel.invokeMethod<String>('getValue') ?? '';
}
```

---

## Project Structure

```
lib/
  main.dart              # entry point — minimal; call runApp, set up ProviderScope
  app.dart               # MaterialApp.router config, theme, router
  core/
    theme/               # ThemeData, ColorScheme, TextTheme
    router/              # GoRouter definition
    network/             # Dio / http client, interceptors
    error/               # failure types, error handler
  features/
    auth/
      data/              # repositories, remote/local data sources, DTOs
      domain/            # entities, use cases (business logic)
      presentation/      # screens, widgets, providers / blocs
    home/
    profile/
  shared/
    widgets/             # reusable UI components
    extensions/          # Dart extension methods
    utils/               # pure utility functions
test/
  unit/
  widget/
  integration/
```

---

## Common Patterns

### JSON model with code generation

```dart
// Use json_serializable — generates _$UserFromJson / _$UserToJson
import 'package:json_annotation/json_annotation.dart';

part 'user.g.dart';

@JsonSerializable()
class User {
  const User({required this.id, required this.name, required this.email});

  final String id;
  final String name;
  final String email;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
  Map<String, dynamic> toJson() => _$UserToJson(this);
}
```

Run code generation: `dart run build_runner build --delete-conflicting-outputs`

### Sealed class result type (like Ruby pattern matching)

```dart
sealed class Result<T> {
  const Result();
}

class Success<T> extends Result<T> {
  const Success(this.value);
  final T value;
}

class Failure<T> extends Result<T> {
  const Failure(this.error);
  final Object error;
}

// Exhaustive switch — compiler enforces all cases are handled
switch (result) {
  case Success(:final value): print(value);
  case Failure(:final error): print('Error: $error');
}
```

### Theming

```dart
// Access in any widget — no need to pass theme down manually
final theme = Theme.of(context);
final colors = theme.colorScheme;

Text('Hello', style: theme.textTheme.headlineMedium);
Container(color: colors.surface);
```

---

## Testing

| Type | Tool | Analogy |
|---|---|---|
| Unit | `flutter test` (built-in) | RSpec unit / Go `testing` |
| Widget | `WidgetTester` in `flutter_test` | React Testing Library |
| Integration | `integration_test` package | Playwright / Capybara |
| Mocking | `mocktail` (preferred) | RSpec mocks / `testify/mock` |

```dart
// Widget test
testWidgets('UserCard shows name', (WidgetTester tester) async {
  final user = User(id: '1', name: 'Alice', email: 'alice@example.com');

  await tester.pumpWidget(
    MaterialApp(child: UserCard(user: user)),
  );

  expect(find.text('Alice'), findsOneWidget);
  expect(find.text('alice@example.com'), findsOneWidget);
});
```

```dart
// Unit test with mocktail
class MockUserRepository extends Mock implements UserRepository {}

void main() {
  late MockUserRepository mockRepo;

  setUp(() => mockRepo = MockUserRepository());

  test('fetchUser returns user on success', () async {
    when(() => mockRepo.fetchUser('1')).thenAnswer((_) async =>
        const User(id: '1', name: 'Alice', email: 'alice@example.com'));

    final result = await mockRepo.fetchUser('1');
    expect(result.name, 'Alice');
  });
}
```

---

## Lint — analysis_options.yaml

```yaml
include: package:flutter_lints/flutter.yaml

linter:
  rules:
    # flutter_lints already enables prefer_const_constructors and many others —
    # only list extras here.
    - avoid_dynamic_calls
    - always_use_package_imports
    - prefer_final_locals
```

Auto-fix: `dart fix --apply` (equivalent to `go fmt` / `rubocop -a`)

---

## CLI Reference

| Task | Command |
|---|---|
| Create project | `flutter create my_app` |
| Install dependencies | `flutter pub get` |
| Run (debug) | `flutter run` |
| Run on specific device | `flutter run -d <device_id>` |
| List connected devices | `flutter devices` |
| Run tests | `flutter test` |
| Analyse code | `dart analyze` |
| Auto-fix lint | `dart fix --apply` |
| Generate code | `dart run build_runner build --delete-conflicting-outputs` |
| Build iOS IPA | `flutter build ipa --release` |
| Build Android App Bundle | `flutter build appbundle --release` |
| Upgrade packages | `flutter pub upgrade` |
| Clean build cache | `flutter clean` |
| Check Flutter environment | `flutter doctor` |
