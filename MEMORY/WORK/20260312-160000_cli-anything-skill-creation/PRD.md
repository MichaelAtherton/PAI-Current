---
task: Create exhaustive CLI-Anything exploration skill from our research
slug: 20260312-160000_cli-anything-skill-creation
effort: advanced
phase: verify
progress: 11/11
mode: interactive
started: 2026-03-12T16:00:00-06:00
updated: 2026-03-12T16:15:00-06:00
---

## Context

Michael wanted to turn the CLI-Anything exploration (repo analysis, first principles, council debate, wild ideas, ranked roadmap) into a sophisticated multi-file PAI skill that seeds context and cross-references other PAI skills for further exploration. Not a simple single-file skill — a context hub.

## Criteria

- [x] ISC-1: SKILL.md under 500 lines with proper frontmatter (name, description)
- [x] ISC-2: Description triggers on CLI-Anything related queries
- [x] ISC-3: Multi-file structure with references/, workflows/, assets/
- [x] ISC-4: TechnicalFoundation reference covers repo analysis + architecture
- [x] ISC-5: FirstPrinciples reference covers 6 atomic primitives + constraint classification
- [x] ISC-6: IdeationLandscape reference covers council debate + wild ideas
- [x] ISC-7: ActionableRoadmap reference covers top 10 ranked + execution order
- [x] ISC-8: MetaInsights reference covers meta-learnings + mental models
- [x] ISC-9: 4 workflow files that route to other PAI skills (ExploreNewIdea, BuildPipeline, ValidateBusiness, DeepDive)
- [x] ISC-10: Cross-references to Thinking (6 modes), Research (4 modes), Agents, Investigation, ContentAnalysis
- [x] ISC-11: Progressive context loading (load only what's needed per intent)

## Decisions

- Used context-hub architecture: SKILL.md provides routing table + core insight, references provide deep domain knowledge, workflows define processes that invoke other PAI skills
- SKILL.md at 114 lines — lean hub that loads references on-demand
- 5 reference files covering the full exploration journey
- 4 workflow files covering the 4 primary use cases (ideate, build, validate, research)
- Quick reference card in assets/ for one-page orientation

## Verification

- Skill appears in available skills list (confirmed via system-reminder)
- SKILL.md is 114 lines (under 500-line limit)
- 11 files total across 4 directories
- All references contain the actual thinking/analysis, not summaries
- All workflows route to specific PAI skills with clear trigger conditions
