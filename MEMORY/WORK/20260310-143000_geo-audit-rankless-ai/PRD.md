---
task: GEO audit of rankless.ai website
slug: 20260310-143000_geo-audit-rankless-ai
effort: standard
phase: complete
progress: 10/10
mode: interactive
started: 2026-03-10T14:30:00-06:00
updated: 2026-03-10T14:42:00-06:00
---

## Context

Michael wants a full GEO (Generative Engine Optimization) audit of www.rankless.ai using the GeoSeo skill. This will analyze the site's visibility to AI search engines (ChatGPT, Perplexity, Gemini, Claude, Copilot) across citability, crawler access, brand authority, schema markup, content quality, and technical foundations. Output: comprehensive audit report with composite GEO score and actionable recommendations.

### Risks
- Site may be behind Cloudflare or other WAF blocking fetches → RESOLVED: site accessible
- Site may be a SPA with limited server-rendered content → CONFIRMED: /articles is JS-only shell

## Criteria

- [x] ISC-1: Homepage successfully fetched and analyzed
- [x] ISC-2: Business type correctly identified for rankless.ai
- [x] ISC-3: AI crawler access analyzed via robots.txt
- [x] ISC-4: Citability score calculated for key pages
- [x] ISC-5: Schema/structured data inventory completed
- [x] ISC-6: E-E-A-T content quality signals assessed
- [x] ISC-7: Technical SEO foundations evaluated
- [x] ISC-8: Platform-specific readiness scored per AI engine
- [x] ISC-9: Composite GEO score calculated with category breakdown
- [x] ISC-10: Audit report generated with prioritized findings

## Decisions

- Business type classified as Agency/Services based on consultation CTA, case studies, client testimonials, and service positioning
- E-E-A-T score (11/30 = 37/100 scaled) used as Brand Authority proxy since no brand mention scanning was possible via subagent tools
- Composite score: 32/100 (Critical tier)

## Verification

- ISC-1: Homepage fetched via WebFetch, full content extracted including headings, links, structured data check, OG tags
- ISC-2: Agency/Services — detected via consultation CTA, case study, testimonials, "search intelligence company" positioning
- ISC-3: robots.txt returns 404 — documented as CRITICAL finding, all crawlers default-allowed but no guidance
- ISC-4: Citability scored by GeoAiVisibility agent — 27.6/100, zero blocks above Grade D
- ISC-5: GeoSchema agent confirmed zero JSON-LD on any page — score 4/100
- ISC-6: GeoContent agent scored E-E-A-T at 11/30 — no authors, no credentials, anonymous testimonials
- ISC-7: GeoTechnical agent scored 31/100 — missing robots.txt, sitemap, JS-only articles, no schemas
- ISC-8: GeoPlatformAnalysis scored 41.5/100 — per-platform breakdown for 6 AI engines
- ISC-9: Composite GEO Score = 32/100 using canonical weighted formula
- ISC-10: Full report written to output/GeoSeo/rankless-ai/2026-03-10/GEO-AUDIT-REPORT.md
