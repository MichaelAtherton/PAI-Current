---
task: Launch three parallel agents to prototype reveal options
slug: 20260310-153000_three-reveal-prototypes
effort: advanced
phase: observe
progress: 0/8
mode: interactive
started: 2026-03-10T15:30:00-06:00
updated: 2026-03-10T15:30:00-06:00
---

## Context

Michael wants to see tangible output from three competing approaches to the BriefingPro reveal mode animation. Each approach will be prototyped by a separate agent working in an isolated worktree so the outputs don't conflict. Michael will compare and choose.

### The Three Options
1. **Prototype** — Build a `/reveal` route in BriefingPro with Motion + FlowToken + Aceternity UI
2. **GSAP MCP** — Install GSAP Master MCP server and demonstrate its animation generation capabilities
3. **PAI Skill** — Build a reusable cinematic animation skill wrapping Motion + FlowToken + Aceternity

## Criteria

- [ ] ISC-1: Option 1 agent launched in isolated worktree on BriefingPro
- [ ] ISC-2: Option 2 agent launched for GSAP MCP installation
- [ ] ISC-3: Option 3 agent launched in isolated worktree for PAI skill creation
- [ ] ISC-4: All three agents given complete context from prior research
- [ ] ISC-5: All three agents running in parallel
- [ ] ISC-6: Results collected and presented for comparison
- [ ] ISC-7: Michael can see tangible output from each option
- [ ] ISC-8: Clear comparison summary produced

## Decisions

### 21st.dev Magic Assessment (post-investigation)

After comprehensive investigation (3 live MCP queries + background research), 21st.dev Magic is a **retrieval-based component tool**, not a generative animation engine. Animation generation is "Coming Soon." However, the `component_inspiration` tool serves as a useful animation pattern catalog with 108+ Framer Motion components. Best used as a reference library for animation patterns, not as the primary animation generation tool.

The existing Option 1 prototype (RevealPage with Motion) and Option 3 (cinematic-animation skill) remain the strongest paths. 21st.dev can supplement by providing animation pattern inspiration (VerticalCutReveal, BlurText, SparklesText patterns).

## Verification
