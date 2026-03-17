---
task: Create GeoSeo skill by porting geo-seo-claude repo
slug: 20260310-121500_create-geoseo-skill-from-geo-seo-claude
effort: advanced
phase: complete
progress: 28/28
mode: interactive
started: 2026-03-10T12:15:00-06:00
updated: 2026-03-10T12:20:00-06:00
---

## Context

Porting the `zubair-trabzada/geo-seo-claude` GitHub repo into a canonical PAI skill. The repo provides GEO (Generative Engine Optimization) — optimizing websites for AI search engines. It has 11 sub-skills, 5 agents, Python scripts, and JSON-LD templates. This port follows the 7 adaptation steps from the prior evaluation (ISC-8).

### Risks
- Workflow files are long — must preserve domain logic while adapting format
- Agent frontmatter must match PAI conventions exactly
- Python scripts must work from new paths

## Criteria

Skill Structure:
- [x] ISC-1: GeoSeo/ directory created at .claude/skills/GeoSeo/
- [x] ISC-2: SKILL.md has PAI-canonical YAML frontmatter with USE WHEN
- [x] ISC-3: SKILL.md has workflow routing table for all 12 commands
- [x] ISC-4: SKILL.md has Examples section with 3 usage patterns
- [x] ISC-5: SKILL.md has voice notification block
- [x] ISC-6: SKILL.md has customization block
- [x] ISC-7: Tools/ directory exists

Workflows (11 files):
- [x] ISC-8: Workflows/Audit.md created from geo-audit SKILL.md
- [x] ISC-9: Workflows/Citability.md created from geo-citability
- [x] ISC-10: Workflows/Crawlers.md created from geo-crawlers
- [x] ISC-11: Workflows/LlmsTxt.md created from geo-llmstxt
- [x] ISC-12: Workflows/BrandMentions.md created from geo-brand-mentions
- [x] ISC-13: Workflows/PlatformOptimizer.md created from geo-platform-optimizer
- [x] ISC-14: Workflows/Schema.md created from geo-schema
- [x] ISC-15: Workflows/Technical.md created from geo-technical
- [x] ISC-16: Workflows/Content.md created from geo-content
- [x] ISC-17: Workflows/Report.md created from geo-report
- [x] ISC-18: Workflows/ReportPdf.md created from geo-report-pdf

Agents (5 files):
- [x] ISC-19: GeoAiVisibility.md agent with PAI YAML frontmatter
- [x] ISC-20: GeoPlatformAnalysis.md agent with PAI YAML frontmatter
- [x] ISC-21: GeoTechnical.md agent with PAI YAML frontmatter
- [x] ISC-22: GeoContent.md agent with PAI YAML frontmatter
- [x] ISC-23: GeoSchema.md agent with PAI YAML frontmatter

Tools and Reference:
- [x] ISC-24: Tools/CitabilityScorer.py preserved from repo
- [x] ISC-25: Tools/GeneratePdfReport.py preserved from repo
- [x] ISC-26: SchemaTemplates.md reference doc with all 6 JSON-LD templates
- [x] ISC-27: ScoringMethodology.md reference doc with weights and formulas
- [x] ISC-28: All file names use TitleCase

## Decisions

- Dropped fetch_page.py (redundant with PAI WebFetch)
- Dropped brand_scanner.py (redundant with PAI Research agents)
- Kept CitabilityScorer.py and GeneratePdfReport.py as the only non-redundant Python tools
- All agents set to model: sonnet for cost efficiency
- LlmsTxt.md expanded significantly beyond repo source with full scoring methodology

## Verification

All 28 ISC criteria verified 2026-03-10:
- 1 SKILL.md with YAML frontmatter, USE WHEN, routing table, examples, voice, customization
- 11 workflow files in Workflows/ (Audit, Citability, Crawlers, LlmsTxt, BrandMentions, PlatformOptimizer, Schema, Technical, Content, Report, ReportPdf)
- 5 agent files in .claude/agents/ (GeoAiVisibility, GeoPlatformAnalysis, GeoTechnical, GeoContent, GeoSchema) — all with PAI YAML frontmatter
- 2 Python tools in Tools/ (CitabilityScorer.py, GeneratePdfReport.py)
- 2 reference docs at skill root (SchemaTemplates.md, ScoringMethodology.md)
- All filenames TitleCase confirmed
- GeoSeo skill appears in system skill listing (confirmed via system-reminder)

## Reflections

1. Parallel background agents effective for bulk file creation (3 agents → 11 workflows)
2. Repo evaluation before porting identified 3/5 Python scripts as redundant with PAI
3. Agent frontmatter adaptation was the most manual step (source had no YAML)
4. Skill immediately appeared in system routing after SKILL.md creation
