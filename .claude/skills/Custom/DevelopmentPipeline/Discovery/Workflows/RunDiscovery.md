# RunDiscovery — Phases 0 and 0b

Thin wrapper that routes to AgentBuild's orientation and idea refinement workflows. Produces all Discovery deliverables needed for the Design container to cold-start.

---

## Prerequisites

- A raw product idea (can be one sentence)
- No prior files needed — this is the pipeline entry point

## Execution

### Phase 0: Orientation

**Route to:** `.claude/skills/Custom/AgentBuild/Workflows/FullBuild.md` — Phase 0 section only.

Read the Phase 0 section of FullBuild.md and follow its instructions exactly:
1. Ask the two orientation questions (What does this do for whom? How do you know it worked?)
2. Wait for both answers
3. Lock the two sentences

**Do NOT proceed to Phase 1 of FullBuild.md.** Stop after locking the orientation sentences.

### Phase 0b: Idea Refinement

**Route to:** `.claude/skills/Custom/AgentBuild/Workflows/IdeaRefinement.md`

Read IdeaRefinement.md and follow its full 7-step process:
1. Discovery — users, context, JTBD, who is NOT the user
2. User empathy — construct named persona with anxieties, mental models
3. UX advocacy — challenge weak assumptions with research
4. Consultative proposal — 2-3 design approaches with tradeoffs
5. Collaborative refinement — iterate until clear
6. Specification generation — Level 3 UX spec (behavior only, no visual)
7. Review & validation — state assumptions, identify validation gaps

**This phase is conversational.** It may span many exchanges. Do not rush it.

## Deliverable Checklist

Before declaring Discovery complete, verify ALL of these exist:

- [ ] `docs/specs/users/[persona-name].md` — at least one named persona with JTBD, anxieties, mental models
- [ ] `docs/specs/ux/[feature-name]-ux.md` — Level 3 interaction spec for the core user journey
- [ ] Orientation sentences locked and confirmed (what + done) — save to a local `orientation.md` scratchpad since no PID exists yet
- [ ] PM has confirmed the direction

**Save deliverables to the project working directory.** These files will be committed to git when the repo is initialized in Phase 5. Orientation sentences will be written to the PID registry `orientation` field when PID is generated in Phase 4.

## Session Boundary

Discovery is complete. Its deliverables are at the file paths listed above.

**If context is heavy** (7+ exchanges, multiple refine loops), start a new session and resume at Phase 1 (Design) by reading:
- `docs/specs/users/[persona-name].md`
- `docs/specs/ux/[feature-name]-ux.md`
- The locked orientation sentences

**If context is light**, continue directly to the Design container.
