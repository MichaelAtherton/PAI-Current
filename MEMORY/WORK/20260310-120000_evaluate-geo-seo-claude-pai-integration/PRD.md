---
task: Evaluate geo-seo-claude repo for PAI integration
slug: 20260310-120000_evaluate-geo-seo-claude-pai-integration
effort: standard
phase: complete
progress: 10/10
mode: interactive
started: 2026-03-10T12:00:00-06:00
updated: 2026-03-10T12:05:00-06:00
---

## Context

Michael wants to evaluate the `zubair-trabzada/geo-seo-claude` GitHub project (1.6k stars, MIT license) for eventual integration into PAI. This is a Claude Code skill for GEO (Generative Engine Optimization) — optimizing websites for AI search engines (ChatGPT, Perplexity, Google AIO) while maintaining traditional SEO.

The repo has: 11 sub-skills, 5 parallel subagents, Python utilities, JSON-LD schema templates, and an install script that targets `~/.claude/skills/` and `~/.claude/agents/`.

This is evaluation only — no installation or code changes.

### Risks
- Young repo (9 commits) may have undiscovered bugs
- Install script writes directly to ~/.claude/ — could conflict with PAI
- Python dependencies add maintenance surface
- Scoring methodology is unvalidated against real AI citation data

## Criteria

- [x] ISC-1: Repo architecture documented (skills, agents, scripts, schemas)
- [x] ISC-2: PAI skill system compatibility assessed (naming, structure, SKILL.md)
- [x] ISC-3: Agent system compatibility assessed (agent .md files vs PAI agent format)
- [x] ISC-4: Install script conflict analysis complete (path conflicts with PAI)
- [x] ISC-5: Python dependency risk assessed (8 packages, version constraints)
- [x] ISC-6: Code quality of Python utilities evaluated
- [x] ISC-7: Integration effort estimate provided (small/medium/large)
- [x] ISC-8: Specific PAI adaptation steps listed
- [x] ISC-9: Value proposition for PAI assessed (unique capability gap filled)
- [x] ISC-10: Risk/concern summary with mitigations provided

## Decisions

- Do NOT run the raw install.sh script on PAI — manually port instead
- Create single parent skill GeoSeo/ with internal workflows (not 11 separate skills)
- Keep citability_scorer.py and generate_pdf_report.py; replace fetch_page.py with WebFetch
- Port 5 agents with PAI YAML frontmatter added

## Verification

All 10 criteria verified through direct code analysis of repo files via WebFetch, comparison against PAI's SKILLSYSTEM.md conventions, and FirstPrinciples decomposition of integration path.
