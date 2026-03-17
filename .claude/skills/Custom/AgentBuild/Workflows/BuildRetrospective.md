# Workflow: BuildRetrospective

> Post-MVP review that extracts compounding learnings from a completed build and proposes concrete improvements to AgentBuild itself. Each build makes the next build faster.

**Invoke when:** "retrospective", "build retrospective", "what did we learn", "improve AgentBuild", after MVP gate passes or a build cycle concludes

---

## When to Run

Run this workflow after:
- MVP gate passes (celebrate and learn)
- A build cycle concludes without reaching MVP (learn from the failure)
- A major unexpected error consumed significant time (extract the lesson while fresh)

Do NOT run this workflow during an active build. Retrospective is reflection, not execution.

---

## The Retrospective Structure

The retrospective has five sections, each producing a concrete output. All five must be completed — partial retrospectives lose the compounding value.

---

## Section 1: Build Summary

**Purpose:** Establish the facts of the build before drawing conclusions.

Answer each:

```markdown
## Build Summary

**Project:** [Name]
**Date range:** [start date] → [end date]
**Build #:** [this is the Nth AgentBuild project]
**Maturity score at completion:** [N/18 from MeasureSuccess]
**Time to MVP gate:** [days / sessions]

**Phase completion:**
- Phase 0 (Orientation): ✓ / ✗
- Phase 1 (Environment): ✓ / ✗
- Phase 2 (Knowledge Capture): ✓ / ✗
- Phase 3 (Spec Repo): ✓ / ✗
- Phase 4 (Build Loop): ✓ / ✗
- Phase 5 (Environment Diagnosis): ✓ / ✗
- Phase 6 (Observability): ✓ / ✗
- MVP Gate: ✓ / ✗ (if reached)

**Modules used:**
- [ ] AuthClerk
- [ ] DbSupabase
- [ ] DeployRailway
- [ ] ObservabilitySentry
- [ ] [Other: ___]

**Total errors encountered:** [N]
**Errors resolved autonomously:** [N] ([%])
**Errors requiring human escalation:** [N]
```

---

## Section 2: Error Pattern Analysis

**Purpose:** Identify which error types appeared most often and whether they're now in the known fix library.

```markdown
## Error Patterns

| Error | Type | Resolved By | In Library? | New Fix? |
|-------|------|-------------|-------------|----------|
| [error 1] | Infra/Logic/Spec/Env | Autonomous / Human | ✓/✗ | ✓/✗ |
| [error 2] | ... | ... | ... | ... |

**Most common error type this build:** [Infrastructure / Logic / Spec Gap / Environment]
**Average attempts to resolve:** [N]
**Longest blocked by a single error:** [N hours/days]

**New entries added to docs/known-fixes/ this build:**
- [fix 1 filename]
- [fix 2 filename]
```

---

## Section 3: Spec Quality Assessment

**Purpose:** Were the specs complete enough? Every agent follow-up question or unexpected behavior is evidence of a spec gap.

```markdown
## Spec Quality

**Agent follow-up questions during build:** [N]
(Every question is a spec gap — the answer should be in the spec, not the conversation)

**Spec gaps discovered during build:**
- [Gap 1]: [what was missing] → [what was added to spec]
- [Gap 2]: ...

**Edge cases that weren't in the spec but appeared in production:**
- [Case 1]: [what happened, what should have been specified]
- ...

**Spec sections that caused the most implementation ambiguity:**
- [Section]: [why it was ambiguous]

**What would have made Phase 2 (Knowledge Capture) more effective for this build:**
[Honest assessment — were personas diverse enough? Were failure modes complete?]
```

---

## Section 4: Module & Infrastructure Assessment

**Purpose:** Did the modules save time? Did any cause unexpected problems? What new module is needed?

```markdown
## Module Assessment

**Modules that worked well:**
- [Module]: [what specifically saved time or worked without problems]

**Modules that needed modification:**
- [Module]: [what had to be changed, and why it should be updated in the module itself]

**Module gaps (needed but didn't exist):**
- [Capability needed]: [why it came up, estimated recurrence probability]

**AGENTS.md quality assessment:**
- Did agents follow AGENTS.md consistently? [Yes / Mostly / No]
- What did agents ignore or misinterpret?
- What should be added to AGENTS.md based on this build?

**Time saved by using known modules vs starting fresh:**
[Estimate — "Saved ~2 sessions by using AuthClerk instead of building from scratch"]
```

---

## Section 5: Proposed Improvements

**Purpose:** Translate learnings into concrete, actionable proposals. Each proposal requires approval before being applied to the AgentBuild skill.

```markdown
## Proposed Improvements

Each proposal is either PENDING APPROVAL (requires Michael's sign-off) or AUTO-APPLY (safe to apply without review).

### Proposals Requiring Approval

**Proposal 1: [Title]**
- Type: [Module update / New module / Workflow change / AGENTS.md template / SKILL.md change]
- What to change: [specific file and what changes]
- Why: [evidence from this build — specific error or friction that caused this]
- Impact: [who benefits and how]
- Estimated effort: [small / medium / large]
- Status: PENDING APPROVAL

[Repeat for each proposal]

### Auto-Apply Proposals (Safe to Apply Now)

**Auto-Apply 1: Known Fix Addition**
- File: `docs/known-fixes/[filename].md`
- Change: [Add new known fix entry]
- Applying now: [Yes / No — if no, explain why]

**Auto-Apply 2: AGENTS.md Update (project-specific)**
- Section: Domain-Specific Notes
- Addition: [specific text to add]
- Applying now: [Yes / No]
```

**Approval request format:**

After completing the retrospective, present proposals to Michael:

```
BUILD RETROSPECTIVE COMPLETE — [Project Name]

I've identified [N] proposed improvements from this build.

AUTO-APPLIED:
- [list of auto-applied changes with files]

PENDING YOUR APPROVAL:
1. [Proposal 1 — 1-sentence summary]
2. [Proposal 2 — 1-sentence summary]
...

Which proposals should I apply? You can approve individual ones, all, or none.
```

---

## Compounding Value Tracking

After each retrospective, update the AgentBuild maturity log:

```markdown
# AgentBuild Maturity Log

| Build # | Date | Project | Maturity Score | Errors | Autonomous % | New Fixes | New Proposals |
|---------|------|---------|---------------|--------|-------------|-----------|---------------|
| 1 | [date] | [name] | [N/18] | [N] | [%] | [N] | [N] |
| 2 | [date] | [name] | [N/18] | [N] | [%] | [N] | [N] |
```

This log lives at: `.claude/skills/AgentBuild/BuildHistory.md`

The maturity score trend across builds is the single best indicator of whether AgentBuild is improving. Expect Tier 1 to stabilize by Build 3. Tier 2 by Build 5. Tier 3 is a long-term progression.

---

## The Compounding Loop

```
Build concludes
    ↓
MeasureSuccess (score this build)
    ↓
BuildRetrospective (extract learnings)
    ↓
Error → known-fixes (never hit this one blind again)
    ↓
Module updates approved (fix what was rough)
    ↓
New modules added (never solve this from scratch again)
    ↓
SKILL.md / workflow updates approved
    ↓
Next build starts with a smarter system
```

Each pass through this loop is a permanent, compounding improvement. The goal is not just to build the current project — it is to leave AgentBuild measurably better for the next project.

---

## Integration

- **Invoked by:** End of any build cycle (MVP gate passed or session concluded)
- **Invoked after:** `Workflows/MvpGate.md` when gate passes
- **Reads:** `Workflows/MeasureSuccess.md` output (maturity score)
- **Reads:** `docs/known-fixes/` (error patterns)
- **Reads:** Build session notes / PRD logs
- **Updates:** `docs/known-fixes/` (new entries)
- **Updates:** `AGENTS.md` (project-specific additions)
- **Proposes updates to:** `Modules/*.md`, `Workflows/*.md`, `SKILL.md`
- **Creates:** `.claude/skills/AgentBuild/BuildHistory.md` entry
