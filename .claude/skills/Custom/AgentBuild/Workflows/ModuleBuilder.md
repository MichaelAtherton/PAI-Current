# Workflow: ModuleBuilder

> Create high-quality AgentBuild modules through deep research, stack-aware branching, and iterative validation. Modules are AI-consumed specifications — not human tutorials.

**Invoke when:** "create module", "new module", "build a module", "add integration", "module builder", or when Phase 1 identifies a needed integration that has no existing module

---

## Core Philosophy

> **Modules are consumed by AI agents, not humans. They must be executable specifications — deterministic, branching, validatable — not prose tutorials.**

A module is correct when an AI agent following its instructions produces a working integration on first build, for any supported tech stack, without asking a follow-up question.

### What Makes AI-Consumed Instructions Different

| Dimension | Human Tutorial | AI Module |
|-----------|---------------|-----------|
| **Reader** | Developer with context and intuition | LLM with no prior state |
| **Format** | Narrative prose, screenshots, "try this" | Deterministic steps with validation after each |
| **Branching** | "For Next.js users, do X" | `WHEN: nextjs` → Section A |
| **Error handling** | "You might see this error..." | Error pattern → exact cause → exact resolution |
| **Idempotency** | Assumed | Required — running twice must not break things |
| **Validation** | "Verify it works" | Specific check command with expected output |
| **Dependencies** | Listed at top | Per-stack dependency tree with exact versions |
| **Vendor interaction** | "Go to the dashboard and..." | CLI/API/MCP first, dashboard fallback only |

### CLI-First Interaction Hierarchy (Non-Negotiable)

> **Modules interact with vendors programmatically first. Dashboard/GUI is always a labeled fallback, never the primary path.**

Every module that integrates with an external vendor MUST follow this hierarchy:

```
1. MCP Server (highest autonomy — Claude calls vendor API natively via tool calls)
2. Vendor CLI (high autonomy — Lucy runs commands programmatically)
3. Vendor REST API (direct HTTP calls when no CLI/MCP exists)
4. Dashboard / GUI (FALLBACK ONLY — labeled "Only When CLI Is Unavailable")
```

**Why:** The entire point of AgentBuild is that agents own infrastructure. An instruction like "go to the Supabase dashboard and click Create Table" requires a human. An instruction like `supabase db push` requires zero humans. CLI-first is what makes autonomous builds possible.

**Every module MUST include:**
- **Step 0: Detect and Install CLI** — check if vendor CLI exists, offer install via AskUserQuestion
- **Authentication flow** — `vendor login` or token-based auth before any operations
- **CLI-driven operations** — all setup, config, and deployment via CLI commands
- **Dashboard Fallback section** — clearly labeled "(Only When CLI Is Unavailable)" at the bottom

### Module Status Progression

```
DRAFT → BETA → STABLE

DRAFT:   Written, not validated. May have gaps.
BETA:    Passed dry run + RedTeam. Ready for first real use.
STABLE:  Used successfully in at least 1 real AgentBuild project.
```

A module is NOT marked STABLE until a real build uses it without triggering ModuleDoctor.

---

## Tech Stack Detection Model

**Modules do NOT ask the user about their tech stack. They detect it.**

By the time a module is invoked, the stack is already known from Phase 1 of FullBuild:

```
Detection priority (first match wins):

1. PID Registry    → Read projects/PID-xxx.json → stack.framework
                     Always available for active AgentBuild projects.

2. package.json    → Detect framework from dependencies:
                     @clerk/nextjs     → nextjs
                     next              → nextjs
                     express           → express
                     @clerk/clerk-react → react
                     vite              → react (SPA)

3. Directory scan  → Detect from project structure:
                     app/ + next.config.* → nextjs
                     src/index.ts + no next → express or react
                     vite.config.*     → react (Vite)

4. Ask user        → LAST RESORT. Should almost never happen.
                     "I couldn't detect your framework. Are you using
                     Next.js, Express, or React (Vite/CRA)?"
```

**The module receives stack context — it doesn't discover it.** This means every module section that differs by framework uses `WHEN:` conditional blocks, and the consuming agent selects the right path automatically.

---

## The 5-Phase Creation Process

### Phase 1: Vendor Research (Deep, Not Cursory)

**This phase determines 80% of module quality.** Bad research = bad module = errors in every project.

**Spawn 5 Research agents in parallel, each with a different angle:**

#### Agent 1: Docs Agent

```
CONTEXT: We are building an AgentBuild module for [vendor]. This module will be
consumed by AI agents (not humans) during automated software builds. The module
must produce a working integration on first build.

TASK: Research the official [vendor] documentation for integration with:
  - Next.js (App Router)
  - Express / Node.js
  - React SPA (Vite)

For EACH framework, extract:
  1. Exact npm package name and current version
  2. Every file that must be created (exact path + exact content)
  3. Every environment variable (exact name, format, validation rule)
  4. Every import path (exact, not from memory)
  5. Setup order (what must happen before what)
  6. The simplest possible working example

DEPTH: Read the ACTUAL documentation pages. Do not summarize from memory.
Check for framework-specific setup guides on the vendor's site.

EFFORT LEVEL: Extended. Return with source URLs for every claim.

OUTPUT: Structured integration steps per framework with source citations.
```

#### Agent 2: Migration Agent

```
CONTEXT: Same as above.

TASK: Research [vendor]'s version history and breaking changes:
  1. Current major version and release date
  2. Breaking changes in the last 2 major versions
  3. Deprecated APIs still commonly referenced online
  4. Renamed methods, moved import paths, changed file conventions
  5. Migration guides between versions
  6. Any upcoming breaking changes announced

DEPTH: Check the vendor's changelog, GitHub releases, and migration docs.
Old blog posts and tutorials are the #1 source of stale module instructions.

EFFORT LEVEL: Extended. Return with version-specific notes.

OUTPUT: Version timeline with breaking changes and migration notes.
```

#### Agent 3: Community Agent

```
CONTEXT: Same as above.

TASK: Research real-world failure patterns for [vendor] integration:
  1. Top 10 GitHub issues (label: bug) in the last 6 months
  2. Top 10 Stack Overflow questions about [vendor] + [each framework]
  3. Common error messages and their actual root causes
  4. Environment-specific gotchas (CI, Docker, serverless, edge runtime)
  5. Things the official docs don't mention but real users hit

DEPTH: Read actual issue threads and SO answers, not just titles.
We need the exact error messages and exact resolutions.

EFFORT LEVEL: Extended. Return error message → cause → fix triples.

OUTPUT: Known failure patterns with exact error strings and resolutions.
```

#### Agent 4: Pattern Agent

```
CONTEXT: Same as above.

TASK: Find 3-5 open-source projects that use [vendor] in production:
  1. Search GitHub for repos importing [vendor SDK package name]
  2. Prioritize: >100 stars, active in last 6 months, uses TypeScript
  3. For each repo, extract:
     - How they initialize the vendor SDK
     - How they handle authentication/middleware
     - How they structure their integration files
     - Any patterns we should adopt or anti-patterns we should avoid

Also check: Does [vendor] have an official example repo or template?
If yes, extract its patterns — these are the vendor's blessed approach.

DEPTH: Read actual source files, not just READMEs.

EFFORT LEVEL: Extended. Return with file paths and code snippets.

OUTPUT: Integration patterns from real codebases with source links.
```

#### Agent 5: CLI & MCP Agent

```
CONTEXT: Same as above.

TASK: Research [vendor]'s programmatic access options for AI agent autonomy:
  1. Does [vendor] offer a CLI tool? What is it called? Install method?
     (npm, Homebrew, curl, standalone binary)
  2. Does [vendor] offer an MCP server for AI agent integration?
     Check: vendor docs, npmjs.com (@vendor/mcp-server), vendor/agents page
  3. What operations does the CLI support? (create, deploy, configure, logs, etc.)
  4. What operations does the MCP server expose? (tool names, capabilities)
  5. Authentication methods: token-based? OAuth? Browser login?
     Can auth be non-interactive (CI/token-based)?
  6. Does the CLI support programmatic env var / secret management?
  7. What operations REQUIRE the dashboard (cannot be done via CLI/API)?
     These become the Dashboard Fallback section.

DEPTH: Install the CLI locally if possible. Run --help. Check the MCP server
npm page for tool documentation. We need to know exactly what Lucy can do
autonomously vs what requires human dashboard interaction.

EFFORT LEVEL: Extended. Return with CLI command reference and MCP capabilities.

OUTPUT: CLI tool name + install method, MCP server package (if exists),
        command/capability inventory, auth flow, dashboard-only operations.
```

#### Research Validation Gate

**Before proceeding to Phase 2, validate research quality:**

```
RESEARCH VALIDATION:
  [ ] All 5 agents returned substantive results (not thin summaries)
  [ ] Source URLs are real vendor documentation (not blog posts or outdated tutorials)
  [ ] Version numbers match the current vendor release
  [ ] Framework-specific steps exist for each supported stack
  [ ] Failure patterns include exact error messages (not vague descriptions)
  [ ] Import paths are verified against current package versions
  [ ] No agent returned "I couldn't find documentation for this"
  [ ] CLI tool identified with install method, OR confirmed vendor has no CLI
  [ ] MCP server checked (npmjs.com, vendor/agents page), availability documented
  [ ] Dashboard-only operations identified (operations with no CLI/API equivalent)

If ANY check fails → send that agent back with a more specific prompt.
Do NOT proceed with incomplete research.
```

---

### Phase 2: Stack Matrix Generation

Synthesize research into a structured matrix of every supported stack path.

**Template:**

```markdown
## Stack Matrix: [Vendor]

### nextjs
- **Package:** [exact name]@[version constraint]
- **Install:** `npm install [package]`
- **Files to create:**
  - `[path]` — [purpose] — [detection logic if path varies]
- **Files to modify:**
  - `[path]` — [what to add/change]
- **Env vars:**
  - `[NAME]` — format: `[pattern]` — required: [yes/no]
- **Import paths:**
  - `[import statement]` — from `[exact module path]`
- **Setup order:** [numbered sequence, dependencies noted]
- **Pre-flight checks:** [validation commands]
- **Version variants:**
  - [framework version] → [what differs]

### express
[Same structure]

### react
[Same structure]
```

**For each stack path, verify:**
- Dependencies actually exist on npm (check with `npm view [package] version`)
- Import paths are correct for current package version
- File paths follow framework conventions
- No circular dependencies between setup steps

---

### Phase 3: Module Drafting (Structured Authoring)

Write the module following the evolved format. This is specification authoring, not prose writing.

#### Evolved Module Format

```markdown
# Module: [Category] — [Vendor]

> [One sentence: what this provides]

**Module status:** DRAFT (v1 — created [date])
**When to use:** [conditions]
**When NOT to use:** [conditions]

---

## What This Module Provides

| Capability | What You Get |
|-----------|--------------|
| [cap] | [description] |

---

## Tech Stack Detection

Source: PID registry → package.json → directory structure

| Detection Signal | Stack | SDK Package |
|-----------------|-------|-------------|
| [signal] | [stack] | [package] |

---

## Environment Variables

### DETECT: deployment environment

### WHEN: development
[Dev-specific env setup, keyless mode if available]

### WHEN: production
[Production env setup with exact var names and formats]

**Validation:**
```bash
# Verify env vars are correctly set
[validation commands per var]
```

---

## Vendor CLI Workflow (CLI-First — Autonomous)

> **Lucy operates programmatically via the vendor CLI. The Dashboard is a fallback only — used when the CLI is unavailable or the user explicitly prefers it.**

### Step 0: Detect and Install Vendor CLI

**Lucy MUST check for the CLI before any setup work.** This is the gate.

```bash
# Check if vendor CLI is installed
[vendor-cli] --version 2>/dev/null
```

**If installed:** Proceed to Step 1.

**If NOT installed:** Use AskUserQuestion to prompt:

```
"The [vendor] CLI is required to set up [vendor] programmatically.
Should I install it?"

Options:
1. "Yes, install via npm" → run: npm install -g [package]
2. "Yes, install via Homebrew" → run: brew install [tap/package]
3. "No, I'll use the Dashboard instead" → switch to Dashboard Fallback section
```

### Step 1: Authenticate

```bash
# Check if already authenticated
[vendor-cli] whoami 2>/dev/null
```

**If NOT authenticated:** Use AskUserQuestion:
```
"[Vendor] CLI needs authentication.
Please run `[vendor-cli] login` in a separate terminal, then tell me when you're done."
```

**Alternative (non-interactive):** If the user has a token:
```bash
export [VENDOR]_TOKEN=your-token-here
[vendor-cli] whoami  # Verify it works
```

### Step 2: Link or Initialize Project

```bash
# Check if already linked to a [vendor] project
[vendor-cli] status 2>/dev/null
```

**If NOT linked:**
```bash
# Option A: Link to existing project
[vendor-cli] link

# Option B: Create new project
[vendor-cli] init
```

### Step 3+: [Vendor-specific setup steps]

[Each step uses CLI commands with verify blocks]

#### Verify: Step N
```bash
[verification command] && echo "PASS" || echo "FAIL: [what to check]"
```

---

## MCP Server Integration (If Available)

> **If the vendor offers an MCP server, document it here for highest-autonomy agent access.**

### Setup
```bash
claude mcp add [vendor]-mcp-server -- npx -y @[vendor]/mcp-server
```

**Requires:** `[VENDOR]_TOKEN` environment variable.

### MCP Capabilities
| Command | What It Does |
|---------|-------------|
| [document each MCP tool the vendor exposes] |

### When to Use MCP vs CLI
| Scenario | Use |
|----------|-----|
| [programmatic setup from scratch] | MCP |
| [deploy local code changes] | CLI |
| [read logs / debug] | Either |

> **If the vendor does NOT offer an MCP server:** Remove this section entirely from the generated module. Do not include an empty placeholder.

---

## Implementation (Framework-Specific Code)

### WHEN: nextjs

#### Step 1: Install Dependencies
```bash
[exact install command]
```
#### Verify: Step 1
```bash
[verification command] && echo "PASS" || echo "FAIL: [what to check]"
```

#### Step 2: [Next step]
[exact code with exact file path]
#### Verify: Step 2
```bash
[verification command]
```

[Continue for all steps...]

### WHEN: express
[Same pattern — steps with verify blocks]

### WHEN: react
[Same pattern]

---

## AGENTS.md Additions

[Block to add to project AGENTS.md — must describe CLI-first workflow, not Dashboard steps]

---

## Pre-Flight Validation (MANDATORY Before First Build)

```bash
# Run ALL checks before attempting build
[comprehensive validation script covering all steps]
```

---

## Known Issues & Fixes

| Issue | Error Message | Stack | Cause | Fix |
|-------|--------------|-------|-------|-----|
| [pre-populated from Community Agent + CLI Agent research] |
| CLI not installed | "command not found: [vendor]" | All | CLI not in PATH | Install via npm or Homebrew (Step 0) |
| Auth token missing | "[vendor]: not authenticated" | All | No login or token | Run `[vendor] login` or set token env var |

---

## Test Coverage Required

[Test stubs per stack]

---

## Dashboard Fallback (Only When CLI Is Unavailable)

> **Use this ONLY when the vendor CLI cannot be installed or the user explicitly requests it.**

If Lucy cannot use the CLI:

1. Direct the user to the vendor's dashboard
2. Provide a checklist of manual setup steps
3. Note which operations are dashboard-only (no CLI equivalent)

### Development
- [ ] [manual steps]

### Production
- [ ] [manual steps]

---

## Module Philosophy

**If this module's instructions produce a build failure, that's a bug in the module — not in the agent or the code.** Every instruction must be precise enough that an AI agent following them step-by-step produces a working integration on first build, for any supported tech stack.

---

*Module created by ModuleBuilder. v1 created [date].*
```

#### Council Review (5 Perspectives)

After drafting, invoke **Council** with 5 agents reviewing the module:

```
Council prompt: "Five agents will each review this module draft from a
different perspective. The module is consumed by AI agents, not humans.

[PASTE FULL MODULE DRAFT]

Agent 1 — First-Time Agent: You've never used [vendor] before. Follow
  these instructions step by step. Where do you get stuck? Where is a
  step ambiguous? Where would you have to guess?

Agent 2 — Experienced Agent: You know [vendor] well. What does this
  module get wrong? What's outdated? What common pattern is missing?

Agent 3 — CI/CD Agent: You're running this in a fresh container with
  no prior state. What fails? Missing system deps? Env var issues?
  File permission problems?

Agent 4 — Security Agent: Where might credentials leak? Are there
  timing issues with secret loading? Does the module accidentally
  expose keys in logs, error messages, or client bundles?

Agent 5 — ModuleDoctor Agent: Based on your experience fixing modules,
  what will break first when a real project uses this? What Known
  Issue is missing? What pre-flight check is incomplete?

Agent 6 — CLI-First Agent: Does this module follow the CLI-first
  interaction hierarchy? Specifically:
  1. Is the vendor CLI workflow the PRIMARY path (not Dashboard)?
  2. Does Step 0 detect and offer to install the CLI?
  3. Is there an authentication step before operations?
  4. Are ALL setup operations done via CLI commands, not 'go to dashboard'?
  5. Is the MCP server documented (if the vendor offers one)?
  6. Is the Dashboard section labeled 'Fallback' and placed at the bottom?
  7. Does the AGENTS.md additions block describe CLI commands, not GUI steps?
  Flag any instruction that tells the agent to use the Dashboard when
  a CLI equivalent exists.

For each finding: state the section, the problem, and the fix."
```

**Address all Council findings before proceeding to Phase 4.**

---

### Phase 4: Dry Run Validation

Before promoting to BETA, validate the module without running a real build.

#### 4a: Static Walkthrough

Walk through every instruction path for every supported stack:

```
For each WHEN block:
  For each step:
    1. Does this step's output enable the next step's input?
    2. Is the file path deterministic (or does it need detection logic)?
    3. Is the code syntactically valid?
    4. Are the import paths correct for the current package version?
    5. Is the verify command actually testing what the step produces?

Flag any gaps as: STEP_GAP: [between step N and N+1] — [what's missing]
```

#### 4b: Dependency Verification

```bash
# For each package in the Stack Matrix:
npm view [package-name] version  # Does it exist? What's current?
npm view [package-name] dependencies  # What does it pull in?
```

#### 4c: Version Currency Check

```
For each vendor API reference in the module:
  1. Is this API still current? (check vendor docs)
  2. Has this been deprecated or renamed? (check Migration Agent findings)
  3. Is the import path still valid? (check package exports)
```

#### 4d: RedTeam Stress Test

Invoke **RedTeam** against the complete module:

```
RedTeam prompt: "Adversarially analyze this AgentBuild module that will
be used by AI agents to set up [vendor] integration.

[PASTE FULL MODULE]

Focus on:
  1. Steps that assume a specific directory structure without checking
  2. Steps that work locally but fail in CI/Docker/serverless
  3. Race conditions in setup order (installing before env vars exist)
  4. Missing error states (what if the vendor API is down? rate limited?)
  5. Version assumptions that will break in 6 months
  6. Steps where the verify command doesn't actually catch failure
  7. Security: credentials in wrong files, keys in client bundles, log exposure
  8. CLI not installed: What happens if the vendor CLI is missing? Does Step 0
     detect this and offer installation, or does it silently fail?
  9. Auth token missing: What happens if the user hasn't authenticated?
     Does the module handle this gracefully with AskUserQuestion?
  10. MCP server unavailability: If the module references an MCP server,
      what happens when VENDOR_TOKEN is not set? Does it fall back to CLI?
  11. Dashboard creep: Are there ANY instructions that tell the agent to
      use the Dashboard when a CLI command exists for that operation?

For each finding: severity (CRITICAL/MODERATE/LOW), the instruction,
the failure scenario, and the fix."
```

**Address all CRITICAL and MODERATE findings. LOW findings go to Known Issues.**

#### 4e: Promotion Gate

```
BETA PROMOTION CHECKLIST:
  [ ] All 5 Research agents returned deep results with source citations
  [ ] Stack Matrix covers all supported frameworks
  [ ] Every step has a Verify block
  [ ] Council review findings addressed (all 6 perspectives)
  [ ] Static walkthrough found no step gaps
  [ ] All dependencies verified to exist at expected versions
  [ ] No deprecated APIs referenced
  [ ] RedTeam CRITICAL/MODERATE findings resolved
  [ ] Pre-flight validation script covers all steps
  [ ] Known Issues pre-populated from Community + CLI Agent research
  [ ] Module Philosophy section present
  [ ] CLI-first workflow is the PRIMARY path (not Dashboard)
  [ ] Step 0 detects vendor CLI and offers installation via AskUserQuestion
  [ ] Authentication step exists before any vendor operations
  [ ] MCP server documented if vendor offers one, omitted if not
  [ ] Dashboard section labeled "Fallback" and placed at bottom of module
  [ ] No instruction tells agent to "go to dashboard" when CLI equivalent exists

If ALL pass → promote to BETA.
If ANY fail → fix and re-check.
```

**After promotion:**

```markdown
**Module status:** BETA (v1 — created [date])
```

---

### Phase 5: Battle Testing (First Real Use)

The module becomes STABLE only after a real AgentBuild project uses it.

**Track the first real use:**

```
BATTLE TEST LOG:
  Project: [PID-xxx]
  Module: [name] v[version] (BETA)
  Stack: [framework detected]

  Build attempt 1:
    Result: [SUCCESS / FAIL]
    If FAIL:
      Error: [exact message]
      Root cause: [module instruction gap / code error / env issue]
      ModuleDoctor invoked: [YES/NO]
      Module patched: [what changed]

  Build attempt N:
    Result: [SUCCESS]

  PROMOTION:
    First successful build: attempt [N]
    ModuleDoctor invocations: [count]
    Known Issues discovered: [count]
    Patches applied: [list]

    → Promote to STABLE (v[N+patches])
```

**After successful first use:**

```markdown
**Module status:** STABLE (v[N] — updated [date])
**Proven on:** 1 AgentBuild project ([PID])
```

The "Proven on" count increments with each successful project use.

---

## Module Lifecycle (Complete Picture)

```
ModuleBuilder Phase 1-3   → DRAFT module created from deep research
ModuleBuilder Phase 4     → BETA after dry run + RedTeam validation
ModuleBuilder Phase 5     → STABLE after first real successful build
                               ↓
                     Module used in projects
                               ↓
                     Error occurs in build
                               ↓
               ErrorRecovery → identifies module gap
                               ↓
               ModuleDoctor → patches module (version bump)
                               ↓
               Patched module → better for next project
                               ↓
                          Repeat forever
```

**Three workflows, one system:**
- **ModuleBuilder** — creates modules correctly from deep research
- **ModuleDoctor** — fixes modules when real usage reveals gaps
- **ErrorRecovery** — detects when code errors are actually module gaps, triggers ModuleDoctor

---

## Integration

### Invoked By
- `Workflows/FullBuild.md` — Phase 1, when a needed integration has no existing module
- Direct user invocation via trigger phrases
- `SKILL.md` routing table

### Invokes (PAI Skills)
- **Research** — 4 parallel agents for deep vendor documentation research (Phase 1)
- **Council** — 5-perspective module draft review (Phase 3)
- **RedTeam** — Adversarial stress testing before BETA promotion (Phase 4)
- **Browser** — Verify vendor docs are current, check dashboard setup (Phase 1, 4)

### Feeds Into
- `Modules/*.md` — The created module file
- `Workflows/ModuleDoctor.md` — Handles post-creation fixes
- `Workflows/ErrorRecovery.md` — Detects module gaps during builds
- `Workflows/BuildRetrospective.md` — Module quality metrics

### Updates
- `SKILL.md` — Key Reference Files → IaC Modules section (adds new module)
- `Workflows/FullBuild.md` — Phase 1 available modules list (adds new module)

---

## Creating a Module (Quick Reference)

```
1. INVOKE: ModuleBuilder
2. SPECIFY: What vendor/service to integrate
3. WAIT: 4 Research agents return deep findings
4. REVIEW: Stack Matrix generated from research
5. REVIEW: Module draft with Council feedback addressed
6. GATE: Dry Run + RedTeam validation → BETA
7. USE: First real project build → STABLE
```

**Estimated time:** Phase 1-4 can complete in one session (~15-30 min with parallel research agents). Phase 5 happens organically when the module is first used in a real build.

---

*Workflow created for AgentBuild. Designed 2026-02-21. Updated 2026-02-22: CLI-first philosophy enforcement — Agent 5 (CLI & MCP), Agent 6 (CLI-First Council), CLI-first module template, RedTeam CLI scenarios, promotion gate CLI checks.*
