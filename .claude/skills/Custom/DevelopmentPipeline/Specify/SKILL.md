---
name: Specify
description: Specify container for the DevelopmentPipeline — knowledge capture and spec repository setup (Phases 6, 7). Produces hardened feature specs, constraint specs, and spec index via Council, Research, RedTeam, and IterativeDepth. USE WHEN edge cases, specifications, spec hardening, knowledge capture, pipeline specify, generate specs, harden specs, capture constraints.
---

# Specify

**Pipeline container: Phases 6 and 7**

Takes UX specs, personas, and approved design and produces hardened feature specifications through a multi-agent process: Research for domain failure modes, Council with 5 synthetic user personas, RedTeam for adversarial analysis, FirstPrinciples for business constraint decomposition, and IterativeDepth for completeness review. This is a high-context zone — Council(5) + Research + IterativeDepth can consume 50-100k+ tokens.

## Customization

**Before executing, check for user customizations at:**
`.claude/PAI/USER/SKILLCUSTOMIZATIONS/DevelopmentPipeline/`

## Voice Notification

**When executing a workflow, do BOTH:**

1. **Send voice notification**:
   ```bash
   curl -s -X POST http://localhost:8888/notify \
     -H "Content-Type: application/json" \
     -d '{"message": "Starting Specify — edge cases, failure modes, and spec hardening"}' \
     > /dev/null 2>&1 &
   ```

2. **Output text notification**:
   ```
   Running the **RunSpecify** workflow in the **DevelopmentPipeline** skill — hardening specifications...
   ```

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **RunSpecify** | "edge cases", "specifications", "spec hardening", "knowledge capture" | `Workflows/RunSpecify.md` |

## Cold-Start Input Spec

This container can be invoked standalone. It needs:

| Required File | Source |
|---------------|--------|
| `docs/specs/users/[persona-name].md` | Discovery output |
| `docs/specs/ux/[feature-name]-ux.md` | Discovery output |
| `design-system/MASTER.md` | Design output |
| `design/reference/[component-name].html` | Design output |
| Active PID in `.claude/skills/Custom/AgentBuild/projects/` | Phase 4 output |
| Initialized git repo with CI green | Phase 5 output |

## Deliverables (Cold-Start Contract)

When Specify completes, these files MUST exist:

| Artifact | File Path | Content |
|----------|-----------|---------|
| Feature specs | `docs/specs/features/[feature-name].md` | Happy path + edge cases + failure modes + constraints |
| Constraint specs | `docs/specs/constraints/business-rules.md` | CONSTRAINT blocks |
| Spec index | `docs/specs/MASTER.md` | Links all spec files |
| Pipeline state | `projects/PID-{hex}.json` → `currentPhase: "build"` | Phase tracking |

**Cold-start test:** A fresh session with ONLY the git repo (which now contains all committed specs, AGENTS.md, design-system/, component references) can execute Phase 8 (Build Loop).

## Examples

**Example 1: Full specification from pipeline**
```
User: "Scaffold is done — specify the features"
→ Reads UX specs and persona files
→ Phase 6: Happy path → Edge cases (Council) → Failure modes (RedTeam) → Constraints → IterativeDepth review
→ Phase 7: Creates spec directory structure, commits to git
→ All specs ready for Build Loop
```

**Example 2: Standalone edge case generation**
```
User: "Generate edge cases for the authentication feature"
→ Cold-starts from existing feature spec
→ Runs Council with 5 synthetic personas + Research
→ User decides Include/Exclude/Defer for each edge case
→ Updates feature spec with approved edge cases
```

## Source Workflows

- Phase 6 (Knowledge Capture): `.claude/skills/Custom/AgentBuild/Workflows/FullBuild.md` — Phase 2 + `.claude/skills/Custom/AgentBuild/Workflows/EdgeCaseGeneration.md`
- Phase 7 (Spec Repository): `.claude/skills/Custom/AgentBuild/Workflows/FullBuild.md` — Phase 3
