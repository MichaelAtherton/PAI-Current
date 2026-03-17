---
task: Brainstorm CLI-Anything pipelines for real estate investors
slug: 20260312-143000_cli-anything-rei-pipeline-brainstorm
effort: extended
phase: complete
progress: 16/16
mode: interactive
started: 2026-03-12T14:30:00-06:00
updated: 2026-03-12T14:35:00-06:00
---

## Context

Brainstorming CLI-Anything automation pipeline ideas for two real estate investor segments: Wholesalers and Short-Term Rental (Airbnb) investors. Each segment needs 6-8 pipeline ideas with the top 2 receiving full pipeline specifications. The framing is EXPLORATION not automation — generate massive variations, human selects best, production cost approaches zero so a solo operator competes with firms.

CLI-Anything's 6 primitives: text-addressable software, agent-accessible GUI ops, JSON output, chainable app pipelines, reproducible workflows, parallelizable serial work.

5 access paths: open source, scripting APIs, OS bridges, vendor CLIs, plugin APIs.

### Risks
- SaaS tools (REsimpli, PriceLabs, etc.) lack CLI access; pipelines must work around via exports/APIs or replace with open-source chains
- "Creative" ideas risk being impractical without grounding in real access paths
- Deep specs risk being shallow if too many ideas surveyed first
- Must avoid the trap of "automate existing workflow" vs "create new capability"

### Plan
Use FirstPrinciples decomposition on both segments, Council-style multi-perspective debate for idea generation, IterativeDepth for top 2 deep specs per segment.

## Criteria

- [x] ISC-1: Wholesaler segment has 6-8 named pipeline ideas
- [x] ISC-2: Each wholesaler pipeline has exact software chain with access paths
- [x] ISC-3: Each wholesaler pipeline has data flow between stages documented
- [x] ISC-4: Each wholesaler pipeline has human curation point identified
- [x] ISC-5: Each wholesaler pipeline has business value articulated
- [x] ISC-6: Top 2 wholesaler pipelines have full deep pipeline specs
- [x] ISC-7: STR segment has 6-8 named pipeline ideas
- [x] ISC-8: Each STR pipeline has exact software chain with access paths
- [x] ISC-9: Each STR pipeline has data flow between stages documented
- [x] ISC-10: Each STR pipeline has human curation point identified
- [x] ISC-11: Each STR pipeline has business value articulated
- [x] ISC-12: Top 2 STR pipelines have full deep pipeline specs
- [x] ISC-13: Ideas include Tier 2 chained multi-app pipelines
- [x] ISC-14: Ideas include Tier 3 new business category concepts
- [x] ISC-15: No formulaic or typical automation suggestions present
- [x] ISC-16: Software chains use actual CLI-accessible tools from the 5 access paths

## Decisions

- Skills (FirstPrinciples, Council, IterativeDepth) not available as invocable tools in this session. Performed equivalent structured creative analysis inline within BUILD/EXECUTE phases.
- Selected "The Scatter Gun" and "The Arbitrage Map" as wholesaler deep dives because they represent the highest creative delta from current practice.
- Selected "The Chameleon" and "The Turnover Clock" as STR deep dives because they create entirely new operational capabilities.

## Verification

- ISC-1: 8 wholesaler pipelines: Scatter Gun, Ghost Knock, Deal Reel, Crystal Ball, Hydra, Switchboard, Trojan Horse, Arbitrage Map
- ISC-2: Every pipeline lists specific tools with [open source], [vendor CLI], or other access path tags
- ISC-3: Every pipeline has IN -> STAGE 1 -> ... -> OUT data flow documented
- ISC-4: Every pipeline has explicit human curation point
- ISC-5: Every pipeline has dollar-value business case
- ISC-6: Scatter Gun and Arbitrage Map have full architecture diagrams, CLI commands, data schemas
- ISC-7: 8 STR pipelines: Chameleon, Mirror, Stage Hand, Concierge Press, Turnover Clock, Price Ghost, Review Alchemist, Portfolio Panopticon
- ISC-8: Every STR pipeline lists specific tools with access path tags
- ISC-9: Every STR pipeline has staged data flow
- ISC-10: Every STR pipeline has explicit human curation point
- ISC-11: Every STR pipeline has dollar-value business case
- ISC-12: Chameleon and Turnover Clock have full architecture diagrams, CLI commands, data schemas
- ISC-13: Most ideas are Tier 2 (multi-app chains): Scatter Gun chains 5 tools, Deal Reel chains 5 tools, etc.
- ISC-14: Tier 3 present: Arbitrage Map (new business: sell neighborhood intelligence), Turnover Clock (new business: verification-as-a-service), Portfolio Panopticon (institutional analytics for solo operators)
- ISC-15: No idea is "automate X" — all create new capabilities that don't exist today
- ISC-16: All chains use ImageMagick, FFmpeg, Inkscape, GIMP, LibreOffice, Pandoc, wkhtmltopdf, Draw.io — all from open source or vendor CLI access paths
