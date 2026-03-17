---
name: Discovery
description: Discovery container for the DevelopmentPipeline — orientation and idea refinement (Phases 0, 0b). Produces user personas, UX specs, and locked orientation sentences. USE WHEN discovery, refine idea, explore idea, who is the user, idea refinement, user research, UX discovery, pipeline discovery.
---

# Discovery

**Pipeline container: Phases 0 and 0b**

Takes a raw product idea through structured discovery to produce user personas, Level 3 UX specs, and locked orientation sentences. This is the highest-iteration zone in the pipeline — expect 7+ user exchanges and multiple refine loops.

## Customization

**Before executing, check for user customizations at:**
`.claude/PAI/USER/SKILLCUSTOMIZATIONS/DevelopmentPipeline/`

## Voice Notification

**When executing a workflow, do BOTH:**

1. **Send voice notification**:
   ```bash
   curl -s -X POST http://localhost:8888/notify \
     -H "Content-Type: application/json" \
     -d '{"message": "Starting Discovery — orientation and idea refinement"}' \
     > /dev/null 2>&1 &
   ```

2. **Output text notification**:
   ```
   Running the **RunDiscovery** workflow in the **DevelopmentPipeline** skill — discovering and refining the product idea...
   ```

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **RunDiscovery** | "discovery", "refine idea", "explore idea", "who is the user" | `Workflows/RunDiscovery.md` |

## Cold-Start Input Spec

This container can be invoked standalone with NO prior conversation. It needs only:
- A raw product idea (can be as vague as one sentence)

## Deliverables (Cold-Start Contract)

When Discovery completes, these files MUST exist:

| Artifact | File Path | Content |
|----------|-----------|---------|
| Orientation sentences | Held in session (written to PID registry in Phase 4 when PID is generated) | Two locked sentences: `what` and `done` |
| User persona(s) | `docs/specs/users/[persona-name].md` | Named persona with JTBD, anxieties, mental models |
| UX spec(s) | `docs/specs/ux/[feature-name]-ux.md` | Level 3 interaction spec (behavior only, no visual) |

**Note:** No PID exists during Discovery. The PID is generated in Phase 4 (Tech Stack Decision) after design complexity is known. Orientation sentences are carried forward in session or in a local scratchpad until then.

**Cold-start test:** A fresh session with ONLY the persona files, UX spec files, and the locked orientation sentences (from prior session notes or user re-statement) + `output/DevelopmentPipeline/PIPELINE.md` can execute Phase 1 (Design System Generation) without any conversation history.

## Examples

**Example 1: New idea from scratch**
```
User: "I want to build a habit tracker for remote workers"
→ Invokes RunDiscovery workflow
→ Phase 0: Asks two orientation questions, locks answers
→ Phase 0b: 7-step UX consultant discovery session
→ Produces persona file + UX spec + updated orientation
```

**Example 2: Standalone invocation**
```
User: "Run discovery on this idea: a dashboard for tracking AI agent costs"
→ Cold-starts with just the idea sentence
→ Full discovery process, outputs all deliverables
→ Ready for Design container to consume
```

## Source Workflows

- Phase 0: `.claude/skills/Custom/AgentBuild/Workflows/FullBuild.md` — Phase 0 section
- Phase 0b: `.claude/skills/Custom/AgentBuild/Workflows/IdeaRefinement.md`
