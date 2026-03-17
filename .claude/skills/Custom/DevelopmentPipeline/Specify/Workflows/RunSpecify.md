# RunSpecify — Phases 6 and 7

Thin wrapper that routes to AgentBuild's knowledge capture and spec repository workflows. Produces hardened feature specs through multi-agent analysis (Council, Research, RedTeam, IterativeDepth).

---

## Prerequisites (Cold-Start Files)

Before starting, read and verify these files exist:

| File | What to check |
|------|---------------|
| `docs/specs/users/[persona-name].md` | Named persona with JTBD, anxieties, mental models |
| `docs/specs/ux/[feature-name]-ux.md` | Level 3 interaction spec |
| `design-system/MASTER.md` | Locked design tokens |
| `design/reference/[component-name].html` | HTML/JS prototypes |
| `AGENTS.md` | Project context and conventions |
| Active PID in AgentBuild `projects/` | Project identity |

If these files don't exist, earlier phases haven't been completed.

## Execution

### Phase 6: Knowledge Capture

**Route to:** `.claude/skills/Custom/AgentBuild/Workflows/FullBuild.md` — Phase 2 section.

Follow the Phase 2 instructions exactly:

**Step 2a: Happy Path Specification**
- User fills in FEATURE/USER/ACTION/RESULT for each feature (format in `.claude/skills/Custom/AgentBuild/SpecFeature.md`)
- Seed from the UX spec produced in Discovery

**Step 2b: Edge Case Generation**
- **Route to:** `.claude/skills/Custom/AgentBuild/Workflows/EdgeCaseGeneration.md`
- Invoke Research for domain failure modes
- Invoke Council with 5 synthetic user personas (seeded from real persona from Phase 0b)
- User decides Include/Exclude/Defer for each edge case

**Step 2c: Failure Mode Specification**
- Invoke RedTeam for adversarial analysis: system failures, input failures, state failures
- User reviews and approves failure behaviors

**Step 2d: Business Constraint Documentation**
- User provides rules, formatted as CONSTRAINT blocks (format in `.claude/skills/Custom/AgentBuild/SpecConstraint.md`)
- Invoke FirstPrinciples if user struggles to articulate constraints

**Step 2e: Compile and Review**
- Compile to `docs/specs/features/[feature-name].md`
- Invoke IterativeDepth for 4-angle completeness check (QA, security, new engineer, customer success)
- Address any gaps flagged

### Phase 7: Spec Repository

**Route to:** `.claude/skills/Custom/AgentBuild/Workflows/FullBuild.md` — Phase 3 section.

**If entering from ResumeFromDesign:** MASTER.md and routes.md already exist (created in Steps 5d/5e). Update them — don't recreate. Specifically: update Spec Status from DRAFT to HARDENED in the build checklist, and verify routes.md is still consistent with the hardened specs.

**If entering from FullBuild:** Follow Phase 3a-3c exactly to create these from scratch.

**Target structure:**

```
docs/specs/MASTER.md              ← Index + build checklist (Phase 3a)
docs/specs/routes.md              ← Route structure + navigation (Phase 3b)
docs/specs/features/              ← Feature specs
docs/specs/constraints/           ← Business constraint blocks
docs/specs/architecture/decisions.md  ← ADRs
```

**Requirements (create or verify):**
1. MASTER.md must include the **build checklist** with dependency order and build status columns (see Phase 3a format)
2. routes.md must define URL paths, layouts, navigation flow, and breadcrumbs (see Phase 3b)
3. Create `docs/known-fixes/.gitkeep` if it doesn't exist
4. Commit everything to git and push

## Deliverable Checklist

Before declaring Specify complete, verify ALL of these exist:

- [ ] `docs/specs/features/[feature-name].md` — complete specs (happy path + edge cases + failure modes + constraints)
- [ ] `docs/specs/constraints/business-rules.md` — CONSTRAINT blocks
- [ ] `docs/specs/MASTER.md` — index with build checklist (dependency order + build status)
- [ ] `docs/specs/routes.md` — route structure with navigation flow
- [ ] `docs/specs/` committed to git
- [ ] Specs pass IterativeDepth review

## Session Boundary

Specify is complete. Its deliverables are committed to the git repo.

**If context is heavy** (Council(5) + Research + IterativeDepth invocations accumulate 50k+ tokens), start a new session and resume at Phase 8 (Build Loop) by reading:
- The git repo (which now contains all specs, AGENTS.md, design-system/, component references)
- `docs/specs/MASTER.md` as the entry point

**If context is light**, continue to the Build container.
