# ResumeFromDesign — Enter Pipeline from Existing Work

Alternative conductor for users who already have design artifacts (HTML designs, PRD, design system, schemas, roadmaps). Ingests existing work, performs necessary transformations, and enters the standard pipeline at the right phase.

**When to use:** You have some or all of: HTML page designs, a MASTER.md design system, a PRD, a schema, a roadmap, feature specs. You want to build from these without re-doing Discovery or Design.

**What this skips:** Discovery (Phases 0-0b), Design (Phases 1-3). These are imported from your existing work.

**What this does NOT skip:** Tech stack decision, repo init, component validation, spec hardening. These cannot be derived from existing artifacts alone.

---

## Step 1: Read & Report

Read the directory the user provides. List every file found and what it is.

**Lucy says:**

> "Let me read what you have."

Read all files in the provided directory (including subdirectories). For each file, identify it:

- **Design system** — file named `MASTER.md` with color/typography/spacing tokens
- **PRD** — file named `PRD.md` or containing Product Vision + Target User + Feature Set sections
- **Schema** — file named `SCHEMA.md` or containing ERD / table definitions
- **Roadmap** — file named `ROADMAP.md` or containing build phases with acceptance criteria
- **Feature spec** — any `.md` file describing a specific feature in detail (e.g., `PODCAST-FEATURE.md`)
- **HTML designs** — `.html` files (pages, components, prototypes)
- **Mockup images** — `.png` / `.jpg` files
- **Persona files** — files in `users/` or containing JTBD / anxieties / mental models
- **UX specs** — files in `ux/` or containing "interaction spec" / "Level 3"
- **Other** — anything else, reported but no action needed

Present a summary:

> "Here's what I found in `[directory]`:
>
> | File | Type | Pipeline Equivalent |
> |------|------|-------------------|
> | `MASTER.md` | Design system | Phase 1 output |
> | `PRD.md` | Product requirements | Phases 0 + 0b output |
> | `SCHEMA.md` | Database schema | Phase 6 input |
> | `ROADMAP.md` | Build plan | Phase 6 input |
> | `PODCAST-FEATURE.md` | Feature spec | Phase 6 input |
> | `pages/*.html` (10 files) | HTML prototypes | Phase 3 output |
>
> This covers **Discovery** and **Design**. I'll import these and start at **Tech Stack**."

**If critical artifacts are missing** (no design system, no PRD, no HTML designs), say what's missing and recommend which pipeline entry point to use instead (Discovery if no PRD, Design if no MASTER.md, etc.).

---

## Step 2: Orientation Confirmation

**If a PRD was found:**

1. Read the PRD's Product Vision and Success Criteria sections
2. Synthesize candidate orientation sentences in the Phase 0 format:
   - **What:** "What does this do for whom?" — one sentence from Product Vision
   - **Done:** "How do you know it worked?" — one sentence from Success Criteria or MVP definition

**Lucy says:**

> "From your PRD, I'd propose these orientation sentences:
>
> **What:** [synthesized sentence]
> **Done:** [synthesized sentence]
>
> These anchor everything downstream — the Build Loop references them, the MVP Gate checks against them. Confirm these, or rewrite them."

**Wait for explicit confirmation.** Do not proceed until the user says "confirmed" or provides rewrites.

**If NO PRD was found:**

Ask the two standard Phase 0 questions directly (same as `.claude/skills/Custom/AgentBuild/Workflows/FullBuild.md` Phase 0). Wait for both answers. Lock them.

---

## Step 3: Tech Stack Decision

**Route to:** `.claude/skills/Custom/AgentBuild/Workflows/FullBuild.md` — Phase 1 section (tech stack questions only).

Read the Phase 1 section and follow its instructions for the three questions:

1. **Language/Framework** — make informed recommendations from what you read:
   - Complex multi-page app with state → recommend React/Next.js
   - Simple static pages → recommend HTML/Tailwind
   - Schema references Postgres/Supabase → recommend DbSupabase module
   - PRD mentions email delivery → flag as external service needing a module
2. **Where will this run?** — Railway recommended for MVPs (module available)
3. **External services?** — flag any referenced in PRD or feature specs

Present available modules. User decides.

**This step cannot be skipped.** HTML designs are framework-agnostic. The tech stack determines CI config, AGENTS.md structure, and which WebDesign validation rules apply.

---

## Step 4: Project Registration & Repo Init

Combines Phase 4 (PID) and Phase 5 (Environment Bootstrap), accelerated with artifact import.

### 4a: Project Location & PID

Follow `.claude/skills/Custom/AgentBuild/Workflows/FullBuild.md` Phase 1a exactly:

1. Ask where projects live on this machine
2. Generate PID: `openssl rand -hex 4`
3. Create project directory at `{path}/{project-slug}/`
4. Register in `.claude/skills/Custom/AgentBuild/projects/PID-{hex}.json`:

```json
{
  "id": "PID-{hex}",
  "name": "[from PRD or user]",
  "slug": "[project-slug]",
  "repoPath": "[full path]",
  "repoRemote": null,
  "currentPhase": "5b",
  "phaseHistory": [
    { "phase": "0", "source": "imported", "importedFrom": "[PRD path] § Product Vision" },
    { "phase": "0b", "source": "imported", "importedFrom": "[PRD path] § Target User" },
    { "phase": "1", "source": "imported", "importedFrom": "[MASTER.md path]" },
    { "phase": "2", "source": "imported", "importedFrom": "[pages/ path]" },
    { "phase": "3", "source": "imported", "importedFrom": "[pages/ path]" },
    { "phase": "4", "completedAt": "[now]" },
    { "phase": "5", "completedAt": "[now]" }
  ],
  "orientation": {
    "what": "[confirmed sentence from Step 2]",
    "done": "[confirmed sentence from Step 2]"
  },
  "modules": ["[selected modules from Step 3]"],
  "stack": {
    "language": "[choice]",
    "framework": "[choice]",
    "deploy": "[choice]",
    "external": ["[services]"]
  },
  "personas": ["[persona slug from Step 5a]"],
  "maturityScore": null,
  "status": "active",
  "prdPath": null,
  "createdAt": "[now]",
  "updatedAt": "[now]"
}
```

5. Display PID to user

### 4b: Repo Initialization

Follow `.claude/skills/Custom/AgentBuild/Workflows/FullBuild.md` Phase 1b:

- Generate standard directory structure, package config, linting, CI, README, AGENTS.md, hello-world

### 4c: Copy Artifacts into Pipeline Paths

Copy imported artifacts into the repo at pipeline-convention paths:

| Source File | Destination in Repo | Notes |
|-------------|-------------------|-------|
| `MASTER.md` | `design-system/MASTER.md` | Direct copy |
| `pages/*.html` | `design/reference/*.html` | Flatten — all HTML files into reference dir |
| `*.png` / `*.jpg` | `design/mockups/*.png` | Image files as mockup references |
| `PRD.md` | `docs/imported/PRD.md` | Source document — NOT a spec |
| `SCHEMA.md` | `docs/imported/SCHEMA.md` | Source document |
| `ROADMAP.md` | `docs/imported/ROADMAP.md` | Source document |
| Feature specs (e.g., `PODCAST-FEATURE.md`) | `docs/imported/[name].md` | Source documents |
| Standalone persona files (if any) | `docs/specs/users/[name].md` | Direct copy |
| Standalone UX specs (if any) | `docs/specs/ux/[name].md` | Direct copy |

**Why `docs/imported/`:** These are source documents in their original format. They are NOT AgentBuild-format specs. The Build Loop reads from `docs/specs/features/`. Keeping them separate prevents the Build Loop from trying to parse a PRD as a feature spec.

### 4d: Hello-World Gate

CI must be green on the hello-world test. Non-negotiable. Same as FullBuild.md Phase 1c.

---

## Step 5: Artifact Transformations

The imported documents need three transformations to produce the files the pipeline expects.

### 5a: Persona Extraction

**If standalone persona files already exist** (found in Step 1): skip — they're already copied.

**If persona exists only inside the PRD** (common):

1. Read PRD § Target User section
2. Extract into standalone file at `docs/specs/users/[persona-slug].md`:

```markdown
# Persona: [Name]

## Who
[Role, title, context from PRD]

## Jobs to Be Done
[What they're trying to accomplish — from PRD behaviors and needs]

## Anxieties
[What worries them about this task — inferred from PRD pain points]

## Mental Models
[How they think about this domain — from PRD behaviors]

## Key Behaviors
[Specific actions they take — from PRD key behaviors list]

## Non-Persona (Explicitly Not This User)
[From PRD non-persona section, if present]
```

3. Present to user for review — this is a transformation, not a copy, so confirm accuracy.

### 5b: Lightweight UX Spec

**If standalone UX specs already exist**: skip.

**If no UX spec exists** (common — most imported projects have PRDs but not UX specs):

1. Read PRD § User Flows section
2. Generate a lightweight Level 3 UX spec for the primary user flow at `docs/specs/ux/[primary-flow]-ux.md`:

```markdown
# UX Spec: [Primary Flow Name]

## Flow
[The step-by-step flow from PRD § User Flows]

## Layout Hierarchy
[Inferred from HTML designs — what's primary, secondary, tertiary on each screen]

## Key Interaction Patterns
[Inferred from HTML designs — forms, modals, navigation, state transitions]

## Edge States
[Empty states, loading states, error states — inferred from designs if present, flagged as gaps if not]
```

**Why this matters:** During the Build Loop, when a UI requirement not covered by the original designs is discovered, the design gap path routes back to the Design Stack. Without a UX spec, the Design Stack has no behavioral anchor for gap decisions. This lightweight spec provides that anchor.

3. Present to user for review.

### 5c: Feature Spec Translation

Read the PRD § MVP Feature Set, ROADMAP acceptance criteria, and any standalone feature specs.

For each feature, produce an AgentBuild-format spec at `docs/specs/features/[feature-name].md` using the template from `.claude/skills/Custom/AgentBuild/SpecFeature.md`:

```markdown
# Feature: [Name]

> [One sentence from PRD feature description]

**Spec status:** DRAFT
**Last updated:** [today]

---

## Happy Path

FEATURE: [name]
USER: [from extracted persona]
ACTION: [from PRD feature description + ROADMAP acceptance criteria]
RESULT: [from ROADMAP acceptance criteria — what the user sees when it works]

---

## Edge Cases

[LEFT EMPTY — populated by Specify container in Step 7]

---

## Failure Behaviors

[LEFT EMPTY — populated by Specify container in Step 7]

---

## Business Constraints That Apply

[Extract from PRD § Technical Constraints if present]

---

## Out of Scope (MVP)

[From PRD § Out of Scope, filtered to this feature]

---

## Test Coverage Required

- [ ] Happy path (Section: Happy Path)
- [ ] All edge cases in Section: Edge Cases
- [ ] All failure behaviors in Section: Failure Behaviors where testable

---

## Acceptance Criteria

[From ROADMAP acceptance criteria for this feature's screen(s)]
```

**These are DRAFT specs.** Edge Cases and Failure Behaviors are intentionally empty — they get populated by the Specify container in Step 7. The happy path and acceptance criteria come from the imported documents.

### 5d: Spec Index with Build Checklist

Create `docs/specs/MASTER.md` as described in `.claude/skills/Custom/AgentBuild/Workflows/FullBuild.md` Phase 3a.

MASTER.md must include:

1. **Spec index** — links to all feature specs, personas, UX specs, constraints, imported documents
2. **Build checklist** — ordered feature table with dependency chain and build status

**Build checklist format:**

```markdown
## Feature Specs — Build Checklist

Build order follows dependency chain. Pick the next `Not started` feature in order.

| # | Feature | File | Spec Status | Build Status | Depends On |
|---|---------|------|-------------|--------------|------------|
| 1 | [Feature] | [link] | DRAFT | Not started | — |
| 2 | [Feature] | [link] | DRAFT | Not started | Feature 1 |
| ...

**Build Status values:** `Not started` → `In progress` → `Built (PR #N)` → `Merged`

When a feature's PR is merged, update its Build Status to `Merged` and commit this file.
```

**Dependency order** is derived from:
- The PRD § User Flows (which screens feed into which)
- The ROADMAP § Build Phases (phase order = dependency order)
- The SCHEMA (foreign key relationships imply data dependencies)

### 5e: Route Structure

Generate `docs/specs/routes.md` from:
- The PRD § User Flows (page-to-page navigation)
- The UX spec from Step 5b (layout hierarchy, interaction patterns)
- The framework choice from Step 3 (React Router, Next.js file routing, etc.)

**routes.md must contain:**
- URL paths for every page/screen
- Route parameters (`:id` params, query params)
- Layout structure (which routes share which layout wrappers)
- Navigation flow diagram
- Breadcrumb patterns per page
- Auth requirements per route (public vs protected)

See FullBuild Phase 3b for the full specification of what routes.md must include.

### 5f: Commit

Create `docs/known-fixes/.gitkeep`.

Commit everything to git and push.

---

## Step 6: Component Validation (Phase 5b)

**Route to:** WebDesign child skills based on chosen framework from Step 3.

| Stack | Route To |
|-------|----------|
| React / Next.js | `.claude/skills/WebDesign/react-best-practices/SKILL.md` + `.claude/skills/WebDesign/composition-patterns/SKILL.md` |
| React Native | `.claude/skills/WebDesign/react-native-skills/SKILL.md` |
| HTML / Tailwind | `.claude/skills/WebDesign/web-design-guidelines/SKILL.md` |

Validate the imported HTML designs against framework-specific rules. Flag violations by priority (CRITICAL / HIGH / MEDIUM / LOW).

**Output:** `docs/component-validation.md` — committed to repo, referenced by AGENTS.md.

---

## Step 7: Handoff to Specify

**Route to:** `Specify/Workflows/RunSpecify.md`

The DRAFT specs from Step 5c have happy paths and acceptance criteria but **empty Edge Cases and Failure Behaviors sections**. The Specify container fills these:

- **Step 2b (Edge Case Generation):** Invoke Research for domain failure modes. Invoke Council with 5 synthetic personas seeded from the extracted persona (Step 5a). User decides Include/Exclude/Defer for each.
- **Step 2c (Failure Mode Specification):** Invoke RedTeam for adversarial analysis. User reviews and approves.
- **Step 2d (Business Constraint Documentation):** Extract from PRD technical constraints + user provides additional rules.
- **Step 2e (IterativeDepth Review):** 4-angle completeness check.

**This is not optional.** Specs without edge cases and failure modes produce brittle code. The Build Loop needs complete specs.

After Specify completes → standard pipeline from **Phase 8 (Build Loop)** onward via `Build/Workflows/RunBuild.md`.

---

## Session Boundary

After Step 5f (transformations + spec index + routes + commit), this is a natural session break point. Context will be heavy from reading imported documents + generating transformations.

**To resume:** Start a new session. The git repo contains everything needed. Read `docs/specs/MASTER.md` as the entry point. The PID registry shows `currentPhase: "5b"` or `"specify"` depending on where the break happened.

---

## Phase Map

| Pipeline Phase | Status in This Workflow | What Happens |
|---|---|---|
| 0 (Orientation) | **Accelerated** | Extracted from PRD, user confirms |
| 0b (Refinement) | **Skipped** | PRD/persona already exist — persona extracted in Step 5a |
| 1 (Design System) | **Skipped** | MASTER.md imported |
| 2 (Mockups) | **Skipped** | HTML designs imported as references |
| 3 (Components) | **Skipped** | HTML designs imported as references |
| 4 (Tech Stack) | **Unchanged** | Standard conversation — can't infer from HTML |
| 5 (Repo Init) | **Accelerated** | Standard init + artifact copy + transformations (5a-5c) + spec index with build checklist (5d) + route structure (5e) + commit (5f) |
| 5b (Validation) | **Unchanged** | Standard WebDesign validation |
| 6-7 (Specify) | **Accelerated start** | Happy paths seeded from PRD, then full Council/RedTeam/IterativeDepth hardening. MASTER.md and routes.md already exist from Step 5d/5e — Specify updates them, does not recreate |
| 8+ (Build → Ship) | **Unchanged** | Standard pipeline from here |
