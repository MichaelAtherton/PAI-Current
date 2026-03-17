---
name: GeoSeo
description: GEO-first AI search optimization — audits websites for AI citability, crawler access, brand mentions, schema markup, platform readiness, and generates client reports with scoring. USE WHEN GEO, SEO, geo audit, seo audit, ai search optimization, citability, ai crawlers, robots.txt ai, llms.txt, brand mentions, schema markup, structured data audit, platform optimization, geo report, geo score, website ai visibility, generative engine optimization.
---

## Customization

**Before executing, check for user customizations at:**
`${PAI_DIR}/PAI/USER/SKILLCUSTOMIZATIONS/GeoSeo/`

If this directory exists, load and apply any PREFERENCES.md, configurations, or resources found there. These override default behavior. If the directory does not exist, proceed with skill defaults.

## 🚨 MANDATORY: Voice Notification (REQUIRED BEFORE ANY ACTION)

**You MUST send this notification BEFORE doing anything else when this skill is invoked.**

1. **Send voice notification**:
   ```bash
   curl -s -X POST http://localhost:8888/notify \
     -H "Content-Type: application/json" \
     -d '{"message": "Running the WORKFLOWNAME workflow in the GeoSeo skill to ACTION"}' \
     > /dev/null 2>&1 &
   ```

2. **Output text notification**:
   ```
   Running the **WorkflowName** workflow in the **GeoSeo** skill to ACTION...
   ```

**This is not optional. Execute this curl command immediately upon skill invocation.**

# GeoSeo Skill

GEO-first, SEO-supported. Optimizes websites for AI-powered search engines (ChatGPT, Claude, Perplexity, Gemini, Google AI Overviews) while maintaining traditional SEO foundations.

**Philosophy:** AI search is eating traditional search. This tool optimizes for where traffic is going, not where it was.

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **Audit** | "geo audit", "full audit", "geo score" | `Workflows/Audit.md` |
| **Citability** | "citability", "citation readiness", "citable" | `Workflows/Citability.md` |
| **Crawlers** | "crawlers", "robots.txt", "ai crawler access" | `Workflows/Crawlers.md` |
| **LlmsTxt** | "llms.txt", "llms txt", "generate llms" | `Workflows/LlmsTxt.md` |
| **BrandMentions** | "brand mentions", "brand scan", "brand authority" | `Workflows/BrandMentions.md` |
| **PlatformOptimizer** | "platform optimization", "platform readiness" | `Workflows/PlatformOptimizer.md` |
| **Schema** | "schema", "structured data", "json-ld" | `Workflows/Schema.md` |
| **Technical** | "technical seo", "technical audit", "core web vitals" | `Workflows/Technical.md` |
| **Content** | "content quality", "e-e-a-t", "eeat" | `Workflows/Content.md` |
| **Report** | "geo report", "client report", "generate report" | `Workflows/Report.md` |
| **ReportPdf** | "pdf report", "generate pdf", "report pdf" | `Workflows/ReportPdf.md` |
| **Quick** | "quick audit", "quick geo", "60-second", "snapshot" | `Workflows/Audit.md` (quick mode) |

## Examples

**Example 1: Full GEO audit**
```
User: "Run a geo audit on https://example.com"
→ Invokes Audit workflow
→ Creates output/GeoSeo/example-com/2026-03-10/
→ Launches 5 parallel subagents for analysis
→ Saves GEO-AUDIT-REPORT.md to domain directory
→ Updates latest symlink
```

**Example 2: Check AI citability of a page**
```
User: "Score this page for ai citability https://example.com/blog/post"
→ Invokes Citability workflow
→ Saves GEO-CITABILITY-SCORE.md to output/GeoSeo/example-com/{date}/
```

**Example 3: Generate client PDF**
```
User: "Generate a pdf report for the last audit"
→ Invokes ReportPdf workflow
→ Reads audit data from output/GeoSeo/{domain}/latest/
→ Runs Tools/GeneratePdfReport.py
→ Saves GEO-REPORT.pdf to domain directory
```

## Output Directory

All GeoSeo output files are saved to a domain-keyed directory under `${PAI_DIR}/output/GeoSeo/`.

**Path convention:**
```
${PAI_DIR}/output/GeoSeo/{domain-slug}/{YYYY-MM-DD}/
```

**Domain normalization (to produce `{domain-slug}`):**
1. Strip protocol (`https://`, `http://`)
2. Strip `www.` prefix
3. Take hostname only (discard path, query, fragment)
4. Replace dots with hyphens
5. Lowercase everything
6. Cap at 63 characters

**Examples:**
- `https://www.example.com/blog/post` → `example-com`
- `https://blog.example.co.uk` → `blog-example-co-uk`
- `http://my-saas-app.io` → `my-saas-app-io`

**Re-audit handling:** If the date directory already exists (same-day re-audit), append `-2`, `-3`, etc. Never overwrite.

**Discovery:** Each domain directory contains a `latest` symlink pointing to the most recent audit date directory. The Report and ReportPdf workflows use this symlink to find sub-workflow outputs.

**Symlink update (after each audit completes):**
```bash
cd ${PAI_DIR}/output/GeoSeo/{domain-slug}
ln -sfn {YYYY-MM-DD} latest
```

**Directory creation (at the start of any workflow):**
```bash
mkdir -p ${PAI_DIR}/output/GeoSeo/{domain-slug}/{YYYY-MM-DD}
```

## Quick Reference

- **Scoring weights:** Citability 25%, Brand 20%, Content 20%, Technical 15%, Schema 10%, Platform 10% *(canonical source: `ScoringMethodology.md`)*
- **Tools:** `Tools/CitabilityScorer.py`, `Tools/GeneratePdfReport.py`
- **Agents:** GeoAiVisibility, GeoPlatformAnalysis, GeoTechnical, GeoContent, GeoSchema
- **Reference:** `ScoringMethodology.md`, `SchemaTemplates.md`
- **Output:** `${PAI_DIR}/output/GeoSeo/{domain-slug}/{date}/` *(see Output Directory above)*
- **Dependencies:** `pip install beautifulsoup4 requests lxml reportlab validators`

## Market Context

| Metric | Value |
|--------|-------|
| GEO services market (2025) | $850M-$886M |
| Projected GEO market (2031) | $7.3B (34% CAGR) |
| AI-referred sessions growth | +527% YoY |
| AI traffic conversion vs organic | 4.4x higher |
| Marketers investing in GEO | Only 23% |
