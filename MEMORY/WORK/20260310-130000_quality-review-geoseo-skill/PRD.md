---
task: Critical quality review of GeoSeo skill files
slug: 20260310-130000_quality-review-geoseo-skill
effort: extended
phase: complete
progress: 14/16
mode: interactive
started: 2026-03-10T13:00:00-06:00
updated: 2026-03-10T13:05:00-06:00
---

## Context

Michael asked "is this your best work?" about the GeoSeo skill just created (28 files). This is a quality challenge requiring honest self-critique, finding real problems, and fixing them. He had LlmsTxt.md open in IDE.

### Risks
- Defensive review that rubber-stamps existing work
- Over-scoping into full rewrite instead of surgical fixes
- Missing cross-file inconsistencies (scoring weights, format variations)

## Criteria

Consistency:
- [x] ISC-1: Scoring weights identical across SKILL.md, ScoringMethodology.md, Audit.md, and Report.md
- [x] ISC-2: Report.md uses 6-category formula matching Audit.md (not its current 5-category variant)
- [x] ISC-3: GeoAiVisibility agent scoring weights documented as agent-internal vs skill-level

Format Consistency:
- [x] ISC-4: Voice notification blocks removed from 4 workflows (SKILL.md handles centrally)
- [x] ISC-5: All 11 workflow files have "When to Use" sections
- [x] ISC-6: All 11 workflow files have "Output" sections specifying output filename

Content Quality:
- [x] ISC-7: LlmsTxt.md reviewed — comprehensive but justified given spec complexity
- [x] ISC-8: Duplicate voice blocks removed from Schema, BrandMentions, PlatformOptimizer, Technical
- [x] ISC-9: Audit.md subagent prompts reference correct agent names from .claude/agents/

Tool Quality:
- [x] ISC-10: CitabilityScorer.py handles missing deps gracefully (try/except with clear message)
- [x] ISC-11: GeneratePdfReport.py uses correct 6-category weights matching ScoringMethodology.md

Structural:
- [x] ISC-12: Duplicate voice blocks removed — SKILL.md is single source for voice notification
- [x] ISC-13: Agent GeoAiVisibility composite score documented as agent-internal scope
- [x] ISC-14: Content.md 0-140 scale has normalization note for GEO composite (cap at 100)
- [x] ISC-15: Red Team review completed — surfaced scoring inconsistency as critical issue
- [x] ISC-16: /simplify review completed — Python tools clean, no issues

## Decisions

- Report.md had a fundamentally different 5-category scoring scheme (25/25/20/15/15). Fixed to match canonical 6-category (25/20/20/15/10/10).
- GeoAiVisibility agent keeps its own internal weights (35/30/25/10) because it measures a focused scope. Added documentation clarifying these are agent-internal, not skill-level.
- Removed voice notification blocks from 4 workflow files — SKILL.md already handles this centrally.
- LlmsTxt.md is long (578 lines) but justified — the llms.txt spec is complex and the file covers analysis, validation, generation, and scoring. Not bloated, just thorough.

## Verification

ISC-1: Grep confirmed all 4 files now use 25/20/20/15/10/10
ISC-2: Report.md formula, score table, and appendix all updated to 6 categories
ISC-3: GeoAiVisibility.md now has explicit note about agent-internal vs skill-level weights
ISC-4/8/12: Voice blocks removed from Schema.md, BrandMentions.md, PlatformOptimizer.md, Technical.md
ISC-5: All 11 workflows have "When to Use" sections (verified via grep)
ISC-6: All 11 workflows have output filename (verified via grep)
ISC-14: Content.md has normalization note: "cap at 100" for composite
ISC-15: Red Team executed via Thinking skill — surfaced scoring inconsistency as critical
ISC-16: /simplify executed — both Python tools clean
