# Skills

Practical skills reference. Intended for AI agents when designing or working on systems, and as a public profile for collaborators.

---

## DevOps

### Programming

#### Ruby

##### Object Model & Metaprogramming
- Eigenclass (singleton class) manipulation: defining per-object methods, `class << self` for DSL-style APIs
- Dynamic dispatch with `send` / `public_send`, safe navigation (`&.`), and `respond_to?` guards
- `method_missing` + `respond_to_missing?` for proxy objects and decorator patterns
- `define_method` for generating families of methods at class load time (e.g., attribute accessors, scope builders)
- Module hooks: `included`, `extended`, `prepended`, `inherited`, `method_added` for framework-style behaviour injection
- `prepend` for clean method wrapping without alias chaining (e.g., instrumentation, logging, caching layers)
- `Refinements` for safely scoping monkey-patches to specific files or modules
- `TracePoint` for runtime introspection: tracing method calls, line execution, class definitions

##### Blocks, Procs & Closures
- Yielding with explicit `&block` capture vs implicit `yield` — choosing based on whether the block needs to be stored or forwarded
- `Proc.new` vs `lambda` vs `->`: differences in arity checking and `return` semantics
- Currying and partial application with `Proc#curry` for building composable filters and validators
- Closures over local bindings for building callback chains and deferred execution

##### Enumerable & Collection Patterns
- `Enumerable` protocol: implementing `each` + `include Enumerable` to get `map`, `select`, `reduce`, `flat_map`, `group_by`, `tally`, `filter_map` for free
- `Enumerator::Lazy` for memory-efficient processing of large or infinite sequences (e.g., streaming CSV rows, paginated API results)
- `each_with_object` for accumulator patterns without mutable outer state
- Custom `Enumerator.new` for wrapping external iterators (e.g., database cursor, file lines, API pagination)

##### Concurrency & Parallelism
- `Ractor` (Ruby 3+) for true parallel execution without shared mutable state — message-passing between actors
- `Fiber` and `Fiber.schedule` for cooperative async I/O (e.g., non-blocking HTTP calls, async database queries)
- `Thread` + `Mutex` + `ConditionVariable` for classic shared-state concurrency; `Queue` / `SizedQueue` for producer-consumer patterns
- `Thread::Pool` patterns for bounding concurrency on batch jobs (e.g., parallel image processing, bulk API calls)
- GVL (Global VM Lock) awareness: CPU-bound work stays serialized in CRuby threads; use `Ractor` or fork-based parallelism for CPU tasks

##### Error Handling & Resilience
- `retry` with exponential backoff in `rescue` blocks for transient failures (network timeouts, rate limits)
- Custom exception hierarchies: domain-specific base error class with typed subclasses for structured `rescue` chains
- `ensure` for resource cleanup (file handles, DB connections, temp files) regardless of exception path
- `throw` / `catch` for non-local jumps in deeply nested iterations (e.g., early exit from search)

##### Testing
- RSpec: `describe` / `context` / `it` structure, `let` / `let!` for lazy/eager fixtures, `subject` for DRY specs
- Test doubles: `instance_double` with verified doubles, `allow` / `expect` message expectations, `have_received` for spies
- Shared examples (`shared_examples_for`) and shared contexts for reducing duplication across spec files
- FactoryBot: `factory`, `trait`, `transient` attributes, `sequence` for unique values, `association` for nested records
- Minitest: `assert_*` / `refute_*` style, `setup` / `teardown` hooks, `Minitest::Mock` for lightweight mocking
- SimpleCov for line and branch coverage reporting; integrating coverage gates into CI

##### Gems & Tooling
- Bundler: `Gemfile` groups, `bundle exec` isolation, `Gemfile.lock` for reproducible builds, private gem server configuration
- Rubocop for style enforcement; custom `.rubocop.yml` with project-specific cops and exclusions
- Pry / IRB: runtime debugging with `binding.pry`, object introspection with `ls`, `show-method`, `cd`
- Sorbet / RBS for gradual type checking: `sig` annotations, `T.let`, `T.nilable`, typed interfaces for critical paths

---

#### Python

##### Core Language & Idioms
- List / dict / set / generator comprehensions for expressive, readable data transformations
- Context managers (`with` statement) via `__enter__` / `__exit__` and `contextlib.contextmanager` for resource lifecycle management
- Decorators with `functools.wraps` for preserving metadata; stacking decorators for cross-cutting concerns (logging, auth, retry)
- Dataclasses and `__slots__` for memory-efficient, self-documenting data containers
- Type hints with `mypy` / `pyright` strict mode: `Optional`, `Union`, `TypeVar`, `Generic`, `Protocol` for structural typing
- `__dunder__` methods: `__repr__`, `__eq__`, `__hash__`, `__lt__` for sortable/hashable domain objects; `__getattr__` / `__setattr__` for attribute interception

##### Async & Concurrency
- `asyncio` event loop: `async def` / `await`, `asyncio.gather` for concurrent coroutines, `asyncio.create_task` for fire-and-forget
- `aiohttp` / `httpx` for non-blocking HTTP clients; `asyncpg` for async PostgreSQL queries
- `concurrent.futures.ThreadPoolExecutor` for I/O-bound parallelism; `ProcessPoolExecutor` for CPU-bound work bypassing the GIL
- `anyio` as a backend-agnostic async abstraction layer (works with asyncio and trio)

##### Data & Scripting
- `pathlib.Path` for cross-platform file operations; `shutil` for bulk file management
- `csv`, `json`, `xml.etree` for structured data parsing; `Pydantic` for schema validation and serialization with detailed error messages
- `pandas` for tabular data: `DataFrame` operations, `groupby` + `agg`, `merge` / `join`, `apply` with lambda for row-wise transformations
- `boto3` for AWS SDK integration: session management, resource vs client API style, waiters for polling long-running operations

##### Testing
- `pytest`: fixtures with `@pytest.fixture` and dependency injection, parametrize for data-driven tests, `conftest.py` for shared setup
- `unittest.mock`: `MagicMock`, `patch` as decorator and context manager, `side_effect` for raising exceptions or returning sequences
- `pytest-asyncio` for testing `async def` coroutines; `respx` / `responses` for mocking HTTP calls

##### Tooling
- `pip` + `pyproject.toml` (PEP 517/518) for package management; `poetry` for dependency resolution and virtual environment management
- `black` for zero-config formatting; `ruff` for fast linting (replaces flake8 + isort + many plugins)
- `venv` / `virtualenv` for isolated environments; `pyenv` for Python version management across projects

---

#### JavaScript

##### Core Language
- Prototype chain and `Object.create` for prototype-based inheritance; `class` syntax as syntactic sugar over prototypes
- Closures and lexical scoping: IIFE pattern for encapsulation, factory functions over classes for functional object creation
- Destructuring (object and array), rest/spread operators, optional chaining (`?.`), nullish coalescing (`??`) for concise data access
- `Symbol`, `WeakMap`, `WeakRef` for private fields and memory-safe caching patterns
- `Proxy` and `Reflect` for building reactive state, validation layers, and API mocking
- `Intl` API for locale-aware number/date formatting without external libraries

##### Async & Event Loop
- Event loop mechanics: call stack, microtask queue (Promises, `queueMicrotask`), macrotask queue (setTimeout, setInterval, I/O)
- `Promise.all` / `Promise.allSettled` / `Promise.race` / `Promise.any` for concurrent async coordination
- `async` / `await` with structured error handling; avoiding unhandled rejection with top-level `try/catch` or `.catch()` fallbacks
- `AbortController` + `AbortSignal` for cancellable fetch requests and cleanup in React `useEffect`
- Streams API: `ReadableStream` / `WritableStream` for processing large responses without buffering entire payloads

##### Node.js
- `EventEmitter` for custom event-driven architectures; `stream.pipeline` for safe stream composition with error propagation
- Worker threads (`worker_threads`) for CPU-bound tasks without blocking the event loop
- `fs/promises` and `path` for async file system operations; `child_process.spawn` for subprocess management
- Express.js: middleware chain, `Router` for modular routing, error-handling middleware (`(err, req, res, next)`)
- `http` module internals: `IncomingMessage`, `ServerResponse`, keep-alive connections, chunked transfer encoding

##### Testing & Tooling
- Jest: `describe` / `it` / `test` structure, `beforeEach` / `afterEach` hooks, `jest.fn()` / `jest.spyOn` for mocks, snapshot testing
- `@testing-library` for component testing focused on user behaviour rather than implementation details
- ESLint with `eslint-config-airbnb` or custom rule sets; Prettier for formatting; `lint-staged` + `husky` for pre-commit hooks
- `npm` workspaces / `pnpm` for monorepo dependency management; `esbuild` / `Vite` for fast bundling and HMR

---

#### Go

##### Core Language
- Static typing with interfaces for implicit satisfaction (duck typing): defining narrow interfaces at the consumer, not the producer
- Structs with embedded types for composition over inheritance; method sets on pointer vs value receivers
- Error handling idiom: `if err != nil` with `fmt.Errorf("context: %w", err)` for wrapping and `errors.Is` / `errors.As` for unwrapping
- `defer` for guaranteed resource cleanup (closing files, releasing locks, recovering from panics)
- Slices vs arrays: slice header internals (pointer, length, capacity), `append` growth behaviour, `copy` for safe cloning

##### Concurrency
- Goroutines as lightweight green threads; `go func()` for fire-and-forget; closures capturing loop variables (common gotcha with `v := v`)
- Channels: unbuffered for synchronization, buffered for decoupling producer/consumer; `select` for multiplexing channel operations with timeouts
- `sync.WaitGroup` for waiting on a group of goroutines; `sync.Mutex` / `sync.RWMutex` for shared state protection
- `context.Context` propagation for cancellation and deadlines: `context.WithTimeout`, `context.WithCancel`, passing ctx as first arg convention
- `errgroup` for fan-out with error collection; `sync.Once` for thread-safe lazy initialization

##### Standard Library & Patterns
- `net/http`: building HTTP servers with `http.ServeMux`, middleware via handler wrapping (`func(http.Handler) http.Handler`), graceful shutdown with `http.Server.Shutdown`
- `encoding/json`: `json.Marshal` / `json.Unmarshal`, struct tags (`json:"field,omitempty"`), custom `MarshalJSON` / `UnmarshalJSON` for complex types
- `database/sql` with `pgx` / `go-mysql-driver`: prepared statements, transaction management (`db.Begin`, `tx.Rollback` in defer), connection pool sizing
- Table-driven tests with `t.Run` subtests: `[]struct{ name, input, expected }` pattern for exhaustive coverage; `t.Parallel()` for concurrent test execution
- `go generate` for code generation (mocks with `mockgen`, SQL queries with `sqlc`); build constraints for platform-specific code

##### Tooling
- `go mod` for dependency management: `go.mod` / `go.sum`, `go get` for version pinning, `go mod tidy` for pruning unused deps
- `golangci-lint` for aggregating linters (errcheck, staticcheck, gosec, gocritic); `.golangci.yml` for project-specific configuration
- `pprof` for CPU and memory profiling: `go tool pprof`, flame graphs for identifying hot paths; `go test -bench` for microbenchmarks
- `dlv` (Delve) debugger: breakpoints, goroutine inspection, stack frames — far more Go-aware than gdb

---

#### Frameworks

##### Ruby on Rails
- ActiveRecord: scopes, eager loading (`includes` / `preload` / `eager_load`), N+1 detection with Bullet, counter caches, polymorphic associations, STI vs delegated types
- ActiveJob + Sidekiq: background job processing, retry strategies, dead-letter queues, unique job deduplication, cron-scheduled recurring jobs
- ActionCable: real-time WebSocket channels, broadcasting patterns, connection authentication
- Rails engines for modular monolith architecture: isolating bounded contexts into mountable engines with their own routes, models, and migrations
- Rack middleware: writing custom middleware for request logging, rate limiting, tenant detection in multi-tenant apps
- Database migrations: zero-downtime schema changes (add column with default, backfill, then add constraint), `strong_migrations` gem for safety checks
- Caching: Russian doll fragment caching, low-level `Rails.cache.fetch` with expiry, cache busting with versioned keys

##### FastAPI
- Path and query parameter declaration with Pydantic models for automatic request validation and OpenAPI schema generation
- Dependency injection system: `Depends()` for shared database sessions, auth extraction, and feature-flagged behaviour across routes
- Background tasks with `BackgroundTasks` for fire-and-forget work (email sending, audit logging) without blocking the response
- `async def` route handlers with `await` for non-blocking database queries and HTTP calls; mixing sync and async handlers in the same app
- Router prefixes and tags for organizing large APIs into logical modules; `APIRouter` for splitting routes across files
- Middleware: `BaseHTTPMiddleware` for cross-cutting concerns (CORS, request ID injection, response time headers)
- Lifespan events (`@asynccontextmanager` with `yield`) for managing startup/shutdown of database pools, cache clients, and background workers

##### WordPress
- Theme development: `functions.php` hooks (`add_action`, `add_filter`, `do_action`, `apply_filters`) for modifying core behaviour without editing core files
- Custom Post Types and Taxonomies registered via `register_post_type` / `register_taxonomy` with capability mapping
- `WP_Query` for custom content retrieval: `meta_query` for custom field filtering, `tax_query` for taxonomy filtering, `posts_per_page` pagination
- REST API extension: registering custom endpoints with `register_rest_route`, custom fields on existing endpoints with `register_rest_field`
- Plugin architecture: singleton pattern with activation/deactivation/uninstall hooks, nonce verification for form submissions, capability checks for admin pages
- Performance: object caching with `wp_cache_set` / `wp_cache_get` using persistent cache backends (Redis via WP Redis), transient API for time-limited cache
- Multisite: network activation, `switch_to_blog` for cross-site queries, `wpmu_blogs` table for site enumeration

---

### Infra

#### AWS

##### Networking & VPC Design
- Multi-AZ VPC layouts: public/private/isolated subnets per AZ, NAT Gateway placement for egress, VPC endpoints (Gateway for S3/DynamoDB, Interface for other services) to avoid NAT costs
- Security group layering: separate SGs for ALB → app → database tiers, referencing SG IDs instead of CIDR blocks for intra-VPC rules
- Transit Gateway for hub-and-spoke connectivity across multiple VPCs and accounts; Route table associations for traffic segmentation
- VPC Flow Logs → CloudWatch Logs Insights for troubleshooting connectivity issues (rejected packets, unexpected traffic paths)
- PrivateLink for exposing internal services to consumers in other VPCs/accounts without internet traversal

##### Compute
- EC2 Auto Scaling: target tracking policies (CPU, request count per target), step scaling for bursty workloads, warm pools for faster scale-out, mixed instances with Spot for cost savings
- Launch templates with user data scripts for bootstrapping (install agents, pull config from SSM Parameter Store, join ECS cluster)
- Graviton (ARM) instances for better price-performance on web servers, containerized workloads, and build pipelines
- Spot Instances: capacity-optimized allocation strategy, Spot interruption handling via EC2 metadata + 2-minute warning, Spot Fleet diversification

##### Containers
- ECS on Fargate: task definition sizing (CPU/memory), service auto-scaling (target tracking on CPU or custom CloudWatch metrics), service discovery via Cloud Map
- ECS deployment strategies: rolling update with `minimumHealthyPercent` / `maximumPercent`, blue/green via CodeDeploy with ALB target group switching, circuit breaker for automatic rollback on failed deployments
- EKS: managed node groups with Cluster Autoscaler or Karpenter for right-sizing, Fargate profiles for isolating batch workloads, IRSA (IAM Roles for Service Accounts) for pod-level permissions
- ECR: image lifecycle policies for cleaning untagged images, cross-region replication, image scanning on push with Inspector

##### Serverless
- Lambda: function sizing (memory/CPU trade-off), cold start mitigation (provisioned concurrency, SnapStart for Java), layers for shared dependencies, Lambda extensions for observability
- Event-driven patterns: S3 → Lambda for file processing, SQS → Lambda with batch window and partial failure reporting (`ReportBatchItemFailures`), EventBridge rules for scheduled or cross-account events
- Step Functions: Express vs Standard workflows, `Map` state for parallel fan-out, `Choice` state for branching, error handling with `Retry` / `Catch`, callback patterns with task tokens
- API Gateway: REST APIs with Lambda proxy integration, request validation via JSON Schema models, Cognito/Lambda authorizers, usage plans with API keys for rate limiting per consumer

##### Storage
- S3: lifecycle policies transitioning objects through Standard → IA → Glacier IR → Glacier Deep Archive based on access patterns; S3 Intelligent-Tiering for unpredictable access
- S3 event-driven pipelines: PUT event → SQS → Lambda for async processing; S3 Batch Operations for bulk tagging, copying, or invoking Lambda on millions of objects
- Cross-region replication with S3 Replication Rules for disaster recovery; same-region replication for log aggregation across accounts
- EBS: gp3 with independently tunable IOPS/throughput for database volumes, io2 Block Express for latency-sensitive workloads, EBS snapshots with DLM (Data Lifecycle Manager) for automated backup rotation
- EFS: bursting vs provisioned throughput modes, EFS Access Points for application-specific mount paths with POSIX user mapping, EFS-to-EFS cross-region replication

##### CI/CD & Infrastructure as Code
- CodePipeline: source (CodeCommit/GitHub) → build (CodeBuild) → deploy (CodeDeploy/ECS/CloudFormation) with manual approval gates for production
- CodeBuild: buildspec.yml with phases (install, pre_build, build, post_build), caching (S3/local) for dependency speed-up, custom build images for specialized toolchains
- CodeDeploy: blue/green deployments for EC2/ECS with traffic shifting (canary 10% → 100%, linear 10% every 5 min), automatic rollback on CloudWatch alarm triggers
- CloudFormation: nested stacks for reusable components, cross-stack references with Exports/Imports, custom resources (Lambda-backed) for unsupported resources, drift detection for manual change auditing
- CDK: TypeScript/Python constructs for type-safe IaC, L2 constructs for sensible defaults, `cdk diff` for change previewing, `Aspects` for enforcing tagging and compliance policies across stacks
- SAM: `template.yaml` for Lambda + API Gateway + DynamoDB local development, `sam local invoke` / `sam local start-api` for local testing

##### Monitoring, Logging & Observability
- CloudWatch: custom metrics with `put-metric-data`, composite alarms combining multiple metric conditions, Logs Insights queries for pattern extraction from application logs, metric filters for turning log patterns into alarms
- X-Ray: instrumenting Lambda, ECS, and API Gateway for distributed tracing, X-Ray daemon sidecar in ECS tasks, service map for visualizing latency bottlenecks across microservices
- CloudTrail: organization trail for multi-account API auditing, CloudTrail Lake for SQL-based querying of events, integration with EventBridge for real-time alerting on sensitive API calls (e.g., IAM policy changes)

##### Security & Access Control
- IAM: least-privilege policies using `Condition` keys (e.g., `aws:SourceVpc`, `aws:PrincipalOrgID`), permission boundaries for delegated admin, SCP guardrails at the OU level in AWS Organizations
- Secrets Manager: automatic rotation with Lambda rotation functions for RDS credentials, cross-account secret sharing via resource policies
- KMS: customer-managed keys with key policies and grants, envelope encryption for application-level data protection, automatic key rotation
- WAF: rate-based rules for DDoS mitigation, managed rule groups (AWS, marketplace) for OWASP Top 10, custom rules for geo-blocking or IP reputation filtering

##### Cost Optimization
- Right-sizing with Compute Optimizer recommendations for EC2, Lambda, and EBS
- Savings Plans (Compute/EC2 Instance) and Reserved Instances for predictable baseline workloads
- Spot for fault-tolerant batch processing, CI/CD build agents, and dev/test environments
- S3 storage class analysis and Intelligent-Tiering for reducing storage costs without manual lifecycle management
- Cost allocation tags + Cost Explorer for per-team/per-service cost attribution and budgeting alerts

---

#### DigitalOcean

##### Compute & Droplets
- Droplet sizing: choosing between shared CPU (Basic) and dedicated CPU (General Purpose / CPU-Optimized / Memory-Optimized) tiers based on workload characteristics
- Droplet snapshots for point-in-time backups and golden image creation; restoring or spinning up new Droplets from snapshots for fast environment replication
- User data (cloud-init) scripts for bootstrapping: installing packages, configuring `systemd` services, pulling secrets from environment variables at first boot
- Reserved IPs for stable public endpoints that survive Droplet replacement; floating IPs for zero-downtime cutover between Droplets during maintenance

##### Kubernetes (DOKS)
- DigitalOcean Kubernetes Service: node pool management (standard vs autoscale pools), upgrading control plane and node pools with minimal downtime
- `doctl kubernetes cluster kubeconfig` for local `kubectl` access; integrating DOKS with DigitalOcean Container Registry (DOCR) via pre-configured imagePullSecrets
- Cluster autoscaler on DOKS: min/max node counts per pool, scale-to-zero for batch workloads, node pool separation for CPU-intensive vs memory-intensive services

##### Networking
- VPC Networks for isolating Droplets, Databases, and Kubernetes clusters within a private IP space; firewall rules scoped to tags for dynamic group-based access control
- DigitalOcean Load Balancer: HTTP/HTTPS with SSL termination (Let's Encrypt integration), backend health checks, sticky sessions, proxy protocol for preserving client IPs
- Spaces (S3-compatible object storage): `s3cmd` / `aws-cli` with custom endpoint (`https://<region>.digitaloceanspaces.com`), CDN edge caching for public assets, bucket policies for fine-grained access

##### Managed Databases & App Platform
- Managed PostgreSQL / MySQL / Redis / MongoDB clusters: automatic failover with standby nodes, read-only replicas for read scaling, connection pooling via PgBouncer (PostgreSQL)
- App Platform: deploying containerized apps or source repos directly (GitHub/GitLab integration), environment variable management, auto-deploy on push, built-in review apps for PRs
- DigitalOcean Functions (serverless): deploying Go, Python, Node.js functions with `doctl serverless`, trigger via HTTP or scheduled cron, shared package dependencies via `packages`

---

#### Vultr

##### Compute Instances
- Cloud Compute vs High Frequency vs Bare Metal: choosing instance class based on CPU contention tolerance, NVMe vs SSD storage needs, and dedicated core requirements
- Startup scripts for automated instance provisioning; SSH key injection at deployment time for keyless access; instance snapshots for environment versioning and rapid cloning
- Reserved IPs and Anycast IPs for stable endpoints; attaching/detaching IPs across instances for failover without DNS TTL delays

##### Networking & Storage
- VPC 2.0 for private inter-instance networking across regions; security groups for stateful firewall rules applied to instances or groups
- Vultr Block Storage: attaching additional NVMe volumes to instances, resizing volumes online, manual snapshot backups before risky operations
- Vultr Object Storage (S3-compatible): `s3cmd` / MinIO client for bucket operations, pre-signed URLs for temporary upload/download access, lifecycle rules for automated deletion

##### Kubernetes (VKE)
- Vultr Kubernetes Engine: node pool creation via the Vultr API or CLI (`vultr-cli`), kubeconfig download for `kubectl` access
- High-availability control plane option for production clusters; integrating VKE with Vultr Container Registry for private image pulls

---

#### Databases

##### PostgreSQL
- Schema design: normalisation through 3NF for transactional data, deliberate denormalisation (materialized views, JSONB columns) for read-heavy analytical queries
- Indexes: B-tree for equality/range, partial indexes (`WHERE is_deleted = false`) to reduce index size, GIN indexes for full-text search and JSONB containment queries, covering indexes (`INCLUDE`) to avoid heap fetches
- Query optimization: `EXPLAIN (ANALYZE, BUFFERS)` for identifying sequential scans and hash joins; rewriting correlated subqueries as `LATERAL JOIN` or `CTEs`; query plan pinning with `pg_hint_plan`
- Transactions and isolation levels: `READ COMMITTED` vs `REPEATABLE READ` vs `SERIALIZABLE`; advisory locks (`pg_advisory_xact_lock`) for application-level mutex patterns
- Connection pooling: PgBouncer in transaction mode for high-concurrency apps; sizing `max_connections` relative to available shared memory
- Logical replication: `CREATE PUBLICATION` / `CREATE SUBSCRIPTION` for selective table streaming to replicas or downstream consumers; slot monitoring to prevent WAL accumulation
- Extensions: `pgcrypto` for column-level encryption, `uuid-ossp` / `gen_random_uuid()` for UUIDs, `pg_trgm` for trigram similarity search, `TimescaleDB` for time-series workloads

##### MySQL
- Storage engines: InnoDB for ACID transactions with row-level locking vs MyISAM for read-heavy, non-transactional workloads; choosing engine per table
- Index strategy: composite index column order (left-prefix rule), covering indexes for `SELECT` columns, avoiding full-table scans with `FORCE INDEX` hints when optimizer makes poor choices
- EXPLAIN output: reading `type` column (const → ref → range → ALL), identifying `Using filesort` and `Using temporary` for optimization targets
- Replication: GTID-based replication for reliable failover and slave promotion; semi-synchronous replication for durability guarantees; `pt-table-checksum` for replica consistency verification
- `pt-online-schema-change` (Percona Toolkit) for zero-downtime schema migrations on large tables; `gh-ost` as an alternative using binlog-based approach
- Slow query log analysis with `pt-query-digest` for identifying top offenders; `performance_schema` for real-time query profiling

##### MongoDB
- Document model design: embedding vs referencing trade-offs — embed for one-to-few with co-access patterns, reference for one-to-many or independently queried data
- Aggregation pipeline: `$match` → `$group` → `$project` → `$lookup` for cross-collection joins; `$unwind` for flattening arrays; `$facet` for parallel multi-bucket aggregations
- Indexes: single-field, compound (field order matches query predicate + sort), multikey for array fields, text indexes for full-text search, TTL indexes for automatic document expiry
- Transactions (multi-document ACID since MongoDB 4.0): session-based `startTransaction` / `commitTransaction` with retry logic for transient write conflicts
- Replica sets: primary/secondary election with Raft-like consensus, read preference (`primaryPreferred`, `secondaryPreferred`, `nearest`) for balancing latency and consistency
- Change streams: `collection.watch()` for real-time event-driven processing of inserts/updates/deletes without polling; resumable with `resumeAfter` token after reconnection
- Schema validation with `$jsonSchema` in collection validators for enforcing required fields and type constraints without a rigid relational schema

##### DynamoDB
- Single-table design with composite keys (PK/SK) and GSI overloading for access pattern flexibility
- On-demand vs provisioned capacity: choosing based on traffic predictability; auto-scaling provisioned capacity with target utilization
- TTL for automatic item expiry; DynamoDB Streams → Lambda for change data capture and event-driven pipelines
- Conditional writes (`ConditionExpression`) for optimistic locking patterns; `TransactWriteItems` for multi-item ACID transactions (up to 100 items)
- GSI and LSI design: projecting only needed attributes to minimize read costs; sparse indexes via conditional attribute presence

##### Redis
- Data structures in practice: `String` for counters and cached values, `Hash` for session storage and user profiles, `Sorted Set` for leaderboards and priority queues, `List` for activity feeds and job queues, `Stream` for durable event logs with consumer groups
- Expiry strategies: `EXPIRE` / `PEXPIRE` for TTL-based eviction; `EXPIREAT` for calendar-aligned expiry; eviction policies (`allkeys-lru`, `volatile-lru`, `allkeys-lfu`) for memory-bounded caches
- Pub/Sub vs Streams: Pub/Sub for ephemeral fan-out (no persistence, no consumer tracking); Streams (`XADD` / `XREADGROUP`) for durable, consumer-group-based message processing with acknowledgement
- Lua scripting with `EVAL` for atomic multi-command operations (e.g., check-and-set, rate limiting with sliding window counters)
- Cluster mode: hash slot distribution across shards, `CLUSTER KEYSLOT` for verifying key placement, multi-key commands require `{}` hash tags to colocate keys on the same slot
- Sentinel for high availability in non-clustered deployments: automatic failover, `SENTINEL get-master-addr-by-name` for client reconnection after promotion

---

#### CI/CD

##### Jenkins
- Pipeline as Code with `Jenkinsfile` (Declarative and Scripted syntax): `pipeline { agent; stages; post }` structure for Declarative, `node {}` blocks with Groovy scripting for Scripted
- Shared Libraries (`@Library`): centralizing reusable pipeline steps in a Git repo (`vars/` for global steps, `src/` for helper classes); versioning libraries by branch/tag
- Agents and node labels: static agents with SSH or JNLP connection, dynamic agents via Kubernetes plugin (ephemeral pods per build), Docker plugin for containerized build environments
- Parallel stages: `parallel { stage('A') {}; stage('B') {} }` for fan-out builds (multi-platform, multi-region deploys); `failFast: true` for early termination on first failure
- Blue Ocean UI for visual pipeline visualization and PR-level build status; integrating with GitHub/GitLab webhooks for push- and PR-triggered pipelines
- Credentials management: `credentials()` binding in `withCredentials` block for secrets injection; avoiding secrets in console output with masked credentials
- Build triggers: SCM polling (`pollSCM`), webhook-driven builds, scheduled cron (`@daily`, `H 2 * * *`), upstream job dependencies with `build job:` step
- Post-build actions: `junit` for test result publishing, `archiveArtifacts` for build outputs, Slack/email notifications in `post { failure {} success {} }` blocks

##### GitHub Actions
- Workflow syntax: `on:` triggers (push, pull_request, schedule, workflow_dispatch, workflow_call), `jobs:` with `needs:` for sequential dependency chains, `if:` conditions for environment-gated deployments
- Reusable workflows (`workflow_call`) and composite actions for DRY pipeline logic; versioning shared actions with semantic tags (`uses: org/action@v2`)
- Matrix strategy: `strategy.matrix` with `include` / `exclude` for parallel cross-platform or multi-version builds; `fail-fast: false` to collect all matrix results before stopping
- Secrets and variables: `${{ secrets.* }}` for encrypted values, `${{ vars.* }}` for non-sensitive config, environment-scoped secrets for production isolation; `GITHUB_TOKEN` for API and package registry access
- Environments with deployment protection rules: required reviewers, wait timers, and environment-specific secrets for staging vs production gates
- Caching: `actions/cache` with cache keys built from lock file hashes (`hashFiles('**/Gemfile.lock')`); `actions/setup-*` built-in caching flags for language runtimes
- Artifact management: `actions/upload-artifact` / `actions/download-artifact` for passing build outputs between jobs; retention period configuration
- Self-hosted runners: runner groups for org-level access control, ephemeral runners for security isolation, labels for targeting specific hardware (GPU, ARM, high-memory)
- OpenID Connect (OIDC): keyless cloud authentication for AWS (`aws-actions/configure-aws-credentials`), GCP, and Azure — short-lived tokens instead of stored cloud credentials

---

#### Observability

##### New Relic
- APM agent instrumentation: Ruby (`newrelic_rpm` gem), Python (`newrelic` package), Go (`newrelic/go-agent`) for automatic transaction tracing, external service calls, and database query performance
- Custom instrumentation: `NewRelic::Agent.record_metric` for business-level metrics, `NewRelic::Agent.notice_error` for enriching error events with custom attributes
- Distributed tracing: W3C Trace Context propagation across microservices, cross-account trace linking, trace waterfall for identifying latency in multi-hop request flows
- NRQL (New Relic Query Language): `SELECT`, `WHERE`, `FACET`, `TIMESERIES`, `EXTRAPOLATE` for building dashboards; `BASELINE` alerts for anomaly detection without fixed thresholds
- Alerts and notification channels: NRQL-based alert conditions, signal loss detection for missing data gaps, multi-condition policies, PagerDuty / Slack integrations
- Infrastructure monitoring: host-level CPU/memory/disk/network via the Infrastructure agent; process monitoring; cloud integrations (AWS CloudWatch metrics pulled via polling or Metric Streams)
- Browser and synthetics: Real User Monitoring (RUM) for Core Web Vitals, scripted browser monitors for critical user journey uptime checks

##### Datadog
- Unified agent: single `datadog-agent` collecting metrics, logs, and traces; DogStatsD for custom metric submission from application code (`increment`, `gauge`, `histogram`, `distribution`)
- APM and Distributed Tracing: `dd-trace` libraries for auto-instrumentation of web frameworks and DB clients; Continuous Profiler for CPU/memory flame graphs in production without overhead
- Log Management: structured log ingestion with JSON pipeline processors; log-to-metric conversions for counting error patterns; Log Archives to S3/GCS for long-term retention; correlation between logs and APM traces via `dd.trace_id` injection
- Dashboards and Notebooks: `@` annotations on graphs for event overlays (deployments, incidents); template variables for multi-service/multi-env boards; Notebooks for incident post-mortems with embedded live graphs
- Monitors: threshold, change, anomaly (ML-based), forecast, and outlier monitor types; composite monitors combining multiple signals; downtime scheduling for planned maintenance
- Synthetic Monitoring: API tests for endpoint health and response validation; browser tests with recorded user journeys; CI visibility integration for blocking deploys on synthetic failures
- Service Catalog and Service Map: upstream/downstream dependency visualization, SLO tracking (error budget burn rate alerts), ownership metadata for on-call routing

---

## Management

### Agile / Scrum

#### Sprint Execution
- Facilitating Sprint Planning: helping the team decompose Product Backlog Items into tasks, defining clear Sprint Goals that provide focus and enable "Done" decisions
- Running effective Daily Scrums: keeping it under 15 min, focused on progress toward Sprint Goal rather than status reporting, surfacing blockers early
- Sprint Review as a feedback loop: demonstrating working Increment to stakeholders, capturing feedback directly into Product Backlog refinement
- Sprint Retrospective techniques: Start/Stop/Continue, 4Ls (Liked, Learned, Lacked, Longed For), sailboat retro, dot voting for action item prioritization
- Tracking improvement actions across Sprints to ensure retro outcomes don't get forgotten

#### Product Backlog Management
- Writing user stories with acceptance criteria: "As a [role], I want [capability], so that [benefit]" with specific, testable conditions
- Backlog refinement: breaking epics into vertical slices that deliver end-to-end user value, INVEST criteria for well-formed stories
- Estimation: Planning Poker with Fibonacci sequence, relative sizing with T-shirt sizes, using reference stories as calibration points
- Ordering by value/risk/dependency: prioritizing high-value, high-uncertainty items early for fast learning
- Definition of Ready: ensuring items entering Sprint Planning are small enough, understood, and have clear acceptance criteria

#### Scrum Mastery
- Detecting and addressing team dysfunctions: lack of trust, fear of conflict, avoidance of accountability, inattention to results
- Coaching Product Owners on effective backlog ordering: maximizing value delivery, managing stakeholder expectations, saying "no" to low-priority requests
- Removing organizational impediments: escalating cross-team blockers, negotiating for dedicated team capacity, shielding teams from mid-Sprint scope changes
- Evidence-Based Management: measuring Current Value (revenue, satisfaction), Time-to-Market (release frequency, cycle time), Ability to Innovate (technical debt ratio, defect trends), Unrealized Value (market share, customer requests backlog)
- Fostering self-management: moving from "Scrum Master assigns tasks" to team members pulling work and collectively owning Sprint commitments

#### Agile Leadership
- Creating psychological safety: enabling team members to raise risks, admit mistakes, and challenge decisions without fear
- Decentralized decision-making: empowering teams to make technical and process decisions within guardrails, reserving only strategic decisions for leadership
- Connecting team-level outcomes to business goals: OKRs (Objectives and Key Results) aligned across product, engineering, and business
- Budgeting for agile: moving from project-based funding to persistent team funding with value-stream alignment

#### Kanban Integration
- Visualizing Sprint work on a Kanban board: columns mapped to workflow stages (To Do → In Dev → In Review → QA → Done), WIP limits per column
- Measuring cycle time (item start → item done) and lead time (item created → item done) to identify bottlenecks
- Cumulative Flow Diagrams: reading band widths for WIP, band slopes for throughput, narrowing bands for bottleneck detection
- Probabilistic forecasting with Monte Carlo: "85% chance of completing 20 items by Sprint end" based on historical throughput data
- Using Service Level Expectations (SLEs): "85% of items complete within 5 days" for setting and communicating delivery predictability

#### Scaled Scrum & Scaling Frameworks

##### Nexus Framework
- Nexus Integration Team: composed of Scrum Masters and rotating developers from each team, responsible for coaching integration practices and resolving cross-team technical conflicts
- Nexus Sprint Planning: two parts — all teams align on a shared Sprint Goal and identify inter-team dependencies, then individual teams plan their Sprint Backlogs with integration points explicit
- Cross-team dependency management: dependency boards mapping team-to-team handoffs, minimizing dependencies by aligning team boundaries to product architecture (e.g., feature teams over component teams)
- Integrated Increment: all 3–9 Scrum Teams produce a single combined, tested, releasable Increment every Sprint — requires shared CI pipeline, automated integration tests, and a unified Definition of Done
- Nexus Sprint Retrospective: two phases — representatives from all teams identify cross-team improvement areas first, then individual teams retrospect on their own process

##### Scrum of Scrums
- Ambassador model: one representative per Scrum Team attends Scrum of Scrums, reporting blockers, inter-team dependencies, and integration risks
- Meeting cadence: typically 2–3 times per week (not daily) to balance coordination overhead with execution time
- Focus on three questions per team: What did our team complete since last SoS? What will we complete before next SoS? What cross-team blockers need escalation?
- Escalation path: Scrum of Scrums surfaces issues; a Chief Scrum Master or RTE owns resolution and tracks follow-up across teams
- Differs from Nexus in that it adds no new artifacts or roles — it's a lightweight overlay on existing Scrum without framework-level changes

##### LeSS (Large-Scale Scrum)
- Single Product Owner managing one Product Backlog across all teams — avoids backlog fragmentation and ensures unified prioritization
- Feature teams: each team can work on any part of the codebase, reducing handoffs and enabling end-to-end delivery of customer features
- Sprint coordination: teams select items from the shared backlog during a joint Sprint Planning Part 1, then plan independently in Part 2
- Overall Sprint Review: all teams demo to stakeholders together, providing a whole-product view instead of per-team showcases
- Overall Retrospective: cross-team systemic issues are addressed by team representatives + management, focusing on organizational impediments
- LeSS Huge (8+ teams): introduces Requirement Areas — each area has an Area Product Owner and a subset of teams, while the overall Product Owner coordinates across areas

##### SAFe (Scaled Agile Framework)
- Agile Release Train (ART): 5–12 teams working on a shared cadence (typically 8–12 week Program Increment), synchronized through PI Planning
- PI Planning execution: 2-day face-to-face event where teams break features into stories, identify cross-team dependencies on a program board, negotiate scope with Product Management, and commit to PI Objectives with business value scores
- Release Train Engineer (RTE): facilitates ART-level events, escalates program-level impediments, tracks program predictability via PI Objective achievement rates
- Inspect & Adapt (I&A): ART-level retrospective at the end of each PI — quantitative review of PI metrics + problem-solving workshop using root cause analysis (e.g., fishbone diagrams)
- Innovation and Planning (IP) iteration: dedicated Sprint within each PI for hackathons, tech debt reduction, PI Planning preparation, and cross-team knowledge sharing
- Continuous Delivery Pipeline: Continuous Exploration (hypotheses, MVPs) → Continuous Integration (automated builds, tests) → Continuous Deployment (feature flags, canary releases) → Release on Demand
- Portfolio Kanban: Epics flow through Funnel → Reviewing → Analyzing → Portfolio Backlog → Implementing → Done, with Lean Business Cases evaluated at each stage gate

#### Technical Agile Practices
- Test-Driven Development: Red → Green → Refactor cycle; writing the failing test first forces clear API design before implementation
- Behaviour-Driven Development: Gherkin (Given/When/Then) scenarios as living documentation, bridging business language and automated tests
- Continuous Integration: every commit triggers build + full test suite; broken builds are fixed immediately ("stop the line"); trunk-based development with short-lived feature branches
- Continuous Delivery: every green build is a release candidate; deployment pipeline stages (build → unit test → integration test → staging → canary → production)
- Refactoring discipline: extract method, rename, introduce parameter object, replace conditional with polymorphism — applied continuously, not in dedicated "refactoring Sprints"
- Pair programming: driver/navigator rotation for knowledge sharing, complex problem solving, and real-time code review; mob programming for high-stakes design decisions
- Emergent architecture: starting simple and evolving design through refactoring as requirements clarify, rather than big upfront design; using Architecture Decision Records (ADRs) to document key trade-offs
- Extreme Programming (XP): the 12 XP practices as an integrated system — planning game for collaborative release and iteration planning; small releases delivering working software in short cycles; system metaphor providing a shared architectural vocabulary; simple design with the fewest classes and methods needed today; collective code ownership so any developer can improve any code at any time; coding standards as a prerequisite for collective ownership; on-site customer (or proxy) for real-time feedback and priority decisions; 40-hour week to sustain a predictable, sustainable pace without accumulating fatigue debt; XP values (communication, simplicity, feedback, courage, respect) as the foundation for the practices
