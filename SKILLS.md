# Skills

Practical skills reference. Intended for AI agents when designing or working on systems, and as a public profile for collaborators.

---

## Ruby

### Object Model & Metaprogramming
- Eigenclass (singleton class) manipulation: defining per-object methods, `class << self` for DSL-style APIs
- Dynamic dispatch with `send` / `public_send`, safe navigation (`&.`), and `respond_to?` guards
- `method_missing` + `respond_to_missing?` for proxy objects and decorator patterns
- `define_method` for generating families of methods at class load time (e.g., attribute accessors, scope builders)
- Module hooks: `included`, `extended`, `prepended`, `inherited`, `method_added` for framework-style behaviour injection
- `prepend` for clean method wrapping without alias chaining (e.g., instrumentation, logging, caching layers)
- `Refinements` for safely scoping monkey-patches to specific files or modules
- `TracePoint` for runtime introspection: tracing method calls, line execution, class definitions

### Blocks, Procs & Closures
- Yielding with explicit `&block` capture vs implicit `yield` — choosing based on whether the block needs to be stored or forwarded
- `Proc.new` vs `lambda` vs `->`: differences in arity checking and `return` semantics
- Currying and partial application with `Proc#curry` for building composable filters and validators
- Closures over local bindings for building callback chains and deferred execution

### Enumerable & Collection Patterns
- `Enumerable` protocol: implementing `each` + `include Enumerable` to get `map`, `select`, `reduce`, `flat_map`, `group_by`, `tally`, `filter_map` for free
- `Enumerator::Lazy` for memory-efficient processing of large or infinite sequences (e.g., streaming CSV rows, paginated API results)
- `each_with_object` for accumulator patterns without mutable outer state
- Custom `Enumerator.new` for wrapping external iterators (e.g., database cursor, file lines, API pagination)

### Concurrency & Parallelism
- `Ractor` (Ruby 3+) for true parallel execution without shared mutable state — message-passing between actors
- `Fiber` and `Fiber.schedule` for cooperative async I/O (e.g., non-blocking HTTP calls, async database queries)
- `Thread` + `Mutex` + `ConditionVariable` for classic shared-state concurrency; `Queue` / `SizedQueue` for producer-consumer patterns
- `Thread::Pool` patterns for bounding concurrency on batch jobs (e.g., parallel image processing, bulk API calls)
- GVL (Global VM Lock) awareness: CPU-bound work stays serialized in CRuby threads; use `Ractor` or fork-based parallelism for CPU tasks

### Error Handling & Resilience
- `retry` with exponential backoff in `rescue` blocks for transient failures (network timeouts, rate limits)
- Custom exception hierarchies: domain-specific base error class with typed subclasses for structured `rescue` chains
- `ensure` for resource cleanup (file handles, DB connections, temp files) regardless of exception path
- `throw` / `catch` for non-local jumps in deeply nested iterations (e.g., early exit from search)

### Testing
- RSpec: `describe` / `context` / `it` structure, `let` / `let!` for lazy/eager fixtures, `subject` for DRY specs
- Test doubles: `instance_double` with verified doubles, `allow` / `expect` message expectations, `have_received` for spies
- Shared examples (`shared_examples_for`) and shared contexts for reducing duplication across spec files
- FactoryBot: `factory`, `trait`, `transient` attributes, `sequence` for unique values, `association` for nested records
- Minitest: `assert_*` / `refute_*` style, `setup` / `teardown` hooks, `Minitest::Mock` for lightweight mocking
- SimpleCov for line and branch coverage reporting; integrating coverage gates into CI

### Rails-Specific
- ActiveRecord: scopes, eager loading (`includes` / `preload` / `eager_load`), N+1 detection with Bullet, counter caches, polymorphic associations, STI vs delegated types
- ActiveJob + Sidekiq: background job processing, retry strategies, dead-letter queues, unique job deduplication, cron-scheduled recurring jobs
- ActionCable: real-time WebSocket channels, broadcasting patterns, connection authentication
- Rails engines for modular monolith architecture: isolating bounded contexts into mountable engines with their own routes, models, and migrations
- Rack middleware: writing custom middleware for request logging, rate limiting, tenant detection in multi-tenant apps
- Database migrations: zero-downtime schema changes (add column with default, backfill, then add constraint), `strong_migrations` gem for safety checks
- Caching: Russian doll fragment caching, low-level `Rails.cache.fetch` with expiry, cache busting with versioned keys

### Gems & Tooling
- Bundler: `Gemfile` groups, `bundle exec` isolation, `Gemfile.lock` for reproducible builds, private gem server configuration
- Rubocop for style enforcement; custom `.rubocop.yml` with project-specific cops and exclusions
- Pry / IRB: runtime debugging with `binding.pry`, object introspection with `ls`, `show-method`, `cd`
- Sorbet / RBS for gradual type checking: `sig` annotations, `T.let`, `T.nilable`, typed interfaces for critical paths

---

## AWS

### Networking & VPC Design
- Multi-AZ VPC layouts: public/private/isolated subnets per AZ, NAT Gateway placement for egress, VPC endpoints (Gateway for S3/DynamoDB, Interface for other services) to avoid NAT costs
- Security group layering: separate SGs for ALB → app → database tiers, referencing SG IDs instead of CIDR blocks for intra-VPC rules
- Transit Gateway for hub-and-spoke connectivity across multiple VPCs and accounts; Route table associations for traffic segmentation
- VPC Flow Logs → CloudWatch Logs Insights for troubleshooting connectivity issues (rejected packets, unexpected traffic paths)
- PrivateLink for exposing internal services to consumers in other VPCs/accounts without internet traversal

### Compute
- EC2 Auto Scaling: target tracking policies (CPU, request count per target), step scaling for bursty workloads, warm pools for faster scale-out, mixed instances with Spot for cost savings
- Launch templates with user data scripts for bootstrapping (install agents, pull config from SSM Parameter Store, join ECS cluster)
- Graviton (ARM) instances for better price-performance on web servers, containerized workloads, and build pipelines
- Spot Instances: capacity-optimized allocation strategy, Spot interruption handling via EC2 metadata + 2-minute warning, Spot Fleet diversification

### Containers
- ECS on Fargate: task definition sizing (CPU/memory), service auto-scaling (target tracking on CPU or custom CloudWatch metrics), service discovery via Cloud Map
- ECS deployment strategies: rolling update with `minimumHealthyPercent` / `maximumPercent`, blue/green via CodeDeploy with ALB target group switching, circuit breaker for automatic rollback on failed deployments
- EKS: managed node groups with Cluster Autoscaler or Karpenter for right-sizing, Fargate profiles for isolating batch workloads, IRSA (IAM Roles for Service Accounts) for pod-level permissions
- ECR: image lifecycle policies for cleaning untagged images, cross-region replication, image scanning on push with Inspector

### Serverless
- Lambda: function sizing (memory/CPU trade-off), cold start mitigation (provisioned concurrency, SnapStart for Java), layers for shared dependencies, Lambda extensions for observability
- Event-driven patterns: S3 → Lambda for file processing, SQS → Lambda with batch window and partial failure reporting (`ReportBatchItemFailures`), EventBridge rules for scheduled or cross-account events
- Step Functions: Express vs Standard workflows, `Map` state for parallel fan-out, `Choice` state for branching, error handling with `Retry` / `Catch`, callback patterns with task tokens
- API Gateway: REST APIs with Lambda proxy integration, request validation via JSON Schema models, Cognito/Lambda authorizers, usage plans with API keys for rate limiting per consumer

### Storage
- S3: lifecycle policies transitioning objects through Standard → IA → Glacier IR → Glacier Deep Archive based on access patterns; S3 Intelligent-Tiering for unpredictable access
- S3 event-driven pipelines: PUT event → SQS → Lambda for async processing; S3 Batch Operations for bulk tagging, copying, or invoking Lambda on millions of objects
- Cross-region replication with S3 Replication Rules for disaster recovery; same-region replication for log aggregation across accounts
- EBS: gp3 with independently tunable IOPS/throughput for database volumes, io2 Block Express for latency-sensitive workloads, EBS snapshots with DLM (Data Lifecycle Manager) for automated backup rotation
- EFS: bursting vs provisioned throughput modes, EFS Access Points for application-specific mount paths with POSIX user mapping, EFS-to-EFS cross-region replication

### Databases
- RDS PostgreSQL: Multi-AZ for automatic failover, read replicas for read scaling, Performance Insights for identifying slow queries, pg_stat_statements analysis, parameter group tuning (shared_buffers, work_mem, effective_cache_size)
- Aurora PostgreSQL: global databases for cross-region DR with <1s replication lag, Aurora Serverless v2 for variable workloads, cloning for instant non-production environments
- DynamoDB: single-table design with composite keys (PK/SK) and GSI overloading for access pattern flexibility, on-demand vs provisioned capacity, TTL for automatic item expiry, DynamoDB Streams → Lambda for change data capture
- ElastiCache Redis: cluster mode for horizontal sharding, read replicas for read-heavy workloads, Redis Streams for lightweight event streaming, cache-aside pattern with TTL-based invalidation

### CI/CD & Infrastructure as Code
- CodePipeline: source (CodeCommit/GitHub) → build (CodeBuild) → deploy (CodeDeploy/ECS/CloudFormation) with manual approval gates for production
- CodeBuild: buildspec.yml with phases (install, pre_build, build, post_build), caching (S3/local) for dependency speed-up, custom build images for specialized toolchains
- CodeDeploy: blue/green deployments for EC2/ECS with traffic shifting (canary 10% → 100%, linear 10% every 5 min), automatic rollback on CloudWatch alarm triggers
- CloudFormation: nested stacks for reusable components, cross-stack references with Exports/Imports, custom resources (Lambda-backed) for unsupported resources, drift detection for manual change auditing
- CDK: TypeScript/Python constructs for type-safe IaC, L2 constructs for sensible defaults, `cdk diff` for change previewing, `Aspects` for enforcing tagging and compliance policies across stacks
- SAM: `template.yaml` for Lambda + API Gateway + DynamoDB local development, `sam local invoke` / `sam local start-api` for local testing

### Monitoring, Logging & Observability
- CloudWatch: custom metrics with `put-metric-data`, composite alarms combining multiple metric conditions, Logs Insights queries for pattern extraction from application logs, metric filters for turning log patterns into alarms
- X-Ray: instrumenting Lambda, ECS, and API Gateway for distributed tracing, X-Ray daemon sidecar in ECS tasks, service map for visualizing latency bottlenecks across microservices
- CloudTrail: organization trail for multi-account API auditing, CloudTrail Lake for SQL-based querying of events, integration with EventBridge for real-time alerting on sensitive API calls (e.g., IAM policy changes)

### Security & Access Control
- IAM: least-privilege policies using `Condition` keys (e.g., `aws:SourceVpc`, `aws:PrincipalOrgID`), permission boundaries for delegated admin, SCP guardrails at the OU level in AWS Organizations
- Secrets Manager: automatic rotation with Lambda rotation functions for RDS credentials, cross-account secret sharing via resource policies
- KMS: customer-managed keys with key policies and grants, envelope encryption for application-level data protection, automatic key rotation
- WAF: rate-based rules for DDoS mitigation, managed rule groups (AWS, marketplace) for OWASP Top 10, custom rules for geo-blocking or IP reputation filtering

### Cost Optimization
- Right-sizing with Compute Optimizer recommendations for EC2, Lambda, and EBS
- Savings Plans (Compute/EC2 Instance) and Reserved Instances for predictable baseline workloads
- Spot for fault-tolerant batch processing, CI/CD build agents, and dev/test environments
- S3 storage class analysis and Intelligent-Tiering for reducing storage costs without manual lifecycle management
- Cost allocation tags + Cost Explorer for per-team/per-service cost attribution and budgeting alerts

---

## Agile / Scrum

### Sprint Execution
- Facilitating Sprint Planning: helping the team decompose Product Backlog Items into tasks, defining clear Sprint Goals that provide focus and enable "Done" decisions
- Running effective Daily Scrums: keeping it under 15 min, focused on progress toward Sprint Goal rather than status reporting, surfacing blockers early
- Sprint Review as a feedback loop: demonstrating working Increment to stakeholders, capturing feedback directly into Product Backlog refinement
- Sprint Retrospective techniques: Start/Stop/Continue, 4Ls (Liked, Learned, Lacked, Longed For), sailboat retro, dot voting for action item prioritization
- Tracking improvement actions across Sprints to ensure retro outcomes don't get forgotten

### Product Backlog Management
- Writing user stories with acceptance criteria: "As a [role], I want [capability], so that [benefit]" with specific, testable conditions
- Backlog refinement: breaking epics into vertical slices that deliver end-to-end user value, INVEST criteria for well-formed stories
- Estimation: Planning Poker with Fibonacci sequence, relative sizing with T-shirt sizes, using reference stories as calibration points
- Ordering by value/risk/dependency: prioritizing high-value, high-uncertainty items early for fast learning
- Definition of Ready: ensuring items entering Sprint Planning are small enough, understood, and have clear acceptance criteria

### Scrum Mastery
- Detecting and addressing team dysfunctions: lack of trust, fear of conflict, avoidance of accountability, inattention to results
- Coaching Product Owners on effective backlog ordering: maximizing value delivery, managing stakeholder expectations, saying "no" to low-priority requests
- Removing organizational impediments: escalating cross-team blockers, negotiating for dedicated team capacity, shielding teams from mid-Sprint scope changes
- Evidence-Based Management: measuring Current Value (revenue, satisfaction), Time-to-Market (release frequency, cycle time), Ability to Innovate (technical debt ratio, defect trends), Unrealized Value (market share, customer requests backlog)
- Fostering self-management: moving from "Scrum Master assigns tasks" to team members pulling work and collectively owning Sprint commitments

### Agile Leadership
- Creating psychological safety: enabling team members to raise risks, admit mistakes, and challenge decisions without fear
- Decentralized decision-making: empowering teams to make technical and process decisions within guardrails, reserving only strategic decisions for leadership
- Connecting team-level outcomes to business goals: OKRs (Objectives and Key Results) aligned across product, engineering, and business
- Budgeting for agile: moving from project-based funding to persistent team funding with value-stream alignment

### Kanban Integration
- Visualizing Sprint work on a Kanban board: columns mapped to workflow stages (To Do → In Dev → In Review → QA → Done), WIP limits per column
- Measuring cycle time (item start → item done) and lead time (item created → item done) to identify bottlenecks
- Cumulative Flow Diagrams: reading band widths for WIP, band slopes for throughput, narrowing bands for bottleneck detection
- Probabilistic forecasting with Monte Carlo: "85% chance of completing 20 items by Sprint end" based on historical throughput data
- Using Service Level Expectations (SLEs): "85% of items complete within 5 days" for setting and communicating delivery predictability

### Scaled Scrum & Scaling Frameworks

#### Nexus Framework
- Nexus Integration Team: composed of Scrum Masters and rotating developers from each team, responsible for coaching integration practices and resolving cross-team technical conflicts
- Nexus Sprint Planning: two parts — all teams align on a shared Sprint Goal and identify inter-team dependencies, then individual teams plan their Sprint Backlogs with integration points explicit
- Cross-team dependency management: dependency boards mapping team-to-team handoffs, minimizing dependencies by aligning team boundaries to product architecture (e.g., feature teams over component teams)
- Integrated Increment: all 3–9 Scrum Teams produce a single combined, tested, releasable Increment every Sprint — requires shared CI pipeline, automated integration tests, and a unified Definition of Done
- Nexus Sprint Retrospective: two phases — representatives from all teams identify cross-team improvement areas first, then individual teams retrospect on their own process

#### Scrum of Scrums
- Ambassador model: one representative per Scrum Team attends Scrum of Scrums, reporting blockers, inter-team dependencies, and integration risks
- Meeting cadence: typically 2–3 times per week (not daily) to balance coordination overhead with execution time
- Focus on three questions per team: What did our team complete since last SoS? What will we complete before next SoS? What cross-team blockers need escalation?
- Escalation path: Scrum of Scrums surfaces issues; a Chief Scrum Master or RTE owns resolution and tracks follow-up across teams
- Differs from Nexus in that it adds no new artifacts or roles — it's a lightweight overlay on existing Scrum without framework-level changes

#### LeSS (Large-Scale Scrum)
- Single Product Owner managing one Product Backlog across all teams — avoids backlog fragmentation and ensures unified prioritization
- Feature teams: each team can work on any part of the codebase, reducing handoffs and enabling end-to-end delivery of customer features
- Sprint coordination: teams select items from the shared backlog during a joint Sprint Planning Part 1, then plan independently in Part 2
- Overall Sprint Review: all teams demo to stakeholders together, providing a whole-product view instead of per-team showcases
- Overall Retrospective: cross-team systemic issues are addressed by team representatives + management, focusing on organizational impediments
- LeSS Huge (8+ teams): introduces Requirement Areas — each area has an Area Product Owner and a subset of teams, while the overall Product Owner coordinates across areas

#### SAFe (Scaled Agile Framework)
- Agile Release Train (ART): 5–12 teams working on a shared cadence (typically 8–12 week Program Increment), synchronized through PI Planning
- PI Planning execution: 2-day face-to-face event where teams break features into stories, identify cross-team dependencies on a program board, negotiate scope with Product Management, and commit to PI Objectives with business value scores
- Release Train Engineer (RTE): facilitates ART-level events, escalates program-level impediments, tracks program predictability via PI Objective achievement rates
- Inspect & Adapt (I&A): ART-level retrospective at the end of each PI — quantitative review of PI metrics + problem-solving workshop using root cause analysis (e.g., fishbone diagrams)
- Innovation and Planning (IP) iteration: dedicated Sprint within each PI for hackathons, tech debt reduction, PI Planning preparation, and cross-team knowledge sharing
- Continuous Delivery Pipeline: Continuous Exploration (hypotheses, MVPs) → Continuous Integration (automated builds, tests) → Continuous Deployment (feature flags, canary releases) → Release on Demand
- Portfolio Kanban: Epics flow through Funnel → Reviewing → Analyzing → Portfolio Backlog → Implementing → Done, with Lean Business Cases evaluated at each stage gate

### Technical Agile Practices
- Test-Driven Development: Red → Green → Refactor cycle; writing the failing test first forces clear API design before implementation
- Behaviour-Driven Development: Gherkin (Given/When/Then) scenarios as living documentation, bridging business language and automated tests
- Continuous Integration: every commit triggers build + full test suite; broken builds are fixed immediately ("stop the line"); trunk-based development with short-lived feature branches
- Continuous Delivery: every green build is a release candidate; deployment pipeline stages (build → unit test → integration test → staging → canary → production)
- Refactoring discipline: extract method, rename, introduce parameter object, replace conditional with polymorphism — applied continuously, not in dedicated "refactoring Sprints"
- Pair programming: driver/navigator rotation for knowledge sharing, complex problem solving, and real-time code review; mob programming for high-stakes design decisions
- Emergent architecture: starting simple and evolving design through refactoring as requirements clarify, rather than big upfront design; using Architecture Decision Records (ADRs) to document key trade-offs
