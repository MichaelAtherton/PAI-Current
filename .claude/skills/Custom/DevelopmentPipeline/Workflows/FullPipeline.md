# FullPipeline — Sequential Conductor

The full 14-phase development pipeline from raw idea to deployed MVP. This workflow conducts 4 containerized zones (Discovery, Design, Specify, Build) plus inline orchestration for mechanical phases (Scaffold, Ship).

**Pattern:** Sequential child invocation with file-based handoff. Each container produces file-based deliverables at documented paths. The next container cold-starts from those files. Session boundaries are recommended at each handoff point but not enforced.

**Source of truth:** `output/DevelopmentPipeline/PIPELINE.md`

---

## Phase Execution Sequence

### Zone 1: Discovery (Phases 0, 0b) — CONTAINERIZED

**Invoke:** `Discovery/Workflows/RunDiscovery.md`

**What happens:**
- Phase 0: Two orientation questions → locked `what` and `done` sentences
- Phase 0b: 7-step UX consultant discovery → persona files, Level 3 UX specs

**Deliverables produced:**

| Artifact | Path |
|----------|------|
| Orientation sentences | Held in session — no PID exists yet. Save to local scratchpad or carry in session notes. Written to PID registry `orientation` field in Phase 4 when PID is generated. |
| User persona(s) | `docs/specs/users/[persona-name].md` |
| UX spec(s) | `docs/specs/ux/[feature-name]-ux.md` |

**Session boundary recommendation:** Discovery involves 7+ user exchanges and multiple refine loops. If context exceeds ~50k tokens, start a new session before entering Design. **If breaking session here:** the orientation sentences must be re-stated or read from a local scratchpad since no PID registry exists yet.

---

### Zone 2: Design (Phases 1, 2, 3) — CONTAINERIZED

**Invoke:** `Design/Workflows/RunDesign.md`

**Cold-start from:** persona files + UX specs from Discovery

**What happens:**
- Phase 1: Design system generation via UI/UX Pro Max → `design-system/MASTER.md`
- Phase 2: Mockup generation via Stitch MCP → `design/mockups/`
- Phase 3: Component generation via 21st.dev Magic → `design/reference/`

**Deliverables produced:**

| Artifact | Path |
|----------|------|
| Design system | `design-system/MASTER.md` |
| Mockup screens | `design/mockups/[screen-name].png` + `.html` |
| Component files | `design/reference/[component-name].html` |

**Session boundary recommendation:** Design involves 4+ refine loops and heavy MCP tool calls. If context exceeds ~50k tokens, start a new session before entering Scaffold.

---

### Zone 3: Scaffold (Phases 4, 5, 5b) — INLINE (orchestrator runs directly)

These phases are mechanical and context-lean. No containerization needed.

#### Phase 4: Tech Stack Decision

**Route to:** `.claude/skills/Custom/AgentBuild/Workflows/FullBuild.md` — Phase 1 section (tech stack questions only).

1. Present available modules (Framework, Auth, Database, Deploy, Observability, Slack, Chat UI)
2. Ask three questions: Language/Framework, Deployment target, External services
3. Generate PID and register project in `.claude/skills/Custom/AgentBuild/projects/PID-{hex}.json`
4. Record orientation sentences (from Discovery) in the PID registry `orientation` field
5. Lock stack choice and module selection

**Note:** PID is generated HERE (Phase 4), not Phase 1 (AgentBuild's default). The pipeline delays PID until after design because design complexity informs tech stack.

#### Phase 5: Environment Bootstrap

**Route to:** `.claude/skills/Custom/AgentBuild/Workflows/FullBuild.md` — Phase 1b (repo init) + Phase 1c (hello-world gate).

1. Initialize repo at registered path
2. Generate: directory structure, package config, linting, CI, README, AGENTS.md
3. Commit `design-system/MASTER.md` to repo
4. Place component files from Phase 3 in `design/reference/`
5. Commit persona and UX spec files to `docs/specs/`
6. Run hello-world gate — CI MUST be green before proceeding

**Gate:** CI green on hello-world test. Non-negotiable.

#### Phase 5b: Component Code Quality Validation

**Route to:** WebDesign child skills based on chosen framework:

| Stack | Route To |
|-------|----------|
| React / Next.js | `.claude/skills/WebDesign/react-best-practices/SKILL.md` + `.claude/skills/WebDesign/composition-patterns/SKILL.md` |
| React Native | `.claude/skills/WebDesign/react-native-skills/SKILL.md` |
| HTML / Tailwind | `.claude/skills/WebDesign/web-design-guidelines/SKILL.md` |

1. Validate component architecture against framework-specific rules
2. Flag violations by priority (CRITICAL / HIGH / MEDIUM / LOW)
3. Produce validation report: `docs/component-validation.md`
4. Reference report in AGENTS.md so Build Loop agent knows constraints

**Gate:** Report produced. CRITICAL violations documented for Build Loop to address.

**Deliverables produced:**

| Artifact | Path |
|----------|------|
| Initialized repo | Git repo at registered path, CI green |
| AGENTS.md | `AGENTS.md` |
| Component validation | `docs/component-validation.md` |
| PID registry | `.claude/skills/Custom/AgentBuild/projects/PID-{hex}.json` |

---

### Zone 4: Specify (Phases 6, 7) — CONTAINERIZED

**Invoke:** `Specify/Workflows/RunSpecify.md`

**Cold-start from:** the git repo (which now contains personas, UX specs, MASTER.md, components, AGENTS.md)

**What happens:**
- Phase 6: Happy path specs → Edge cases (Council) → Failure modes (RedTeam) → Constraints → IterativeDepth review
- Phase 7: Spec directory structure created, committed to git

**Deliverables produced:**

| Artifact | Path |
|----------|------|
| Feature specs | `docs/specs/features/[feature-name].md` |
| Constraint specs | `docs/specs/constraints/business-rules.md` |
| Spec index | `docs/specs/MASTER.md` |

**Session boundary recommendation:** Council(5) + Research + IterativeDepth can consume 50-100k+ tokens. Start a new session before entering Build.

---

### Zone 5: Build (Phases 8, 8e) — CONTAINERIZED

**Invoke:** `Build/Workflows/RunBuild.md`

**Cold-start from:** the git repo (main branch, all specs committed, AGENTS.md, design-system/, component references)

**What happens:**
- Phase 8: 8-step Build Loop for each feature (PICK → TASK → BUILD → GATE → REVIEW → MERGE → OBSERVE → REPEAT)
- Phase 8e: Error Recovery invoked as needed (3-attempt budget, known-fixes library)

**Deliverables produced:**

| Artifact | Path |
|----------|------|
| Working code | Git `main` branch, CI green |
| Known fixes | `docs/known-fixes/*.md` |
| Updated AGENTS.md | `AGENTS.md` |

**Session boundary recommendation:** Context grows linearly with features. For 5+ features, consider breaking every 3-5 features. A new session cold-starts from the git repo.

---

### Zone 6: Ship (Phases 9-13) — INLINE (orchestrator runs directly)

These phases are checklists and evaluations — bounded context, mechanical execution.

#### Phase 9: Observability

**Route to:** `.claude/skills/Custom/AgentBuild/Workflows/FullBuild.md` — Phase 6.

Issue build task: Sentry integration, request logging, 3-5 business metric events, health check at `/health`. Verify via Browser.

**Output:** Observability stack running — Sentry receiving errors, request logs appearing, health check returning 200.

#### Phase 10: Environment Diagnosis

**Route to:** `.claude/skills/Custom/AgentBuild/Workflows/EnvironmentDiagnosis.md`

5-category diagnosis: Feedback Signal Quality, Constraint Enforcement, Context Completeness, Scope Clarity, Recovery Path.

**Output:** `docs/environment-diagnosis.md`

#### Phase 11: MVP Gate

**Route to:** `.claude/skills/Custom/AgentBuild/Workflows/MvpGate.md`

6-item gate: Core Value Demonstrable, CI Green on Main, Observability Live, Real User Confirmed, Environment Diagnosed, AGENTS.md Current.

**Output:** `docs/mvp-gate-report.md`

#### Phase 11b: Deploy to Railway

**Route to:** `.claude/skills/Custom/AgentBuild/Modules/DeployRailway.md`

CLI-first deployment: detect/install Railway CLI, authenticate, create project, set env vars, deploy, generate public URL, verify health check.

**Output:** `docs/deployment.md` (URL + date)

#### Phase 12: Measure Success

**Route to:** `.claude/skills/Custom/AgentBuild/Workflows/MeasureSuccess.md`

Three-tier evaluation: Infrastructure (6 checks), User Journey (6 checks), Autonomous Recovery (6 checks). Combined maturity score: N/18.

**Output:** `docs/success-measurement.md`

#### Phase 13: Retrospective

**Route to:** `.claude/skills/Custom/AgentBuild/Workflows/BuildRetrospective.md`

Five-section review: Build Summary, Error Pattern Analysis, Spec Quality Assessment, Module & Infrastructure Assessment, Proposed Improvements.

**Output:** Retrospective report. Approved improvements applied. BuildHistory.md updated.

---

## Pipeline Complete

When Phase 13 is done:
1. Update PID registry: `currentPhase: "complete"`, `status: "complete"`
2. Record maturity score in PID registry
3. Report live Railway URL to user
4. The next build starts with a smarter system

---

## Summary: Phase → Zone → Source

| Phase | Name | Zone | Source |
|-------|------|------|--------|
| 0 | Orientation | Discovery (containerized) | AgentBuild FullBuild Phase 0 |
| 0b | Idea Refinement | Discovery (containerized) | AgentBuild IdeaRefinement |
| 1 | Design System | Design (containerized) | Design Stack FullDesign Phase 2 |
| 2 | Mockups | Design (containerized) | Design Stack FullDesign Phase 3 |
| 3 | Components | Design (containerized) | Design Stack FullDesign Phase 4 |
| 4 | Tech Stack | Scaffold (inline) | AgentBuild FullBuild Phase 1 |
| 5 | Environment | Scaffold (inline) | AgentBuild FullBuild Phase 1b-1c |
| 5b | Validation | Scaffold (inline) | WebDesign child skills |
| 6 | Knowledge Capture | Specify (containerized) | AgentBuild FullBuild Phase 2 + EdgeCaseGeneration |
| 7 | Spec Repository | Specify (containerized) | AgentBuild FullBuild Phase 3 |
| 8 | Build Loop | Build (containerized) | AgentBuild BuildLoop |
| 8e | Error Recovery | Build (containerized) | AgentBuild ErrorRecovery |
| 9 | Observability | Ship (inline) | AgentBuild FullBuild Phase 6 |
| 10 | Env Diagnosis | Ship (inline) | AgentBuild EnvironmentDiagnosis |
| 11 | MVP Gate | Ship (inline) | AgentBuild MvpGate |
| 11b | Deploy | Ship (inline) | AgentBuild DeployRailway |
| 12 | Measure Success | Ship (inline) | AgentBuild MeasureSuccess |
| 13 | Retrospective | Ship (inline) | AgentBuild BuildRetrospective |
