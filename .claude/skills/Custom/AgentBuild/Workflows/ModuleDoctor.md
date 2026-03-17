# Workflow: ModuleDoctor

> Trace build errors back to module documentation gaps and fix the module — not just the code. Every error is evidence that the module's instructions weren't precise enough.

**Invoke when:** "module error", "fix the module", "module doctor", "module is wrong", "this error came from the module", or when ErrorRecovery escalates with root cause `module_gap`

---

## Core Philosophy

> **If an agent faithfully follows a module's instructions and the build fails, the module is broken. Fix the module. The code fix is a side effect.**

This skill does NOT debug application code. It investigates WHY the module's instructions produced code that failed, then patches the module so no future project ever hits the same error.

The distinction matters:
- **ErrorRecovery** fixes code in THIS project (scope: `src/`, output: code patch)
- **ModuleDoctor** fixes the module for ALL future projects (scope: `Modules/*.md`, output: documentation patch)

---

## When ModuleDoctor Gets Invoked

### Path 1: ErrorRecovery Escalation (Automatic)

```
BuildLoop → CI fails → ErrorRecovery invoked →
  ErrorRecovery classifies error →
    Root cause: agent followed module instructions correctly, but instructions were wrong →
      ErrorRecovery escalates to ModuleDoctor with:
        - The error message
        - The module that was followed
        - What the agent did (the code it wrote)
        - Why ErrorRecovery believes the module is at fault
```

### Path 2: Direct Invocation (Manual)

The user pastes a terminal error and says something like:
- "This error came from following the AuthClerk module"
- "The deploy module told the agent to do X and it broke"
- "Fix the module — this keeps happening"

---

## The Three Root Cause Types

Every module error has exactly one of three root causes. Classify before investigating.

| Type | What Happened | Signal | Example |
|------|--------------|--------|---------|
| **WRONG** | Module instruction is factually incorrect | Agent did exactly what module said, result is wrong | "Put middleware in root" but project has `src/` directory |
| **INCOMPLETE** | Module omits a critical step | Agent followed all steps, but a gap between steps causes failure | No mention that `.env.local` takes precedence over `.env` in Next.js |
| **STALE** | Vendor API changed since module was written | Module was correct when written, now outdated | Next.js 16 renamed `middleware.ts` to `proxy.ts` |

The classification determines investigation strategy:
- **WRONG** → compare module instruction to vendor docs
- **INCOMPLETE** → find the missing step between last-working and first-failing instruction
- **STALE** → check vendor changelog for breaking changes since module version date

---

## The 7-Step Investigation Process

### Step 1: Intake & Triage

**Accept the error input.** The skill takes one of:
- Raw terminal output (paste)
- Build log excerpt
- CI failure output
- Runtime error with stack trace

**Identify the module.** Match the error domain to the responsible module:

| Error Domain | Module |
|-------------|--------|
| Authentication, Clerk, JWT, session, sign-in | `Modules/AuthClerk.md` |
| Database, Supabase, Postgres, RLS, query | `Modules/DbSupabase.md` |
| Deployment, Railway, hosting, build, port | `Modules/DeployRailway.md` |
| Error tracking, Sentry, logging, Pino | `Modules/ObservabilitySentry.md` |
| Slack, messaging, Socket Mode, bot | `Modules/SlackIntegration.md` |
| Chat UI, assistant-ui, streaming, tool vis | `Modules/ChatInterface.md` |

**If the error doesn't map to any module** → this is not a ModuleDoctor issue. Route back to ErrorRecovery.

**Output:**

```
INTAKE:
  Error: [exact error message]
  Module: [which module .md file]
  Error Domain: [auth/db/deploy/observability/slack/chat]
  Source: [ErrorRecovery escalation / direct user report]
```

---

### Step 2: Root Cause Classification

Read the identified module. Read the code the agent produced. Determine which root cause type applies.

**The diagnostic question:** "Did the agent follow the module's instructions faithfully?"

- **YES, and it still broke** → the module is WRONG or INCOMPLETE
- **YES, but the vendor changed** → the module is STALE
- **NO, the agent deviated** → this is NOT a module issue — route back to ErrorRecovery

**For WRONG vs INCOMPLETE:** Did the module address this scenario at all?
- If the module gave a specific instruction that caused the error → **WRONG**
- If the module never mentioned this scenario → **INCOMPLETE**

**Output:**

```
CLASSIFICATION:
  Root Cause Type: [WRONG / INCOMPLETE / STALE]
  Reasoning: [1-2 sentences explaining the classification]
  Module Section: [which section of the module is involved]
```

---

### Step 3: Trace to Module Line

**This is the accountability step.** Find and quote the EXACT section of the module that produced the wrong instruction. Not "the auth module needs updating" — but "the Environment Variables section says X, which caused error Y."

**For WRONG errors:**
> "Section 'Standard Implementation Pattern', Step 2, instructs: '[quote the instruction]'. This instruction causes [error] because [reason]."

**For INCOMPLETE errors:**
> "The module's '[section name]' covers [what it covers] but does NOT mention [what's missing]. An agent following these instructions has no guidance for [the scenario that failed]."

**For STALE errors:**
> "Section '[section name]' was written for [vendor version X]. The current vendor version is [Y], which changed [what changed]. The module's instruction '[quote]' no longer works because [reason]."

**Output:**

```
TRACE:
  Module File: [path]
  Section: [section name]
  Line Reference: [approximate location in the module]
  Quoted Instruction: "[exact text from the module]"
  Why This Caused the Error: [explanation]
```

---

### Step 4: Vendor Documentation Verification

**Invoke Research** to fetch the current vendor documentation and compare against the module's instruction.

**Research prompt template:**

```
CONTEXT: An AgentBuild module for [vendor] integration contains an instruction
that is producing build errors. I need to verify the correct approach.

TASK: Fetch the current official documentation for [vendor] regarding [specific topic].
Specifically:
  - What is the correct way to [the thing the module got wrong]?
  - Has this changed in recent versions?
  - Are there any known gotchas or common mistakes?

EFFORT LEVEL: Complete within 60 seconds.
OUTPUT: The correct approach with version-specific notes.
```

**Compare:**
- What the module says vs. what the vendor docs say
- If they differ → the module needs updating
- If they agree → the error may be environmental (route back to ErrorRecovery)

**Output:**

```
VENDOR VERIFICATION:
  Vendor Docs Say: [what the vendor documentation states]
  Module Says: [what our module states]
  Discrepancy: [YES: describe / NO: module matches vendor — investigate further]
  Vendor Doc Source: [URL or reference]
```

---

### Step 5: Draft Module Patch

**Write the corrected/added/updated instruction.** This is the primary output — the module documentation fix.

**The patch must include:**

1. **The corrected instruction** — replacing the wrong/incomplete/stale text
2. **A Known Issues entry** — added to the module's Known Issues table with:
   - Exact error message (so future agents can match it)
   - Root cause explanation
   - The fix
3. **Updated pre-flight validation** — if the module has a validation script, add a check that catches this error before build
4. **Updated AGENTS.md additions** — if the module has an AGENTS.md section, add guidance that prevents this error

**Patch format:**

```
MODULE PATCH:
  File: [module .md path]
  Type: [CORRECTION / ADDITION / UPDATE]

  BEFORE (current module text):
  """
  [quoted current text]
  """

  AFTER (patched module text):
  """
  [the corrected text]
  """

  KNOWN ISSUES ENTRY:
  | [Issue name] | [Exact error message] | [Cause] | [Fix] |

  PRE-FLIGHT ADDITION (if applicable):
  [new validation check]
```

---

### Step 6: Stress Test (Optional — Recommended for WRONG and STALE fixes)

**Invoke RedTeam** to probe the patched module section for adjacent gaps that haven't surfaced yet.

**RedTeam prompt template:**

```
CONTEXT: A module for [vendor] integration had a documentation error in the
[section name] section. The error was: [describe]. The fix was: [describe].

TASK: Adversarially analyze the ENTIRE [section name] section of this module
(provided below) for similar classes of errors:

[PASTE THE FULL SECTION]

Focus on:
  1. Other instructions in this section that might be wrong for the same reason
  2. Missing steps that an agent would need but aren't documented
  3. Version-specific assumptions that may have gone stale
  4. Edge cases the section doesn't address (e.g., src/ vs root, version differences)

For each finding: state the instruction, the potential failure, and the fix.
```

**If RedTeam finds additional gaps** → add them to the module patch before applying.

---

### Step 7: Commit & Propagate

**Apply the patch:**

1. Edit the module .md file with the corrected text
2. Update the module status line with new version:
   ```
   **Module status:** STABLE (v[N+1] — updated [today's date])
   ```
3. Update the changelog line at the bottom:
   ```
   *Module maintained by AgentBuild. v[N+1] updated [date] — [one-line description of what was fixed].*
   ```

**Cross-project check:**

```bash
# Check if other active AgentBuild projects use this module
cat .claude/skills/AgentBuild/projects/PID-*.json 2>/dev/null | grep -l "[module name]"
```

If other active projects use this module → produce a cross-project alert:

```
CROSS-PROJECT ALERT:
  Module [name] was patched (v[N] → v[N+1]).
  Active projects using this module:
    - [Project Name] (PID-xxxx) at [repoPath]

  These projects may have code generated from the old module version.
  Review [specific area] for the same error pattern.
```

**Output summary:**

```
MODULE DOCTOR COMPLETE:
  Module: [name] (v[old] → v[new])
  Root Cause: [WRONG / INCOMPLETE / STALE]
  Trace: [section] — [1-line description]
  Patch: [what was changed]
  Known Issues: [entry added]
  Pre-flight: [check added / N/A]
  Stress Test: [N findings / skipped]
  Cross-Project: [N projects alerted / none]
```

---

## Integration

### Invoked By
- `Workflows/ErrorRecovery.md` — Step 5 escalation when root cause is `module_gap`
- Direct user invocation via trigger phrases

### Invokes (PAI Skills)
- **Research** — Vendor documentation verification (Step 4)
- **RedTeam** — Adversarial stress testing of patched module (Step 6)
- **Council** — Debate multiple valid fix approaches when ambiguous (Step 5, when needed)
- **Browser** — Visual validation for UI-producing modules (Step 6, when applicable)
- **Science** — Hypothesis-test cycle for hard-to-reproduce errors (Step 2, when classification is unclear)

### Updates
- `Modules/*.md` — The patched module file
- Module's Known Issues table
- Module's pre-flight validation script (if applicable)
- Module's AGENTS.md additions section (if applicable)

### Feeds Into
- `Workflows/BuildRetrospective.md` — Module fix patterns section
- `Workflows/MeasureSuccess.md` — Tier 3: module self-healing metrics

---

## The Compounding Effect

```
Project 1 builds with AuthClerk module → hits middleware placement error
  → ErrorRecovery can't fix (module gap) → ModuleDoctor patches AuthClerk v2 → v3
Project 2 builds with AuthClerk v3 → middleware placement is correct
  → hits env var loading error → ModuleDoctor patches AuthClerk v3 → v4
Project 3 builds with AuthClerk v4 → both issues pre-solved
  → clean build on first attempt
```

Every project that fails makes the modules better for every subsequent project. The modules accumulate battle-tested knowledge. This is not a bug-fixing tool — it is a **module evolution engine**.

---

*Workflow created for AgentBuild. Designed 2026-02-21.*
