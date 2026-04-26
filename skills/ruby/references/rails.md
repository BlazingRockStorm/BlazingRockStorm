# Ruby on Rails Reference

Use this reference for full-stack Rails applications, API-only Rails apps, or when inheriting an existing Rails project.

## Architecture

- Fat models, skinny controllers — move business logic to service objects (`app/services/`)
- Name service objects after the action they perform: `CreateOrder`, `ProcessPayment`, `ArchiveUser`
- Use `app/queries/` for complex query objects; keep `ActiveRecord` scopes for simple, reusable filters
- Keep `ApplicationRecord` and `ApplicationController` clean — use concerns only for cross-cutting behaviour shared by 3+ classes

## ActiveRecord

- Use scopes (`scope :active, -> { where(active: true) }`) for reusable query logic; chain them freely
- Avoid raw SQL unless profiling proves it necessary; use Arel for dynamic query building
- Always add database-level constraints in addition to model validations — validations can be bypassed
- Use `includes` / `eager_load` to prevent N+1 queries; check with Bullet gem in development
- Prefer `find_each` / `find_in_batches` over `all.each` for large datasets

## Controllers

- `strong_parameters` strictly: permit only the exact fields needed, never `permit!` in production
- Keep controller actions to the 7 RESTful actions; extract custom actions to a new controller
- Use `before_action` for auth and record lookup; avoid deep callback chains

## Background Jobs

- Use `ActiveJob` with an appropriate adapter (Sidekiq for production, `:async` for dev)
- Name jobs after the action: `ProcessPaymentJob`, `SendWelcomeEmailJob`
- Keep jobs idempotent — they may be retried; use a job-level `idempotency_key` when needed
- Avoid passing ActiveRecord objects directly to jobs; pass IDs and re-fetch inside `perform`

## API Mode

- Use `rails new --api` for pure JSON APIs; skip view-layer middleware
- Version APIs under `api/v1/` namespace from day one — retrofitting versions is painful
- Respond with consistent JSON envelopes: `{ data: ..., errors: [...], meta: { ... } }`
- Use `jbuilder` or `active_model_serializers` / `fast_jsonapi` for complex serialisation; avoid `.to_json` on models

## Testing (Rails-specific)

- Use `rails generate rspec:install` and `rails generate factory_bot:model` for setup
- Test service objects and query objects in isolation from Rails; no `rails_helper` needed for pure Ruby objects
- Use `request specs` for API endpoints rather than `controller specs`
- Use `DatabaseCleaner` with `:transaction` strategy for speed; switch to `:deletion` for specs that use database triggers

## Performance

- Enable `rack-mini-profiler` in development to catch slow pages early
- Use HTTP caching (`stale?`, `fresh_when`) for read-heavy endpoints
- Cache expensive queries with `Rails.cache`; key on model `cache_key_with_version`
- Use `counter_cache: true` for association counts shown in lists

## When to Choose Rails

- Greenfield product with a team expecting conventions
- Projects that need the full ecosystem: auth (`devise`), admin (`administrate`/`avo`), background jobs, mailers, ActionCable
- Inheriting an existing Rails codebase
