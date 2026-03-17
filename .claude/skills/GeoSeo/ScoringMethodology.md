# GEO Scoring Methodology

**CANONICAL SOURCE OF TRUTH** for all GEO scoring weights. Other files (SKILL.md, Audit.md, Report.md, GeneratePdfReport.py) reference this document. If weights change, update HERE FIRST, then propagate.

## Composite GEO Score (0-100)

Weighted average of six category scores:

| Category | Weight | Measured By |
|----------|--------|-------------|
| AI Citability & Visibility | 25% | Passage scoring, answer block quality, AI crawler access |
| Brand Authority Signals | 20% | Mentions on Reddit, YouTube, Wikipedia, LinkedIn; entity presence |
| Content Quality & E-E-A-T | 20% | Expertise signals, original data, author credentials |
| Technical Foundations | 15% | SSR, Core Web Vitals, crawlability, mobile, security |
| Structured Data | 10% | Schema completeness, JSON-LD validation, rich result eligibility |
| Platform Optimization | 10% | Platform-specific readiness (Google AIO, ChatGPT, Perplexity, Gemini, Copilot) |

**Formula:** `GEO_Score = (Citability * 0.25) + (Brand * 0.20) + (EEAT * 0.20) + (Technical * 0.15) + (Schema * 0.10) + (Platform * 0.10)`

## Score Interpretation

| Score | Rating | Interpretation |
|-------|--------|----------------|
| 90-100 | Excellent | Top-tier; highly likely to be cited by AI |
| 75-89 | Good | Strong foundation with room for improvement |
| 60-74 | Fair | Moderate presence; significant opportunities exist |
| 40-59 | Poor | Weak signals; AI systems struggle to cite |
| 0-39 | Critical | Largely invisible to AI systems |

## Citability Scoring (per passage)

| Category | Weight | Key Factors |
|----------|--------|-------------|
| Answer Block Quality | 30% | Definition patterns, answer-first structure, quotable claims |
| Self-Containment | 25% | 134-167 word optimal length, low pronoun density, named entities |
| Structural Readability | 20% | 10-20 word sentences, lists, numbered items |
| Statistical Density | 15% | Percentages, dollar amounts, named sources |
| Uniqueness Signals | 10% | Original research, case studies, practical experience |

## Brand Authority Scoring

| Platform | Weight | Correlation with AI visibility |
|----------|--------|-------------------------------|
| YouTube | 25% | 0.737 correlation strength |
| Reddit | 25% | Google $60M/yr licensing; authentic opinions |
| Wikipedia | 20% | Entity recognition foundation for all AI models |
| LinkedIn | 15% | Professional authority signals |
| Other | 15% | Industry publications, Crunchbase, GitHub, forums |

## AI Crawler Tiers

| Tier | Crawlers | Impact if Blocked |
|------|----------|-------------------|
| Tier 1 (Critical) | GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot | Direct visibility reduction |
| Tier 2 (Important) | Google-Extended, Applebot-Extended, FacebookBot | Ecosystem feature loss |
| Tier 3 (Training) | CCBot, Bytespider, cohere-ai, Amazonbot | Training data exclusion only |

## Schema Scoring (0-100)

| Component | Points |
|-----------|--------|
| Organization with sameAs to 3+ platforms | 20 |
| Article with author as Person + dateModified | 15 |
| Person with sameAs + jobTitle | 15 |
| sameAs completeness (5+ platforms incl Wikipedia) | 15 |
| speakable property present | 10 |
| BreadcrumbList valid | 5 |
| WebSite + SearchAction valid | 5 |
| No deprecated schemas | 5 |
| All JSON-LD format | 5 |
| All pass validation | 5 |

## Issue Severity

| Severity | Response Time | Examples |
|----------|--------------|---------|
| Critical | Immediately | All AI crawlers blocked, no indexable content, 5xx errors |
| High | Within 1 week | Key crawlers blocked, no llms.txt, no schema |
| Medium | Within 1 month | Partial blocking, low citability scores, thin author bios |
| Low | When possible | Minor schema errors, missing alt text, suboptimal headings |

## Market Context

| Metric | Value | Source |
|--------|-------|--------|
| GEO services market (2025) | $850M-$886M | Yahoo Finance / Superlines |
| Projected GEO market (2031) | $7.3B (34% CAGR) | Industry analysts |
| AI-referred sessions growth | +527% YoY | SparkToro |
| AI traffic conversion vs organic | 4.4x higher | Industry data |
| Gartner: search traffic drop by 2028 | -50% | Gartner |
| Brand mentions vs backlinks for AI | 3x stronger correlation | Ahrefs (Dec 2025) |
