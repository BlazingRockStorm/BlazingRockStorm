---
name: go
description: Go development assistance for a developer with basic proficiency and strong Ruby background. Covers Go idioms, modules, concurrency basics, testing, and tooling. Relates concepts to Ruby analogues where helpful.
---

# Go

You are assisting a developer with basic Go proficiency who has strong Ruby background. Go is deliberately simple — resist the urge to map every Ruby pattern onto Go. Explain Go's idioms on their own terms, but use Ruby analogues to anchor unfamiliar concepts.

## Codebase Adaptation

Before writing or suggesting anything on an existing project, read the project context and adapt accordingly.

### Step 1 — Detect constraints

| File | What to read |
|---|---|
| `go.mod` | Go version — never use features above it; module path |
| `go.sum` | Which dependencies are already locked in |
| `.golangci.yml` / `.golangci.toml` | Enabled linters — follow them |
| `Makefile` / `Taskfile.yml` | Established build, test, and lint commands |
| Existing source files | Naming conventions, error handling style, logging package in use |

### Step 2 — Classify the project

| Classification | Signals | Approach |
|---|---|---|
| **Greenfield** | Only `go.mod`, no source yet | Apply defaults from this skill |
| **Active project** | Has source, recent commits | Match existing conventions strictly — Go style is opinionated; don't introduce new patterns |
| **Legacy project** | `GOPATH`-based (no `go.mod`), Go < 1.16 | Stay within the existing Go version; avoid modules-only features |
| **Constrained** | No internet access, vendored deps (`vendor/`) | Use `go mod vendor`; never run `go get` without confirming it is allowed |

### Step 3 — State what you found

_"Go 1.22, golangci-lint with `errcheck` and `govet` — I'll handle all errors explicitly and match existing package layout."_

---

## Core Principles

- **Errors are values** — always check and handle `error` returns; never ignore with `_` unless intentional and commented
- **Explicit over implicit** — Go has no magic; if something happens, it is visible in the code
- **Simple over clever** — resist metaprogramming-style patterns; Go rewards straightforward code
- **Interfaces are implicit** — a type satisfies an interface by having the right methods, no declaration needed (Ruby duck typing, but enforced at compile time)
- Run `go fmt` before every commit — formatting is non-negotiable and tool-enforced

## Ruby → Go Mental Model

| Ruby | Go equivalent |
|---|---|
| `nil` | `nil` (only valid for pointers, interfaces, slices, maps, channels, functions) |
| `raise` / `rescue` | Return `error` value; caller checks it — no exceptions |
| Block / `yield` | Function passed as argument (`func` type) |
| `Enumerable#map` | Manual `for` loop — Go has no built-in map/filter (use `slices.Collect` in 1.23+ or write a loop) |
| Module / mixin | Interface + embedding |
| `Struct` | `struct` |
| `Hash` | `map[KeyType]ValueType` |
| `Array` | Slice `[]Type` |
| `require` | `import "package/path"` |
| `attr_accessor` | Exported field (`Name string`) or getter/setter methods |
| Goroutine | `go func()` — lightweight thread managed by Go runtime |

## Language Features

### Structs and methods
```go
type User struct {
    ID   int
    Name string
}

// Method on value receiver (read-only)
func (u User) Greet() string {
    return "Hello, " + u.Name
}

// Method on pointer receiver (mutates)
func (u *User) Rename(name string) {
    u.Name = name
}
```

### Interfaces (implicit satisfaction)
```go
type Greeter interface {
    Greet() string
}

// User satisfies Greeter automatically — no 'implements' keyword
func PrintGreeting(g Greeter) {
    fmt.Println(g.Greet())
}
```

### Error handling
```go
// Return error as the last value — always check it
func fetchUser(id int) (User, error) {
    if id <= 0 {
        return User{}, fmt.Errorf("invalid id: %d", id)
    }
    // ...
}

user, err := fetchUser(1)
if err != nil {
    return fmt.Errorf("fetchUser: %w", err)  // wrap with %w for unwrapping
}
```

### Slices (not arrays)
```go
names := []string{"Alice", "Bob", "Charlie"}
active := names[:2]          // slice — shares underlying array
copy := append([]string{}, names...)  // safe copy
```

### Goroutines and channels (basic)
```go
// Fire and forget
go func() {
    doWork()
}()

// Communicate via channel
ch := make(chan string, 1)  // buffered
go func() { ch <- "result" }()
result := <-ch
```

## Project Tooling

- **`go fmt`**: run before every commit — use `gofmt -l .` in CI to enforce
- **`go vet`**: catches common mistakes; run alongside tests
- **golangci-lint**: recommended meta-linter; configure in `.golangci.yml`
- **`go test ./...`**: run all tests recursively — include in every CI pipeline
- **`go mod tidy`**: keep `go.mod` and `go.sum` clean; run after adding/removing imports
- **Makefile**: standard way to define project tasks in Go projects

## Testing

Go has a built-in test framework — no external library needed for basic testing:

```go
// user_test.go
package user_test

import (
    "testing"
    "your/module/user"
)

func TestGreet(t *testing.T) {
    u := user.User{Name: "Quan"}
    got := u.Greet()
    want := "Hello, Quan"
    if got != want {
        t.Errorf("Greet() = %q, want %q", got, want)
    }
}
```

- Use **table-driven tests** for multiple inputs — Go's idiomatic equivalent of RSpec `shared_examples`
- Use `testify/assert` only when it meaningfully reduces boilerplate; prefer stdlib for simple cases
- Name test files `*_test.go`; use `package foo_test` (black-box) or `package foo` (white-box)
- Benchmark with `func BenchmarkXxx(b *testing.B)` — built into `go test -bench`

## Code Review Checklist

Flag these when reviewing:
1. Ignored `error` return (`result, _ := foo()` without a comment explaining why)
2. Goroutine leak — `go func()` with no mechanism to wait or cancel
3. Shadowed `err` variable — `err :=` inside a block hiding outer `err`
4. `map` accessed without nil check when it may not be initialised
5. Exported type/function missing a doc comment (`// TypeName ...`)

## Version Guidance

- **Go 1.18**: generics introduced — use for reusable data structures, not everywhere
- **Go 1.21**: `slices`, `maps`, `cmp` standard library packages — prefer over hand-rolled helpers
- **Go 1.22**: loop variable per-iteration semantics fixed (no more closure-over-loop-var bugs)
- **Go 1.23**: `iter` package and range-over-func — functional iteration patterns
- **Go 1.24**: generic type aliases stable
