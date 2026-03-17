---
task: Design GeoSeo output directory and file tracking
slug: 20260310-140000_geoseo-output-directory-design
effort: standard
phase: learn
progress: 10/10
mode: interactive
started: 2026-03-10T14:00:00-05:00
updated: 2026-03-10T14:00:05-05:00
---

## Context

The GeoSeo skill produces 11 output files across 11 workflows but currently dumps them all to the current working directory with no domain awareness. If Michael audits multiple websites, files from site B overwrite site A. There's no way to locate prior audit results for a specific domain, and the Report/ReportPdf workflows can't reliably find sub-workflow outputs.

### Current output files
- GEO-AUDIT-REPORT.md, GEO-CITABILITY-SCORE.md, GEO-CRAWLER-ACCESS.md
- GEO-LLMSTXT-ANALYSIS.md, GEO-BRAND-MENTIONS.md, GEO-SCHEMA-REPORT.md
- GEO-TECHNICAL-AUDIT.md, GEO-CONTENT-ANALYSIS.md, GEO-PLATFORM-OPTIMIZATION.md
- GEO-CLIENT-REPORT.md, GEO-REPORT.pdf

### PAI conventions for output directories
- OSINT: `MEMORY/WORK/{current_work}/YYYY-MM-DD-HHMMSS_osint-[target]/` (active), `History/research/YYYY-MM/[target]-osint/` (archived)
- Research: `MEMORY/WORK/{current_work}/` (active), `History/research/YYYY-MM/YYYY-MM-DD_[topic]/` (permanent)
- Recon: `MEMORY/WORK/{current_work}/recon-[target]/`

### Risks
- Domain normalization: `https://www.example.com`, `example.com`, `http://example.com/page` must all map to same directory
- Re-audits: Running a second audit on the same domain should not silently overwrite the first
- Report workflow must reliably discover sub-workflow outputs without hardcoding paths
- Output directory must work whether invoked from Algorithm mode or standalone skill invocation

## Criteria

- [x] ISC-1: Output directory schema defined with domain-keyed subdirectories
- [x] ISC-2: Domain normalization function extracts clean domain from any URL format
- [x] ISC-3: Re-audit handling defined (timestamp subdirs or append strategy)
- [x] ISC-4: SKILL.md documents output directory convention and path resolution
- [x] ISC-5: All 11 workflow files updated to write to domain-keyed directory
- [x] ISC-6: Report.md prerequisite check reads from domain directory not CWD
- [x] ISC-7: ReportPdf.md reads from domain directory not CWD
- [x] ISC-8: GeneratePdfReport.py output_path parameter uses domain directory
- [x] ISC-9: Audit.md passes domain directory to all 5 subagents
- [x] ISC-10: No existing workflow logic broken by directory changes

## Decisions

- **Single-path over two-stage**: Write directly to `output/GeoSeo/{domain-slug}/{YYYY-MM-DD}/` instead of MEMORY/WORK → History promotion. Eliminates archive step that LLM could mishandle. Marcus's practical point won: fewer variables = fewer silent failures.
- **Domain normalization**: Strip protocol + www, hostname only, dots→hyphens, lowercase. 63-char cap. `https://www.example.co.uk/blog` → `example-co-uk`.
- **Re-audit handling**: Same-day suffix `-2`, `-3`. Never overwrite.
- **Discovery**: `latest` symlink per domain, managed by Audit workflow via `ln -sf`.
- **Path convention**: `${PAI_DIR}/output/GeoSeo/{domain-slug}/{YYYY-MM-DD}/` for all output files.

## Verification

- Grep confirms 31 `output/GeoSeo` references across 12 skill files — all output paths updated
- Grep confirms zero remaining references to wrong filenames (GEO-CRAWLER-REPORT, GEO-LLMSTXT-REPORT, GEO-SCHEMA-AUDIT, GEO-PLATFORM-REPORT, GEO-CITABILITY-REPORT)
- /simplify review caught and fixed 5 critical filename mismatches in Report.md and ReportPdf.md
- All 10 ISC criteria verified complete

## Learning

- **Filename consistency is the #1 integration risk in multi-workflow skills.** The output directory changes were clean, but the Review caught 5 pre-existing filename mismatches between producing workflows and consuming workflows. These would have caused silent data loss in Report/ReportPdf generation.
- **Single-path output > two-stage promotion** for LLM-executed workflows. Fewer variables, fewer failure modes. The Council debate's practical argument (Marcus) was correct over the architectural ideal (separate active/archive stages).
- **"See SKILL.md" pointer pattern works well** for sub-workflows. 7 of 11 workflows correctly deferred to SKILL.md for domain normalization instead of re-stating the rules inline. The 2 orchestrator workflows (Audit, Report) appropriately include inline copies since they drive the process.
- **Always grep for all variant names** when renaming output files. The mismatches suggest the original skill was authored with different naming conventions across workflows that were never reconciled.
