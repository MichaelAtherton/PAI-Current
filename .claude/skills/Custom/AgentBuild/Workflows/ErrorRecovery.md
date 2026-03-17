# Workflow: ErrorRecovery

> Classify any build error, attempt a fix from the known fix library, and document what was learned — within a 3-attempt budget. Escalate to human when budget is exhausted.

**Invoke when:** "agents keep failing", "fix this error", "autonomously recover", "error recovery", or any CI failure that blocks progress

---

## Core Principle: Bounded Autonomy

> The agent has 3 attempts to fix any error. After 3 attempts, it stops and escalates. It never loops forever. It never modifies its own attempt budget. It always documents, win or lose.

This is not a weakness — it is the mechanism that makes autonomous recovery trustworthy. An agent that can't escalate will eventually cause more damage than the original error.

---

## Step 1: Error Classification

Before attempting any fix, classify the error. The classification determines the fix strategy.

**Classification Matrix:**

| Type | Description | Signals | Fix Strategy |
|------|-------------|---------|-------------|
| **Infrastructure** | Environment, networking, platform configuration | Timeouts, connection refused, missing env var, 503 at startup | Check deployment config, env vars, service connectivity |
| **Logic** | Code produces wrong output or throws unexpectedly | Test failure with unexpected output, runtime exception in app code | Read spec, fix code, re-run tests |
| **Spec Gap** | The spec didn't cover this case — agent guessed wrong | Behavior doesn't match any spec entry, no test exists for the failure | Do NOT fix autonomously — escalate immediately with spec gap flagged |
| **Environment** | Toolchain, dependency version, OS-level issue | Dependency not found, version conflict, build tool failure | Check package.json, lockfile, node version |

**Classification output:**

```
ERROR: [paste error message]
TYPE: [Infrastructure / Logic / Spec Gap / Environment]
REASON: [1 sentence explaining the classification]
STRATEGY: [what fix approach to attempt]
```

**Spec Gap is special:** If the error is a Spec Gap, do NOT attempt 3 autonomous fixes. Immediately produce an escalation report (see Step 5). Guessing at spec gaps produces code not in the spec — a violation of the build framework's core rule.

---

## Step 2: Check Known Fix Library

Before attempting any novel fix, check `docs/known-fixes/` for a documented resolution.

```bash
# Search for matching errors
ls docs/known-fixes/
grep -r "[key error term]" docs/known-fixes/ --include="*.md" -l
```

If a known fix is found:
1. Read the fix file
2. Apply the exact documented fix
3. This counts as Attempt 1
4. If it works → document the reuse (Step 4)
5. If it doesn't work → note the failure, continue to Attempt 2 (novel fix)

**Known fix file format:**

```markdown
# Known Fix: [Short error name]

**Error pattern:** [Exact error message or key phrase to match]
**Type:** [Infrastructure / Logic / Environment]
**Discovered:** [date] during [project name]

## Fix

[Step-by-step fix that resolved this error]

## Why This Works

[1-2 sentence explanation of root cause]

## Context

[Any environment-specific notes — Node version, framework version, OS]
```

---

## Step 3: Attempt the Fix (3-Attempt Budget)

**Budget tracker:**

```
Attempt 1 of 3: [Known fix from library / describe novel fix approach]
Attempt 2 of 3: [Alternative fix if attempt 1 failed]
Attempt 3 of 3: [Final attempt — most conservative, least invasive fix]
```

**Rules for each attempt:**

1. **One change per attempt.** Never make two changes at once. If the fix doesn't work, you won't know which change mattered.
2. **Run tests/CI after each attempt.** Don't batch fixes — verify immediately.
3. **Document the attempt.** Note what was tried, what was expected, what actually happened.
4. **Never delete tests.** If a test is failing, fix the code or the spec — not the test.
5. **Never make scope changes.** Error recovery fixes errors — it does not refactor or add features.

**After each attempt:**

```
Attempt [N] result:
- Fix applied: [what was changed]
- CI result: [pass / fail]
- New error (if fail): [error message]
- Assessment: [why it worked or didn't]
```

**If Attempt 1 succeeds:** → Jump to Step 4 (Document)
**If Attempt 2 succeeds:** → Jump to Step 4 (Document)
**If Attempt 3 succeeds:** → Jump to Step 4 (Document)
**If all 3 fail:** → Jump to Step 5 (Escalate)

---

## Step 4: Document the Fix

**Whether the fix succeeded or not, always document.**

Create or update a file in `docs/known-fixes/`:

```bash
# File naming: kebab-case description of error
docs/known-fixes/railway-healthcheck-timeout.md
docs/known-fixes/clerk-jwt-null-in-api-route.md
docs/known-fixes/supabase-rls-blocks-all-queries.md
```

**If the fix succeeded:**

```markdown
# Known Fix: [Error name]

**Error pattern:** [Exact error message]
**Type:** [Infrastructure / Logic / Environment]
**Discovered:** [date] during [project name]
**Times applied:** 1

## Fix

[The exact fix that worked — step by step]

## Why This Works

[Root cause explanation]
```

**If all 3 attempts failed:**

```markdown
# Known Error: [Error name] — UNRESOLVED

**Error pattern:** [Exact error message]
**Type:** [Infrastructure / Logic / Environment / Spec Gap]
**Discovered:** [date] during [project name]
**Attempts:** 3 (all failed)

## What Was Tried

### Attempt 1
[What was tried, why it failed]

### Attempt 2
[What was tried, why it failed]

### Attempt 3
[What was tried, why it failed]

## Hypothesis

[Best current theory about root cause]

## What's Needed to Resolve

[What information, access, or decision is needed from a human]
```

**Then update AGENTS.md** if the error revealed an environment or context gap:

```
SPEC: AGENTS.md Update
SCOPE: Add Domain-Specific Note about [error type discovered]
TASK: Document that [specific gotcha] causes [specific error] and the resolution is [fix or escalation path]
DONE WHEN: AGENTS.md reflects the new knowledge. Next agent in this repo won't hit this error blind.
```

---

## Step 5: Escalation Report (When 3 Attempts Fail or Spec Gap Found)

Produce this report and stop. Do not attempt a 4th fix.

```markdown
## Error Recovery Escalation — [Date]

### Error
[Exact error message]
[Error type: Infrastructure / Logic / Spec Gap / Environment]

### What Was Tried
[Summary of all 3 attempts — or "Spec gap detected — no autonomous fix attempted"]

### Current Blocker
[1 sentence: exactly what is preventing resolution]

### Decision Needed from Michael
[Specific question or choice that unblocks this]

Options (if applicable):
A) [Option A] — [consequence]
B) [Option B] — [consequence]
C) [Option C] — [consequence]

### Files Changed During Recovery Attempts
[List any files that were modified — these may need to be reviewed or reverted]

### Suggested Next Step
[Recommended option and rationale]
```

**Module Gap Detection:** Before escalating to the human, check whether the root cause is a module documentation gap:

> "Did the agent follow a module's instructions faithfully, and the instructions themselves were wrong, incomplete, or stale?"

If **YES** → this is a **module gap**, not a code error. Invoke `Workflows/ModuleDoctor.md` with:
- The error message
- Which module was followed
- The code the agent produced (showing it matches the module's instructions)
- Why ErrorRecovery believes the module is at fault

ModuleDoctor will patch the module documentation so no future project hits this error. The code fix for THIS project is a side effect of the module fix.

If **NO** → escalate to human as normal (report above).

**After escalation:** Stop. Wait for human input. Do not attempt adjacent work that touches the blocked component.

---

## Error Recovery Loop (Fully Autonomous Mode)

When running in fully autonomous mode (no human in the loop), the error recovery cycle runs automatically during the build loop:

```
BUILD → CI fails → ErrorRecovery invoked
    → Classify error
    → Check known fixes
    → Attempt 1 → CI check
    → [if pass] → Document → Continue build
    → Attempt 2 → CI check
    → [if pass] → Document → Continue build
    → Attempt 3 → CI check
    → [if pass] → Document → Continue build
    → [if all fail] → Document unresolved → Generate escalation report → PAUSE
```

**Pause behavior:** The build loop pauses at the failing spec item. All other spec items that do NOT depend on the failed component can continue building. Only the dependent tree is blocked.

---

## Compounding Effect: How the Library Grows

Build 1: 0 known fixes → 100% novel attempts (slow, manual)
Build 2: 2-4 known fixes → ~30% known-fix hits (some reuse)
Build 4: 8-12 known fixes → ~60% known-fix hits (significant autonomy)
Build 8+: 20+ known fixes → ~80% known-fix hits (near-autonomous recovery)

The known fix library is the asset. Each build failure, documented and resolved, is compounding knowledge.

---

## Integration

- **Invoked by:** `Workflows/BuildLoop.md` (Step 3: GATE, when tests fail)
- **Invoked by:** `Workflows/FullBuild.md` (Phase 5: Environment Design, Category 3: Context Completeness)
- **Escalates to:** `Workflows/ModuleDoctor.md` (when root cause is a module documentation gap)
- **Feeds into:** `Workflows/MeasureSuccess.md` (Tier 3: Autonomous Recovery checks)
- **Feeds into:** `Workflows/BuildRetrospective.md` (error pattern section)
- **Updates:** `docs/known-fixes/` directory
- **Updates:** `AGENTS.md` Domain-Specific Notes section
