# Workflow: Explore New Ideas

Use this workflow when the user wants to brainstorm, ideate, or explore new CLI-Anything applications.

## Prerequisites

Before entering this workflow, ensure you've loaded:
- `references/FirstPrinciples.md` (the 6 atomic primitives and constraint classification)
- `references/IdeationLandscape.md` (existing ideas to avoid duplication and build upon)

## Process

### 1. Understand the Domain or Constraint

Ask (or infer from context): What domain, industry, or constraint is the user exploring? Examples:
- A specific industry (healthcare, education, real estate)
- A specific capability (video production, data visualization)
- A specific business model (recurring revenue, marketplace, productized service)
- A wild "what if" scenario

### 2. Software Compatibility Pre-Screen

Before designing pipelines, classify the software involved. Load `references/SoftwareCompatibility.md` if needed.

For each software the domain uses:
1. **Identify the access path**: Open source? Scripting API? OS bridge? Vendor CLI? Plugin system?
2. **Run the 5-question quick filter**: Can it be invoked from CLI? Headless? Scripting API? Already has full API (skip it)? Output capturable?
3. **Skip "already agent-accessible" software** — web apps with REST/MCP/GraphQL APIs don't need CLI-Anything (the vibe-kanban lesson)
4. **Don't limit to the 11 demo harnesses** — the world is your oyster. Any software you can communicate with programmatically is a candidate: Photoshop (ExtendScript), AutoCAD (AutoLISP), Maya (Python), DaVinci Resolve, FFmpeg, and hundreds more.

### 3. Apply the 6 Primitives as Lenses

For each primitive, ask: "What does this unlock in the user's domain?"
1. Software Comprehension → Structured Interface
2. Human-Only → Agent-Accessible
3. Unstructured Output → JSON
4. Isolated Apps → Chainable Pipeline
5. Manual → Reproducible
6. One-at-a-time → Parallelizable

### 4. Route to PAI Thinking Skills

Based on the depth and style of exploration needed:

| Intent | Invoke |
|---|---|
| "I want wild, creative ideas" | **Thinking/BeCreative** — MaximumCreativity workflow (5 radically different options, p<0.10 each) |
| "Think from first principles about X" | **Thinking/FirstPrinciples** — Deconstruct → Challenge → Reconstruct |
| "Debate this from multiple angles" | **Thinking/Council** — 4-perspective debate (Entrepreneur, Artist, Scientist, Systems Thinker) |
| "What are the risks/weaknesses?" | **Thinking/RedTeam** — Adversarial critique |
| "Is this feasible? Test the hypothesis." | **Thinking/Science** — Scientific hypothesis testing |
| "What are all the angles?" | **Thinking/IterativeDepth** — Multi-angle progressive deepening |

When invoking these skills, seed them with the CLI-Anything context from the loaded references. The thinking skills work best when they have domain-specific input.

### 5. Cross-Reference Existing Ideas

After generating new ideas, compare against the existing landscape in `references/IdeationLandscape.md`:
- Does this overlap with an existing idea? If so, it's a variant — note what's different.
- Does this fill a gap? (A domain, business model, or pipeline combination not yet explored?)
- Does this compound with existing ideas? (e.g., a new idea that makes the Production OS more valuable)

### 6. Score and Rank

Use the same 4 dimensions from our original ranking:
- **Feasibility**: Can Michael build this with current tools?
- **Value**: Revenue potential or strategic value?
- **Uniqueness**: Does this require Michael's specific capabilities (PAI + CLI-Anything + domain knowledge)?
- **Compounding**: Does this get more valuable over time? Does it feed the flywheel?

### 7. Deep-Dive the Winner

For the highest-scoring idea, define:
- The specific pipeline (which apps, in what order)
- The input/output at each stage
- The human-in-the-loop touchpoints (where does taste/judgment matter?)
- The business model (one-time, recurring, marketplace, etc.)
- First concrete test: What's the smallest thing you can build to validate this?
