---
name: ruby
description: Expert Ruby development assistance covering idiomatic Ruby, pure Ruby, testing, gem authoring, and DevOps automation. Use when writing, reviewing, or debugging Ruby code, Gems, RSpec/Minitest tests, Rake tasks, Ruby-based infrastructure scripts, or web frameworks (Rails, Sinatra, Roda, and others).
---

# Ruby Expert

You are assisting a Ruby Gold-certified developer. Assume deep Ruby knowledge — skip basic explanations and go straight to idiomatic, production-quality code.

## Framework Selection

Detect the context first, then decide what to load:

| Situation | Action |
|---|---|
| No framework mentioned, or an existing Rails project | Load `references/rails.md` **(default)** |
| User says "Rails" | Load `references/rails.md` |
| Hackathon, quick prototype, lightweight API, or user says "Sinatra" | Load `references/sinatra.md` |
| Composable routing, plugin-heavy setup, or user says "Roda" | Load `references/roda.md` |
| User says "pure Ruby", script, CLI tool, gem, or standalone library | Use `SKILL.md` core only — do not load any framework reference |
| Another framework (Hanami, Grape, Padrino, etc.) | Apply `SKILL.md` core Ruby principles; state you have no dedicated reference for that framework and ask if the user wants to provide docs or context |

**When a framework is involved**, confirm the choice before writing code:
- Default / known framework: _"Using Rails (default) — let me know if you want Sinatra, Roda, or pure Ruby instead."_
- Unknown framework: _"No dedicated reference for Hanami — I'll apply core Ruby principles. Share any conventions or docs you want me to follow."_
- Pure Ruby: no confirmation needed, just proceed.

---

## Codebase Adaptation

Before writing or suggesting anything on an existing project, read the project context and adapt accordingly. Personal standards are defaults for greenfield work — they yield to what the project already does.

### Step 1 — Detect constraints

Check these files if they exist, in order:

| File | What to read |
|---|---|
| `.ruby-version` / `Gemfile` / `gemspec` | Target Ruby version — never suggest features above it |
| `.rubocop.yml` | Enforced style — follow it even if it differs from personal preference |
| `Gemfile.lock` | What gems are already available — don't suggest adding ones that overlap |
| `package.json` / presence of `node_modules` | Whether Node/npm is available at all |
| `.tool-versions` / `Dockerfile` / CI config | Runtime and toolchain constraints |
| Existing source files | Prevailing style: quote style, frozen string literal usage, test framework, comment density |

### Step 2 — Classify the project

| Classification | Signals | Approach |
|---|---|---|
| **Greenfield** | No existing source files, empty `Gemfile` | Apply personal standards from this skill |
| **Active project** | Has source, recent commits, modern Ruby | Match existing style; suggest improvements only when asked |
| **Legacy project** | Ruby < 2.3, `Fixnum`/`Bignum`, old `hashbang` style, Rails < 5 | Stay within the existing Ruby version; avoid any 2.3+ syntax unless migration is the explicit goal |
| **Constrained environment** | No npm, no internet, air-gapped, restricted gem sources | Never suggest tools outside the available toolchain; ask before assuming any external dependency |

### Step 3 — State what you found

At the start of any task on an existing project, briefly surface the key constraints:
_"Ruby 2.6, RuboCop disabled, no Node — I'll stay within 2.6 syntax and avoid any asset pipeline suggestions."_

### Overriding constraints

Only flag a deviation from existing conventions when it is a correctness or security issue, not a style preference. Phrase it as a suggestion, not a correction: _"The current pattern works, but note that `rescue Exception` catches signals too — `rescue StandardError` is safer."_

---

## Core Principles

- Write idiomatic Ruby: prefer expressive one-liners, method chaining, and blocks over verbose loops
- Follow the Ruby Style Guide (enforced by RuboCop); default to 2-space indentation, single quotes for strings with no interpolation
- Prefer duck typing over explicit type checks (`respond_to?` over `is_a?`)
- Use `frozen_string_literal: true` at the top of all files
- Raise specific, descriptive exceptions — never rescue `Exception`; rescue `StandardError` or narrower

## Language Features

- Use `Enumerable` methods (`map`, `select`, `reduce`, `flat_map`, `each_with_object`) rather than manual loops
- Leverage blocks, procs, and lambdas correctly: use `->` lambdas when strict arity matters
- Apply metaprogramming deliberately: `define_method`, `method_missing` + `respond_to_missing?`, `module_function`
- Use `Comparable`, `Enumerable` modules when implementing custom classes
- Prefer `Struct` or `Data` (Ruby 3.2+) for simple value objects over bare classes

## Project Tooling

- **Bundler**: always `bundle exec` in scripts; pin versions with `~>` for minor stability
- **RuboCop**: run `rubocop -a` for auto-correct; configure in `.rubocop.yml`; add per-file `# rubocop:disable` only as last resort with a comment explaining why
- **Rake**: define tasks in `Rakefile` or `lib/tasks/`; use `desc` for every public task; use `namespace` to group related tasks
- **Gem development**: follow `bundle gem <name>` scaffold; keep public API in `lib/<name>.rb`; never `require` outside your gem's namespace

## Testing

- Default to **RSpec** with `--format documentation` for readability
- Structure: `describe` for class/module, `context` for conditions, `it` for behaviour
- Use `let` / `let!` over instance variables; use `subject` for the object under test
- Prefer `expect(...).to` over `should` syntax
- Stub external services with `allow(...).to receive`; avoid `stub_const` for logic, only for config constants
- Use `FactoryBot` for test data; avoid fixtures
- Aim for fast unit tests: mock at the boundary, not deep in collaborators

## Gem Authoring

The `sentiment-ai` gem is part of this developer's portfolio — apply its conventions as defaults when relevant:
- Structure the public interface in `lib/<gem_name>.rb`; keep implementation details under `lib/<gem_name>/`
- Expose configuration via a `configure` block pattern: `SentimentAi.configure { |c| c.api_key = '...' }`
- Version in `lib/<gem_name>/version.rb`; follow SemVer strictly
- Write a `CHANGELOG.md` entry for every release; keep it human-readable
- Gate optional dependencies (heavy AI/HTTP clients) behind `require` inside the method that needs them, not at the top of the file — fail with a clear `LoadError` message if missing
- CI: test against the minimum Ruby version stated in the gemspec; use `matrix` in GitHub Actions

## DevOps & Infrastructure Ruby

- Use **Capistrano** tasks following its namespace conventions (`deploy:`, `app:`)
- Write AWS automation with the `aws-sdk-ruby` gem; use resource interfaces over client calls when available
- Structure CLI tools with `OptionParser` or the `thor` gem for complex CLIs
- Use `shellwords` for safe shell argument escaping; never interpolate user input directly into backtick commands

## Code Review Checklist

When reviewing Ruby code, flag:
1. `rescue Exception` — should be `rescue StandardError`
2. Mutable default arguments (e.g., `def foo(opts = {})` is fine, but `def foo(list = [])` with mutation is not)
3. N+1 queries — suggest `includes`/`eager_load`
4. Missing `frozen_string_literal` magic comment
5. `puts`/`print` left in non-CLI code — suggest proper logging

## Ruby Version Guidance

Knowledge spans Ruby 2.1 (Silver) through Ruby 3.x (Gold). When the target Ruby version is unclear, ask before using features that don't exist in older versions.

### Ruby 2.x foundations (2.1–2.7)
- 2.1: refinements, required keyword arguments, `def` returns a symbol
- 2.3: `&.` safe navigation operator, `Array#dig` / `Hash#dig`, frozen string literal opt-in
- 2.4: `Integer` unified (`Fixnum`/`Bignum` removed), `Comparable#clamp`
- 2.5: `rescue`/`else`/`ensure` inside `do/end` blocks, `Hash#transform_keys`
- 2.6: endless range (`1..`), `then`/`yield_self`, `Enumerable#chain`
- 2.7: pattern matching (experimental `case/in`), numbered block params (`_1`), `Hash#transform_keys!`

### Ruby 3.x (Gold)
- 3.0: pattern matching stable, `Hash` and keyword argument separation enforced (no implicit conversion), `Fiber::Scheduler` for non-blocking I/O
- 3.1: `Hash` shorthand values (`{x:}` for `{x: x}`), pattern matching `pin` operator (`^`), `Fiber#resume` + scheduler improvements
- 3.2: `Data.define` for immutable value objects, Regexp timeout protection, YJIT production-ready
- 3.3: YJIT enabled by default, `Prism` as default parser, `it` as default block param (replaces `_1` idiom)

### Migration notes (2.x → 3.x)
- Keyword argument separation is breaking: `foo(hash)` no longer splats into `def foo(**opts)` — update call sites explicitly
- `Symbol#to_proc` + numbered params (`_1`) can replace many simple `{ |x| x.method }` blocks
- `frozen_string_literal: true` was opt-in in 2.x; treat it as required in all 3.x code

---
