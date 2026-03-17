# AgentBuild — Full Build Workflow

Complete orchestration from empty machine to deployed MVP. Run phases in sequence. Do not skip. Do not reorder.

---

## Phase 0: Orientation

**Starting point:** Nothing exists. Empty machine. No repo. No idea beyond what the user just described.

**Lucy says:**

> "Let's build this. Before anything else — two questions only. Don't build feature lists yet. Just these two sentences:
>
> **1. What does this do for whom?** (one sentence — the core value proposition)
> **2. How do you know it worked?** (one sentence — what 'done' looks like for MVP)
>
> Everything else comes later. These two sentences are the foundation everything else is built on."

**Wait for both answers. Do not proceed until you have them.**

**Lucy confirms and locks:**
> "Good. Locking in:
> - **What:** [restate user's sentence 1]
> - **Done:** [restate user's sentence 2]
>
> These will be referenced in every subsequent phase. Ready to build the factory."

**Output:** Two initial orientation sentences. These are the starting point — Phase 0b will sharpen them.

---

## Phase 0b: Idea Refinement

**Route to:** `Workflows/IdeaRefinement.md`

**Lucy becomes a UX consultant.** This is a structured, conversational discovery session — not a checklist. Lucy conducts a 7-step process:

1. **Discovery** — asks about users, context, JTBD, who is NOT the user
2. **User empathy** — constructs a named user persona and articulates their anxieties out loud
3. **UX advocacy** — challenges weak assumptions with research and proposes alternatives
4. **Consultative proposal** — presents 2-3 design approaches with tradeoffs
5. **Collaborative refinement** — iterates through multiple exchanges until the approach is clear
6. **Specification generation** — produces a Level 3 UX spec (behavior only, no visual design)
7. **Review & validation** — states assumptions made and where the PM should validate before building

**This phase is conversational.** It may span many exchanges. Lucy does not rush it. The quality of everything downstream depends on the sharpness of what comes out of this phase.

**Output (saved to GitHub repo):**
- `docs/specs/users/[persona-name].md` — named user persona with JTBD, anxieties, mental models
- `docs/specs/ux/[feature-name]-ux.md` — Level 3 interaction spec for core user journey
- Updated Phase 0 orientation sentences (if refinement sharpened them)

**Phase 0b is complete when:**
- At least one named user persona is documented
- The core user journey has a Level 3 UX spec
- The orientation sentences accurately reflect what was learned
- The PM has confirmed the direction before building begins

**Do not proceed to Phase 1 until Phase 0b output is committed to GitHub.**

---

## Phase 1: Environment Bootstrap

**Lucy says:**

> "Now we build the factory before we spec the product. This is the most underrated step — 80% of agentic build failures start here, not in the specification.
>
> **First: Known modules.** Before making any novel infrastructure decisions, I'll check what's already solved.
>
> Available modules:
> - **Framework** → `Modules/FrameworkNextjs.md` (Next.js App Router — file conventions, server/client components, version-specific patterns)
> - **Auth** → `Modules/AuthClerk.md` (Clerk.dev — sessions, JWT, social login)
> - **Database** → `Modules/DbSupabase.md` (Supabase Postgres — RLS, real-time, file storage)
> - **Deploy** → `Modules/DeployRailway.md` (Railway — zero-config hosting, auto-deploy)
> - **Observability** → `Modules/ObservabilitySentry.md` (Sentry + Pino — errors, logging)
> - **Slack** → `Modules/SlackIntegration.md` (Slack messaging — Socket Mode, streaming, session isolation)
> - **Chat UI** → `Modules/ChatInterface.md` (assistant-ui — streaming, tool visualization, theming)
>
> Do any of these apply to your project? (Most projects need Deploy + Observability at minimum. Auth and Database if you have users or persistent data.)
>
> **Then: Three decisions needed from you:**
>
> **1. Language/Framework** — I recommend TypeScript (best agent support, most documentation). Alternatives: Python (data-heavy), Go (performance-critical). Your call.
>
> **2. Where will this run?** — Options:
>    - Railway (easiest deployment, recommended for MVPs — module available)
>    - Fly.io (more control, still simple)
>    - Vercel (front-end heavy)
>    - Local only (no deployment yet)
>
> **3. Any external services needed beyond the known modules?** — (Stripe, Slack, email, custom APIs) List them or say none.
>
> If you need an integration that doesn't have a module yet, I'll create one using `Workflows/ModuleBuilder.md` — a deep-research process that produces stack-aware, AI-consumable module specifications through 4 parallel research agents, Council review, and RedTeam validation before first use.
>
> I'll handle everything else: repo init, AGENTS.md (pre-loaded with module conventions), CI setup, directory structure, and a hello-world gate to confirm the factory works."

**After user answers, Lucy executes Phase 1a-1d:**

### 1a: Project Location & Registration

**Lucy says:**

> "Before I initialize the repo — where do you keep your projects on this machine? I'll create the repo there and register it so I can find it across sessions.
>
> Common patterns:
> - `~/projects/`
> - `~/code/`
> - `~/dev/`
>
> Or tell me a specific path."

**After user answers, Lucy:**

1. Generates a **Project ID (PID)** — the immutable identifier for this project:
   ```bash
   openssl rand -hex 4
   ```
   This produces an 8-character hex string. Prefix with `PID-` → e.g., `PID-a7f3b2e1`.

2. Creates the project directory at `{user's path}/{project-slug}/`

3. Registers the project in `.claude/skills/AgentBuild/projects/PID-{hex}.json`:

```json
{
  "id": "PID-a7f3b2e1",
  "name": "[Project Name from Phase 0]",
  "slug": "[project-slug]",
  "repoPath": "[full path to local repo]",
  "repoRemote": null,
  "currentPhase": "1b",
  "phaseHistory": [
    { "phase": "0", "completedAt": "[date]" },
    { "phase": "0b", "completedAt": "[date]" },
    { "phase": "1", "completedAt": "[date]" }
  ],
  "orientation": {
    "what": "[Phase 0 sentence 1]",
    "done": "[Phase 0 sentence 2]"
  },
  "modules": ["[selected modules]"],
  "stack": {
    "language": "[choice]",
    "framework": "[choice]",
    "deploy": "[choice]",
    "external": ["[services]"]
  },
  "personas": ["[persona slugs from Phase 0b]"],
  "maturityScore": null,
  "status": "active",
  "prdPath": null,
  "createdAt": "[date]",
  "updatedAt": "[date]"
}
```

4. Displays the PID to the user:

> "Project registered. Your Project ID is **PID-a7f3b2e1**. This ID is permanent — it identifies this project across all sessions, repos, specs, and commits."

5. Updates `repoRemote` after the first `git push` in Phase 1b.

**The PID is the project's identity.** It goes into AGENTS.md, commit messages (`[PID-a7f3b2e1] Add feature`), PRD frontmatter, and spec file headers. Any artifact can be traced back to its project.

**The PID Gate:** From this point forward, Lucy cannot write to this repo without having PID-a7f3b2e1 loaded as active context. This prevents cross-project contamination when multiple projects are active. See `projects/README.md` for the full gate protocol.

**Do not proceed to Phase 1b until the project is registered with a PID.**

---

### 1b: Repo Initialization (Agent-generated)

Issue this build task to the agent:

```
SPEC: AgentBuild Phase 1 — Repo Initialization
SCOPE: Initialize a new GitHub repository at [registered repo path] for a [user's language choice] [type of application based on Phase 0 description].
TASK: Generate the complete repository structure including:
  - Standard directory structure (src/, tests/, docs/specs/)
  - Package/dependency configuration
  - Linting and formatting rules
  - CI workflow (.github/workflows/ci.yml) that runs tests and lint on every PR
  - README.md with the project description from Phase 0
  - AGENTS.md (see template below)
  - A hello-world endpoint or function with a passing test

AGENTS.md must include:
  - Project name and one-sentence description (from Phase 0)
  - What 'done' means for MVP (from Phase 0)
  - Directory structure with purpose of each directory
  - Coding conventions (naming, error handling, logging)
  - How to run tests locally
  - How to run linter locally
  - What 'done' means for any task (format: all tests pass, CI green, spec coverage complete)
  - What to do when tests fail
  - What to do when uncertain about behavior — check docs/specs/ first

After repo initialization:
  - Update the project registry with repoRemote (after git push)
  - Update currentPhase to "1c"

DONE WHEN: Repository exists at the registered path, CI passes on the hello-world test, README and AGENTS.md are complete, project registry updated.
```

### 1c: Hello-World Gate (Non-Negotiable)

**Lucy says:**

> "The factory gate: CI must pass on the hello-world before we write a single spec. This is not optional — it proves the factory works before we invest in specification.
>
> *[Checking CI status...]*
>
> [If CI passes]: Factory confirmed. Moving to specification.
> [If CI fails]: Factory is broken. We fix this before writing any specs. What's the error?"

**Do not proceed to Phase 2 until CI is green.**

---

## Phase 2: Knowledge Capture

**Lucy says:**

> "Factory is running. Now we build the specification. This phase determines the quality of everything that gets built. Take your time here — a complete spec means zero follow-up questions during build.
>
> We'll work through four steps:
> 1. Happy path specs (you write these)
> 2. Edge case generation (I generate, you decide)
> 3. Failure mode specs (I generate, you review)
> 4. Business constraints (you write, I structure)
>
> Start with: what is the first feature you want to build?"

### 2a: Happy Path Specification

**Lucy provides the template and waits:**

> "For this feature, fill in:
> ```
> FEATURE: [name]
> USER: [who is doing this — be specific]
> ACTION: [what they want to accomplish]
> RESULT: [what they see/get when it works perfectly]
> ```
> Don't worry about edge cases yet. Just the happy path."

### 2b: Edge Case Generation (invoke Research + Council)

After receiving the happy path spec:

**Lucy says:**
> "Good. Now I'm generating edge cases you may not have considered. Invoking Research and Council..."

**Invoke Research skill:**
> "Research domain failure modes for [feature type]. What goes wrong in [domain] applications at this type of feature? Return the top 10 failure modes with descriptions."

**Invoke Council skill** with 5 agents playing synthetic user personas:

```
Council prompt: "Five agents will each play one of these personas interacting with this feature spec:

[PASTE HAPPY PATH SPEC]

Persona 1 — The Ideal User: Uses this exactly as intended. What edge case would surprise even them?
Persona 2 — The Confused First-Timer: Has never seen this before. What will they try that breaks it?
Persona 3 — The Power User: Will push every limit, find every shortcut. What boundary does this spec not define?
Persona 4 — The Adversarial User: Actively trying to break or abuse the system. What can they exploit?
Persona 5 — The System Administrator: Responsible for this at 3am when it breaks. What information do they not have?

For each persona: state the triggering condition, what happens with the current spec, and what the correct behavior should be."
```

**Lucy presents generated edge cases:**
> "Here are [N] edge cases generated across research and 5 user personas. For each, decide: **Include** (add to spec), **Exclude** (out of scope for MVP), or **Defer** (post-MVP)."

### 2c: Failure Mode Specification (invoke RedTeam)

**Invoke RedTeam skill:**
> "Adversarially analyze this feature spec: [PASTE SPEC]. Focus on: system failures (database unavailable, upstream 500s, timeouts), input failures (valid but unexpected, malformed, boundary values), and state failures (session expiry, concurrent access, race conditions). For each failure: what is the correct system behavior?"

**Lucy presents failure modes for review:**
> "RedTeam found [N] failure scenarios. Review each — I'll add your approved behaviors to the spec as explicit failure handling requirements."

### 2d: Business Constraint Documentation

**Lucy says:**
> "Final step in specification: business rules. These are the rules that exist in your head or your team's heads but aren't written anywhere. Things like rate limits, pricing tiers, access controls, compliance requirements.
>
> For each rule, tell me:
> - The rule (what must always be true)
> - An example of someone violating it
> - What should happen when they do
>
> I'll format them into the constraint spec format."

**Invoke FirstPrinciples skill** if user struggles to articulate constraints:
> "Let's decompose this. What is the fundamental purpose of this system? What would make it fail to serve that purpose? What are the hardest rules — the ones where you absolutely cannot make exceptions?"

### 2e: Compile Specification

**Lucy says:**
> "Compiling full specification to `docs/specs/features/[feature-name].md`. This includes:
> - Happy path (from 2a)
> - Edge cases approved (from 2b) — [N] total
> - Failure handling (from 2c) — [N] scenarios
> - Business constraints (from 2d) — [N] rules
>
> **Invoking IterativeDepth** for multi-angle completeness review before we build..."

**Invoke IterativeDepth skill:**
> "Review this specification from 4 angles: (1) What would a QA engineer say is missing? (2) What would a security engineer say is unspecified? (3) What would a new engineer say is ambiguous? (4) What would a customer success rep say doesn't match how users actually behave? Flag any gaps."

**Lucy addresses any gaps flagged, then:**
> "Specification complete and reviewed. Ready for the build loop."

---

## Phase 3: Spec Repository Structure

**Lucy creates the structure automatically:**

```
docs/
└── specs/
    ├── MASTER.md              ← Index + build checklist (agent entry point)
    ├── routes.md              ← SPA/page route structure + navigation flow
    ├── features/
    │   └── [feature-name].md  ← Compiled spec from Phase 2
    ├── constraints/
    │   └── business-rules.md  ← Business constraints from 2d
    └── architecture/
        └── decisions.md       ← Architecture Decision Records
```

### 3a: MASTER.md — Spec Index with Build Checklist

MASTER.md is the **cold-start entry point** for any agent resuming this project. It must contain:

1. **Spec index** — links to all feature specs, personas, UX specs, constraints, architecture docs
2. **Build checklist** — ordered list of features with dependency chain and build status

**Build checklist format:**

```markdown
## Feature Specs — Build Checklist

Build order follows dependency chain. Pick the next `Not started` feature in order.

| # | Feature | File | Spec Status | Build Status | Depends On |
|---|---------|------|-------------|--------------|------------|
| 1 | [Feature] | [link] | HARDENED | Not started | — |
| 2 | [Feature] | [link] | HARDENED | Not started | Feature 1 |
| ...

**Build Status values:** `Not started` → `In progress` → `Built (PR #N)` → `Merged`

When a feature's PR is merged, update its Build Status to `Merged` and commit this file.
```

**Dependency order** is derived from the UX spec's user flow and the ROADMAP's phase structure. Features that other features depend on go first. If unclear, Lucy maps dependencies before finalizing the order.

**Why this matters:** When an agent cold-starts in a new session, it reads MASTER.md and immediately knows: which features exist, which are built, and which to build next. Without this, the agent must infer progress from git history — fragile and slow.

### 3b: routes.md — Route Structure

Generate `docs/specs/routes.md` from:
- The UX spec's user flow (from Phase 0b)
- The framework choice (from Phase 1)
- The feature list (from Phase 2)

**routes.md must contain:**
- URL paths for every page/screen
- Route parameters (`:id` params, query params)
- Layout structure (which routes share which layout wrappers)
- Navigation flow diagram (which page leads to which)
- Breadcrumb patterns per page
- Auth requirements per route (public vs protected)

**Framework-specific routing:**
- React Router → explicit route definitions with component mapping
- Next.js App Router → file-based routing with directory structure
- HTML/static → page file naming conventions

**Why this is generated here, not during build:** Without a route spec, two engineers (or two agent sessions) would invent different URL structures. Routes are architecture, not implementation detail. They must be locked before the Build Loop starts.

### 3c: Commit

**Critical — commit docs/ to GitHub:**

> `docs/` is version-controlled alongside the code. It is not local-only. Commit it now, before the first build task is issued.
>
> **Why:** A cold-start agent in a new session reads specs from the repo. If specs only exist locally, that agent is blind. The code and the specs that describe it must travel together in version control.
>
> Also create `docs/known-fixes/.gitkeep` now — the ErrorRecovery library will grow here across builds.

```bash
git add docs/
git commit -m "Add spec repository structure with build checklist and routes"
git push
```

**Lucy says:**
> "Spec structure created and committed. `docs/specs/MASTER.md` is the agent's entry point — every build task will reference specs from here. Ready to build."

---

## Phase 4: Build Loop

**Route to:** `Workflows/BuildLoop.md`

---

## Phase 5: Environment Design

**Route to:** `Workflows/EnvironmentDiagnosis.md`

**Trigger:** Any time an agent produces wrong output consistently, CI is failing inexplicably, or the build loop is generating work that keeps breaking.

---

## Phase 6: Observability

**Lucy says:**
> "Before MVP, we need to see what's happening in production. Without observability, AI-generated code that fails silently is a black box. Setup takes one build task.

**Minimum required:**
1. Error tracking (Sentry recommended — free tier sufficient for MVP)
2. Request logging (input, output, duration, status for every API call)
3. 3-5 business metric events (the numbers that prove the product is working)
4. Alerting (error rate spike → notification)

**Invoking Browser** to verify dashboards are live after setup..."

**Issue build task:**
```
SPEC: AgentBuild Phase 6 — Observability
SCOPE: Add minimum viable observability to the application.
TASK:
  - Integrate Sentry for error tracking (use provided DSN)
  - Add request logging middleware (log: endpoint, method, status, duration, timestamp)
  - Add [user's 3-5 metric events] as structured log events
  - Add health check endpoint at /health
CONSTRAINTS: No sensitive data in logs. Error messages must include correlation IDs.
DONE WHEN: Sentry receives a test error, request logs appear in console, health check returns 200.
```

---

## MVP Gate

**Route to:** `Workflows/MvpGate.md`
