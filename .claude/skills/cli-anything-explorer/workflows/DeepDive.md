# Workflow: Deep Dive

Use this workflow when the user wants to go deeper on a specific topic, tool, market, or concept within the CLI-Anything space.

## Prerequisites

Load the most relevant reference file(s) based on the topic. If unclear, start with `references/MetaInsights.md` for orientation.

## Process

### 1. Identify the Dive Target

What specifically does the user want to go deeper on?

| Target Type | Example | Primary Reference |
|---|---|---|
| A specific software tool | "Go deep on Blender's CLI capabilities" | `TechnicalFoundation.md` |
| A specific business idea | "Deep dive on ComplianceGhost" | `IdeationLandscape.md` + `ActionableRoadmap.md` |
| A market/industry | "Deep dive on the legal tech market" | Route to **Research** |
| A technical pattern | "Deep dive on the backend wrapper pattern" | `TechnicalFoundation.md` |
| A pipeline design | "Deep dive on the video production pipeline" | `ActionableRoadmap.md` |
| A concept | "Deep dive on the possibility engine idea" | `FirstPrinciples.md` + `MetaInsights.md` |

### 2. Choose the Research Approach

| Depth Needed | Approach |
|---|---|
| Quick context (~2 min) | Load references, synthesize from existing knowledge |
| Medium depth (~10 min) | Quick Research via **Research** skill (1 Perplexity agent) |
| Substantial (~30 min) | Standard Research via **Research** skill (3 agents: Perplexity + Claude + Gemini) |
| Exhaustive (~60+ min) | Extensive Research via **Research** skill (12 agents) or Deep Investigation |

### 3. Structured Output

Present the deep dive in a consistent format:

```
## Deep Dive: [Topic]

### Current Understanding
What we already know from our exploration (reference existing context).

### New Findings
What the research/analysis revealed that we didn't know.

### Implications for CLI-Anything
How this changes or deepens our thinking about applications.

### Action Items
Specific next steps if the user wants to act on this.

### Cross-References
Which other ideas, pipelines, or concepts this connects to.
```

### 4. Update the Knowledge Base

If the deep dive reveals significant new insights:
- Suggest updating the relevant reference file in the skill
- Or suggest creating a new reference file for a new domain
- Connect new findings back to the 6 atomic primitives and the Stack Model

## Routing to Other Skills

| Need | Skill |
|---|---|
| Web research on a topic | **Research** (Quick/Standard/Extensive) |
| Extract insights from a specific article/video | **ContentAnalysis** |
| Think deeply about implications | **Thinking/IterativeDepth** |
| Generate new ideas from deep dive findings | **Thinking/BeCreative** |
| Investigate a company or competitor | **Investigation** (OSINT) |
