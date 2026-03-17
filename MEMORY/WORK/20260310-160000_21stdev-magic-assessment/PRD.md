---
task: Synthesize 21st.dev Magic findings and update skill docs
slug: 20260310-160000_21stdev-magic-assessment
effort: standard
phase: complete
progress: 10/10
mode: interactive
started: 2026-03-10T16:00:00-06:00
updated: 2026-03-10T16:00:00-06:00
---

## Context

Michael asked to take a closer look at 21st.dev Magic MCP to determine if the claude-code-design-stack skill accurately represents its animation capabilities. Three investigation threads completed: (1) live MCP tool schema inspection, (2) three inspiration queries returning 10+ animated components, (3) comprehensive background research via ClaudeResearcher.

The key finding: 21st.dev Magic is a retrieval-based component tool (searches a community registry of 284+ components), NOT a generative animation engine. Animation support is explicitly "Coming Soon" per their GitHub README. However, the platform hosts 108+ Framer Motion community components that Magic can retrieve, including text reveals, blur effects, sparkle animations, and stagger effects.

The skill documentation calls 21st.dev a "Component Library" which is accurate but incomplete — it doesn't mention the animation component catalog or the retrieval-vs-generation distinction.

### Risks
- Overcorrecting the skill docs to promise animation capabilities that are retrieval-dependent
- Undervaluing the 108 Framer Motion components in the registry as animation pattern sources
- Losing focus on the actual reveal prototype work

## Criteria

- [x] ISC-1: Corrected assessment document written with evidence from all three research threads
- [x] ISC-2: 21st.dev retrieval-vs-generation distinction documented clearly
- [x] ISC-3: Animation "Coming Soon" status documented with source
- [x] ISC-4: 108 Framer Motion community components acknowledged as pattern source
- [x] ISC-5: design-stack SKILL.md updated with animation capability notes
- [x] ISC-6: Specific components identified that map to reveal mode needs
- [x] ISC-7: Integration recommendation produced (what to use 21st.dev for vs. hand-code)
- [x] ISC-8: Comparison to earlier (incorrect) assessment that overstated capabilities
- [x] ISC-9: Three-prototypes PRD updated with 21st.dev findings
- [x] ISC-10: Actionable next step for Michael clearly stated

## Decisions

### Corrected Assessment: What 21st.dev Magic Actually Is

**Previous claim (incorrect):** "21st.dev Magic is a full animation component generator that produces cinematic, motion-rich React components from natural language descriptions."

**Corrected assessment:** 21st.dev Magic is a **retrieval-based component tool** that searches a community registry of 284+ pre-built React components. It does NOT generate animation code from scratch. Animation generation is listed as "Coming Soon" on their GitHub README.

**Evidence:**
1. ClaudeResearcher confirmed: "Magic does NOT generate code from scratch. It uses a library-based retrieval approach."
2. Live test of component_builder with a detailed cinematic text reveal request returned generic shadcn instructions, not a custom animated component.
3. GitHub README explicitly lists "Component Enhancement — adding advanced features and animations" as **Coming Soon**.
4. The 108 Framer Motion components found via inspiration are community-contributed, not Magic-generated.

### What 21st.dev IS Good For (in the reveal context)

The `component_inspiration` tool is genuinely useful as an **animation pattern catalog**. Live queries returned:
- **VerticalCutReveal** — characters slide up with blur-to-sharp + spring physics (Framer Motion)
- **TimelineContent** — scroll-triggered stagger reveal with blur (Framer Motion useInView)
- **TextReveal** — blur-to-sharp per character (CSS @keyframes)
- **SparklesText** — animated SVG sparkles over text (Framer Motion)
- **BlurText** — blur-to-sharp per word/letter (Framer Motion)

These are real, working components whose animation patterns can be extracted and adapted into the RevealPage prototype.

### Integration Recommendation

| Layer | Best Tool | Why |
|-------|-----------|-----|
| Dark stage layout | Hand-coded (done) | Architectural, not a component |
| Streaming text logic | Custom useStreamedText hook (done) | Real-time streaming, not retrievable |
| Text animation effects | **Mine 21st.dev inspiration** for patterns, then hand-code with motion/react | Patterns are great, but need adaptation for streaming context |
| Section choreography | Hand-coded SectionGroup (done) | Custom orchestration logic |
| Component polish | **21st.dev refiner** could help | After core animation works |

**Bottom line:** Use 21st.dev Magic's `component_inspiration` as a pattern reference library. Don't rely on `component_builder` for animation generation — it can't do that yet. The existing RevealPage prototype + cinematic-animation skill + direct Framer Motion coding is the right path.

## Verification
