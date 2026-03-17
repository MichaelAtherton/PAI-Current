---
name: cli-anything-explorer
description: CLI-Anything exploration hub — seeds deep context about CLI-Anything (auto-generated CLI wrappers for any GUI software) and routes to PAI skills for ideation, pipeline building, business validation, and deep research. USE WHEN cli-anything, cli anything, agent-native software, GUI to CLI, CLI wrapper, harness, software automation pipeline, cli-anything ideas, cli-anything business, what can I do with cli-anything, explore cli-anything, cli-anything brainstorm, build a pipeline, agent-addressable software, production OS, possibility engine, cli-anything roadmap.
---

# CLI-Anything Explorer

An intelligence amplifier that seeds your context with deep research, first-principles analysis, council debates, and wild ideation about CLI-Anything — then routes you to the right PAI skills for whatever you want to do next.

## What This Skill Contains

This skill encapsulates an exhaustive multi-agent exploration of CLI-Anything (HKUDS, University of Hong Kong). The research includes:

- **Technical Foundation** — Architecture, code quality, 7-phase pipeline, 11 demo harnesses, competitive positioning
- **First Principles Decomposition** — 6 atomic primitives, constraint classification, the 3-tier unlock
- **Council Debate** — 4 perspectives (Entrepreneur, Artist, Scientist, Systems Thinker) with convergence points
- **Wild Ideas** — 10 non-obvious business applications with specific pipelines and revenue models
- **Ranked Roadmap** — Top 10 ideas scored by feasibility, value, uniqueness, and compounding
- **Meta-Insights** — What we learned about how to think about this category

## Context Loading

Load context progressively based on what the user needs. Don't load everything at once.

| User Intent | Load This Reference | Then Route To |
|---|---|---|
| "What is CLI-Anything?" / overview questions | `references/TechnicalFoundation.md` | Answer directly |
| "What can I build?" / brainstorm / ideas | `references/FirstPrinciples.md` + `references/IdeationLandscape.md` | `workflows/ExploreNewIdea.md` |
| "I want to build X" / implement a pipeline | `references/TechnicalFoundation.md` + `references/ActionableRoadmap.md` | `workflows/BuildPipeline.md` |
| "Is this idea viable?" / validate / red team | `references/ActionableRoadmap.md` | `workflows/ValidateBusiness.md` |
| "Go deeper on X" / research a specific topic | Load the most relevant reference | `workflows/DeepDive.md` |
| "Where should I start?" / roadmap | `references/ActionableRoadmap.md` | Answer directly from roadmap |
| "Remind me what we learned" / recap | `references/MetaInsights.md` | Answer directly |
| "Can CLI-Anything wrap X?" / compatibility / access | `references/SoftwareCompatibility.md` | Answer directly from compatibility model |
| "What software can I use?" / not just open source | `references/SoftwareCompatibility.md` + `references/FirstPrinciples.md` | Answer directly |

## The Core Insight (Always in Context)

CLI-Anything dissolves the barrier between "what an AI can think" and "what professional software can do." Its real value is not automation — it is **EXPLORATION**: generating the full parameter space of a creative or analytical problem, then navigating it.

You're not building a production line. You're building a **possibility engine**.

The 6 atomic primitives it unlocks:
1. Software Comprehension → Structured Interface (any software becomes text-addressable)
2. Human-Only → Agent-Accessible (GUI operations become deterministic text commands)
3. Unstructured Output → JSON (software output becomes composable data)
4. Isolated Apps → Chainable Pipeline (any two CLI-ified apps can pipe together)
5. Manual → Reproducible (any workflow becomes scriptable)
6. One-at-a-time → Parallelizable (human-speed becomes machine-speed)

## Quick Reference

**CLI-Anything Plugin Commands** (already installed):
- `/cli-anything <path-or-repo>` — Full 7-phase pipeline: Analyze → Design → Implement → Plan Tests → Write Tests → Document → Publish
- `/cli-anything:refine <path> [focus]` — Gap analysis + expand coverage
- `/cli-anything:test <path>` — Run tests, update TEST.md
- `/cli-anything:validate <path>` — Validate against HARNESS.md standards
- `/cli-anything:list` — Show all generated harnesses

**What it produces**: Click-based Python CLI with stateful REPL + subcommand interface, `--json` flag for agent consumption, namespace packaging under `cli_anything.*`, comprehensive test suite.

**Key architecture**: `utils/<software>_backend.py` wraps real software via `subprocess.run()`. The backend pattern is what makes the CLIs real — they invoke actual GIMP/Blender/Inkscape/etc., not toy replacements.

## Existing Harnesses (11 demo CLIs in the repo)

| Software | Tests | Domain |
|---|---|---|
| GIMP | 107 | Image editing |
| Blender | 208 | 3D modeling/rendering |
| Inkscape | 202 | Vector graphics |
| Audacity | 161 | Audio editing |
| LibreOffice | 158 | Documents/Spreadsheets/Presentations |
| OBS Studio | 153 | Streaming/Recording |
| Kdenlive | 155 | Video editing |
| Shotcut | 154 | Video editing |
| Zoom | 22 | Video conferencing |
| Draw.io | 138 | Diagramming |
| AnyGen | 50 | Generic template |

## Routing to PAI Skills

This skill is a **context hub** — it provides the domain knowledge, then routes to PAI's analytical and creative skills for the actual work.

### For Ideation & Thinking
- **Thinking/BeCreative** — Generate new application ideas using MaximumCreativity, TreeOfThoughts, or DomainSpecific workflows
- **Thinking/FirstPrinciples** — Deconstruct a specific pipeline or business model to find the real value
- **Thinking/Council** — Debate an idea from 4 perspectives (Entrepreneur, Artist, Scientist, Systems Thinker)
- **Thinking/RedTeam** — Stress-test a business concept or technical approach
- **Thinking/Science** — Hypothesis-test a pipeline's feasibility

### For Research
- **Research** (Standard/Extensive/Deep) — Investigate a specific software's API, market size, competitor landscape, or technical feasibility
- **Research/ExtractAlpha** — Find the highest-value insight from a body of research

### For Building
- **CLI-Anything Plugin** (`/cli-anything`) — Actually generate CLIs from software source code
- **Agents** — Compose custom agents with specialized perspectives for pipeline work
- **Utilities** — CLI generation, skill scaffolding, agent delegation

### For Validation
- **Thinking/WorldThreatModelHarness** — Model threats and test investment thesis across time horizons
- **Research/DeepInvestigation** — Progressive iterative research on a market or technology

## Domain Research Vault

The `research/` directory stores persistent artifacts from domain-specific brainstorming sessions. Each domain exploration (real estate, healthcare, education, etc.) gets its own file preserving the full thinking chain — ranked ideas, council debates, wild ideas, meta-insights, and execution orders.

| Domain | File | Ideas | Top Idea |
|---|---|---|---|
| Real Estate Investing | `research/real-estate-investors.md` | 46 | Instant OM Machine (9.6) |

Load a domain research file to seed a conversation with full brainstorming context without re-running agents.

## How to Use This Skill

**Starting a new exploration session:**
> "I want to explore CLI-Anything possibilities" → Loads core context + routes to ExploreNewIdea workflow

**Picking up where we left off:**
> "What were the top CLI-Anything ideas?" → Loads ActionableRoadmap reference, presents the ranked top 10

**Going from idea to implementation:**
> "I want to build the Consulting Deliverable Machine" → Loads TechnicalFoundation + ActionableRoadmap, routes to BuildPipeline workflow

**Challenging an idea:**
> "Red team the ComplianceGhost concept" → Loads relevant context, routes to ValidateBusiness workflow which invokes Thinking/RedTeam
