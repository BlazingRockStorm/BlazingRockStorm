# Extreme Programming (XP) Reference

PSD I knowledge. Apply when the team wants to adopt XP practices, improve engineering discipline, or combine XP with Scrum. XP and Scrum are highly complementary — Scrum provides the management framework; XP provides the engineering practices.

## Core Idea

XP is a software development methodology built on five values: **Communication**, **Simplicity**, **Feedback**, **Courage**, and **Respect**. It produces high-quality software through short iterations, continuous feedback, and disciplined technical practices.

XP is not a process to be followed — it is a set of practices that reinforce each other. Adopting one practice makes the others more valuable.

---

## The Five Values

| Value | In Practice |
|---|---|
| **Communication** | Pair programming, on-site customer, stand-ups, shared codebase — no silos |
| **Simplicity** | Build only what is needed today; YAGNI (You Aren't Gonna Need It) |
| **Feedback** | TDD gives seconds-fast feedback; CI gives minutes-fast; customer reviews give days-fast |
| **Courage** | Refactor ruthlessly; discard code that no longer serves; raise issues early |
| **Respect** | No code ownership beyond the team; no blame; everyone's contribution matters |

---

## The Twelve Practices

### Planning Practices

**The Planning Game**
- Customers write User Stories on cards; Developers estimate each story
- Customers prioritise by value; Developers plan iterations by capacity
- No long-term fixed plan — the next iteration is planned from the current backlog
- Equivalent to: Sprint Planning + Backlog Refinement in Scrum

**Small Releases**
- Release working software as frequently as possible — ideally after every iteration
- Each release should deliver tangible customer value
- Forces small, integrable stories; prevents big-bang integration risk

**Customer On-Site**
- A real customer representative is embedded with the team
- They answer questions immediately, write acceptance tests, and prioritise continuously
- Equivalent to: Product Owner in Scrum — but XP expects even more availability

### Team Practices

**Whole Team**
- Cross-functional team includes developers, testers, the customer, and any other role needed
- No hand-offs to separate QA or BA teams — everyone is responsible for quality

**Sustainable Pace**
- Work no more than 40 hours per week
- Overtime one week predicts lower productivity the next — it is a debt, not a gift
- Courage to say "no" to unrealistic deadlines is an XP value in action

### Development Practices

**Test-Driven Development (TDD)**
Red → Green → Refactor cycle:
1. Write a failing test for the smallest possible unit of behaviour
2. Write the minimum code to make the test pass (Green)
3. Refactor — improve the design without changing behaviour

```
// Red
test('adds two numbers', () => {
  expect(add(2, 3)).toBe(5)  // add doesn't exist yet — test fails
})

// Green
function add(a, b) { return a + b }

// Refactor if needed — code is already clean here
```

Benefits beyond just catching bugs:
- Tests are the living specification of behaviour
- Enables fearless refactoring — test suite is a safety net
- Forces small, testable units of design

**Acceptance Test-Driven Development (ATDD)**
- Customers (or the team with the customer) write acceptance tests before development begins
- Defines "done" for a story at the behaviour level
- Tools: Cucumber, FitNesse, SpecFlow

**Pair Programming**
- Two developers share one workstation: one **Driver** types, one **Navigator** thinks ahead
- Switch roles frequently (every 25–30 minutes)
- Rotate pairs daily — spreads knowledge, prevents silos, eliminates the bus factor
- Not a cost-doubling exercise: pairs produce fewer defects, review code continuously, and transfer knowledge in real time

Common objections and responses:
| Objection | Response |
|---|---|
| "It's twice as expensive" | Defect rates drop 15–50%; code review is built-in; knowledge transfer is instant |
| "Our developers don't want to pair" | Start with new joiners + experienced devs; demonstrate value first |
| "We work remotely" | Use screen sharing + video call; works well with VS Code Live Share |

**Continuous Integration (CI)**
- Every developer integrates their code into the shared trunk at least once per day
- Automated build and test suite runs on every integration
- A broken build is the team's highest priority — fix or revert within 10 minutes
- No long-lived feature branches — they delay integration and create merge risk

**Collective Code Ownership**
- Any developer can change any part of the codebase at any time
- No "that's John's code — ask him"
- Requires: good test coverage, coding standards, and a culture of refactoring

**Coding Standards**
- Team agrees on a consistent style and enforces it automatically (linter, formatter)
- Code should look like it was written by one person
- Standards enable collective ownership — you can read and change anyone's code

**Simple Design**
Four rules (Kent Beck):
1. Passes all the tests
2. Reveals intention — code is readable without comments
3. No duplication (DRY)
4. Fewest elements — no speculative abstraction, no extra classes/methods

**Refactoring**
- Continuously improve the design of existing code without changing its behaviour
- Not a separate phase — refactor in the Red/Green/Refactor cycle, every day
- A codebase without refactoring accumulates design debt that compounds over time
- Courage to refactor comes from test coverage

**Metaphor**
- The team agrees on a simple, shared story that describes how the system works
- Provides a common vocabulary for naming classes, methods, and concepts
- Example: "the system is like an assembly line — each order moves through stations"
- Often replaced in practice by Domain-Driven Design (DDD) ubiquitous language

---

## XP + Scrum (Combined)

XP and Scrum are commonly used together — Scrum for the framework, XP for the engineering practices. This is the most common "Scrum with engineering discipline" configuration.

| Scrum provides | XP provides |
|---|---|
| Sprint cadence and ceremonies | TDD, pair programming, refactoring |
| Product Owner and Scrum Master roles | Customer on-site (maps to PO) |
| Definition of Done | Acceptance tests, CI gate |
| Sprint Retrospective | Sustainable pace, continuous improvement |
| Sprint Backlog | Planning Game (story cards + iteration planning) |

### Introducing XP Practices into a Scrum Team

Start with the practices that give the most immediate feedback:

1. **CI first** — automated build on every commit; team experiences fast integration feedback
2. **TDD next** — write tests before code; start with new features, not existing code
3. **Pair programming** — introduce on complex or risky stories first; don't mandate across the board immediately
4. **Collective ownership** — follows naturally from pairing and CI
5. **Simple design + refactoring** — enabled by test coverage from TDD

---

## XP Failure Modes

| Anti-Pattern | Root Cause | Fix |
|---|---|---|
| TDD abandoned under deadline pressure | Team sees tests as overhead, not design tool | Measure defect rate before/after; reframe tests as specification |
| Pairing becomes code review | Navigator is passive; no switching | Timebox roles strictly; use a timer |
| CI but no CD | Build passes but deployment is manual and infrequent | Automate deployment; treat every green build as releasable |
| "Simple design" used to justify no design | Misreading YAGNI as "don't think ahead" | Simple design still requires thought; it means no speculative complexity |
| Stories too large for one iteration | Planning Game not breaking stories down | Apply INVEST; spike to reduce uncertainty before pulling into an iteration |
