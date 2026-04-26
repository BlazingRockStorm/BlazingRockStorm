# Scaled Scrum Reference

SPS (Nexus) knowledge. Covers Nexus, Scrum of Scrums, LeSS, and SAFe for multi-team coordination, cross-team dependency management, and organisational scaling. For leadership and EBM, consult `references/Evidence Based Management Guide 2024.pdf`.

## Scaling Framework Comparison

| Framework | Best for | Teams | Complexity |
|---|---|---|---|
| **Scrum of Scrums** | Lightweight coordination, low overhead | 2–5 teams | Low |
| **Nexus** | One product, 3–9 teams, Scrum-native scaling | 3–9 teams | Medium |
| **LeSS** | Org-level Scrum adoption, single or multiple products | 2–8 teams (LeSS) / 8+ (LeSS Huge) | Medium |
| **SAFe** | Large enterprise, multiple value streams, top-down rollout | 50–125+ people | High |

When advising on scaling, diagnose the org's size, maturity, and appetite for change before recommending a framework. Nexus is the default recommendation for Scrum practitioners — it adds the least overhead and stays closest to the Scrum Guide.

---

## Nexus Framework (SPS)

Nexus scales Scrum for 3–9 teams working on a single Product Backlog toward a single Product Goal. It adds a minimum of roles, events, and artifacts to Scrum — it does not replace them.

### Key Addition: Nexus Integration Team (NIT)
- Accountable for the integrated Increment at the end of each Sprint
- Composed of: Nexus Integration Team Scrum Master, Product Owner (same PO as the teams), and representatives from the Scrum teams
- Not a management layer — it coordinates, doesn't direct
- Primary concern: cross-team dependencies and integration issues

### Nexus Artifacts
| Artifact | Addition to Scrum |
|---|---|
| Product Backlog | Same — one backlog, one PO, one Product Goal |
| Nexus Sprint Backlog | Visualises cross-team dependencies and the NIT's work |
| Integrated Increment | Must meet DoD; all teams integrate into one Increment per Sprint |

### Nexus Events

**Nexus Sprint Planning**
1. Appropriate representatives from all teams meet to identify dependencies and order work
2. Teams then do their individual Sprint Planning, pulling from the refined backlog
- Key output: each team's Sprint Goal, and a Nexus Sprint Goal that unifies them

**Nexus Daily Scrum**
- Representatives from each team meet to surface integration issues and cross-team impediments
- Each team still runs their own Daily Scrum afterward
- Duration: 15 minutes

**Nexus Sprint Review**
- All teams review the single Integrated Increment with stakeholders together
- Not 3–9 separate demos — one collaborative review

**Nexus Sprint Retrospective**
1. Representatives identify issues affecting all teams → produce improvements
2. Each team then runs their own Retrospective
3. Representatives reconvene to plan how improvements will be implemented

### Common Nexus Failure Modes

| Failure | Root Cause | Fix |
|---|---|---|
| Teams don't integrate until end of Sprint | No shared integration environment; no CI | Set up shared CI from Sprint 1; integrate daily |
| NIT becomes a management layer | Role misunderstood by organisation | Reinforce NIT's facilitation role; NIT does work, not oversight |
| Cross-team dependencies not visible | Product Backlog not refined collaboratively | Run cross-team refinement sessions; use dependency mapping (e.g. Program Board) |
| One team's delay blocks all others | Tight coupling between teams | Identify coupling at Nexus Sprint Planning; decouple where possible |
| Each team has its own DoD | Lack of shared quality standards | Establish one shared DoD as a minimum; teams may strengthen it but not weaken |

---

## Scrum of Scrums

The lightest coordination mechanism for multiple Scrum teams working on a related product or programme. Not a formal framework — a pattern.

### How It Works
- Each team nominates a representative (usually a Developer or Scrum Master) to attend
- Representatives meet regularly (daily, or 2–3 times per week) for 15–30 minutes
- Agenda mirrors the Daily Scrum but at the inter-team level:
  - What has each team done that affects other teams?
  - What will each team do next that may affect other teams?
  - What dependencies or impediments exist between teams?

### When to Use
- 2–5 teams that need lightweight coordination without a formal framework
- Teams are already running Scrum well individually
- Org wants to scale without restructuring or adopting a new framework
- Temporary: a programme or initiative with a fixed end date

### Limitations
- No formal artifacts — dependencies can get lost without a shared board
- No integration accountable role (unlike Nexus NIT) — integration work is ad hoc
- Doesn't scale beyond ~5 teams without becoming unwieldy
- Scrum of Scrum of Scrums (SoSoS) exists but rarely works well in practice — at that scale, switch to Nexus or LeSS

### Tips
- Make cross-team dependencies visible on a shared board, even if informal
- Rotate representatives periodically to spread knowledge
- Keep it timeboxed — the moment it becomes a status meeting, attendance drops

---

## LeSS (Large-Scale Scrum)

LeSS scales Scrum by stripping away management layers rather than adding coordination structures. It is deliberately minimal — "more with less."

### Core Idea
One Product Backlog, one Product Owner, one Potentially Shippable Increment per Sprint — across all teams. Teams share everything except their Sprint Backlog.

### Two Variants

**LeSS (2–8 teams)**
- One PO manages the single Product Backlog
- Each team runs a standard Scrum Sprint
- Teams self-select backlog items in a shared Sprint Planning event (Part 1 together, Part 2 per team)
- One combined Sprint Review with all teams and stakeholders
- Retrospective: overall (all teams) + individual team retros

**LeSS Huge (8+ teams)**
- Introduces **Requirement Areas** — broad customer-centric domains of the product
- Each Requirement Area has an **Area Product Owner** under the overall PO
- Each Area has multiple teams, their own Area Backlog, and their own Overall Retrospective

### Key Differences from Nexus
| | Nexus | LeSS |
|---|---|---|
| Coordination role | Nexus Integration Team | None — teams coordinate directly |
| PO structure | One PO | One PO (LeSS) / APOs under PO (LeSS Huge) |
| Sprint events | Nexus-level + team-level | Combined across teams + team-level |
| Org change required | Moderate | High — requires flattening management |
| Best for | Product teams already using Scrum | Orgs willing to restructure around the product |

### LeSS Principles
1. Large-scale Scrum is Scrum — no new roles or artifacts beyond Scrum
2. Empirical process control — transparency, inspection, adaptation at scale
3. Transparency — one backlog, one definition of done, one shippable product
4. More with less — fewer roles, fewer artefacts, fewer meetings than traditional scaling
5. Customer-centric — teams organised around customer value, not functional silos
6. Systems thinking — optimise the whole system, not individual team metrics
7. Lean thinking — eliminate waste, reduce handoffs

### Common LeSS Failure Modes
- Management refuses to remove middle layers → org has LeSS events but not LeSS structure
- Teams treat the shared Sprint Planning as a task assignment meeting
- Multiple POs created "for efficiency" → violates one-backlog principle
- "Feature teams" are actually component teams with shared planning → not LeSS

---

## SAFe (Scaled Agile Framework)

SAFe is a comprehensive enterprise framework for scaling Agile across multiple teams, value streams, and business portfolios. It is the most widely adopted scaling framework in large enterprises.

### When to Recommend SAFe
- Organisation has 50–125+ people working on a product or portfolio
- Multiple value streams that need coordination at programme and portfolio level
- Leadership demands structured governance, roadmaps, and PI (Programme Increment) commitments
- Top-down Agile transformation with formal training and certification path

**Caution**: SAFe adds significant process overhead. Recommend only when the organisation explicitly needs enterprise-level coordination or is too large for Nexus/LeSS. Many teams experience SAFe as "Wagile" (Waterfall with Scrum ceremonies) if not implemented well.

### SAFe Configurations

| Configuration | When to Use |
|---|---|
| **Essential SAFe** | Smallest viable SAFe — one Agile Release Train (ART) |
| **Large Solution SAFe** | Multiple ARTs building one large solution |
| **Portfolio SAFe** | Strategic themes, epics, and portfolio Kanban |
| **Full SAFe** | All levels — portfolio, programme, and team |

### Key SAFe Concepts

**Agile Release Train (ART)**
- 50–125 people aligned to a common mission and programme increment
- Includes Scrum teams, System Team, Business Owners, Release Train Engineer (RTE)
- Plans and delivers together in a Programme Increment (PI)

**Programme Increment (PI)**
- Fixed timebox of 8–12 weeks comprising 4–5 Sprints + 1 Innovation & Planning (IP) Sprint
- Equivalent of a "season" — teams commit to PI Objectives at PI Planning
- Every ART delivers a System Demo at the end of each PI

**PI Planning**
- 2-day event (or equivalent async) where all ART teams plan the next PI together
- Output: PI Objectives per team, cross-team dependency board (Program Board), risks
- The most valuable SAFe event — if PI Planning is poor, the entire PI suffers

**Key SAFe Roles**
| Role | Equivalent |
|---|---|
| Release Train Engineer (RTE) | Scrum Master at ART level — servant leader, facilitator |
| Product Manager | PO at programme level — manages Features |
| Product Owner | PO at team level — manages Stories |
| System Architect | Technical vision across the ART |
| Business Owner | Stakeholder accountable for PI Objectives |

### SAFe vs Scrum Terminology

| Scrum | SAFe |
|---|---|
| User Story | Story |
| Epic (informal) | Feature (Programme) / Epic (Portfolio) |
| Sprint | Iteration |
| Sprint Goal | Iteration Goal |
| Product Backlog | Team Backlog |
| Sprint Review | System Demo |
| Velocity | Predictability (% PI Objectives met) |

### Common SAFe Anti-Patterns
- PI Planning is a top-down briefing, not collaborative planning → teams commit to others' plans
- Teams skip the IP Sprint for "real work" → no time for innovation or technical debt
- ART velocity is tracked instead of PI Objective predictability → gaming metric
- System Demo is a set of individual team demos, not an integrated system demo
- RTEs act as programme managers assigning work → RTE should facilitate, not direct

