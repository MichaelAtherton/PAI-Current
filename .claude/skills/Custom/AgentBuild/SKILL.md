---
name: AgentBuild
description: Orchestrates AI-driven software development from empty repo to deployed MVP. USE WHEN agentbuild, agent build, build with agents, build software with AI, agentic software, no-code build, zero code build, build from idea, idea to MVP, build a product, build an app, build a tool, ship software with AI.
---

## Customization

**Before executing, check for user customizations at:**
`.claude/skills/PAI/USER/SKILLCUSTOMIZATIONS/AgentBuild/`

If this directory exists, load and apply any PREFERENCES.md, configurations, or resources found there. These override default behavior. If the directory does not exist, proceed with skill defaults.

## 🚨 MANDATORY: Voice Notification (REQUIRED BEFORE ANY ACTION)

**You MUST send this notification BEFORE doing anything else when this skill is invoked.**

1. **Send voice notification**:
   ```bash
   curl -s -X POST http://localhost:8888/notify \
     -H "Content-Type: application/json" \
     -d '{"message": "Starting AgentBuild — zero to MVP with no human-written code"}' \
     > /dev/null 2>&1 &
   ```

2. **Output text notification**:
   ```
   Running the **AgentBuild** skill — orchestrating AI-driven development from idea to MVP...
   ```

**This is not optional. Execute this curl command immediately upon skill invocation.**

# AgentBuild

**One orchestrating conductor. Zero human-written code. Idea to deployed MVP.**

AgentBuild guides the full arc of AI-native software development using the Agentic Build Framework (ABF). It does not implement software — it orchestrates Lucy's capabilities (Research, Council, RedTeam, Browser, Science, and the Algorithm) at exactly the right phases to produce working software without a human writing code.

**The mental model:** You are not writing software. You are designing a factory that produces software. Your job is specification, constraint, and environment. The agents do everything else.

## Core Concept: Complete-State Thinking

Before running this skill, internalize one idea:

> *Describe a system's intended behavior so completely — including edge cases, failure modes, and business logic — that a machine can build it without asking a follow-up question.*

This is the skill that makes the framework work. Every phase below is a structured way to practice it.

---

## Active Project Check & PID Gate (Before Routing)

**On every AgentBuild invocation, before routing to any workflow:**

### Step 1: Load Project Registry

1. Read all `PID-*.json` files in `projects/` directory
2. Filter to `status: "active"` projects
3. Route based on what's found:

**No active projects:**
> Route directly to Workflow Routing below (new project — PID will be generated in Phase 1a).

**One active project:**
> "You have an active project: **[name]** (`[id]`) — currently at Phase [currentPhase].
> Repo: `[repoPath]`
>
> Continue with this project, or start a new one?"
>
> If continue → load PID into session context, `cd` to repoPath, read AGENTS.md, resume at currentPhase.
> If new → route to Workflow Routing below.

**Multiple active projects:**
> "You have [N] active AgentBuild projects:
>
> 1. **[name]** (`PID-{id}`) — Phase [currentPhase] — `[repoPath]`
> 2. **[name]** (`PID-{id}`) — Phase [currentPhase] — `[repoPath]`
> ...
>
> Which project would you like to continue, or would you like to start a new one?"
>
> If selected → load PID into session context, `cd` to repoPath, read AGENTS.md, resume at currentPhase.
> If new → route to Workflow Routing below.

### Step 2: PID Gate Enforcement (Non-Negotiable)

**Before ANY write operation to a project repo, Lucy must have a valid PID loaded.**

This is the Clerk authentication pattern applied to projects: no `userId`, no access. No `projectId`, no changes.

**Gate check sequence:**

```
1. Is there an active PID in session context?
   → NO: HALT. "Which project are you working on?" List active projects.

2. Does the PID match a registered project in projects/PID-{id}.json?
   → NO: HALT. "PID-{id} not found in registry."

3. Does the repoPath in the registry match where we're about to write?
   → NO: WARN. "You're about to write to {path} but PID-{id} is registered at {repoPath}."
```

**If any check fails → do not write. Resolve first.**

**Why:** Without the gate, multi-project work risks writing project A's code into project B's repo. The PID gate makes cross-contamination structurally impossible.

**Project registry location:** `.claude/skills/AgentBuild/projects/`
**Schema documentation:** `projects/README.md`

---

## Workflow Routing

| Trigger | Workflow |
|---------|----------|
| New project (default) | `Workflows/FullBuild.md` |
| "phase 0", "start over", "new idea" | `Workflows/FullBuild.md` — Phase 0 |
| "refine my idea", "challenge my assumptions", "help me think through this", "I have a rough idea" | `Workflows/IdeaRefinement.md` |
| "phase 2", "spec", "edge cases", "generate edge cases" | `Workflows/EdgeCaseGeneration.md` |
| "build loop", "next feature", "build this spec" | `Workflows/BuildLoop.md` |
| "environment", "agents keep failing", "fix environment" | `Workflows/EnvironmentDiagnosis.md` |
| "MVP gate", "are we ready", "check MVP" | `Workflows/MvpGate.md` |
| "measure success", "what tier", "are we successful" | `Workflows/MeasureSuccess.md` |
| "fix error", "error recovery", "autonomously recover", "agents keep failing" | `Workflows/ErrorRecovery.md` |
| "create module", "new module", "build a module", "add integration", "module builder" | `Workflows/ModuleBuilder.md` |
| "module error", "fix the module", "module doctor", "module is wrong", "this error came from the module" | `Workflows/ModuleDoctor.md` |
| "retrospective", "build retrospective", "what did we learn", "improve AgentBuild" | `Workflows/BuildRetrospective.md` |

**Default:** If no specific phase is referenced, route to `Workflows/FullBuild.md` and begin at Phase 0.

---

## The ABF Phases (Quick Reference)

| Phase | Name | Human Owns | Agent Owns | Key PAI Skills |
|-------|------|-----------|-----------|----------------|
| 0 | Orientation | Two sentences | Nothing yet | Algorithm |
| 1 | Environment Bootstrap | Toolchain decisions | Repo init, AGENTS.md, CI, hello-world | — |
| 2 | Knowledge Capture | Happy path specs, constraint decisions | Edge case generation, failure modes, synthetic personas | Research, Council, RedTeam |
| 3 | Spec Repo Setup | Review and approve | Structure creation | — |
| 4 | Build Loop | Task issuance, PR review (correctness only) | Implementation, tests, CI | Browser |
| 5 | Environment Design | Diagnosis decisions | Environment capability gap analysis | Science |
| 6 | Observability | Dashboard review | Setup and configuration | Browser |
| MVP Gate | Readiness check | Gate evaluation | — | — |

---

## Human Attention Model

The bottleneck is human attention. Spend it here:

**Humans own (cannot delegate):**
- The two orientation sentences (Phase 0)
- Toolchain selection (Phase 1)
- Happy path specifications (Phase 2a)
- Edge case include/exclude decisions (Phase 2b)
- Business constraint documentation (Phase 2d)
- Build task issuance (Phase 4)
- PR correctness review — 3 questions only (Phase 4)
- Environment diagnosis decisions (Phase 5)
- MVP gate evaluation

**Agents own (zero human time):**
- Repo initialization and structure
- AGENTS.md creation and updates
- CI/CD configuration
- Code implementation
- Test writing
- Edge case generation
- Failure mode specification
- Observability setup

---

## Integration

### Uses (PAI Skills Invoked)
- **Research** — Domain failure mode research; synthetic user persona generation (Phase 2b)
- **Council** — 5-agent synthetic user protocol; spec debate and gap-finding (Phase 2b)
- **RedTeam** — Adversarial spec analysis; finds what breaks before build starts (Phase 2c)
- **FirstPrinciples** — Business logic decomposition; surface tacit rules (Phase 2d)
- **IterativeDepth** — Multi-angle spec completeness review (Phase 3)
- **Science** — Environment capability gap diagnosis; hypothesis-test-analyze cycle (Phase 5)
- **Browser** — Visual verification of running product; observability dashboard confirmation (Phase 4, 6)
- **Documents** — AGENTS.md processing and formatting (Phase 1, 5)
- **THEALGORITHM** — ISC tracking throughout; PRD maintains build state across sessions

### Feeds Into
- **AgentBuild** itself (iterative — each new feature restarts at Phase 2)
- Any deployed product (the output IS the product)

---

## Key Reference Files

### Spec Formats
- `Agentsmd.md` — AGENTS.md template and update protocol
- `SpecFeature.md` — Feature specification format (FEATURE/USER/ACTION/RESULT)
- `SpecConstraint.md` — Business constraint format (CONSTRAINT/RULE/VIOLATION/ENFORCEMENT)
- `BuildTask.md` — Build task format (SPEC/SCOPE/CONSTRAINTS/DONE WHEN)

### Workflows
- `Workflows/FullBuild.md` — Complete phase-by-phase orchestration
- `Workflows/IdeaRefinement.md` — Phase 0b: UX consultant discovery session (JTBD, personas, Level 3 UX spec)
- `Workflows/BuildLoop.md` — The 8-step build cycle
- `Workflows/EdgeCaseGeneration.md` — 5-persona Synthetic User Protocol + Constraint Mining Session
- `Workflows/EnvironmentDiagnosis.md` — 5-category environment capability analysis
- `Workflows/MvpGate.md` — MVP readiness checklist
- `Workflows/MeasureSuccess.md` — Three-tier success model + maturity score
- `Workflows/ErrorRecovery.md` — Error classification, 3-attempt budget, escalation path
- `Workflows/ModuleBuilder.md` — Deep-research module creation with stack branching (DRAFT→BETA→STABLE)
- `Workflows/ModuleDoctor.md` — Trace build errors to module documentation gaps, patch modules
- `Workflows/BuildRetrospective.md` — Post-MVP learning extraction + skill improvement proposals

### IaC Modules (Pre-solved infrastructure)
- `Modules/FrameworkNextjs.md` — Next.js App Router (file conventions, server/client components, version-specific patterns, proxy/middleware)
- `Modules/FrameworkReactSpa.md` — React SPA (Vite + React Router v7 Data Mode + TanStack Query v5 + Zustand; client-only SPAs)
- `Modules/AuthClerk.md` — Clerk.dev authentication (sessions, JWT, social login)
- `Modules/DbSupabase.md` — Supabase Postgres (RLS, real-time, file storage)
- `Modules/DeployRailway.md` — Railway deployment (zero-config, auto-deploy, HTTPS)
- `Modules/ObservabilitySentry.md` — Sentry + Pino (error tracking, structured logging)
- `Modules/SlackIntegration.md` — Slack messaging (Socket Mode, session isolation, streaming, access control)
- `Modules/ChatInterface.md` — Chat UI (assistant-ui, streaming, tool visualization, theming)

### Project Registry
- `projects/README.md` — Registry schema documentation and multi-project behavior
- `projects/{slug}.json` — One file per active project (repo path, phase, orientation, stack)

---

## The Non-Negotiable Rule

**The hello-world gate (Phase 1d) must pass before writing a single spec.**

If CI is not green on a trivial test before specification begins, the factory is broken. No amount of excellent specification fixes a broken factory. Phase 1 is complete when — and only when — CI passes on a generated hello-world. Do not proceed otherwise.
