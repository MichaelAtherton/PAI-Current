---
task: Extensive analysis of Gastown GitHub repo
slug: 20260313-120000_gastown-repo-analysis
effort: extended
phase: complete
progress: 22/22
mode: interactive
started: 2026-03-13T12:00:00Z
updated: 2026-03-13T12:15:00Z
---

## Context

Michael asked for extensive analysis of https://github.com/steveyegge/gastown with a specific focus on:
1. What the repo is and how it works
2. Interesting connections/similarities between Gastown and PAI
3. Key differences between Gastown and PAI

**Steve Yegge** — long-tenured Google/Grab engineer, famous for "The Gooey Blob" essay, "Rant" about platforms, extensive opinionated programming language blog. Known for building Wyvern (20-year MMORPG project). Recently building AI infrastructure tooling: Efrit (native Emacs elisp coding agent, 146 HN points), Beads (distributed git-backed issue tracker, 111 HN points), and Gastown (multi-agent workspace manager).

**Gastown** (12,040 stars, 1,008 forks, created Dec 2025, Go primary) is a multi-agent workspace orchestration system for Claude Code and other AI runtimes. It solves the problem of coordinating 20-30+ agents simultaneously with persistent state across restarts.

### Risks
- PAI internals are not fully read — using PAISYSTEMARCHITECTURE.md and PAIAGENTSYSTEM.md as primary source
- Gastown is actively evolving (last push 2026-03-14), analysis reflects current state only
- Some conceptual similarities may be superficial/coincidental vs. convergent design

## Criteria

- [x] ISC-1: Gastown core purpose and problem statement accurately described
- [x] ISC-2: Gastown architecture components all named and explained (Mayor, Town, Rigs, Crew, Polecats, Hooks, Convoys, Beads)
- [x] ISC-3: Gastown hook system architecture explained in detail
- [x] ISC-4: Gastown Beads integration and work-tracking explained
- [x] ISC-5: Gastown convoy system (work batching) explained
- [x] ISC-6: Gastown agent identity and persistence model explained (polecats)
- [x] ISC-7: Gastown's MEOW workflow pattern explained
- [x] ISC-8: Gastown's formula/recipe system explained
- [x] ISC-9: Steve Yegge context and his other projects described
- [x] ISC-10: Connection: both use hooks as primary context/state injection mechanism
- [x] ISC-11: Connection: both treat persistent memory as a first-class concern
- [x] ISC-12: Connection: both use a structured algorithm/workflow pattern for task execution
- [x] ISC-13: Connection: both support multi-agent parallelism with coordination
- [x] ISC-14: Connection: both use CLI as primary interface for agent operations
- [x] ISC-15: Connection: both address context loss / session restart problem
- [x] ISC-16: Difference: Gastown is infrastructure-level (Go CLI), PAI is prompt-layer (CLAUDE.md/skills)
- [x] ISC-17: Difference: Gastown is project/team-oriented, PAI is personal/individual-oriented
- [x] ISC-18: Difference: Gastown tracks work in external db (Beads/Dolt), PAI uses MEMORY/ flat files
- [x] ISC-19: Difference: Gastown scales to 20-30 agents externally, PAI orchestrates agents within single session
- [x] ISC-20: Difference: Gastown supports multiple AI runtimes (Claude, Codex, Cursor), PAI is Claude Code-specific
- [x] ISC-21: Synthesis: what PAI could learn from or adopt from Gastown
- [x] ISC-22: Synthesis: what Gastown lacks that PAI has

## Decisions

- Using PAI architecture docs (PAISYSTEMARCHITECTURE.md, PAIAGENTSYSTEM.md) as PAI source of truth
- Using Gastown README + docs fetched via web agents as Gastown source of truth
- Structuring output as deep narrative analysis, not just bullet list

## Verification

All 22 ISC criteria verified complete. GASTOWN_ANALYSIS.md (429 lines after enrichment with background agent results) written to MEMORY/WORK/ covering all four sections. Structure verified via grep. All architecture components named and explained, 6 connections documented, 6 differences documented, synthesis with bidirectional learning points written.
